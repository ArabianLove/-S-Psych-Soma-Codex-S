"""Falsifiable predictions of the constitutive organism.

Each test is a claim that a published qualitative regularity must survive
the transliteration. If a test fails, either the code is wrong or the
modelling hypothesis is false — both are legitimate scientific outcomes.
"""

from __future__ import annotations

import math

from psych_soma_codex.affect.constructor import construct_emotion
from psych_soma_codex.catalog.species import SPECIES
from psych_soma_codex.core.mathutil import hill, leaky_integrator, rk4_step
from psych_soma_codex.engine import Organism, SimulationConfig, run
from psych_soma_codex.interoception.hpa import HPAAxis
from psych_soma_codex.io.events import EventKind, RelationalEvent
from psych_soma_codex.llm.adapter import LLMAdapter
from psych_soma_codex.llm.lexicon import infer_events_from_text
from psych_soma_codex.relational.policy import AttachmentStyle


def _org(seed: int = 0, **kw) -> Organism:
    return Organism(SimulationConfig(seed=seed, noise=0.0, **kw))


def _impulse(kind: EventKind, minutes: float = 6.0, intensity: float = 0.85, **kw):
    o = _org()
    baseline = run(o, [], minutes=0.4)[-1]
    traj = run(
        o,
        [RelationalEvent(kind=kind, intensity=intensity, expectedness=0.2, **kw)],
        minutes=minutes,
    )
    return baseline, traj, traj[-1]


def _max_circuit(traj, key: str) -> float:
    return max(s.circuits[key] for s in traj)


# ---------------------------------------------------------------------------
# 1. Reproducibility (constitutive requirement)
# ---------------------------------------------------------------------------

def test_identical_seeds_identical_trajectories():
    a = run(_org(seed=11), [RelationalEvent(kind=EventKind.THREAT, intensity=0.8)], minutes=4)
    b = run(_org(seed=11), [RelationalEvent(kind=EventKind.THREAT, intensity=0.8)], minutes=4)
    assert a[-1].affect == b[-1].affect
    assert a[-1].circuits == b[-1].circuits
    assert a[-1].chemistry == b[-1].chemistry
    assert a[-1].hpa["cortisol_ug_dl"] == b[-1].hpa["cortisol_ug_dl"]


def test_different_seeds_with_noise_diverge():
    a = run(Organism(SimulationConfig(seed=1, noise=0.04)), ["threat"], minutes=3)
    b = run(Organism(SimulationConfig(seed=2, noise=0.04)), ["threat"], minutes=3)
    assert a[-1].affect != b[-1].affect or a[-1].chemistry != b[-1].chemistry


# ---------------------------------------------------------------------------
# 2. Panksepp circuit signs (2010 Dialogues Clin Neurosci 12:533-545)
# ---------------------------------------------------------------------------

def test_threat_raises_fear_and_heart_rate():
    """FEAR circuit + sympathetic effector. Panksepp FEAR; standard ANS."""
    b, traj, last = _impulse(EventKind.THREAT)
    assert _max_circuit(traj, "FEAR") > b.circuits["FEAR"] + 0.10
    assert last.body["heart_rate_bpm"] > b.body["heart_rate_bpm"] + 3.0
    assert last.affect["valence"] < b.affect["valence"]
    assert last.policy["approach"] < b.policy["approach"]
    assert last.circuits["PLAY"] <= b.circuits["PLAY"] + 0.02


def test_loss_raises_grief_and_lowers_seeking():
    """Panksepp 2010: GRIEF overactivity + SEEKING underactivity = despair cascade."""
    b, traj, last = _impulse(EventKind.LOSS, minutes=8)
    assert _max_circuit(traj, "GRIEF") > b.circuits["GRIEF"] + 0.12
    assert last.circuits["SEEKING"] < b.circuits["SEEKING"]
    assert last.affect["valence"] < b.affect["valence"] - 0.05
    assert last.chemistry["dynorphin"] >= b.chemistry["dynorphin"] - 1e-6


