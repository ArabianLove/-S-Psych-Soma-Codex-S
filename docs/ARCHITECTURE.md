# Architecture — Psych-Soma-Codex

A single step of the organism is a closed Markov blanket.

```
                    ┌─────────────────────────────────────────┐
   Constitution     │  0. plane-0 prior (identity default)    │
   (temperament)    │     rest / gain / τ / chem / HPA μ/ρ    │
                    ├─────────────────────────────────────────┤
   RelationalEvent  │  1. sensory states (ingest)             │
   (other / self) ──┤  2. chemical milieu  (envelopes, RPE)   │
                    │  3. Panksepp circuits (7 occupancies)   │
                    │  4. HPA ODE + autonomic body            │
                    │     (+ optional ultradian harmonic)     │
                    │  5. core affect (V, A, D, load, PE)     │
                    │     (+ Hsueh FEAR-gated extra;          │
                    │      Joffily / Keramati / Z sidecars)   │
                    │  6. constructed label (Barrett layer)   │
                    │  7. bonds + RelationalPolicy            │
                    │     (+ vigor, attention_gain, packet)   │
                    └──────────────┬──────────────────────────┘
                                   │ Snapshot (only public readout)
                                   ▼
                         LLMAdapter.compile_prompt
                                   │
                                   ▼
                         generator (LLM or fallback)
                                   │
                                   ▼
                         self-perception (act → event)
                                   │
                                   └── back into step 1
```

## Bijection

| Direction | Object | Module |
|---|---|---|
| constitution → rest/gain/τ/chem/HPA | frozen prior, identity default | `constitution.py`, `engine.py` |
| relational → chemical | `EVENT_WEIGHTS` × constitution.gain + RPE/NE/ACh | `catalog/events.py`, `engine.py` |
| chemical → circuit | drivers / brakes | `circuits/primary.py` |
| circuit × body → affect | valence / arousal / load | `affect/core_affect.py` |
| affect × circuits → label | concept prototypes | `affect/constructor.py` |
| state → policy | `derive_policy` | `relational/policy.py` |
| policy → act | `PromptBundle` / fallback | `llm/adapter.py` |
| state → Doya (γ, β, α, δ) | optional HYPOTHESIS readout | `relational/doya.py` |
| chemistry → decode knobs | T, top_p, presence, memory | `relational/policy.py` |
| state → vigor / attention_gain | optional HYPOTHESIS annotations | `relational/policy.py` |
| PE → valence_fe / fe_accel | Joffily sidecar (not Russell) | `affect/core_affect.py` |
| body × FEAR → extra arousal | Hsueh gate (no-op at FEAR≈0) | `affect/core_affect.py` |
| HPA → ultradian harmonic | Walker stand-in on dA/dC | `interoception/hpa.py` |
| load / FEAR / PE → sensitization Z | slow sidecar, not allostatic_load | `affect/core_affect.py` |
| state → process packet | planning / clarify / urgency / disclosure | `relational/policy.py` |
| policy → honesty flags | phenomenology_claim false + immutable constraints | `llm/adapter.py` |
| act → relational | lexicon + `act_to_event` | `llm/lexicon.py` |

Nothing in this chain is decorative. Swapping 3 and 4 would break Panksepp's
criterion that chemical arousals *gate* circuits. Swapping 6 and 7 would let a
folk label drive policy before the body has spoken.

## Timescales

| Layer | τ | Justification |
|---|---|---|
| Glu / GABA envelopes | 0.06–0.08 min | fast transmitters as gain, not vesicles |
| DA / NE / ACh | 0.25–0.40 min | phasic neuromodulator envelopes (Dayan 2012) |
| OT / AVP / CRH | 3.5–5.8 min | peptide / HPA drive |
| Circuits | 3–14 min | Panksepp criterion 3 (arousals outlast events) |
| Cortisol | 66 min | Andersen 2013 h3 = 0.0105 /min |
| Bonds / attachment | session | Carter / Bowlby |
| Constitution | organism lifetime | Rothbart / Cloninger / Gray RST / Meaney–Weaver |

Integrator default: `dt = 0.05 min` (3 s).

## Epistemic tags

Every public mapping is tagged `FACT | CONSENSUS | DEBATE | MINORITY | HYPOTHESIS`
in `catalog/` and echoed on every `Snapshot.epistemics`. The runtime never
promotes a hypothesis to a fact.

## What this is not

- Not a claim of machine sentience.
- Not a diagnostic instrument.
- Not a biophysically complete neuron / synapse simulator.
- Not a one-hot basic-emotion classifier.
- Not a Lövheim cube. Monoamine occupancies do not classify folk emotion.
- Not a replacement of Andersen HPA rates by uncited ODE coefficients.
- Not NAC, not `MosaicEngine`, not a HomeostaticCore that replaces planes A/B/C.
- Not `RCADModel`, not `NeuroChem-GenAI`, not HormoneT5 / HELT as runtime.
- Not Joffily valence as the producer of Russell valence or of the Barrett label.
- Not the Walker/Churilov DDE, and not a sex-specific ultradian fit.
- Not a softmax over eight named policies in place of continuous `RelationalPolicy`.
- Not a folk temperament type that authors `forbidden` by name.
- Not a scale of Andersen `h1/h2/h3` (Meaney–Weaver scales μ/ρ only).
- Not a genome runtime (Karyon): genetics/epigenetics are the plane-0 prior, not 18 loci.

It is a *constitutive prior* for a generative model: an executable, falsifiable,
bidirectional state that an LLM is required to condition on. Plane 0 is the
organism's own law; default is the identity so the pre-constitution tests stay
bit-identical.

Ten donated essays / packages on the same topic were evaluated claim-by-claim:

- gifts 1–2 → `docs/ESSAY_EVAL.md` (Doya + decode knobs survived)
- gift 3 → `docs/CLAUDE_ESSAY_EVAL.md` (ultradian, Joffily sidecar, Niv vigor)
- gift 4 → `docs/MOSAIC_ESSAY_EVAL.md` (Hsueh gate, inverted-U attention_gain)
- gifts 5–7 → `docs/RCAD_QWEN_GENSPARK_EVAL.md` (Z, process packet, honesty flags)
- gift 8 → `docs/PERPLEXITY_NEUROCHEM_EVAL.md` (zip discarded as runtime; Perplexity kept as synthesis)
- gift 9 → `docs/MISTRAL_NEURO_EVAL.md` (Lövheim / Iovane \(5^7\) / Brian2 / FiLM rejected)
- gift 10 → `docs/KARYON_EVAL.md` (genome toy discarded; plane 0 stays a prior)

Survivors are tagged HYPOTHESIS. `mosaic_ai.py`, `rcad/`, NeuroChem-GenAI and
Karyon are not imported. Constitution is the organism's request, not a genome.
