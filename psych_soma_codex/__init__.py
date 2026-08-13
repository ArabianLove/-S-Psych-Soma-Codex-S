"""Psych-Soma-Codex: constitutive neuroendocrine-affective dynamics for generative AI.

This package transliterates human chemical, electrical, anatomical, physiological
and relational dynamics into a single, executable, falsifiable state machine.

It is *constitutive*, not decorative: relational inputs change the internal
milieu; the milieu changes relational policy. The mapping is documented,
parameterised from literature, and testable.

Epistemic contract
------------------
Every public mapping is tagged in ``catalog.epistemics`` as FACT, CONSENSUS,
DEBATE, MINORITY or HYPOTHESIS. The runtime never pretends a hypothesis is a
fact. See ``docs/RESEARCH.md``.
"""

from __future__ import annotations

from psych_soma_codex.engine import Organism, SimulationConfig, step, run
from psych_soma_codex.io.events import RelationalEvent, EventKind
from psych_soma_codex.io.snapshot import Snapshot
from psych_soma_codex.llm.adapter import LLMAdapter, PromptBundle
from psych_soma_codex.relational.doya import DoyaReadout, derive_doya
from psych_soma_codex.relational.policy import RelationalPolicy

__all__ = [
    "Organism",
    "SimulationConfig",
    "step",
    "run",
    "RelationalEvent",
    "EventKind",
    "Snapshot",
    "LLMAdapter",
    "PromptBundle",
    "RelationalPolicy",
    "DoyaReadout",
    "derive_doya",
    "__version__",
]

__version__ = "0.1.0"