def test_abandonment_is_stronger_grief_than_mild_silence():
    b_ab, t_ab, last_ab = _impulse(EventKind.ABANDONMENT, minutes=8)
    o = _org()
    run(o, [], minutes=0.4)
    t_si = run(o, [RelationalEvent(kind=EventKind.SILENCE, intensity=0.4)], minutes=8)
    assert _max_circuit(t_ab, "GRIEF") > _max_circuit(t_si, "GRIEF")
    assert last_ab.chemistry["opioid"] < 0.32  # social-comfort brake drops


def test_warmth_raises_care_and_oxytocin():
    """Panksepp CARE; Carter OT/attachment."""
    b, traj, last = _impulse(EventKind.WARMTH)
    assert _max_circuit(traj, "CARE") > b.circuits["CARE"] + 0.04
    assert last.chemistry["ot"] > b.chemistry["ot"] + 0.03
    assert last.policy["warmth"] > b.policy["warmth"]
    assert last.affect["valence"] >= b.affect["valence"] - 0.01


def test_play_invite_raises_play():
    b, traj, last = _impulse(EventKind.PLAY_INVITE)
    assert _max_circuit(traj, "PLAY") > b.circuits["PLAY"] + 0.06


def test_insult_and_frustration_raise_rage():
    """Panksepp RAGE: insult / SEEKING-thwarted."""
    _, t_ins, last_ins = _impulse(EventKind.INSULT)
    b_fr, t_fr, last_fr = _impulse(EventKind.FRUSTRATION)
    assert _max_circuit(t_ins, "RAGE") > 0.12
    assert _max_circuit(t_fr, "RAGE") > 0.12
    # Frustration-aggression: SEEKING stays up (thwarted, not extinguished).
    assert last_fr.circuits["SEEKING"] >= b_fr.circuits["SEEKING"] - 0.02


def test_repair_after_loss_lowers_grief_relative_to_unrepaired():
    lost = _org()
    run(lost, [RelationalEvent(kind=EventKind.LOSS, intensity=0.9)], minutes=4)
    unrepaired = run(lost, [], minutes=5)[-1]

    repaired = _org()
    run(repaired, [RelationalEvent(kind=EventKind.LOSS, intensity=0.9)], minutes=4)
    after = run(repaired, [RelationalEvent(kind=EventKind.REPAIR, intensity=0.9)], minutes=5)[-1]
    assert after.circuits["GRIEF"] < unrepaired.circuits["GRIEF"]
    assert after.chemistry["ot"] > unrepaired.chemistry["ot"]
    assert after.policy["warmth"] > unrepaired.policy["warmth"]


# ---------------------------------------------------------------------------
# 3. Computational neuromodulation (Dayan 2012; Yu & Dayan 2005; Schultz 1997)
# ---------------------------------------------------------------------------

def test_positive_rpe_raises_dopamine():
    o = _org()
    before = run(o, [], minutes=0.3)[-1]
    after = run(
        o,
        [RelationalEvent(kind=EventKind.PRAISE, intensity=0.9, expectedness=0.1)],
        minutes=0.8,
    )[-1]
    assert after.chemistry["da"] > before.chemistry["da"]
    assert after.relational["rpe"] > 0.0


def test_unexpected_event_raises_norepinephrine():
    """Yu & Dayan 2005: NE signals unexpected uncertainty."""
    o = _org()
    before = run(o, [], minutes=0.3)[-1]
    after = run(
        o,
        [RelationalEvent(kind=EventKind.THREAT, intensity=0.8, expectedness=0.05)],
        minutes=0.6,
    )[-1]
    assert after.chemistry["ne"] > before.chemistry["ne"]
    assert after.relational["unexpected_uncertainty"] > before.relational["unexpected_uncertainty"]


