"""Default weights: relational event kind → chemical / circuit injections.

These weights are constitutive *priors*, tagged HYPOTHESIS unless a specific
source is cited. They are the bijective half of the mapping
relational stimulus → milieu. The inverse half lives in ``relational.policy``.
"""

from __future__ import annotations

from psych_soma_codex.catalog.epistemics import Epistemic

# Each entry: {target: (delta, tau_override_or_None)}
# Targets may be species keys or circuit keys (circuit keys inject into
# the circuit's instantaneous drive, not its slow state).

EVENT_WEIGHTS: dict[str, dict[str, tuple[float, float | None]]] = {
    "warmth": {
        "ot": (0.28, None),
        "opioid": (0.18, None),
        "CARE": (0.38, None),
        "GRIEF": (-0.14, None),
        "fiveht": (0.06, None),
    },
    "praise": {
        "da": (0.28, 0.3),
        "SEEKING": (0.26, None),
        "opioid": (0.10, None),
        "PLAY": (0.14, None),
    },
    "trust_signal": {
        "ot": (0.32, None),
        "CARE": (0.24, None),
        "FEAR": (-0.12, None),
    },
    "inclusion": {
        "ot": (0.20, None),
        "opioid": (0.20, None),
        "PLAY": (0.18, None),
        "GRIEF": (-0.18, None),
    },
    "play_invite": {
        "PLAY": (0.48, None),
        "da": (0.16, None),
        "endocannabinoid": (0.14, None),
        "opioid": (0.12, None),
        "FEAR": (-0.08, None),
    },
    "novelty": {
        "ach": (0.24, None),
        "da": (0.14, 0.25),
        "SEEKING": (0.24, None),
        "ne": (0.10, None),
    },
    "threat": {
        "FEAR": (0.55, None),
        "crh": (0.30, None),
        "ne": (0.34, 0.2),
        "adrenaline": (0.38, 0.4),
        "cortisol": (0.10, None),
        "PLAY": (-0.22, None),
        "SEEKING": (-0.08, None),
    },
    "loss": {
        "GRIEF": (0.58, None),
        "crh": (0.22, None),
        "glu": (0.18, None),
        "opioid": (-0.24, None),
        "ot": (-0.10, None),
        "dynorphin": (0.22, None),
        "SEEKING": (-0.16, None),
    },
    "rejection": {
        "GRIEF": (0.42, None),
        "RAGE": (0.20, None),
        "opioid": (-0.18, None),
        "ot": (-0.14, None),
        "dynorphin": (0.16, None),
        "fiveht": (-0.08, None),
    },
    "frustration": {
        "RAGE": (0.48, None),
        "substance_p": (0.24, None),
        "glu": (0.16, None),
        "da": (-0.10, None),
        "SEEKING": (0.10, None),  # SEEKING remains on; thwarted
    },
    "insult": {
        "RAGE": (0.44, None),
        "substance_p": (0.20, None),
        "adrenaline": (0.16, None),
        "ot": (-0.12, None),
    },
    "abandonment": {
        "GRIEF": (0.62, None),
        "crh": (0.28, None),
        "opioid": (-0.28, None),
        "ot": (-0.20, None),
        "dynorphin": (0.24, None),
        "SEEKING": (-0.20, None),
        "FEAR": (0.16, None),
    },
    "safety": {
        "FEAR": (-0.24, None),
        "opioid": (0.14, None),
        "gaba": (0.12, None),
        "adrenaline": (-0.12, None),
        "CARE": (0.12, None),
    },
    "repair": {
        "ot": (0.24, None),
        "opioid": (0.18, None),
        "GRIEF": (-0.22, None),
        "RAGE": (-0.18, None),
        "CARE": (0.22, None),
        "dynorphin": (-0.10, None),
    },
    "boundary": {
        "avp": (0.12, None),
        "RAGE": (0.06, None),
        "FEAR": (-0.04, None),
        "fiveht": (0.06, None),
    },
    "demand": {
        "ne": (0.10, None),
        "cortisol": (0.06, None),
        "SEEKING": (0.06, None),
        "ach": (0.08, None),
    },
    "silence": {
        "GRIEF": (0.08, None),
        "ach": (0.10, None),  # expected uncertainty about the other
        "ne": (0.04, None),
    },
    "humor": {
        "PLAY": (0.20, None),
        "opioid": (0.10, None),
        "endocannabinoid": (0.08, None),
        "FEAR": (-0.06, None),
        "RAGE": (-0.06, None),
    },
    "confession": {
        "ot": (0.10, None),
        "FEAR": (0.08, None),
        "CARE": (0.10, None),
        "fiveht": (0.04, None),
    },
    "sickness": {
        "il6": (0.28, None),
        "SEEKING": (-0.20, None),
        "PLAY": (-0.16, None),
        "cortisol": (0.10, None),
    },
}

EVENT_EPISTEMIC = Epistemic.HYPOTHESIS
EVENT_EPISTEMIC_NOTE = (
    "Event→chemistry weights are constitutive priors (HYPOTHESIS). "
    "Qualitative signs follow Panksepp 2010 circuit chemistries; magnitudes "
    "are free parameters exposed for calibration and falsification."
)
