"""Seven Panksepp primary-process circuits as leaky occupancies.

A circuit occupancy a_i ∈ [0, 1] is driven by:
  - its chemical drivers (weighted mean of species occupancies)
  - event pulses injected onto the circuit itself
  - cross-talk (SEEKING thwarted → RAGE; GRIEF sustained → SEEKING down)
  - a homeostatic leak toward a low resting tone

This is a *circuit* model (Panksepp primary-process), not a folk-emotion
label. Labels are constructed later from the joint (circuits × core affect
× concepts). See Barrett 2017 vs Panksepp 2010 in docs/RESEARCH.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from psych_soma_codex.catalog.circuits import CIRCUITS
from psych_soma_codex.chemistry.milieu import ChemicalMilieu
from psych_soma_codex.core.mathutil import clamp, leaky_integrator

# Circuit time constants (minutes). Primary arousals outlast precipitating
# circumstances (Panksepp criterion 3, 2010, Table I / text).
TAU: dict[str, float] = {
    "SEEKING": 4.0,
    "RAGE": 3.0,
    "FEAR": 5.0,
    "LUST": 8.0,
    "CARE": 10.0,
    "GRIEF": 14.0,
    "PLAY": 6.0,
}

REST: dict[str, float] = {
    "SEEKING": 0.22,
    "RAGE": 0.06,
    "FEAR": 0.08,
    "LUST": 0.08,
    "CARE": 0.14,
    "GRIEF": 0.06,
    "PLAY": 0.10,
}


@dataclass
class PrimaryCircuits:
    levels: dict[str, float] = field(default_factory=dict)
    pulses: dict[str, float] = field(default_factory=dict)
    rest: dict[str, float] = field(default_factory=dict)
    tau: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.rest:
            self.rest = dict(REST)
        if not self.tau:
            self.tau = dict(TAU)
        if not self.levels:
            self.levels = dict(self.rest)
        self.pulses = {k: 0.0 for k in CIRCUITS}

    def get(self, key: str) -> float:
        return self.levels.get(key, self.rest.get(key, REST.get(key, 0.0)))

    def inject(self, key: str, delta: float) -> None:
        if key in CIRCUITS:
            self.pulses[key] = self.pulses.get(key, 0.0) + delta

    def chemical_drive(self, milieu: ChemicalMilieu) -> dict[str, float]:
        drives: dict[str, float] = {}
        for key, spec in CIRCUITS.items():
            if spec.drivers:
                d = sum(milieu.get(s) for s in spec.drivers) / len(spec.drivers)
            else:
                d = 0.0
            if spec.brakes:
                b = sum(milieu.get(s) for s in spec.brakes) / len(spec.brakes)
            else:
                b = 0.0
            # Drivers pull up from rest; brakes pull down. Scaled to stay gentle.
            drives[key] = 0.55 * d - 0.40 * b
        return drives

    def crosstalk(self) -> dict[str, float]:
        """Qualitative couplings declared in Panksepp 2010.

        SEEKING thwarted → RAGE (frustration-aggression).
        Sustained GRIEF → SEEKING down (despair cascade).
        FEAR and RAGE are neighbours (fight/flight).
        CARE brakes GRIEF; PLAY brakes FEAR/RAGE.
        """
        s = self.get("SEEKING")
        r = self.get("RAGE")
        f = self.get("FEAR")
        g = self.get("GRIEF")
        c = self.get("CARE")
        p = self.get("PLAY")
        return {
            "RAGE": 0.18 * max(0.0, 0.45 - s) + 0.08 * f,
            "FEAR": 0.06 * r,
            "SEEKING": -0.22 * g - 0.08 * f,
            "GRIEF": -0.16 * c - 0.08 * p,
            "FEAR_brake": -0.10 * p,  # folded below
            "PLAY": -0.12 * f - 0.10 * g,
            "CARE": -0.10 * g,
        }

    def step(self, dt: float, milieu: ChemicalMilieu) -> None:
        chem = self.chemical_drive(milieu)
        x = self.crosstalk()
        for key in CIRCUITS:
            extra = x.get(key, 0.0)
            if key == "FEAR":
                extra += x.get("FEAR_brake", 0.0)
            pulse = self.pulses.get(key, 0.0)
            rest = self.rest.get(key, REST[key])
            tau = self.tau.get(key, TAU[key])
            target = rest + chem[key] + extra + pulse
            y = leaky_integrator(self.levels[key], target, tau, dt)
            self.levels[key] = clamp(y, 0.0, 1.0)
            # Envelope outlasts the event (Panksepp 2010 criterion 3).
            self.pulses[key] = leaky_integrator(pulse, 0.0, tau, dt)

    def as_dict(self) -> dict[str, float]:
        return dict(self.levels)

    def dominant(self) -> str:
        return max(self.levels, key=self.levels.get)