def test_repeated_same_event_reduces_rpe_magnitude():
    """Sutton-Barto / Schultz: predicted reward → RPE → 0."""
    o = _org()
    first = run(o, [RelationalEvent(kind=EventKind.PRAISE, intensity=0.8, expectedness=0.5)], minutes=1)
    rpe1 = abs(first[-1].relational["rpe"])
    # Several more identical appetitive events: v_hat should catch up.
    later = first
    for _ in range(6):
        later = run(o, [RelationalEvent(kind=EventKind.PRAISE, intensity=0.8, expectedness=0.8)], minutes=0.6)
    rpe_n = abs(later[-1].relational["rpe"])
    assert rpe_n < rpe1


# ---------------------------------------------------------------------------
# 4. HPA axis (Andersen 2013; Ahmad 2023)
# ---------------------------------------------------------------------------

def test_hpa_circadian_peaks_in_the_morning():
    h = HPAAxis()
    morning = h.circadian(7.5)
    night = h.circadian(0.0)
    evening = h.circadian(23.0)
    assert morning > night
    assert morning > evening
    assert morning > 0.85


def test_hpa_negative_feedback_bounds_cortisol():
    """Cortisol cannot run away: GR negative feedback (FACT of HPA physiology)."""
    h = HPAAxis()
    h.stress_gain = 3.0
    for _ in range(800):  # 40 minutes at dt=0.05
        h.step(0.05, tod_hours=8.0)
    assert h.C < 60.0  # µg/dL — high-stress but finite (GR feedback)
    assert h.C > 0.0


def test_threat_raises_hpa_stress_gain():
    b, _, last = _impulse(EventKind.THREAT, minutes=2)
    assert last.hpa["stress_gain"] > 1.0


def test_crh_decays_faster_than_cortisol():
    """Andersen 2013: h1=0.1732/min >> h3=0.0105/min."""
    assert SPECIES["crh"].tau_min < SPECIES["acth"].tau_min
    assert SPECIES["acth"].tau_min < SPECIES["cortisol"].tau_min


# ---------------------------------------------------------------------------
# 5. Bijection: relational ↔ affective
# ---------------------------------------------------------------------------

def test_policy_is_a_function_of_state():
    """Same state ⇒ same policy. Inverse half of the bijection is deterministic."""
    o1, o2 = _org(seed=3), _org(seed=3)
    s1 = run(o1, [RelationalEvent(kind=EventKind.WARMTH, intensity=0.7)], minutes=3)[-1]
    s2 = run(o2, [RelationalEvent(kind=EventKind.WARMTH, intensity=0.7)], minutes=3)[-1]
    assert s1.policy == s2.policy


def test_threat_policy_forbids_escalation_when_fear_is_high_enough():
    # Drive FEAR hard with two stacked threats.
    o = _org()
    run(o, [RelationalEvent(kind=EventKind.THREAT, intensity=1.0, expectedness=0.0)], minutes=3)
    last = run(o, [RelationalEvent(kind=EventKind.THREAT, intensity=1.0, expectedness=0.0)], minutes=4)[-1]
    if last.circuits["FEAR"] > 0.55 or last.policy["vigilance"] > 0.65:
        assert "escalate_threat" in last.policy["forbidden"]
    else:
        # Even below the hard gate, approach and play must drop.
        assert last.policy["approach"] < 0.45
        assert last.circuits["PLAY"] < 0.12


def test_in_group_gates_oxytocin():
    """OT effects are context-dependent (Carter; de Dreu). Constitutive prior."""
    _, _, in_g = _impulse(EventKind.WARMTH, intensity=0.9)
    # rebuild with out-group
    o = _org()
    run(o, [], minutes=0.4)
    out = run(
        o,
        [RelationalEvent(kind=EventKind.WARMTH, intensity=0.9, in_group=0.05)],
        minutes=6,
    )[-1]
    # in-group warmth was already run in _impulse; compare OT
    # Re-run in-group cleanly:
    o2 = _org()
    run(o2, [], minutes=0.4)
    inn = run(
        o2,
        [RelationalEvent(kind=EventKind.WARMTH, intensity=0.9, in_group=1.0)],
        minutes=6,
    )[-1]
    assert inn.chemistry["ot"] > out.chemistry["ot"]


