"""Minimal mechanistic HPA axis (CRH, ACTH, cortisol).

Equations follow the Vinther / Andersen / Ahmad lineage of three coupled
nonlinear ODEs, simplified for real-time affective coupling:

    dR/dt = (k1 + D*k2) * stress_gain * (1 - mu * hill(C, Rc, beta)) - h1 R
    dA/dt = (k4 R + k3 * avp_drive) * (1 - rho * hill(C, Rc, beta)) - h2 A
            + ultradian_acth_amp * U
    dC/dt = k5 A - h3 C + ultradian_cortisol_amp * U

Parameters default to Andersen et al. 2013 Math Biosci 246:122-138 Table-class
values as compiled by Ahmad, Jena, Priyadarshi 2023 arXiv:2311.04570 Table 2:

    h1 = 0.1732 /min   (CRH removal)
    h2 = 0.0315 /min   (ACTH removal)
    h3 = 0.0105 /min   (cortisol removal)

Circadian drive D is a raised, phase-shifted sinusoid peaking ~07:30
(cortisol awakening response; Ahmad et al. 2023 §1.1; Van Cauter lineage).

Ultradian drive U (HYPOTHESIS) is a small harmonic stand-in for the
pituitary–adrenal delay loop (Walker, Terry & Lightman 2010 Proc R Soc B
277:1627–1633). Period ~75 min sits in the 60–90 min band (Windle 1998a
interpulse ~47–55 min is the empirical centre; we take a round mid-band
period, not a fitted DDE). This is NOT the Walker/Churilov delay-differential
equation and NOT a sex-specific 16.4♂ / 18.5♀ deconvolution fit. Andersen
removal rates are untouched.

Units
-----
R is a dimensionless hypothalamic drive (not a plasma assay).
A is tracked in a normalized unit that maps onto pg/mL via ``acth_scale``.
C is tracked in µg/dL (human total cortisol, order 5–25 µg/dL diurnal).

Epistemic
---------
FACT: half-lives / removal rates (Andersen 2013).
CONSENSUS: negative feedback of cortisol on CRH and ACTH.
HYPOTHESIS: the precise coupling coefficients from affective circuits
on ``stress_gain`` (we expose them for falsification).
HYPOTHESIS: small ultradian harmonic on ACTH/cortisol (Walker 2010
mechanism as stand-in, not the DDE).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from psych_soma_codex.core.mathutil import clamp, hill, rk4_step


@dataclass
class HPAParams:
    h1: float = 0.1732
    h2: float = 0.0315
    h3: float = 0.0105
    k1: float = 0.35
    k2: float = 0.28
    k3: float = 0.18
    k4: float = 0.0821
    k5: float = 0.18  # scaled so diurnal C sits near 8–20 µg/dL
    mu: float = 0.85
    rho: float = 0.75
    rc: float = 10.0  # µg/dL saturation (GR occupancy)
    beta: float = 3.0
    acth_scale: float = 20.0  # 1.0 internal ≈ 20 pg/mL
    cortisol_ref: float = 12.0  # µg/dL typical morning mid
    # Ultradian harmonic (HYPOTHESIS). Period ~75 min sits in the 60–90 min
    # band (Walker 2010; Windle 1998a interpulse ~47–55 min is the empirical
    # centre; we take a round mid-band period, not a fitted DDE).
    ultradian_period_min: float = 75.0
    ultradian_acth_amp: float = 0.012
    ultradian_cortisol_amp: float = 0.35  # µg/dL — small vs diurnal 5–25


@dataclass
class HPAAxis:
    """Physical HPA integrator.

    State: R (drive), A (internal ACTH), C (µg/dL cortisol).
    """

    params: HPAParams | None = None
    R: float = 0.4
    A: float = 0.4
    C: float = 8.0
    stress_gain: float = 1.0
    avp_drive: float = 0.2

    def __post_init__(self) -> None:
        if self.params is None:
            self.params = HPAParams()

    @staticmethod
    def circadian(tod_hours: float) -> float:
        """Raised sinusoid, peak near 07:30, trough near 00:00.

        Ahmad et al. 2023 eq. (2.1) use a Fourier sum; a single harmonic
        captures the first-order awakening response for our purposes.
        """
        # Peak at 7.5 h: sin(2π (t - 1.5)/24) is 0 at 1.5, 1 at 7.5.
        phase = 2.0 * math.pi * (tod_hours - 1.5) / 24.0
        return 0.55 + 0.45 * math.sin(phase)

    def ultradian(self, tod_hours: float) -> float:
        """Unit-amplitude sinusoid, period = ``ultradian_period_min``.

        Walker 2010: pulses arise from pituitary–adrenal delay + feedback,
        not a hypothalamic pulse generator. We do not integrate that DDE;
        this harmonic is a declared stand-in (HYPOTHESIS).
        """
        p = self.params
        assert p is not None
        period_h = p.ultradian_period_min / 60.0
        if period_h <= 1e-12:
            return 0.0
        return math.sin(2.0 * math.pi * tod_hours / period_h)

    def rhs(self, t: float, y: list[float], tod_hours: float) -> list[float]:
        p = self.params
        assert p is not None
        R, A, C = y
        D = self.circadian(tod_hours)
        U = self.ultradian(tod_hours)
        fb_c = hill(max(C, 0.0), p.rc, p.beta)
        dR = (p.k1 + D * p.k2) * self.stress_gain * (1.0 - p.mu * fb_c) - p.h1 * R
        dA = (p.k4 * max(R, 0.0) + p.k3 * self.avp_drive) * (1.0 - p.rho * fb_c) - p.h2 * A
        dA = dA + p.ultradian_acth_amp * U
        dC = p.k5 * max(A, 0.0) - p.h3 * C + p.ultradian_cortisol_amp * U
        return [dR, dA, dC]

    def step(self, dt: float, tod_hours: float) -> None:
        def f(t: float, y: list[float]) -> list[float]:
            return self.rhs(t, y, tod_hours)

        y1 = rk4_step(f, 0.0, [self.R, self.A, self.C], dt)
        self.R = max(y1[0], 0.0)
        self.A = max(y1[1], 0.0)
        self.C = max(y1[2], 0.0)

    @property
    def cortisol_ug_dl(self) -> float:
        return self.C

    @property
    def acth_pg_ml(self) -> float:
        assert self.params is not None
        return self.A * self.params.acth_scale

    def cortisol_norm(self) -> float:
        """Saturating map µg/dL → [0, 1] around a 12 µg/dL reference."""
        assert self.params is not None
        return clamp(self.C / (self.C + self.params.cortisol_ref), 0.0, 1.0)

    def crh_norm(self) -> float:
        return clamp(self.R / (self.R + 0.8), 0.0, 1.0)

    def acth_norm(self) -> float:
        return clamp(self.A / (self.A + 0.8), 0.0, 1.0)

    def as_dict(self) -> dict[str, float]:
        return {
            "crh_drive": self.R,
            "acth_internal": self.A,
            "cortisol_ug_dl": self.C,
            "acth_pg_ml": self.acth_pg_ml,
            "cortisol_norm": self.cortisol_norm(),
            "circadian": self.circadian(0.0),  # placeholder; engine overwrites
            "ultradian": 0.0,  # placeholder; engine overwrites
        }
