"""Constructed emotion: circuit occupancies × core affect × relational concept.

This is the Barrett half of the dual architecture.

Panksepp supplies the *primary-process occupancies* (subcortical command
systems). Barrett supplies the claim that the *word* "anger" / "grief" /
"anxiety" is a conceptual categorisation of affect + context, not a natural
kind with a neural fingerprint (Barrett 2017 Soc Cogn Affect Neurosci 12:1-23,
esp. §§classical-view / degeneracy / Table 1).

We therefore:
  1. keep circuit occupancies as first-class state (Panksepp);
  2. construct a labelled emotion as the nearest neighbour in a small,
     explicit concept space (Barrett / Barsalou ad-hoc concepts);
  3. allow mixtures (mean-field; Friston-style factorisation noted in
     Smith, Parr, Friston 2020 Front Comput Neurosci 14:30).

The concept space is a documented, editable prior — not a claim that these
are the only human emotions. Degeneracy is honoured: the same label can be
reached from different circuit combinations.
"""

from __future__ import annotations

from dataclasses import dataclass

from psych_soma_codex.affect.core_affect import CoreAffect
from psych_soma_codex.circuits.primary import PrimaryCircuits
from psych_soma_codex.core.mathutil import cosine_similarity, softmax


# Concept prototypes live in the joint space
# [SEEKING, RAGE, FEAR, LUST, CARE, GRIEF, PLAY, valence, arousal, dominance]
# Values are constitutive priors (HYPOTHESIS), signs follow Panksepp 2010.

CONCEPTS: dict[str, tuple[float, ...]] = {
    "curious": (0.80, 0.05, 0.10, 0.10, 0.15, 0.05, 0.25, 0.45, 0.55, 0.60),
    "eager": (0.85, 0.10, 0.08, 0.20, 0.15, 0.04, 0.30, 0.55, 0.70, 0.65),
    "angry": (0.25, 0.85, 0.25, 0.05, 0.05, 0.10, 0.05, -0.45, 0.75, 0.70),
    "irritated": (0.20, 0.55, 0.20, 0.05, 0.08, 0.08, 0.05, -0.25, 0.50, 0.55),
    "afraid": (0.15, 0.15, 0.85, 0.04, 0.10, 0.20, 0.04, -0.55, 0.80, 0.20),
    "anxious": (0.20, 0.10, 0.60, 0.05, 0.12, 0.18, 0.06, -0.30, 0.55, 0.30),
    "desirous": (0.55, 0.08, 0.10, 0.85, 0.25, 0.05, 0.20, 0.50, 0.65, 0.55),
    "tender": (0.25, 0.04, 0.08, 0.15, 0.85, 0.10, 0.20, 0.55, 0.30, 0.45),
    "protective": (0.35, 0.20, 0.15, 0.08, 0.80, 0.08, 0.10, 0.25, 0.50, 0.65),
    "grief-stricken": (0.08, 0.10, 0.20, 0.04, 0.20, 0.90, 0.04, -0.75, 0.45, 0.15),
    "lonely": (0.15, 0.08, 0.15, 0.08, 0.25, 0.65, 0.08, -0.45, 0.30, 0.25),
    "playful": (0.45, 0.08, 0.06, 0.15, 0.25, 0.04, 0.85, 0.60, 0.60, 0.55),
    "joyful": (0.50, 0.04, 0.05, 0.20, 0.35, 0.04, 0.70, 0.75, 0.55, 0.55),
    "calm": (0.20, 0.04, 0.06, 0.08, 0.25, 0.06, 0.15, 0.25, 0.18, 0.50),
    "numb": (0.08, 0.05, 0.08, 0.04, 0.08, 0.20, 0.04, -0.15, 0.12, 0.30),
    "ashamed": (0.10, 0.12, 0.30, 0.05, 0.15, 0.40, 0.04, -0.50, 0.40, 0.15),
    "trusting": (0.30, 0.04, 0.08, 0.12, 0.70, 0.06, 0.25, 0.50, 0.28, 0.50),
    "vigilant": (0.40, 0.15, 0.55, 0.06, 0.10, 0.10, 0.08, -0.10, 0.65, 0.45),
}


@dataclass(frozen=True)
class ConstructedEmotion:
    label: str
    confidence: float
    mixture: dict[str, float]
    granularity: float
    notes: str


def _feature_vector(circuits: PrimaryCircuits, affect: CoreAffect) -> list[float]:
    return [
        circuits.get("SEEKING"),
        circuits.get("RAGE"),
        circuits.get("FEAR"),
        circuits.get("LUST"),
        circuits.get("CARE"),
        circuits.get("GRIEF"),
        circuits.get("PLAY"),
        affect.valence,
        affect.arousal,
        affect.dominance,
    ]


def construct_emotion(
    circuits: PrimaryCircuits,
    affect: CoreAffect,
    temperature: float = 0.18,
) -> ConstructedEmotion:
    vec = _feature_vector(circuits, affect)
    keys = list(CONCEPTS.keys())
    sims = [cosine_similarity(vec, CONCEPTS[k]) for k in keys]
    # Shift cosine from [-1,1] to a non-negative weight.
    weights = [(s + 1.0) * 0.5 for s in sims]
    probs = softmax(weights, temperature=temperature)
    mixture = {k: float(p) for k, p in zip(keys, probs)}
    best_i = max(range(len(keys)), key=lambda i: probs[i])
    # Granularity: entropy of the mixture, inverted. High = precise label.
    import math

    ent = -sum(p * math.log(p + 1e-12) for p in probs)
    max_ent = math.log(len(probs))
    granularity = 1.0 - (ent / max_ent if max_ent > 0 else 0.0)
    return ConstructedEmotion(
        label=keys[best_i],
        confidence=float(probs[best_i]),
        mixture=mixture,
        granularity=float(granularity),
        notes=(
            "Constructed category over Panksepp circuits × Russell core affect. "
            "Not a natural-kind fingerprint (Barrett 2017)."
        ),
    )
