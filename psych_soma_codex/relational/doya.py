"""Doya 2002 metalearning readout — optional HYPOTHESIS layer.

Doya, K. (2002), *Metalearning and neuromodulation*, *Neural Networks*
15:495–506, section 3, items 1–4 (primary PDF verified 13 August 2026):

    1. Dopamine signals the TD error δ.
    2. Serotonin controls the discount factor γ.
    3. Noradrenaline controls the inverse temperature β.
    4. Acetylcholine controls the learning rate α.

These are *metalearning hypotheses*, not biological facts. They sit
beside — they do not replace — the constitutive Yu & Dayan 2005 mapping
already in ``engine.LearningState`` (ACh = expected uncertainty, NE =
unexpected uncertainty).

This module is a *readout*. It never writes chemistry, never labels an
emotion, never decides ``forbidden`` / ``preferred_acts``. Those remain
Panksepp occupancy + Barrett mixture + ``derive_policy``.

Ranges
------
γ ∈ [0.50, 0.99]   high 5-HT → far-sighted discount
β ∈ [0.40, 8.00]   high NE  → more exploitative (inverse temperature)
α ∈ [0.02, 0.45]   high ACh → faster learning-rate recommendation
δ ∈ ℝ              last reward-prediction error, passed through

Epistemic: HYPOTHESIS (Doya 2002 §3). Compatible with, not identical to,
Yu & Dayan 2005.
"""

from __future__ import annotations

from dataclasses import dataclass

from psych_soma_codex.chemistry.milieu import ChemicalMilieu
from psych_soma_codex.core.mathutil import clamp


@dataclass(frozen=True)
class DoyaReadout:
    """Four Doya metalearning numbers derived from the current milieu."""

    gamma: float
    beta: float
    alpha: float
    delta: float
    epistemic: str = "HYPOTHESIS (Doya 2002 Neural Networks 15:495-506 §3)"

    def as_dict(self) -> dict:
        return {
            "gamma": self.gamma,
            "beta": self.beta,
            "alpha": self.alpha,
            "delta": self.delta,
            "epistemic": self.epistemic,
        }


def derive_doya(milieu: ChemicalMilieu, last_rpe: float = 0.0) -> DoyaReadout:
    """Map 5-HT / NE / ACh occupancies onto (γ, β, α); pass δ through.

    The maps are affine on the unit occupancy interval, then clamped.
    Magnitudes are constitutive priors (HYPOTHESIS). Signs follow Doya §3:
    more serotonin → larger γ; more noradrenaline → larger β; more
    acetylcholine → larger α.
    """
    fiveht = milieu.get("fiveht")
    ne = milieu.get("ne")
    ach = milieu.get("ach")
    gamma = clamp(0.50 + 0.49 * fiveht, 0.50, 0.99)
    beta = clamp(0.40 + 7.60 * ne, 0.40, 8.00)
    alpha = clamp(0.02 + 0.43 * ach, 0.02, 0.45)
    return DoyaReadout(gamma=gamma, beta=beta, alpha=alpha, delta=float(last_rpe))