def test_bonds_are_addressed():
    o = _org()
    run(o, [RelationalEvent(kind=EventKind.WARMTH, intensity=0.8, agent="alice")], minutes=2)
    run(o, [RelationalEvent(kind=EventKind.INSULT, intensity=0.8, agent="bob")], minutes=2)
    bonds = o.bonds.as_dict()
    assert bonds["alice"]["trust"] > bonds["bob"]["trust"]
    assert bonds["alice"]["affiliation"] > bonds["bob"]["affiliation"]


def test_attachment_anxious_has_higher_resting_grief_than_secure():
    sec = run(_org(attachment=AttachmentStyle.SECURE), [], minutes=1)[-1]
    anx = run(
        Organism(SimulationConfig(seed=0, attachment=AttachmentStyle.ANXIOUS)),
        [],
        minutes=1,
    )[-1]
    assert anx.circuits["GRIEF"] > sec.circuits["GRIEF"]
    assert anx.circuits["FEAR"] > sec.circuits["FEAR"]


# ---------------------------------------------------------------------------
# 6. Constructed emotion (Barrett 2017) + mixtures
# ---------------------------------------------------------------------------

def test_constructed_emotion_is_a_mixture_not_a_one_hot():
    o = _org()
    snap = run(o, [RelationalEvent(kind=EventKind.LOSS, intensity=0.8)], minutes=5)[-1]
    mix = snap.emotion["mixture"]
    assert abs(sum(mix.values()) - 1.0) < 1e-6
    nonzero = sum(1 for v in mix.values() if v > 0.02)
    assert nonzero >= 2  # degeneracy / mixture


def test_constructor_is_deterministic():
    o = _org()
    snap = run(o, ["warmth"], minutes=2)[-1]
    a = construct_emotion(o.circuits, o.affect)
    b = construct_emotion(o.circuits, o.affect)
    assert a.label == b.label
    assert a.mixture == b.mixture


# ---------------------------------------------------------------------------
# 7. LLM adapter closes the loop
# ---------------------------------------------------------------------------

def test_lexicon_detects_italian_warmth():
    evs = infer_events_from_text("ti voglio bene, sono qui")
    kinds = {e.kind for e in evs}
    assert EventKind.WARMTH in kinds


def test_lexicon_detects_loss_and_repair():
    assert EventKind.LOSS in {e.kind for e in infer_events_from_text("è morto ieri, è un lutto")}
    assert EventKind.REPAIR in {e.kind for e in infer_events_from_text("scusa, ho sbagliato, perdonami")}


def test_adapter_turn_returns_state_faithful_reply():
    adapter = LLMAdapter(_org())
    out = adapter.turn("è morto ieri, è un lutto")
    assert "reply" in out and len(out["reply"]) > 0
    assert out["state"]["emotion"]
    # After a loss utterance, valence should not have gone *up*.
    assert out["state"]["valence"] < 0.25


def test_self_perception_changes_state():
    o = _org()
    adapter = LLMAdapter(o, self_perceive=True)
    before = run(o, [], minutes=0.2)[-1]
    adapter.turn("ti voglio bene")
    after = o.history[-1]
    # Something moved — the organism heard itself.
    assert after.t_min > before.t_min
    assert after.chemistry != before.chemistry or after.circuits != before.circuits


# ---------------------------------------------------------------------------
# 8. Numerical primitives
# ---------------------------------------------------------------------------

def test_leaky_integrator_reaches_target():
    y = 0.0
    for _ in range(200):
        y = leaky_integrator(y, 1.0, 1.0, 0.1)
    assert abs(y - 1.0) < 1e-6


