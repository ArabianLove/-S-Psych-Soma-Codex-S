"""Plane 0: constitution / temperament as a prior, not a decaying state.

Every organism has a character. It is not a folk label and it is not a
transient occupancy. It is a *prior* on rest, event gain, recovery τ,
chemical baselines and HPA glucocorticoid feedback, derived from genetics,
epigenetics, experience and the organism's own law.

Default is the identity. Same seed + same events remain bit-identical to
the pre-constitution organism. Named archetypes change the prior; they
never author ``forbidden`` by name, never touch Andersen ``h1/h2/h3``,
never classify an emotion.

Literature (signs CONSENSUS / DEBATE; magnitudes HYPOTHESIS)
------------------------------------------------------------
- Rothbart temperament (surgency / negative affectivity / effortful control)
  as a slow prior on resting circuit tone.
- Cloninger TCI (novelty seeking ≈ BAS, harm avoidance ≈ FFFS/BIS).
- Gray / McNaughton RST: BAS, FFFS, BIS as gain systems, not emotions.
- Meaney–Weaver maternal care → GR expression → HPA feedback
  (CONSENSUS mechanism; HYPOTHESIS magnitudes). Andersen removal rates
  stay FACT and are not scaled.

Epistemic: the *existence* of constitutional priors is CONSENSUS; every
number below is a modelling choice tagged HYPOTHESIS.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _norm_name(name: str) -> str:
    return name.strip().lower().replace("-", "_").replace(" ", "_")


@dataclass(frozen=True)
class Constitution:
    """Frozen prior. Empty maps and unit scales are the identity."""

    name: str = "default"
    event_gain: dict[str, float] = field(default_factory=dict)
    rest_offsets: dict[str, float] = field(default_factory=dict)
    tau_scale: float = 1.0
    tau_scales: dict[str, float] = field(default_factory=dict)
    chem_baseline_offsets: dict[str, float] = field(default_factory=dict)
    hpa_mu_scale: float = 1.0
    hpa_rho_scale: float = 1.0
    rest_stress_gain: float = 1.0
    notes: tuple[str, ...] = ()

    def is_identity(self) -> bool:
        if self.event_gain or self.rest_offsets or self.tau_scales or self.chem_baseline_offsets:
            return False
        return (
            abs(self.tau_scale - 1.0) < 1e-12
            and abs(self.hpa_mu_scale - 1.0) < 1e-12
            and abs(self.hpa_rho_scale - 1.0) < 1e-12
            and abs(self.rest_stress_gain - 1.0) < 1e-12
        )

    def gain(self, target: str) -> float:
        return float(self.event_gain.get(target, 1.0))

    def rest_offset(self, key: str) -> float:
        return float(self.rest_offsets.get(key, 0.0))

    def tau_for(self, key: str, base_tau: float) -> float:
        return float(base_tau) * self.tau_scale * float(self.tau_scales.get(key, 1.0))

    def chem_offset(self, key: str) -> float:
        return float(self.chem_baseline_offsets.get(key, 0.0))

    @classmethod
    def named(cls, name: str) -> "Constitution":
        key = _norm_name(name)
        if key in ("default", "identity", ""):
            return cls()
        aliases = {
            "fffs": "high_fffs",
            "high_fffs": "high_fffs",
            "bis": "high_bis",
            "high_bis": "high_bis",
            "bas": "high_bas",
            "high_bas": "high_bas",
            "meaney": "meaney_low_nurture",
            "low_nurture": "meaney_low_nurture",
            "meaney_low_nurture": "meaney_low_nurture",
        }
        resolved = aliases.get(key)
        if resolved is None or resolved not in ARCHETYPES:
            known = ", ".join(NAMES)
            raise ValueError(f"unknown constitution {name!r}; known: {known}")
        return ARCHETYPES[resolved]


# Named archetypes. Magnitudes are HYPOTHESIS; signs follow the literature
# cited in the module docstring. Do not treat these as diagnostic types.
ARCHETYPES: dict[str, Constitution] = {
    "high_fffs": Constitution(
        name="high_fffs",
        rest_offsets={"FEAR": 0.07, "PLAY": -0.02},
        event_gain={"FEAR": 1.40, "crh": 1.20, "ne": 1.15, "adrenaline": 1.15},
        tau_scales={"FEAR": 1.30},
        notes=(
            "Gray/McNaughton FFFS: higher resting FEAR, threat-target gain up, "
            "slower FEAR recovery. HYPOTHESIS magnitudes.",
        ),
    ),
    "high_bis": Constitution(
        name="high_bis",
        rest_offsets={"FEAR": 0.04, "GRIEF": 0.04, "SEEKING": -0.02},
        event_gain={"FEAR": 1.15, "GRIEF": 1.15},
        chem_baseline_offsets={"fiveht": 0.05},
        notes=(
            "Gray/McNaughton BIS: anxiety/conflict; resting FEAR/GRIEF up, "
            "5-HT baseline up. HYPOTHESIS magnitudes.",
        ),
    ),
    "high_bas": Constitution(
        name="high_bas",
        rest_offsets={"SEEKING": 0.07, "PLAY": 0.03, "FEAR": -0.02},
        event_gain={"da": 1.30, "SEEKING": 1.25},
        chem_baseline_offsets={"da": 0.05},
        notes=(
            "Gray BAS / Cloninger novelty seeking: higher resting SEEKING, "
            "praise/novelty DA gain up. HYPOTHESIS magnitudes.",
        ),
    ),
    "meaney_low_nurture": Constitution(
        name="meaney_low_nurture",
        rest_offsets={"FEAR": 0.03},
        hpa_mu_scale=0.70,
        hpa_rho_scale=0.75,
        rest_stress_gain=1.30,
        notes=(
            "Meaney–Weaver low nurture: weaker GR feedback (CONSENSUS "
            "mechanism), higher resting stress_gain (HYPOTHESIS magnitudes). "
            "Andersen h1/h2/h3 untouched.",
        ),
    ),
}

NAMES: tuple[str, ...] = ("default",) + tuple(ARCHETYPES.keys())
