"""Canonical time units. The integrator steps in minutes by default.

Why minutes: synaptic events are milliseconds, but the constitutive object of
this system is the *affective episode* (seconds–hours) plus the HPA cascade
(minutes–hours). Fast transmitters are therefore represented as leaky envelopes
of phasic bursts, not as single vesicles. See docs/RESEARCH.md §4.
"""

from __future__ import annotations

from dataclasses import dataclass

SECOND = 1.0 / 60.0
MINUTE = 1.0
HOUR = 60.0
DAY = 1440.0


@dataclass(frozen=True)
class Timebase:
    """Simulation clock.

    ``dt_min`` is the integrator step in minutes.
    ``t_min`` is absolute simulated time from organism birth (or session start).
    """

    dt_min: float = 0.05  # 3 seconds — resolves phasic envelopes without stiffness
    t_min: float = 0.0

    def advanced(self, steps: int = 1) -> "Timebase":
        return Timebase(dt_min=self.dt_min, t_min=self.t_min + self.dt_min * steps)

    @property
    def t_seconds(self) -> float:
        return self.t_min * 60.0

    @property
    def tod_hours(self) -> float:
        """Time of day in [0, 24), midnight-origin. Used by the HPA circadian drive."""
        minutes = self.t_min % DAY
        return minutes / 60.0
