"""Per-agent attachment / pair-bond book.

Oxytocin and vasopressin effects are *target-specific* (Carter; Insel;
Panksepp CARE/LUST). A global OT level without an address is a modelling
error. Each known other has a bond record updated by relational events.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Bond:
    agent: str
    familiarity: float = 0.2
    trust: float = 0.4
    affiliation: float = 0.4  # OT-weighted liking
    territorial: float = 0.2  # AVP-weighted claim / jealousy
    safety: float = 0.5
    last_t_min: float = 0.0
    n_events: int = 0

    def as_dict(self) -> dict[str, float | str | int]:
        return {
            "agent": self.agent,
            "familiarity": self.familiarity,
            "trust": self.trust,
            "affiliation": self.affiliation,
            "territorial": self.territorial,
            "safety": self.safety,
            "n_events": self.n_events,
        }


@dataclass
class BondBook:
    bonds: dict[str, Bond] = field(default_factory=dict)

    def get(self, agent: str) -> Bond:
        if agent not in self.bonds:
            self.bonds[agent] = Bond(agent=agent)
        return self.bonds[agent]

    def update_from_event(
        self,
        agent: str,
        kind: str,
        intensity: float,
        in_group: float,
        ot: float,
        avp: float,
        t_min: float,
    ) -> Bond:
        b = self.get(agent)
        b.n_events += 1
        b.last_t_min = t_min
        b.familiarity = _ema(b.familiarity, min(1.0, b.familiarity + 0.05 + 0.08 * intensity), 0.15)
        appetitive = kind in {
            "warmth",
            "praise",
            "trust_signal",
            "inclusion",
            "play_invite",
            "safety",
            "repair",
            "humor",
            "confession",
            "self_disclosure",
            "other_disclosure",
        }
        aversive = kind in {
            "threat",
            "loss",
            "rejection",
            "insult",
            "abandonment",
            "frustration",
        }
        if appetitive:
            gain = intensity * (0.45 + 0.40 * ot) * (0.5 + 0.5 * in_group)
            b.trust = _ema(b.trust, min(1.0, b.trust + gain), 0.20)
            b.affiliation = _ema(b.affiliation, min(1.0, b.affiliation + gain), 0.18)
            b.safety = _ema(b.safety, min(1.0, b.safety + 0.8 * gain), 0.16)
        if aversive:
            loss = intensity * (0.50 + 0.20 * (1.0 - ot))
            b.trust = _ema(b.trust, max(0.0, b.trust - loss), 0.22)
            b.safety = _ema(b.safety, max(0.0, b.safety - loss), 0.20)
            if kind in {"insult", "rejection", "abandonment"}:
                b.affiliation = _ema(b.affiliation, max(0.0, b.affiliation - 0.7 * loss), 0.18)
        if kind in {"boundary", "demand"}:
            b.territorial = _ema(b.territorial, min(1.0, b.territorial + 0.15 * intensity * (0.4 + avp)), 0.12)
        if kind == "play_invite":
            b.affiliation = _ema(b.affiliation, min(1.0, b.affiliation + 0.12 * intensity), 0.15)
        return b

    def as_dict(self) -> dict[str, dict]:
        return {k: v.as_dict() for k, v in self.bonds.items()}


def _ema(prev: float, target: float, alpha: float) -> float:
    return (1.0 - alpha) * prev + alpha * target
