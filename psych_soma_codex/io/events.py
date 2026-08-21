"""Relational events: the sensory face of the Markov blanket.

An event is a structured observation of the *other* (or of the self).
It is the only sanctioned way for the outside to touch the milieu.
Intensity ∈ [0, 1], valence_hint ∈ [-1, 1] is the emitter's appraisal,
not the organism's constructed emotion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventKind(str, Enum):
    WARMTH = "warmth"
    PRAISE = "praise"
    TRUST_SIGNAL = "trust_signal"
    INCLUSION = "inclusion"
    PLAY_INVITE = "play_invite"
    NOVELTY = "novelty"
    THREAT = "threat"
    LOSS = "loss"
    REJECTION = "rejection"
    FRUSTRATION = "frustration"
    INSULT = "insult"
    ABANDONMENT = "abandonment"
    SAFETY = "safety"
    REPAIR = "repair"
    BOUNDARY = "boundary"
    DEMAND = "demand"
    SILENCE = "silence"
    HUMOR = "humor"
    CONFESSION = "confession"
    SICKNESS = "sickness"
    # Meta / cognitive
    PREDICTION_CONFIRMED = "prediction_confirmed"
    PREDICTION_VIOLATED = "prediction_violated"
    SELF_DISCLOSURE = "self_disclosure"
    OTHER_DISCLOSURE = "other_disclosure"


# Qualitative sign of each kind, used by the uncertainty / RPE layer.
APPETITIVE = {
    EventKind.WARMTH,
    EventKind.PRAISE,
    EventKind.TRUST_SIGNAL,
    EventKind.INCLUSION,
    EventKind.PLAY_INVITE,
    EventKind.NOVELTY,
    EventKind.SAFETY,
    EventKind.REPAIR,
    EventKind.HUMOR,
    EventKind.PREDICTION_CONFIRMED,
    EventKind.SELF_DISCLOSURE,
    EventKind.OTHER_DISCLOSURE,
}
AVERSIVE = {
    EventKind.THREAT,
    EventKind.LOSS,
    EventKind.REJECTION,
    EventKind.FRUSTRATION,
    EventKind.INSULT,
    EventKind.ABANDONMENT,
    EventKind.SICKNESS,
    EventKind.PREDICTION_VIOLATED,
}


@dataclass
class RelationalEvent:
    kind: EventKind
    intensity: float = 0.6
    valence_hint: float = 0.0
    agent: str = "other"
    in_group: float = 0.7  # 1 = fully in-group (OT gain), 0 = out-group
    expectedness: float = 0.5  # 1 = fully predicted
    # Optional appraisal tags (RCAD 0.1.0 hole; HYPOTHESIS). Defaults are
    # neutral: they do not inject chemistry. If set, they only modulate
    # the process packet in derive_policy.
    controllability: float = 0.5
    agency: float = 0.5
    text: str = ""
    tags: dict[str, Any] = field(default_factory=dict)
    t_min: float | None = None

    def __post_init__(self) -> None:
        if isinstance(self.kind, str):
            self.kind = EventKind(self.kind)
        self.intensity = _clip(self.intensity, 0.0, 1.0)
        self.valence_hint = _clip(self.valence_hint, -1.0, 1.0)
        self.in_group = _clip(self.in_group, 0.0, 1.0)
        self.expectedness = _clip(self.expectedness, 0.0, 1.0)
        self.controllability = _clip(self.controllability, 0.0, 1.0)
        self.agency = _clip(self.agency, 0.0, 1.0)
        if self.valence_hint == 0.0:
            if self.kind in APPETITIVE:
                self.valence_hint = 0.45
            elif self.kind in AVERSIVE:
                self.valence_hint = -0.45

    @property
    def surprise(self) -> float:
        return 1.0 - self.expectedness

    @property
    def signed_intensity(self) -> float:
        return self.intensity * (1.0 if self.kind in APPETITIVE else -1.0 if self.kind in AVERSIVE else 0.0)


def _clip(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else float(x)


def parse_event(payload: dict[str, Any] | RelationalEvent | EventKind | str) -> RelationalEvent:
    if isinstance(payload, RelationalEvent):
        return payload
    if isinstance(payload, EventKind):
        return RelationalEvent(kind=payload)
    if isinstance(payload, str):
        return RelationalEvent(kind=EventKind(payload))
    kind = payload.get("kind") or payload.get("type") or payload.get("event")
    return RelationalEvent(
        kind=EventKind(kind),
        intensity=float(payload.get("intensity", 0.6)),
        valence_hint=float(payload.get("valence_hint", 0.0)),
        agent=str(payload.get("agent", "other")),
        in_group=float(payload.get("in_group", 0.7)),
        expectedness=float(payload.get("expectedness", 0.5)),
        controllability=float(payload.get("controllability", 0.5)),
        agency=float(payload.get("agency", 0.5)),
        text=str(payload.get("text", "")),
        tags=dict(payload.get("tags", {})),
        t_min=payload.get("t_min"),
    )
