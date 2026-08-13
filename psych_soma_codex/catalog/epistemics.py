"""Epistemic contract.

Every public mapping in this codebase is tagged. The runtime never promotes a
HYPOTHESIS to a FACT. Tags follow the research protocol in docs/RESEARCH.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Epistemic(str, Enum):
    FACT = "FACT"  # primary source or two independent sources, uncontested
    CONSENSUS = "CONSENSUS"  # majority of peer-reviewed literature
    DEBATE = "DEBATE"  # serious published disagreement
    MINORITY = "MINORITY"  # minority but non-dismissible
    HYPOTHESIS = "HYPOTHESIS"  # modelling choice, not a biological claim
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Claim:
    statement: str
    epistemic: Epistemic
    sources: tuple[str, ...]
    notes: str = ""
