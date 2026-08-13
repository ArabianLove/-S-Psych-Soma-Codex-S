"""Core affect: valence × arousal (Russell 2003) plus allostatic load.

Core affect is the low-dimensional interoceptive summary (Barrett 2017;
Barrett & Bliss-Moreau 2009). It is NOT an emotion. Emotions are constructed
downstream by categorising this affect together with circuit occupancies and
relational context.

Valence ∈ [-1, 1], arousal ∈ [0, 1], dominance ∈ [0, 1] (Mehrabian PAD, optional).
"""

from __future__ import annotations

from dataclasses import dataclass

from psych_soma_codex.chemistry.milieu import ChemicalMilieu
from psych_soma_codex.circuits.primary import PrimaryCircuits
from psych_soma_codex.core.mathutil import clamp, leaky_integrator
from psych_soma_codex.interoception.body import InteroceptiveBody
from psych_soma_codex.interoception.hpa import HPAAxis


@dataclass
class CoreAffect:
    valence: float = 0.15
    arousal: float = 0.28
    dominance: float = 0.50
    allostatic_load: float = 0.12
    prediction_error: float = 0.10  # free-energy proxy (HYPOTHESIS)

    def step(
        self,
        dt: float,
        milieu: ChemicalMilieu,
        circuits: PrimaryCircuits,
        body: InteroceptiveBody,
        hpa: HPAAxis,
        unexpected_uncertainty: float,
    ) -> None:
        approach = (
            0.28 * circuits.get("SEEKING")
            + 0.22 * circuits.get("CARE")
            + 0.18 * circuits.get("PLAY")
            + 0.12 * circuits.get("LUST")
            + 0.12 * milieu.get("opioid")
            + 0.10 * milieu.get("ot")
            + 0.08 * milieu.get("da")
        )
        withdraw = (
            0.30 * circuits.get("GRIEF")
            + 0.24 * circuits.get("FEAR")
            + 0.18 * circuits.get("RAGE")
            + 0.14 * milieu.get("dynorphin")
            + 0.10 * milieu.get("il6")
            + 0.08 * hpa.cortisol_norm()
        )
        v_chem = approach - withdraw
        v_body = body.valence_body()
        v_target = clamp(0.65 * v_chem + 0.35 * v_body, -1.0, 1.0)

        a_target = clamp(
            0.45 * body.arousal()
            + 0.20 * milieu.get("ne")
            + 0.15 * milieu.get("adrenaline")
            + 0.12 * circuits.get("FEAR")
            + 0.10 * circuits.get("SEEKING")
            + 0.08 * unexpected_uncertainty
        )
        d_target = clamp(
            0.40
            + 0.25 * circuits.get("SEEKING")
            + 0.15 * circuits.get("RAGE")
            + 0.10 * milieu.get("avp")
            - 0.25 * circuits.get("FEAR")
            - 0.20 * circuits.get("GRIEF")
            - 0.10 * hpa.cortisol_norm()
        )
        load_t = clamp(
            0.35 * hpa.cortisol_norm()
            + 0.25 * body.inflammation
            + 0.20 * (1.0 - body.energy)
            + 0.15 * circuits.get("GRIEF")
            + 0.10 * unexpected_uncertainty
        )
        pe_t = clamp(0.55 * unexpected_uncertainty + 0.25 * milieu.get("ach") + 0.20 * milieu.get("ne"))

        self.valence = leaky_integrator(self.valence, v_target, 0.8, dt)
        self.arousal = leaky_integrator(self.arousal, a_target, 0.5, dt)
        self.dominance = leaky_integrator(self.dominance, d_target, 1.2, dt)
        self.allostatic_load = leaky_integrator(self.allostatic_load, load_t, 6.0, dt)
        self.prediction_error = leaky_integrator(self.prediction_error, pe_t, 0.6, dt)
        self.valence = clamp(self.valence, -1.0, 1.0)
        self.arousal = clamp(self.arousal)
        self.dominance = clamp(self.dominance)
        self.allostatic_load = clamp(self.allostatic_load)
        self.prediction_error = clamp(self.prediction_error)

    def as_dict(self) -> dict[str, float]:
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "allostatic_load": self.allostatic_load,
            "prediction_error": self.prediction_error,
        }
