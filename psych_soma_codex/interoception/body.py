"""Autonomic / interoceptive body: a compact allostatic state.

Following Sterling (2012) and Barrett (2017), the brain's job is allostasis:
anticipate the body's needs. We expose a small set of interoceptive axes that
(a) are driven by circuits + HPA + events, and (b) feed core affect.

Axes are unitless occupancies unless noted.
"""

from __future__ import annotations

from dataclasses import dataclass

from psych_soma_codex.chemistry.milieu import ChemicalMilieu
from psych_soma_codex.circuits.primary import PrimaryCircuits
from psych_soma_codex.core.mathutil import clamp, leaky_integrator
from psych_soma_codex.interoception.hpa import HPAAxis


@dataclass
class InteroceptiveBody:
    heart_rate_bpm: float = 70.0
    vagal_tone: float = 0.55
    skin_conductance: float = 0.15
    temperature_dev: float = 0.0  # °C from 37.0
    gut_unease: float = 0.12
    muscle_tension: float = 0.18
    energy: float = 0.70
    inflammation: float = 0.08
    # Somatic-marker cache: running association from situation hash → valence.
    # This is the Damasio as-if body loop, tagged DEBATE (see RESEARCH.md).
    markers: dict[str, float] | None = None

    def __post_init__(self) -> None:
        if self.markers is None:
            self.markers = {}

    def step(
        self,
        dt: float,
        milieu: ChemicalMilieu,
        circuits: PrimaryCircuits,
        hpa: HPAAxis,
    ) -> None:
        adr = milieu.get("adrenaline")
        ne = milieu.get("ne")
        ot = milieu.get("ot")
        opioid = milieu.get("opioid")
        il6 = milieu.get("il6")
        fear = circuits.get("FEAR")
        rage = circuits.get("RAGE")
        care = circuits.get("CARE")
        play = circuits.get("PLAY")
        grief = circuits.get("GRIEF")
        seeking = circuits.get("SEEKING")
        cort = hpa.cortisol_norm()

        sympathetic = 0.45 * adr + 0.25 * ne + 0.20 * fear + 0.18 * rage + 0.10 * cort
        parasymp = 0.40 * ot + 0.30 * opioid + 0.20 * care + 0.15 * play

        hr_target = 70.0 + 55.0 * sympathetic - 22.0 * parasymp + 8.0 * il6
        self.heart_rate_bpm = leaky_integrator(self.heart_rate_bpm, hr_target, 0.4, dt)
        self.heart_rate_bpm = clamp(self.heart_rate_bpm, 42.0, 180.0)

        vag_t = 0.55 + 0.30 * parasymp - 0.35 * sympathetic
        self.vagal_tone = leaky_integrator(self.vagal_tone, clamp(vag_t), 0.6, dt)

        sc_t = 0.12 + 0.55 * sympathetic + 0.15 * fear
        self.skin_conductance = leaky_integrator(self.skin_conductance, clamp(sc_t), 0.3, dt)

        ten_t = 0.15 + 0.35 * rage + 0.30 * fear + 0.15 * cort - 0.15 * play
        self.muscle_tension = leaky_integrator(self.muscle_tension, clamp(ten_t), 0.8, dt)

        gut_t = 0.10 + 0.35 * grief + 0.20 * fear + 0.25 * il6 - 0.10 * opioid
        self.gut_unease = leaky_integrator(self.gut_unease, clamp(gut_t), 1.2, dt)

        en_t = 0.55 + 0.35 * seeking - 0.25 * cort - 0.35 * il6 - 0.15 * grief
        self.energy = leaky_integrator(self.energy, clamp(en_t), 4.0, dt)

        inf_t = 0.06 + 0.80 * il6 + 0.10 * cort
        self.inflammation = leaky_integrator(self.inflammation, clamp(inf_t), 8.0, dt)

        td_t = 0.4 * il6 - 0.15 * ot
        self.temperature_dev = leaky_integrator(self.temperature_dev, td_t, 6.0, dt)

    def arousal(self) -> float:
        hr = (self.heart_rate_bpm - 55.0) / 80.0
        return clamp(0.40 * hr + 0.30 * self.skin_conductance + 0.20 * self.muscle_tension + 0.10 * (1.0 - self.vagal_tone))

    def valence_body(self) -> float:
        """Interoceptive contribution to valence, in [-1, 1]."""
        comfort = 0.35 * self.vagal_tone + 0.25 * self.energy - 0.25 * self.gut_unease
        comfort -= 0.20 * self.inflammation - 0.15 * self.muscle_tension
        return clamp(comfort, -1.0, 1.0) * 2.0 - 0.4  # re-centre

    def write_marker(self, key: str, value: float) -> None:
        assert self.markers is not None
        prev = self.markers.get(key, 0.0)
        self.markers[key] = 0.80 * prev + 0.20 * value

    def read_marker(self, key: str) -> float:
        assert self.markers is not None
        return self.markers.get(key, 0.0)

    def as_dict(self) -> dict[str, float]:
        return {
            "heart_rate_bpm": self.heart_rate_bpm,
            "vagal_tone": self.vagal_tone,
            "skin_conductance": self.skin_conductance,
            "temperature_dev": self.temperature_dev,
            "gut_unease": self.gut_unease,
            "muscle_tension": self.muscle_tension,
            "energy": self.energy,
            "inflammation": self.inflammation,
            "arousal": self.arousal(),
            "valence_body": self.valence_body(),
        }