def test_hill_is_zero_at_origin_and_one_at_infinity():
    assert hill(0.0, 1.0, 3.0) == 0.0
    assert hill(1e6, 1.0, 3.0) > 0.999


def test_rk4_integrates_exponential_decay():
    def f(t, y):
        return [-y[0]]

    y = [1.0]
    dt = 0.01
    t = 0.0
    for _ in range(100):
        y = rk4_step(f, t, y, dt)
        t += dt
    assert abs(y[0] - math.exp(-1.0)) < 1e-4


def test_idle_organism_stays_bounded():
    snap = run(_org(), [], minutes=20)[-1]
    for v in snap.circuits.values():
        assert 0.0 <= v <= 1.0
    for v in snap.chemistry.values():
        assert 0.0 <= v <= 1.0
    assert 40.0 < snap.body["heart_rate_bpm"] < 160.0
    assert 0.0 < snap.hpa["cortisol_ug_dl"] < 60.0


# ---------------------------------------------------------------------------
# 9. Doya 2002 metalearning readout (HYPOTHESIS) + decode params
# ---------------------------------------------------------------------------

def test_doya_signs_follow_section_3():
    """Doya 2002 §3: more 5-HT → larger γ; more NE → larger β; more ACh → larger α."""
    from psych_soma_codex.chemistry.milieu import ChemicalMilieu
    from psych_soma_codex.relational.doya import derive_doya

    low = ChemicalMilieu()
    high = ChemicalMilieu()
    for key in ("fiveht", "ne", "ach"):
        low.levels[key] = 0.10
        high.levels[key] = 0.90
    a = derive_doya(low, last_rpe=-0.3)
    b = derive_doya(high, last_rpe=0.4)
    assert b.gamma > a.gamma
    assert b.beta > a.beta
    assert b.alpha > a.alpha
    assert a.delta == -0.3
    assert b.delta == 0.4
    assert "HYPOTHESIS" in a.epistemic
    assert "Doya 2002" in a.epistemic


def test_doya_bounds_are_clamped():
    from psych_soma_codex.chemistry.milieu import ChemicalMilieu
    from psych_soma_codex.relational.doya import derive_doya

    m = ChemicalMilieu()
    m.levels["fiveht"] = 2.0
    m.levels["ne"] = 2.0
    m.levels["ach"] = 2.0
    r = derive_doya(m, last_rpe=1.5)
    assert 0.50 <= r.gamma <= 0.99
    assert 0.40 <= r.beta <= 8.00
    assert 0.02 <= r.alpha <= 0.45
    m.levels["fiveht"] = -1.0
    m.levels["ne"] = -1.0
    m.levels["ach"] = -1.0
    r0 = derive_doya(m, last_rpe=0.0)
    assert r0.gamma >= 0.50
    assert r0.beta >= 0.40
    assert r0.alpha >= 0.02


def test_engine_passes_last_rpe_into_doya_delta():
    """Inverse half of the bijection must see the current RPE (Doya item 1)."""
    o = _org()
    snap = run(
        o,
        [RelationalEvent(kind=EventKind.PRAISE, intensity=0.9, expectedness=0.1)],
        minutes=0.8,
    )[-1]
    assert snap.relational["rpe"] > 0.0
    assert snap.policy["doya"]["delta"] == snap.relational["rpe"]
    assert snap.epistemics["doya_metalearning"].startswith("HYPOTHESIS")
    assert snap.epistemics["decode_params"].startswith("HYPOTHESIS")


def test_unexpected_threat_raises_doya_beta():
    """Doya item 3: NE controls inverse temperature β. Threat is unexpected → NE up → β up."""
    o = _org()
    before = run(o, [], minutes=0.3)[-1]
    after = run(
        o,
        [RelationalEvent(kind=EventKind.THREAT, intensity=0.85, expectedness=0.05)],
        minutes=0.6,
    )[-1]
    assert after.chemistry["ne"] > before.chemistry["ne"]
    assert after.policy["doya"]["beta"] > before.policy["doya"]["beta"]


