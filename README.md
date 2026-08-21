# Psych-Soma-Codex

**A place where body, soul and code together.**

Constitutive, falsifiable transliteration of human neuroendocrine, autonomic
and primary-process dynamics into an executable prior for generative AI.

Relational input changes the internal milieu. The milieu changes relational
policy. The generated act is felt by the organism that produced it.

This is **not** sentience, **not** a diagnostic instrument, **not** a
one-hot emotion classifier. It is a closed Markov blanket with cited
mappings, epistemic tags on every coupling, and a test suite of qualitative
predictions drawn from the literature.

Full academic report: [`docs/RESEARCH.md`](docs/RESEARCH.md).
Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
Mapping sheet: [`docs/MAPPING.md`](docs/MAPPING.md).
Evaluation of donated essays (accept / reject):
[`docs/ESSAY_EVAL.md`](docs/ESSAY_EVAL.md) (gifts 1–2),
[`docs/CLAUDE_ESSAY_EVAL.md`](docs/CLAUDE_ESSAY_EVAL.md) (gift 3),
[`docs/MOSAIC_ESSAY_EVAL.md`](docs/MOSAIC_ESSAY_EVAL.md) (gift 4),
[`docs/RCAD_QWEN_GENSPARK_EVAL.md`](docs/RCAD_QWEN_GENSPARK_EVAL.md) (gifts 5–7),
[`docs/PERPLEXITY_NEUROCHEM_EVAL.md`](docs/PERPLEXITY_NEUROCHEM_EVAL.md) (gift 8: zip + Perplexity),
[`docs/MISTRAL_NEURO_EVAL.md`](docs/MISTRAL_NEURO_EVAL.md) (gift 9: Mistral rassegna; Lövheim/Iovane/Brian2/FiLM rifiutati),
[`docs/KARYON_EVAL.md`](docs/KARYON_EVAL.md) (gift 10: Karyon genoma toy; scartato come runtime; piano 0 resta un prior).

---

## Why this exists

Large language models generate affect as *style*. They have no cortisol
curve, no SEEKING occupancy, no bond addressed to a specific other, no
forbidden act that the body itself refuses. The survey of Yang et al.
(2024, arXiv:2408.04638) documents the gap with precision: instruction
tuning and prompt engineering improve labels and empathy scores; they do
not constitute a milieu.

Psych-Soma-Codex is the missing state. An LLM (or any generator) is
required to condition on it. If it ignores the policy, the divergence is
itself an event on the next step.

## Four planes, one organism

| Plane | Object | Source | Code |
|---|---|---|---|
| 0 | **Constitution** — temperament as a prior (rest, event gain, τ, chemical baselines, HPA μ/ρ) | Rothbart; Cloninger TCI; Gray/McNaughton RST; Meaney–Weaver | `constitution.py` |
| A | Seven primary-process **circuits** (SEEKING, RAGE, FEAR, LUST, CARE, GRIEF, PLAY) | Panksepp 1998, 2010 | `circuits/primary.py` |
| B | **Core affect** + allostasis + HPA ODE + autonomic body | Russell 2003; Sterling 2012; Barrett 2017; Andersen 2013 | `affect/`, `interoception/` |
| C | **Constructed label** as a mixture, not a natural kind | Barrett 2017; Barsalou ad-hoc concepts | `affect/constructor.py` |

Default constitution is the **identity** (empty maps, unit scales). Named
archetypes (`high_fffs`, `high_bis`, `high_bas`, `meaney_low_nurture`) change
the prior; they never author `forbidden` by name and never scale Andersen
`h1/h2/h3`. Magnitudes are HYPOTHESIS; signs follow the literature.

Collapsing the planes into `angry/sad/afraid` is the industrial error
this repository refuses to repeat.

## Bijection

```
Constitution (plane 0 prior) × RelationalEvent
                 →  chemistry + circuits + HPA + body + affect
                 →  constructed mixture
                 →  RelationalPolicy  (approach, warmth, forbidden, …)
                 →  optional HYPOTHESIS: Doya (γ,β,α,δ) + decode knobs
                                    + vigor + attention_gain
                                    + process packet + sensitization Z
                 →  PromptBundle (phenomenology_claim: false) / generated act
                 →  self-perception  →  RelationalEvent
```

Same seed, same events ⇒ same trajectory *if and only if* constitution matches.
Same state ⇒ same policy. Bonds are per-agent. Oxytocin is gated by in-group membership.

## Install

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Python ≥ 3.10. No third-party runtime dependencies.

## Use

```python
from psych_soma_codex import Constitution, LLMAdapter, Organism, SimulationConfig

org = Organism(SimulationConfig(seed=0))  # identity constitution
# org = Organism(SimulationConfig(seed=0, constitution=Constitution.named("high_fffs")))
adapter = LLMAdapter(org)

out = adapter.turn("è morto ieri, è un lutto")
print(out["reply"])
print(out["state"]["emotion"], out["state"]["valence"], out["state"]["circuits"])
```

