"""Panksepp primary-process circuits and their chemical drivers.

Capitalised names follow Panksepp's convention (Panksepp 1998; 2010 Dialogues
Clin Neurosci 12:533-545; Davis & Montag 2019 Front Neurosci 12:1025).
"""

from __future__ import annotations

from dataclasses import dataclass

from psych_soma_codex.catalog.epistemics import Epistemic


@dataclass(frozen=True)
class CircuitSpec:
    key: str
    name: str
    valence: str  # approach | withdrawal
    drivers: tuple[str, ...]
    brakes: tuple[str, ...]
    anatomy: str
    epistemic: Epistemic
    sources: tuple[str, ...]
    notes: str = ""


CIRCUITS: dict[str, CircuitSpec] = {
    "SEEKING": CircuitSpec(
        key="SEEKING",
        name="SEEKING / expectancy / desire",
        valence="approach",
        drivers=("da",),
        brakes=("dynorphin", "il6", "cortisol"),
        anatomy="VTA → NAc / MFB / mPFC",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545",
            "Alcaro, Huber, Panksepp 2007 Brain Res Rev 56:283-321",
        ),
    ),
    "RAGE": CircuitSpec(
        key="RAGE",
        name="RAGE / anger",
        valence="withdrawal",
        drivers=("substance_p", "glu", "adrenaline"),
        brakes=("gaba", "opioid"),
        anatomy="medial amygdala → medial hypothalamus → dorsal PAG",
        epistemic=Epistemic.CONSENSUS,
        sources=("Panksepp 2010 Dialogues Clin Neurosci 12:533-545",),
        notes="Aroused when SEEKING is thwarted (frustration-aggression).",
    ),
    "FEAR": CircuitSpec(
        key="FEAR",
        name="FEAR / anxiety",
        valence="withdrawal",
        drivers=("crh", "ne", "adrenaline"),
        brakes=("gaba", "opioid"),
        anatomy="amygdala / BNST → hypothalamus → PAG",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545",
            "LeDoux 2012 (defence circuits; see Barrett 2017 for critique of 'fear' label)",
        ),
        notes=(
            "Panksepp treats FEAR as a primary circuit; Barrett 2017 treats "
            "'fear' as a constructed category. We simulate the *circuit* and "
            "construct the *label* downstream. See docs/RESEARCH.md §debate."
        ),
    ),
    "LUST": CircuitSpec(
        key="LUST",
        name="LUST / sexual",
        valence="approach",
        drivers=("da", "ot", "avp"),
        brakes=("cortisol", "il6"),
        anatomy="hypothalamic sexually dimorphic nuclei; OT/AVP sexually biased",
        epistemic=Epistemic.CONSENSUS,
        sources=("Panksepp 2010 Dialogues Clin Neurosci 12:533-545",),
    ),
    "CARE": CircuitSpec(
        key="CARE",
        name="CARE / nurturance",
        valence="approach",
        drivers=("ot", "prolactin", "opioid"),
        brakes=("cortisol",),
        anatomy="MPA / BNST / VTA; OT redeployed from sexuality",
        epistemic=Epistemic.CONSENSUS,
        sources=("Panksepp 2010 Dialogues Clin Neurosci 12:533-545",),
    ),
    "GRIEF": CircuitSpec(
        key="GRIEF",
        name="GRIEF / PANIC / separation-distress",
        valence="withdrawal",
        drivers=("glu", "crh"),
        brakes=("opioid", "ot", "prolactin"),
        anatomy="dorsal PAG → anterior cingulate",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545",
            "Panksepp & Watt 2011 (separation-distress gateway to depression)",
        ),
    ),
    "PLAY": CircuitSpec(
        key="PLAY",
        name="PLAY / social joy",
        valence="approach",
        drivers=("opioid", "endocannabinoid", "da"),
        brakes=("cortisol", "crh"),
        anatomy="subcortical; survives neonatal decortication (Panksepp 1994)",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp et al. 1994 Physiol Behav 56:429-443",
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545",
        ),
    ),
}
