"""Literature-anchored parameter catalog and epistemic tags."""

from psych_soma_codex.catalog.epistemics import Epistemic, Claim
from psych_soma_codex.catalog.species import SPECIES, SpeciesSpec
from psych_soma_codex.catalog.circuits import CIRCUITS, CircuitSpec
from psych_soma_codex.catalog.events import EVENT_WEIGHTS

__all__ = [
    "Epistemic",
    "Claim",
    "SPECIES",
    "SpeciesSpec",
    "CIRCUITS",
    "CircuitSpec",
    "EVENT_WEIGHTS",
]