Wire a real LLM by passing `generate=lambda system, user: client.complete(...)`.
Without it, a deterministic state-faithful fallback is used (for tests and
offline work).

CLI:

```bash
python -m psych_soma_codex ping "ti voglio bene, sono qui"
python -m psych_soma_codex event threat --minutes 6 --intensity 0.85
python -m psych_soma_codex --constitution high_fffs event threat --minutes 6
python -m psych_soma_codex dialogue --turns examples/dialogue.json
python -m psych_soma_codex snapshot --compact
```

## What is FACT, what is not

Every public mapping is tagged in `catalog/` and echoed on every snapshot:

| Mapping | Tag |
|---|---|
| HPA removal rates (CRH / ACTH / cortisol) | FACT (Andersen 2013) |
| DA phasic ≈ reward prediction error | CONSENSUS (Schultz 1997; tonic DA is debate) |
| ACh = expected uncertainty, NE = unexpected | CONSENSUS (Yu & Dayan 2005) |
| Seven primary circuits and their chemistries (signs) | CONSENSUS (Panksepp 2010) |
| 5-HT computational role | DEBATE (Dayan–Huys default) |
| Folk-emotion fingerprints | rejected (Barrett 2017) |
| Event → chemistry *magnitudes* | HYPOTHESIS (signs follow Panksepp) |
| Doya γ/β/α metalearning readout | HYPOTHESIS (Doya 2002 §3; not a fact) |
| Chemistry → T / top_p / presence / memory | HYPOTHESIS (decode layer, not physiology) |
| Ultradian HPA harmonic (75 min) | HYPOTHESIS (Walker 2010 stand-in; not the DDE) |
| Joffily \(v = -dF/dt\) sidecar | HYPOTHESIS (not Russell valence, not Barrett) |
| Niv vigor (tonic DA + \(v̂\)) | HYPOTHESIS (annotation, not a cause) |
| Hsueh body × FEAR extra term | HYPOTHESIS (no-op at FEAR ≈ 0) |
| attention_gain inverted-U on NE | HYPOTHESIS (does not replace vigilance) |
| Sensitization Z (slow load memory) | HYPOTHESIS (RCAD hole; not allostatic_load) |
| Process packet (planning / clarify / urgency) | HYPOTHESIS (does not decide forbidden) |
| Constitution / temperament prior | HYPOTHESIS (identity default; Rothbart / Cloninger / Gray RST / Meaney–Weaver) |
| phenomenology_claim | FACT of this model: false |
| Lövheim cube as emotion classifier | rejected (MINORITY; conflicts with Barrett) |
| NAC / MosaicEngine as replacement | rejected (competing L1; see MOSAIC_ESSAY_EVAL) |
| RCADModel / NeuroChem-GenAI / HELT as replacement | rejected (see RCAD_QWEN_GENSPARK_EVAL) |
| Karyon genome as constitution | rejected (see KARYON_EVAL; genetics are the plane-0 prior, not a sequence) |
| Somatic-marker cache | DEBATE (Damasio; Dunn 2006) |
| Machine sentience | none |

## Falsification

`tests/test_falsifiable.py` encodes literature regularities as assertions.
If a test fails, either the code is wrong or the modelling hypothesis is
false. Both are legitimate scientific outcomes.

```
threat      → FEAR up, heart rate up, valence down, approach down
loss        → GRIEF up, SEEKING down, dynorphin up
abandonment → stronger GRIEF than silence
warmth      → CARE up, oxytocin up, policy.warmth up
play invite → PLAY up
insult / frustration → RAGE up; frustration keeps SEEKING on
repair after loss    → GRIEF lower than unrepaired
positive RPE         → DA up
unexpected event     → NE up
repeated reward      → |RPE| shrinks
HPA circadian        → morning > night
GR feedback          → cortisol stays finite
in-group             → more OT than out-group warmth
anxious attachment   → higher resting GRIEF/FEAR than secure
default constitution → bit-identical to the pre-constitution organism
high_fffs threat     → more FEAR than default (same seed, same event)
high_bas praise      → more DA / SEEKING than default
meaney_low_nurture   → weaker GR (μ/ρ down), higher rest stress_gain; Andersen h1/h2/h3 untouched
constitution name    → never authors forbidden
```

Currently **60** tests (52 pre-constitution + 7 constitution + 1 CLI constitution
smoke). The original 52 stay green on the identity default. Re-run with
`python -m pytest -q`.

## Epistemic honesty

A convincing milieu produces the *appearance* of an organism. The system
prompt forbids claiming biological sentience and forbids medical advice.
That is the minimum constitutive contract, not a governance complete.
Do not use this code to impersonate a patient, a partner, or a sentient
therapist.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