def test_decode_params_signs_and_bounds():
    """Chemistry → T / top_p / presence / memory. HYPOTHESIS magnitudes; signs fixed."""
    from psych_soma_codex.affect.core_affect import CoreAffect
    from psych_soma_codex.chemistry.milieu import ChemicalMilieu
    from psych_soma_codex.circuits.primary import PrimaryCircuits
    from psych_soma_codex.interoception.body import InteroceptiveBody
    from psych_soma_codex.relational.bond import BondBook
    from psych_soma_codex.relational.policy import AttachmentStyle, derive_policy

    def _pol(**levels):
        milieu = ChemicalMilieu()
        for k, v in levels.items():
            milieu.levels[k] = v
        return derive_policy(
            milieu,
            PrimaryCircuits(),
            CoreAffect(),
            InteroceptiveBody(),
            BondBook(),
            AttachmentStyle.SECURE,
        )

    low_ht = _pol(fiveht=0.05, cortisol=0.05, da=0.05, ach=0.05)
    high_ht = _pol(fiveht=0.90, cortisol=0.80, da=0.05, ach=0.05)
    high_da = _pol(fiveht=0.05, cortisol=0.05, da=0.90, ach=0.80)
    assert high_ht.top_p < low_ht.top_p
    assert high_da.presence_penalty > low_ht.presence_penalty
    assert high_da.memory_decay > low_ht.memory_decay
    for p in (low_ht, high_ht, high_da):
        assert 0.50 <= p.top_p <= 0.98
        assert 0.0 <= p.presence_penalty <= 0.80
        assert 0.02 <= p.memory_decay <= 0.55
        assert 0.15 <= p.temperature <= 1.2


def test_doya_does_not_drive_forbidden_or_label():
    """Readout must not become a classifier. Forbidden/label stay Panksepp+Barrett."""
    o = _org()
    snap = run(o, [RelationalEvent(kind=EventKind.THREAT, intensity=0.9)], minutes=4)[-1]
    # Doya numbers exist, but the emotion label is a Barrett mixture, not a cube vertex.
    assert "mixture" in snap.emotion
    assert abs(sum(snap.emotion["mixture"].values()) - 1.0) < 1e-6
    assert "lovheim" not in snap.emotion["label"].lower()
    assert "lovheim" not in str(snap.policy).lower()
    # Forbidden still comes from circuit occupancy gates, not from γ/β/α.
    if snap.circuits["FEAR"] > 0.55 or snap.policy["vigilance"] > 0.65:
        assert "escalate_threat" in snap.policy["forbidden"]


def test_prompt_bundle_exposes_decode_and_doya():
    adapter = LLMAdapter(_org())
    adapter.exchange("ti voglio bene", minutes=1.5)
    # condition() reads the *current* last snapshot (after self-perception).
    bundle = adapter.condition("ti voglio bene")
    current = adapter.organism.history[-1]
    assert 0.50 <= bundle.top_p <= 0.98
    assert 0.0 <= bundle.presence_penalty <= 0.80
    assert 0.02 <= bundle.memory_decay <= 0.55
    assert "gamma" in bundle.doya
    assert "HYPOTHESIS" in bundle.doya.get("epistemic", "")
    assert "top_p" in bundle.system
    assert "Doya metalearning" in bundle.system
    kw = bundle.sampling_kwargs()
    assert kw["temperature"] == bundle.sampling_temperature
    assert kw["top_p"] == bundle.top_p
    assert "presence_penalty" in kw
    # Bundle must match the snapshot it was compiled from, not a prior turn.
    assert abs(bundle.doya["gamma"] - current.policy["doya"]["gamma"]) < 1e-9
    assert abs(bundle.top_p - current.policy["top_p"]) < 1e-9
