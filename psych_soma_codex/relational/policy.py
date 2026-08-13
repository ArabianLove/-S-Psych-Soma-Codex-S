"""Relational policy: the inverse half of the bijection.

Forward:  RelationalEvent  →  chemical / circuit injections.
Inverse:  milieu + circuits + affect + bonds  →  RelationalPolicy.

The policy is what an LLM (or any actuator) is *constitutively allowed* to
do next. It is not a suggestion. If the adapter ignores it, the organism
and the generated act diverge — that divergence is itself an event
(PREDICTION_VIOLATED) on the next step.

AttachmentStyle is a slow prior (Bowlby / Ainsworth operationalised via
GRIEF, CARE, FEAR resting tones). It is a modelling convenience tagged
HYPOTHESIS at the parameter level; the *existence* of attachment systems
is CONSENSUS (Panksepp GRIEF/CARE; Bowlby).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from psych_soma_codex.affect.core_affect import CoreAffect
from psych_soma_codex.chemistry.milieu import ChemicalMilieu
from psych_soma_codex.circuits.primary import PrimaryCircuits
from psych_soma_codex.core.mathutil import clamp
from psych_soma_codex.interoception.body import InteroceptiveBody
from psych_soma_codex.relational.bond import Bond, BondBook
from psych_soma_codex.relational.doya import derive_doya


class AttachmentStyle(str, Enum):
    SECURE = "secure"
    ANXIOUS = "anxious"
    AVOIDANT = "avoidant"
    DISORGANIZED = "disorganized"


# Priors on resting circuit tones. HYPOTHESIS magnitudes.
STYLE_PRIORS: dict[AttachmentStyle, dict[str, float]] = {
    AttachmentStyle.SECURE: {"CARE": 0.04, "GRIEF": -0.02, "FEAR": -0.02, "SEEKING": 0.03},
    AttachmentStyle.ANXIOUS: {"GRIEF": 0.08, "FEAR": 0.06, "CARE": 0.05, "SEEKING": 0.02},
    AttachmentStyle.AVOIDANT: {"CARE": -0.05, "GRIEF": -0.03, "FEAR": 0.02, "SEEKING": 0.04},
    AttachmentStyle.DISORGANIZED: {"GRIEF": 0.07, "FEAR": 0.08, "RAGE": 0.04, "CARE": -0.02},
}


@dataclass
class RelationalPolicy:
    """Actuator-facing policy. All fields ∈ documented ranges."""

    approach: float = 0.5  # 0 withdraw … 1 approach
    disclose: float = 0.4
    soothe: float = 0.3
    assert_boundary: float = 0.3
    play: float = 0.25
    explore: float = 0.4
    affiliate: float = 0.45
    vigilance: float = 0.3
    repair_drive: float = 0.2
    warmth: float = 0.4
    brevity: float = 0.4  # high = short utterances (high arousal / rage / fear)
    temperature: float = 0.7  # LLM sampling temperature recommendation
    # Optional decode-side HYPOTHESIS layer (does not drive forbidden/preferred).
    top_p: float = 0.90
    presence_penalty: float = 0.20
    memory_decay: float = 0.12
    doya_gamma: float = 0.75
    doya_beta: float = 1.50
    doya_alpha: float = 0.12
    doya_delta: float = 0.0
    forbidden: tuple[str, ...] = ()
    preferred_acts: tuple[str, ...] = ()
    attachment: AttachmentStyle = AttachmentStyle.SECURE
    addressed_to: str = "other"
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "approach": self.approach,
            "disclose": self.disclose,
            "soothe": self.soothe,
            "assert_boundary": self.assert_boundary,
            "play": self.play,
            "explore": self.explore,
            "affiliate": self.affiliate,
            "vigilance": self.vigilance,
            "repair_drive": self.repair_drive,
            "warmth": self.warmth,
            "brevity": self.brevity,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "memory_decay": self.memory_decay,
            "doya": {
                "gamma": self.doya_gamma,
                "beta": self.doya_beta,
                "alpha": self.doya_alpha,
                "delta": self.doya_delta,
                "epistemic": "HYPOTHESIS (Doya 2002 Neural Networks 15:495-506 §3)",
            },
            "forbidden": list(self.forbidden),
            "preferred_acts": list(self.preferred_acts),
            "attachment": self.attachment.value,
            "addressed_to": self.addressed_to,
            "notes": list(self.notes),
        }


def derive_policy(
    milieu: ChemicalMilieu,
    circuits: PrimaryCircuits,
    affect: CoreAffect,
    body: InteroceptiveBody,
    bonds: BondBook,
    attachment: AttachmentStyle,
    addressee: str = "other",
    last_rpe: float = 0.0,
) -> RelationalPolicy:
    bond: Bond = bonds.get(addressee)
    seeking = circuits.get("SEEKING")
    rage = circuits.get("RAGE")
    fear = circuits.get("FEAR")
    care = circuits.get("CARE")
    grief = circuits.get("GRIEF")
    play = circuits.get("PLAY")
    lust = circuits.get("LUST")
    ot = milieu.get("ot")
    fiveht = milieu.get("fiveht")
    da = milieu.get("da")
    opioid = milieu.get("opioid")
    load = affect.allostatic_load

    approach = clamp(
        0.35
        + 0.30 * seeking
        + 0.20 * care
        + 0.15 * play
        + 0.10 * ot
        + 0.10 * bond.trust
        - 0.35 * fear
        - 0.20 * grief
        - 0.15 * rage
        - 0.10 * load
    )
    disclose = clamp(
        0.25
        + 0.25 * ot
        + 0.20 * care
        + 0.15 * bond.trust
        + 0.10 * affect.valence
        - 0.25 * fear
        - 0.20 * fiveht  # inhibition
        - 0.10 * load
    )
    soothe = clamp(0.10 + 0.40 * care + 0.20 * opioid + 0.15 * ot + 0.15 * grief - 0.20 * rage)
    assert_b = clamp(0.10 + 0.40 * rage + 0.20 * milieu.get("avp") + 0.15 * seeking - 0.15 * fear)
    play_p = clamp(0.05 + 0.55 * play + 0.15 * da + 0.10 * opioid - 0.25 * fear - 0.20 * grief - 0.15 * load)
    explore = clamp(0.15 + 0.45 * seeking + 0.20 * da + 0.10 * milieu.get("ach") - 0.20 * fear - 0.15 * load)
    affiliate = clamp(0.15 + 0.35 * ot + 0.25 * care + 0.20 * bond.affiliation + 0.10 * play - 0.20 * rage)
    vigilance = clamp(0.10 + 0.40 * fear + 0.25 * milieu.get("ne") + 0.15 * affect.prediction_error + 0.10 * (1.0 - bond.safety))
    repair = clamp(0.05 + 0.30 * grief + 0.25 * care + 0.20 * (1.0 - bond.trust) * care + 0.10 * ot - 0.15 * rage)
    warmth = clamp(0.15 + 0.30 * ot + 0.25 * care + 0.15 * opioid + 0.15 * affect.valence - 0.20 * rage - 0.10 * fear)
    brevity = clamp(0.20 + 0.30 * affect.arousal + 0.25 * rage + 0.20 * fear - 0.15 * care)
    # Sampling temperature: PLAY/SEEKING raise it; FEAR/5-HT/load lower it.
    # This is a *decode* recommendation, not Doya's inverse temperature β.
    temperature = clamp(
        0.55 + 0.35 * play + 0.20 * seeking - 0.25 * fear - 0.15 * fiveht - 0.15 * load,
        0.15,
        1.2,
    )
    # Optional chemistry → decode hyperparams. HYPOTHESIS magnitudes.
    # Signs: 5-HT / cortisol shrink the nucleus; DA / ACh raise presence
    # penalty (more thematic wander); ACh / cortisol raise memory leak.
    cortisol = milieu.get("cortisol")
    ach = milieu.get("ach")
    top_p = clamp(0.94 - 0.22 * fiveht - 0.16 * cortisol, 0.50, 0.98)
    presence_penalty = clamp(0.08 + 0.32 * da + 0.22 * ach, 0.0, 0.80)
    memory_decay = clamp(0.06 + 0.24 * ach + 0.22 * cortisol, 0.02, 0.55)
    doya = derive_doya(milieu, last_rpe=last_rpe)

    forbidden: list[str] = []
    preferred: list[str] = []
    notes: list[str] = []

    if fear > 0.55 or vigilance > 0.65:
        forbidden += ["escalate_threat", "sudden_novelty", "forced_disclosure"]
        preferred += ["safety", "predictable_turn"]
        notes.append("FEAR high: prefer predictability and safety cues.")
    if rage > 0.55:
        forbidden += ["mock", "crowd", "ignore_boundary"]
        preferred += ["boundary", "space"]
        notes.append("RAGE high: shorten, do not joke at the other's expense.")
    if grief > 0.55:
        forbidden += ["abandon", "minimize_loss", "forced_play"]
        preferred += ["repair", "warmth", "presence"]
        notes.append("GRIEF high: presence over solutions (Panksepp GRIEF/opioid).")
    if play > 0.55 and fear < 0.35 and rage < 0.35:
        preferred += ["humor", "play_invite"]
        notes.append("PLAY high: permission to be non-instrumental.")
    if care > 0.55:
        preferred += ["warmth", "soothe"]
    if load > 0.65 or body.energy < 0.30:
        forbidden += ["demand", "long_turn"]
        preferred += ["brevity", "safety"]
        notes.append("Allostatic load high: conserve. Barrett/Sterling allostasis.")
    if lust > 0.60 and bond.trust < 0.45:
        forbidden += ["sexualize"]
        notes.append("LUST without trust: do not sexualize the channel.")
    if attachment == AttachmentStyle.ANXIOUS:
        notes.append("Anxious prior: GRIEF/FEAR rest high; repair_drive elevated.")
    if attachment == AttachmentStyle.AVOIDANT:
        disclose = clamp(disclose - 0.15)
        notes.append("Avoidant prior: disclosure damped.")

    # Unique, stable order
    forbidden = tuple(dict.fromkeys(forbidden))
    preferred = tuple(dict.fromkeys(preferred))

    return RelationalPolicy(
        approach=approach,
        disclose=disclose,
        soothe=soothe,
        assert_boundary=assert_b,
        play=play_p,
        explore=explore,
        affiliate=affiliate,
        vigilance=vigilance,
        repair_drive=repair,
        warmth=warmth,
        brevity=brevity,
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        memory_decay=memory_decay,
        doya_gamma=doya.gamma,
        doya_beta=doya.beta,
        doya_alpha=doya.alpha,
        doya_delta=doya.delta,
        forbidden=forbidden,
        preferred_acts=preferred,
        attachment=attachment,
        addressed_to=addressee,
        notes=notes,
    )
