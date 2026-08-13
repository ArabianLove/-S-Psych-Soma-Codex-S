"""Constitutive engine: one organism, one step, a closed loop.

Order of a step (Markov-blanket consistent):

1. Sensory states  — ingest RelationalEvent(s)
2. Chemical drive  — event weights + HPA/autonomic back-projections
3. Circuits        — primary-process occupancies
4. Interoception   — HPA ODE + autonomic body
5. Core affect     — valence / arousal / load / PE
6. Construction    — labelled emotion (Barrett layer)
7. Bonds + policy  — inverse half of the bijection
8. Snapshot        — the only public readout

Nothing in this order is decorative. Swapping 3 and 4 would break the
Panksepp criterion that chemical arousals *gate* the circuits; swapping
6 and 7 would let a folk label drive policy before the body has spoken.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from psych_soma_codex.affect.constructor import construct_emotion
from psych_soma_codex.affect.core_affect import CoreAffect
from psych_soma_codex.catalog.circuits import CIRCUITS
from psych_soma_codex.catalog.events import EVENT_WEIGHTS
from psych_soma_codex.catalog.species import SPECIES
from psych_soma_codex.chemistry.milieu import ChemicalMilieu
from psych_soma_codex.circuits.primary import REST, PrimaryCircuits
from psych_soma_codex.core.mathutil import clamp
from psych_soma_codex.core.rng import Rng
from psych_soma_codex.core.timebase import Timebase
from psych_soma_codex.interoception.body import InteroceptiveBody
from psych_soma_codex.interoception.hpa import HPAAxis
from psych_soma_codex.io.events import EventKind, RelationalEvent, parse_event
from psych_soma_codex.io.snapshot import Snapshot
from psych_soma_codex.relational.bond import BondBook
from psych_soma_codex.relational.policy import (
    STYLE_PRIORS,
    AttachmentStyle,
    RelationalPolicy,
    derive_policy,
)


@dataclass
class SimulationConfig:
    dt_min: float = 0.05
    seed: int = 0
    noise: float = 0.0
    attachment: AttachmentStyle = AttachmentStyle.SECURE
    name: str = "organism"
    start_tod_hours: float = 8.0  # morning start, near CAR
    rpe_learning_rate: float = 0.12
    expected_reward_leak: float = 0.02


@dataclass
class LearningState:
    """Schultz / Sutton-Barto reward prediction at the episode scale."""

    v_hat: float = 0.0  # expected relational value
    last_rpe: float = 0.0
    unexpected_uncertainty: float = 0.10
    expected_uncertainty: float = 0.20


@dataclass
class Organism:
    config: SimulationConfig = field(default_factory=SimulationConfig)
    time: Timebase = field(init=False)
    rng: Rng = field(init=False)
    chemistry: ChemicalMilieu = field(default_factory=ChemicalMilieu)
    circuits: PrimaryCircuits = field(default_factory=PrimaryCircuits)
    hpa: HPAAxis = field(default_factory=HPAAxis)
    body: InteroceptiveBody = field(default_factory=InteroceptiveBody)
    affect: CoreAffect = field(default_factory=CoreAffect)
    bonds: BondBook = field(default_factory=BondBook)
    learning: LearningState = field(default_factory=LearningState)
    last_policy: RelationalPolicy | None = None
    last_emotion_label: str = "calm"
    history: list[Snapshot] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        self.time = Timebase(dt_min=self.config.dt_min, t_min=self.config.start_tod_hours * 60.0)
        self.rng = Rng(self.config.seed)
        # Attachment prior on resting circuit tones.
        priors = STYLE_PRIORS.get(self.config.attachment, {})
        for k, d in priors.items():
            if k in self.circuits.levels:
                self.circuits.levels[k] = clamp(REST.get(k, 0.1) + d)

    # ------------------------------------------------------------------ ingest
    def ingest(self, events: Iterable[RelationalEvent | dict | str | EventKind]) -> list[RelationalEvent]:
        parsed = [parse_event(e) for e in events]
        for ev in parsed:
            self._apply_event(ev)
        return parsed

    def _apply_event(self, ev: RelationalEvent) -> None:
        weights = EVENT_WEIGHTS.get(ev.kind.value, {})
        scale = ev.intensity
        # In-group gates OT-like effects (Carter / de Dreu context-dependence).
        for target, (delta, _tau) in weights.items():
            d = delta * scale
            if target == "ot":
                d *= 0.40 + 0.60 * ev.in_group
            if target in SPECIES:
                self.chemistry.inject(target, d)
            elif target in CIRCUITS:
                self.circuits.inject(target, d)

        # Reward prediction error (Schultz 1997; Glimcher 2011).
        r = ev.signed_intensity
        rpe = r - self.learning.v_hat
        self.learning.last_rpe = rpe
        self.learning.v_hat += self.config.rpe_learning_rate * rpe
        self.learning.v_hat *= 1.0 - self.config.expected_reward_leak
        # Phasic DA ≈ positive RPE; dynorphin / 5-HT on negative RPE.
        if rpe > 0.0:
            self.chemistry.inject("da", 0.35 * rpe)
        else:
            self.chemistry.inject("dynorphin", 0.20 * (-rpe))
            self.chemistry.inject("fiveht", 0.12 * (-rpe))

        # Yu & Dayan 2005: NE = unexpected uncertainty; ACh = expected.
        surprise = ev.surprise
        self.learning.unexpected_uncertainty = clamp(
            0.70 * self.learning.unexpected_uncertainty + 0.30 * surprise
        )
        # Expected uncertainty rises when outcomes are reliably noisy.
        self.learning.expected_uncertainty = clamp(
            0.85 * self.learning.expected_uncertainty + 0.15 * abs(rpe)
        )
        self.chemistry.inject("ne", 0.28 * surprise * ev.intensity)
        self.chemistry.inject("ach", 0.22 * self.learning.expected_uncertainty)

        # HPA stress gain: threats / losses raise it; safety / repair lower it.
        if ev.kind in {EventKind.THREAT, EventKind.LOSS, EventKind.ABANDONMENT, EventKind.SICKNESS}:
            self.hpa.stress_gain = clamp(self.hpa.stress_gain + 0.35 * ev.intensity, 0.4, 3.5)
        elif ev.kind in {EventKind.SAFETY, EventKind.REPAIR, EventKind.WARMTH}:
            self.hpa.stress_gain = clamp(self.hpa.stress_gain - 0.20 * ev.intensity, 0.4, 3.5)

        # Somatic marker write (Damasio; tagged DEBATE).
        marker_key = f"{ev.kind.value}:{ev.agent}"
        self.body.write_marker(marker_key, ev.valence_hint * ev.intensity)

        # Bond update.
        self.bonds.update_from_event(
            agent=ev.agent,
            kind=ev.kind.value,
            intensity=ev.intensity,
            in_group=ev.in_group,
            ot=self.chemistry.get("ot"),
            avp=self.chemistry.get("avp"),
            t_min=self.time.t_min,
        )

    # -------------------------------------------------------------------- step
    def step(self, events: Iterable[RelationalEvent | dict | str | EventKind] | None = None) -> Snapshot:
        if events:
            self.ingest(events)

        # Slow leak of HPA stress gain back to 1.
        self.hpa.stress_gain = 0.98 * self.hpa.stress_gain + 0.02 * 1.0
        self.hpa.avp_drive = 0.25 + 0.70 * self.chemistry.get("avp")

        # Circuit → chemistry back-projections (constitutive, not decorative).
        self.chemistry.add_drive("da", 0.18 * self.circuits.get("SEEKING"))
        self.chemistry.add_drive("crh", 0.20 * self.circuits.get("FEAR") + 0.16 * self.circuits.get("GRIEF"))
        self.chemistry.add_drive("ot", 0.18 * self.circuits.get("CARE") + 0.08 * self.circuits.get("LUST"))
        self.chemistry.add_drive("opioid", 0.12 * self.circuits.get("PLAY") + 0.10 * self.circuits.get("CARE"))
        self.chemistry.add_drive("adrenaline", 0.20 * self.circuits.get("FEAR") + 0.16 * self.circuits.get("RAGE"))
        self.chemistry.add_drive("substance_p", 0.22 * self.circuits.get("RAGE"))
        self.chemistry.add_drive("glu", 0.12 * self.circuits.get("GRIEF") + 0.10 * self.circuits.get("RAGE"))
        self.chemistry.add_drive("gaba", 0.08 * (1.0 - self.circuits.get("RAGE")) + 0.06 * (1.0 - self.circuits.get("FEAR")))

        # Physical HPA first (minutes–hours), then project onto normalized milieu.
        self.hpa.step(self.time.dt_min, self.time.tod_hours)
        # Soft-clamp normalized hormones toward the physical integrator.
        self.chemistry.levels["cortisol"] = clamp(
            0.65 * self.chemistry.get("cortisol") + 0.35 * self.hpa.cortisol_norm()
        )
        self.chemistry.levels["crh"] = clamp(0.65 * self.chemistry.get("crh") + 0.35 * self.hpa.crh_norm())
        self.chemistry.levels["acth"] = clamp(0.65 * self.chemistry.get("acth") + 0.35 * self.hpa.acth_norm())

        self.chemistry.step(self.time.dt_min, rng=self.rng, noise=self.config.noise)
        self.circuits.step(self.time.dt_min, self.chemistry)
        self.body.step(self.time.dt_min, self.chemistry, self.circuits, self.hpa)
        self.affect.step(
            self.time.dt_min,
            self.chemistry,
            self.circuits,
            self.body,
            self.hpa,
            unexpected_uncertainty=self.learning.unexpected_uncertainty,
        )
        constructed = construct_emotion(self.circuits, self.affect)
        self.last_emotion_label = constructed.label
        policy = derive_policy(
            self.chemistry,
            self.circuits,
            self.affect,
            self.body,
            self.bonds,
            self.config.attachment,
            last_rpe=self.learning.last_rpe,
        )
        self.last_policy = policy
        self.time = self.time.advanced(1)

        hpa_d = self.hpa.as_dict()
        hpa_d["circadian"] = self.hpa.circadian(self.time.tod_hours)
        hpa_d["stress_gain"] = self.hpa.stress_gain

        snap = Snapshot(
            t_min=self.time.t_min,
            tod_hours=self.time.tod_hours,
            chemistry=self.chemistry.as_dict(),
            circuits=self.circuits.as_dict(),
            affect=self.affect.as_dict(),
            body=self.body.as_dict(),
            hpa=hpa_d,
            emotion={
                "label": constructed.label,
                "confidence": constructed.confidence,
                "granularity": constructed.granularity,
                "mixture": constructed.mixture,
                "notes": constructed.notes,
            },
            relational={
                "bonds": self.bonds.as_dict(),
                "v_hat": self.learning.v_hat,
                "rpe": self.learning.last_rpe,
                "unexpected_uncertainty": self.learning.unexpected_uncertainty,
                "expected_uncertainty": self.learning.expected_uncertainty,
            },
            policy=policy.as_dict(),
            epistemics={
                "circuits": "CONSENSUS (Panksepp 2010)",
                "rpe_da": "CONSENSUS (Schultz 1997; debate on tonic DA)",
                "fiveht": "DEBATE (Dayan-Huys default)",
                "ne_ach": "CONSENSUS (Yu & Dayan 2005)",
                "hpa_rates": "FACT (Andersen 2013)",
                "event_weights": "HYPOTHESIS (signs CONSENSUS)",
                "constructed_label": "CONSENSUS/DEBATE (Barrett 2017 vs basic emotion)",
                "somatic_markers": "DEBATE (Damasio; Dunn 2006)",
                "doya_metalearning": "HYPOTHESIS (Doya 2002 Neural Networks 15:495-506 §3)",
                "decode_params": "HYPOTHESIS (chemistry→T/top_p/presence/memory; not physiology)",
            },
        )
        return snap

    def snapshot(self) -> Snapshot:
        """Zero-event readout at current time (does not advance)."""
        if self.history:
            return self.history[-1]
        return self.step([])


def step(organism: Organism, events=None) -> Snapshot:
    snap = organism.step(events)
    organism.history.append(snap)
    return snap


def run(
    organism: Organism,
    events: Iterable[RelationalEvent | dict | str] | None = None,
    minutes: float = 1.0,
) -> list[Snapshot]:
    """Advance ``minutes`` of simulated time, delivering ``events`` at t=0 of the window."""
    if minutes is None or minutes <= 0:
        minutes = organism.time.dt_min
    n = max(1, int(round(float(minutes) / organism.time.dt_min)))
    out: list[Snapshot] = []
    pending = list(events or [])
    for i in range(n):
        evs = pending if i == 0 else []
        snap = step(organism, evs)
        out.append(snap)
    return out
