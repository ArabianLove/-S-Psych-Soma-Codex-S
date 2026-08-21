"""Immutable public snapshot of organism state.

This is the *only* object an LLM adapter, a test, or a UI is allowed to read.
Internal integrators stay private so the bijective contract can be versioned.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Snapshot:
    t_min: float
    tod_hours: float
    chemistry: dict[str, float]
    circuits: dict[str, float]
    affect: dict[str, float]
    body: dict[str, float]
    hpa: dict[str, float]
    emotion: dict[str, Any]
    relational: dict[str, Any]
    policy: dict[str, Any]
    constitution: str = "default"
    epistemics: dict[str, str] = field(default_factory=dict)
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def compact(self) -> dict[str, Any]:
        """Lossy but token-cheap view for LLM system prompts."""
        top_chem = sorted(self.chemistry.items(), key=lambda kv: abs(kv[1] - 0.25), reverse=True)[:8]
        top_circ = sorted(self.circuits.items(), key=lambda kv: kv[1], reverse=True)
        mix = self.emotion.get("mixture", {})
        top_mix = sorted(mix.items(), key=lambda kv: kv[1], reverse=True)[:4]
        return {
            "t_min": round(self.t_min, 3),
            "tod_hours": round(self.tod_hours, 2),
            "emotion": self.emotion.get("label"),
            "emotion_confidence": round(float(self.emotion.get("confidence", 0.0)), 3),
            "granularity": round(float(self.emotion.get("granularity", 0.0)), 3),
            "mixture": {k: round(v, 3) for k, v in top_mix},
            "valence": round(self.affect["valence"], 3),
            "arousal": round(self.affect["arousal"], 3),
            "dominance": round(self.affect["dominance"], 3),
            "allostatic_load": round(self.affect["allostatic_load"], 3),
            "prediction_error": round(self.affect["prediction_error"], 3),
            "sensitization": round(self.affect.get("sensitization", 0.0), 3),
            "circuits": {k: round(v, 3) for k, v in top_circ},
            "chemistry": {k: round(v, 3) for k, v in top_chem},
            "hr_bpm": round(self.body["heart_rate_bpm"], 1),
            "vagal_tone": round(self.body["vagal_tone"], 3),
            "cortisol_ug_dl": round(self.hpa["cortisol_ug_dl"], 2),
            "constitution": self.constitution,
            "policy": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in self.policy.items()},
        }
