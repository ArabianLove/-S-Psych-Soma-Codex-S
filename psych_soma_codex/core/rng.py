"""Seeded RNG. Reproducibility is a first-class requirement."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class Rng:
    seed: int = 0
    _impl: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._impl = random.Random(self.seed)

    def uniform(self, a: float = 0.0, b: float = 1.0) -> float:
        return self._impl.uniform(a, b)

    def gauss(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        return self._impl.gauss(mu, sigma)

    def choice(self, seq):
        return self._impl.choice(seq)
