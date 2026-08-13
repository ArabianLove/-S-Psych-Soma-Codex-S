"""Deterministic numerical primitives used by every dynamical layer.

All state variables that represent concentrations, occupancies or probabilities
are kept in [0, 1] unless a catalog entry explicitly uses a physical unit.
Physical-unit quantities (e.g. cortisol µg/dL) live in ``interoception.hpa``
and are converted to a unit interval via documented saturating maps.
"""

from __future__ import annotations

from typing import Callable, Sequence


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return float(x)


def saturate(x: float) -> float:
    """Logistic squash centred at 0.5 with unit slope near the origin of (x-0.5)."""
    # Numerically stable logistic: 1 / (1 + exp(-k*(x-0.5)))
    z = 6.0 * (x - 0.5)
    if z >= 20.0:
        return 1.0
    if z <= -20.0:
        return 0.0
    return 1.0 / (1.0 + __import__("math").exp(-z))


def hill(x: float, k: float, n: float = 2.0) -> float:
    """Hill activation. x, k >= 0; n > 0. Returns x^n / (k^n + x^n)."""
    if x <= 0.0:
        return 0.0
    if k <= 0.0:
        return 1.0
    xn = x ** n
    kn = k ** n
    return xn / (kn + xn)


def exp_decay(value: float, rate: float, dt: float) -> float:
    """Exact solution of dy/dt = -rate * y over one step."""
    if rate <= 0.0:
        return value
    return value * __import__("math").exp(-rate * dt)


def leaky_integrator(value: float, target: float, tau: float, dt: float) -> float:
    """Exact solution of dy/dt = (target - y) / tau."""
    if tau <= 1e-12:
        return target
    a = __import__("math").exp(-dt / tau)
    return a * value + (1.0 - a) * target


def rk4_step(
    f: Callable[[float, Sequence[float]], list[float]],
    t: float,
    y: Sequence[float],
    dt: float,
) -> list[float]:
    """Classical RK4 for a first-order autonomous-or-not ODE system."""
    y0 = list(y)
    n = len(y0)

    def _add(a: Sequence[float], b: Sequence[float], s: float) -> list[float]:
        return [a[i] + s * b[i] for i in range(n)]

    k1 = f(t, y0)
    k2 = f(t + 0.5 * dt, _add(y0, k1, 0.5 * dt))
    k3 = f(t + 0.5 * dt, _add(y0, k2, 0.5 * dt))
    k4 = f(t + dt, _add(y0, k3, dt))
    return [
        y0[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
        for i in range(n)
    ]


def softmax(xs: Sequence[float], temperature: float = 1.0) -> list[float]:
    import math

    t = max(temperature, 1e-6)
    m = max(xs) if xs else 0.0
    exps = [math.exp((x - m) / t) for x in xs]
    z = sum(exps) or 1.0
    return [e / z for e in exps]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    import math

    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return dot / (na * nb)
