"""Core affect: valence × arousal (Russell 2003) plus allostatic load.

Core affect is the low-dimensional interoceptive summary (Barrett 2017;
Barrett & Bliss-Moreau 2009). It is NOT an emotion. Emotions are constructed
downstream by categorising this affect together with circuit occupancies and
relational context.

Valence ∈ [-1, 1], arousal ∈ [0, 1], dominance ∈ [0, 1] (Mehrabian PAD, optional).

Sidecars (HYPOTHESIS, not producers)
------------------------------------
``valence_fe`` / ``fe_accel`` implement Joffily & Coricelli 2013
(*PLoS Comput Biol* 9(6):e1003094) as a *reading* of the existing
prediction-error proxy: v_FE = −dPE/dt. They do NOT write ``valence``
and do NOT enter Barrett ``_feature_vector``.

``homeostatic_drive`` is a Keramati & Gutkin 2014 annotation computed
from body axes already present. It does NOT replace ``allostatic_load``.

``sensitization`` is a slow Z (gift 7 / RCAD 0.1.0, HYPOTHESIS). It
leaks from load + unexpected uncertainty + FEAR and is extinguished by
vagal tone / energy. τ ≈ 18 min, slower than ``allostatic_load`` (τ = 6).
It does NOT write ``allostatic_load`` and does NOT enter Barrett
``_feature_vector``.

Hsueh et al. 2023 (*Nature* 615:292–299): optically evoked tachycardia
enhances anxiety-like behaviour only in risky contexts. The extra
body-arousal term is multiplied by FEAR occupancy, so at FEAR ≈ 0 the
step is identical to the ungated equation (no idle/warmth regression).
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
    valence_fe: float = 0.0  # Joffily 2013 sidecar: −dPE/dt
    fe_accel: float = 0.0  # d(valence_fe)/dt, annotation only
    homeostatic_drive: float = 0.0  # Keramati annotation, not allostatic_load
    sensitization: float = 0.05  # slow Z; HYPOTHESIS (RCAD); not allostatic_load
    _prev_pe: float = 0.10

    def step(
        self,
        dt: float,
        milieu: ChemicalMilieu,
        circuits: PrimaryCircuits,
        body: InteroceptiveBody,
        hpa: HPAAxis,
        unexpected_uncertainty: float,
    ) -> None:
        fear = circuits.get("FEAR")
        body_arousal = body.arousal()
        # Hsueh 2023: body arousal enhances anxiety-like affect only in a
        # risky context. FEAR occupancy is the existing risk proxy. Extra
        # term is identically 0 at FEAR ≈ 0 (no regression on idle/warmth).
        hsueh = body_arousal * fear

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
            + 0.24 * fear
            + 0.18 * circuits.get("RAGE")
            + 0.14 * milieu.get("dynorphin")
            + 0.10 * milieu.get("il6")
            + 0.08 * hpa.cortisol_norm()
            + 0.08 * hsueh
        )
        v_chem = approach - withdraw
        v_body = body.valence_body()
        v_target = clamp(0.65 * v_chem + 0.35 * v_body, -1.0, 1.0)

        a_target = clamp(
            0.45 * body_arousal
            + 0.18 * hsueh
            + 0.20 * milieu.get("ne")
            + 0.15 * milieu.get("adrenaline")
            + 0.12 * fear
            + 0.10 * circuits.get("SEEKING")
            + 0.08 * unexpected_uncertainty
        )
        d_target = clamp(
            0.40
            + 0.25 * circuits.get("SEEKING")
            + 0.15 * circuits.get("RAGE")
            + 0.10 * milieu.get("avp")
            - 0.25 * fear
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
        prev_pe = self.prediction_error
        self.prediction_error = leaky_integrator(self.prediction_error, pe_t, 0.6, dt)
        self.valence = clamp(self.valence, -1.0, 1.0)
        self.arousal = clamp(self.arousal)
        self.dominance = clamp(self.dominance)
        self.allostatic_load = clamp(self.allostatic_load)
        self.prediction_error = clamp(self.prediction_error)

        # Joffily & Coricelli 2013: valence_fe = −dF/dt, F ≈ PE proxy.
        # Scale is a prior (PE ∈ [0, 1], dt ~ 0.05 min). Sidecar only.
        dpe = (self.prediction_error - prev_pe) / max(dt, 1e-9)
        prev_vfe = self.valence_fe
        self.valence_fe = clamp(-dpe, -1.0, 1.0)
        self.fe_accel = clamp((self.valence_fe - prev_vfe) / max(dt, 1e-9), -1.0, 1.0)
        self._prev_pe = prev_pe

        # Keramati & Gutkin 2014 annotation: distance from a comfortable
        # body set. Does NOT replace allostatic_load. Does NOT write valence.
        self.homeostatic_drive = clamp(
            0.40 * (1.0 - body.energy)
            + 0.35 * self.allostatic_load
            + 0.25 * (1.0 - body.vagal_tone)
        )

        # Slow sensitization Z (RCAD 0.1.0 hole; HYPOTHESIS). Leaky from
        # current load / unexpected uncertainty / FEAR; extinguished by
        # recovery axes already on the body. Does NOT write allostatic_load.
        sens_t = clamp(
            0.45 * self.allostatic_load
            + 0.25 * unexpected_uncertainty
            + 0.20 * fear
            - 0.15 * body.vagal_tone
            - 0.10 * body.energy
        )
        self.sensitization = leaky_integrator(self.sensitization, sens_t, 18.0, dt)
        self.sensitization = clamp(self.sensitization)

    def as_dict(self) -> dict[str, float]:
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "allostatic_load": self.allostatic_load,
            "prediction_error": self.prediction_error,
            "valence_fe": self.valence_fe,
            "fe_accel": self.fe_accel,
            "homeostatic_drive": self.homeostatic_drive,
            "sensitization": self.sensitization,
        }
