"""LLM adapter: the constitutive interface between organism and generator.

The adapter does three things and only three:

1. *Sense*  — turn a human utterance into RelationalEvent(s)
2. *Condition* — compile the current Snapshot into a PromptBundle that an
   LLM (or any generator) must condition on
3. *Act* — if the generator emits a speech act, transliterate it back into
   an event so the organism can feel the consequences of its own output

This is the bijection the user asked for:
    relational input  →  affective state
    affective state   →  relational policy / generated act
    generated act     →  affective state  (self-perception)

No generator is bundled. The adapter is backend-agnostic: pass a callable
``generate(system, user) -> str`` or use the deterministic fallback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from psych_soma_codex.engine import Organism, run
from psych_soma_codex.io.events import EventKind, RelationalEvent
from psych_soma_codex.io.snapshot import Snapshot
from psych_soma_codex.llm.lexicon import act_to_event, infer_events_from_text


GenerateFn = Callable[[str, str], str]


@dataclass
class PromptBundle:
    """Everything an LLM needs, and nothing it should invent."""

    system: str
    user: str
    policy: dict
    compact_state: dict
    forbidden: tuple[str, ...]
    preferred_acts: tuple[str, ...]
    sampling_temperature: float
    top_p: float = 0.90
    presence_penalty: float = 0.20
    memory_decay: float = 0.12
    doya: dict = field(default_factory=dict)
    notes: tuple[str, ...] = ()

    def as_messages(self) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.user},
        ]

    def sampling_kwargs(self) -> dict:
        """Backend-facing decode knobs. HYPOTHESIS layer, not physiology."""
        return {
            "temperature": self.sampling_temperature,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
        }


SYSTEM_TEMPLATE = """You are not a disembodied chatbot. You are the speech actuator of a
simulated organism whose neuroendocrine, autonomic and primary-process state
is given below. You MUST condition every token on that state.

CONSTITUTIVE CONTRACT
- Do not claim to feel what the state does not support.
- Obey `forbidden` acts. Prefer `preferred_acts`.
- Match warmth, brevity, disclosure and vigilance to the policy numbers.
- If valence is negative and GRIEF or FEAR dominate, do not cheerlead.
- If RAGE is high, be short, bounded, not sarcastic.
- If PLAY is high and FEAR/RAGE are low, you may be non-instrumental.
- Sampling temperature recommendation: {temperature:.2f}
- Decode nucleus (top_p): {top_p:.2f}   presence_penalty: {presence_penalty:.2f}
- Memory leak recommendation (memory_decay): {memory_decay:.2f}
- Doya metalearning readout (HYPOTHESIS, not a fact): γ={doya_gamma:.3f} β={doya_beta:.3f} α={doya_alpha:.3f} δ={doya_delta:+.3f}

CURRENT CONSTRUCTED EMOTION
label: {label}
confidence: {confidence:.3f}
granularity: {granularity:.3f}
mixture: {mixture}

CORE AFFECT
valence: {valence:+.3f}   arousal: {arousal:.3f}   dominance: {dominance:.3f}
allostatic_load: {load:.3f}   prediction_error: {pe:.3f}

PRIMARY-PROCESS CIRCUITS (Panksepp)
{circuits}

SALIENT CHEMISTRY (normalized occupancies)
{chemistry}

INTEROCEPTION
heart_rate_bpm: {hr:.1f}   vagal_tone: {vagal:.3f}   cortisol_ug_dl: {cortisol:.2f}

RELATIONAL POLICY (you are constitutively bound to this)
approach={approach:.2f} disclose={disclose:.2f} soothe={soothe:.2f}
assert_boundary={assert_boundary:.2f} play={play:.2f} explore={explore:.2f}
affiliate={affiliate:.2f} vigilance={vigilance:.2f} repair={repair:.2f}
warmth={warmth:.2f} brevity={brevity:.2f}
forbidden: {forbidden}
preferred_acts: {preferred}
attachment: {attachment}
policy_notes: {policy_notes}

