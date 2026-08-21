"""Normalized chemical milieu.

Each species y obeys a leaky integrator toward a homeostatic baseline, plus
phasic injections from events and from circuit / interoceptive coupling:

    dy/dt = (baseline + drive - y) / tau + noise

``drive`` is the sum of event pulses, circuit-to-chemistry back-projections
and HPA / autonomic couplings. Values are occupancies in [floor, ceiling].
"""

from __future__ import annotations

from dataclasses import dataclass, field

from psych_soma_codex.catalog.species import SPECIES, SpeciesSpec
from psych_soma_codex.core.mathutil import clamp, leaky_integrator
from psych_soma_codex.core.rng import Rng


@dataclass
class ChemicalMilieu:
    levels: dict[str, float] = field(default_factory=dict)
    drives: dict[str, float] = field(default_factory=dict)
    pulses: dict[str, float] = field(default_factory=dict)
    baseline_offsets: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.levels:
            self.levels = {
                k: clamp(s.baseline + self.baseline_offsets.get(k, 0.0), s.floor, s.ceiling)
                for k, s in SPECIES.items()
            }
        self.drives = {k: 0.0 for k in SPECIES}
        self.pulses = {k: 0.0 for k in SPECIES}

    def spec(self, key: str) -> SpeciesSpec:
        return SPECIES[key]

    def baseline_of(self, key: str) -> float:
        spec = SPECIES[key]
        return spec.baseline + self.baseline_offsets.get(key, 0.0)

    def get(self, key: str) -> float:
        return self.levels.get(key, self.baseline_of(key) if key in SPECIES else 0.0)

    def inject(self, key: str, delta: float) -> None:
        if key not in SPECIES:
            return
        self.pulses[key] = self.pulses.get(key, 0.0) + delta

    def set_drive(self, key: str, value: float) -> None:
        if key in SPECIES:
            self.drives[key] = value

    def add_drive(self, key: str, value: float) -> None:
        if key in SPECIES:
            self.drives[key] = self.drives.get(key, 0.0) + value

    def step(self, dt: float, rng: Rng | None = None, noise: float = 0.0) -> None:
        # Pulses are decaying envelopes, not one-shot kicks. Panksepp criterion 3:
        # arousals outlast precipitating circumstances. Envelope tau = species tau.
        for key, spec in SPECIES.items():
            y = self.levels[key]
            pulse = self.pulses.get(key, 0.0)
            drive = self.drives.get(key, 0.0) + pulse
            target = spec.baseline + self.baseline_offsets.get(key, 0.0) + drive
            y = leaky_integrator(y, target, spec.tau_min, dt)
            if rng is not None and noise > 0.0:
                y += rng.gauss(0.0, noise) * (dt ** 0.5)
            self.levels[key] = clamp(y, spec.floor, spec.ceiling)
            # Exact decay of the residual pulse toward 0.
            self.pulses[key] = leaky_integrator(pulse, 0.0, spec.tau_min, dt)
            self.drives[key] = 0.0

    def as_dict(self) -> dict[str, float]:
        return dict(self.levels)

    def vector(self, keys: tuple[str, ...] | None = None) -> list[float]:
        ks = keys or tuple(SPECIES.keys())
        return [self.get(k) for k in ks]