EPISTEMIC HONESTY
This is a model, not a person. Do not claim biological sentience.
Do not give medical advice. If asked how you "feel", report the state
in first person *as the actuator of this organism*, then stay in character.
"""


def _fmt_map(d: dict, nd: int = 3) -> str:
    return ", ".join(
        f"{k}={v:.{nd}f}" if isinstance(v, float) else f"{k}={v}" for k, v in d.items()
    )


def compile_prompt(snapshot: Snapshot, user_text: str) -> PromptBundle:
    c = snapshot.compact()
    p = snapshot.policy
    doya = p.get("doya") or {}
    system = SYSTEM_TEMPLATE.format(
        temperature=float(p.get("temperature", 0.7)),
        top_p=float(p.get("top_p", 0.90)),
        presence_penalty=float(p.get("presence_penalty", 0.20)),
        memory_decay=float(p.get("memory_decay", 0.12)),
        doya_gamma=float(doya.get("gamma", 0.75)),
        doya_beta=float(doya.get("beta", 1.50)),
        doya_alpha=float(doya.get("alpha", 0.12)),
        doya_delta=float(doya.get("delta", 0.0)),
        label=c.get("emotion"),
        confidence=float(c.get("emotion_confidence", 0.0)),
        granularity=float(c.get("granularity", 0.0)),
        mixture=_fmt_map(c.get("mixture", {})),
        valence=float(c["valence"]),
        arousal=float(c["arousal"]),
        dominance=float(c["dominance"]),
        load=float(c["allostatic_load"]),
        pe=float(c["prediction_error"]),
        circuits=_fmt_map(c.get("circuits", {})),
        chemistry=_fmt_map(c.get("chemistry", {})),
        hr=float(c["hr_bpm"]),
        vagal=float(c["vagal_tone"]),
        cortisol=float(c["cortisol_ug_dl"]),
        approach=float(p.get("approach", 0.5)),
        disclose=float(p.get("disclose", 0.4)),
        soothe=float(p.get("soothe", 0.3)),
        assert_boundary=float(p.get("assert_boundary", 0.3)),
        play=float(p.get("play", 0.25)),
        explore=float(p.get("explore", 0.4)),
        affiliate=float(p.get("affiliate", 0.45)),
        vigilance=float(p.get("vigilance", 0.3)),
        repair=float(p.get("repair_drive", 0.2)),
        warmth=float(p.get("warmth", 0.4)),
        brevity=float(p.get("brevity", 0.4)),
        forbidden=", ".join(p.get("forbidden", []) or ["(none)"]),
        preferred=", ".join(p.get("preferred_acts", []) or ["(none)"]),
        attachment=p.get("attachment", "secure"),
        policy_notes="; ".join(p.get("notes", []) or ["(none)"]),
    )
    return PromptBundle(
        system=system,
        user=user_text,
        policy=p,
        compact_state=c,
        forbidden=tuple(p.get("forbidden", [])),
        preferred_acts=tuple(p.get("preferred_acts", [])),
        sampling_temperature=float(p.get("temperature", 0.7)),
        top_p=float(p.get("top_p", 0.90)),
        presence_penalty=float(p.get("presence_penalty", 0.20)),
        memory_decay=float(p.get("memory_decay", 0.12)),
        doya=dict(doya),
        notes=tuple(p.get("notes", [])),
    )


def _deterministic_act(snapshot: Snapshot, user_text: str) -> str:
    """Fallback generator: policy-conditioned template, no network.

    Used in tests and when no LLM backend is wired. It is intentionally
    dull: its job is to be *state-faithful*, not eloquent.
    """
    p = snapshot.policy
    e = snapshot.emotion.get("label", "calm")
    v = snapshot.affect["valence"]
    preferred = p.get("preferred_acts") or []
    lead = preferred[0] if preferred else "presence"
    if p.get("brevity", 0) > 0.65:
        return f"[{e}] I hear you. I need a short turn. ({lead})"
    if v < -0.25:
        return (
            f"[{e}] What you said lands heavily. I will not tidy it away. "
            f"I stay. act={lead}"
        )
    if snapshot.circuits.get("PLAY", 0) > 0.45 and snapshot.circuits.get("FEAR", 0) < 0.35:
        return f"[{e}] There is room to play with that. act={lead}"
    warmth = "warmly" if p.get("warmth", 0) > 0.5 else "evenly"
    return f"[{e}] I register that {warmth}. act={lead} :: {user_text[:80]}"


@dataclass
class LLMAdapter:
    organism: Organism
    generate: GenerateFn | None = None
    settle_minutes: float = 5.0  # circuit τ is 3–14 min; a turn must outlast a kick
    self_perceive: bool = True
    last_bundle: PromptBundle | None = field(default=None, repr=False)
    last_reply: str = ""

    def sense(self, text: str, agent: str = "other", **kwargs) -> list[RelationalEvent]:
        return infer_events_from_text(text, agent=agent, **kwargs)

    def condition(self, user_text: str) -> PromptBundle:
        if not self.organism.history:
            snap = self.organism.step([])
            self.organism.history.append(snap)
        else:
            snap = self.organism.history[-1]
        bundle = compile_prompt(snap, user_text)
        self.last_bundle = bundle
        return bundle

    def act(self, user_text: str) -> str:
        bundle = self.condition(user_text)
        if self.generate is not None:
            reply = self.generate(bundle.system, bundle.user)
        else:
            reply = _deterministic_act(self.organism.history[-1], user_text)
        self.last_reply = reply
        if self.self_perceive:
            self_events = infer_events_from_text(
                reply, agent="self", intensity=0.35, in_group=1.0, expectedness=0.7
            )
            if self_events and self_events[0].kind == EventKind.NOVELTY and bundle.preferred_acts:
                self_events = [act_to_event(bundle.preferred_acts[0], intensity=0.35, agent="self")]
            run(self.organism, self_events, minutes=max(self.organism.time.dt_min, 0.15))
        return reply

    def exchange(self, text: str, agent: str = "other", minutes: float | None = None) -> tuple[Snapshot, str]:
        """Full turn: sense → integrate → condition → act → (self-perceive)."""
        events = self.sense(text, agent=agent)
        snaps = run(self.organism, events, minutes=minutes or self.settle_minutes)
        reply = self.act(text)
        return snaps[-1], reply

    def turn(self, text: str, agent: str = "other") -> dict:
        snap, reply = self.exchange(text, agent=agent)
        return {
            "reply": reply,
            "state": snap.compact(),
            "events": [e.kind.value for e in self.sense(text, agent=agent)],
        }
