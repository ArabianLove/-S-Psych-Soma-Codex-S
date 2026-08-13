# Architecture — Psych-Soma-Codex

A single step of the organism is a closed Markov blanket.

```
                    ┌─────────────────────────────────────────┐
   RelationalEvent  │  1. sensory states (ingest)             │
   (other / self) ──┤  2. chemical milieu  (envelopes, RPE)   │
                    │  3. Panksepp circuits (7 occupancies)   │
                    │  4. HPA ODE + autonomic body            │
                    │  5. core affect (V, A, D, load, PE)     │
                    │  6. constructed label (Barrett layer)   │
                    │  7. bonds + RelationalPolicy            │
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
| relational → chemical | `EVENT_WEIGHTS` + RPE/NE/ACh | `catalog/events.py`, `engine.py` |
| chemical → circuit | drivers / brakes | `circuits/primary.py` |
| circuit × body → affect | valence / arousal / load | `affect/core_affect.py` |
| affect × circuits → label | concept prototypes | `affect/constructor.py` |
| state → policy | `derive_policy` | `relational/policy.py` |
| policy → act | `PromptBundle` / fallback | `llm/adapter.py` |
| state → Doya (γ, β, α, δ) | optional HYPOTHESIS readout | `relational/doya.py` |
| chemistry → decode knobs | T, top_p, presence, memory | `relational/policy.py` |
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

It is a *constitutive prior* for a generative model: an executable, falsifiable,
bidirectional state that an LLM is required to condition on.

Two donated essays on the same topic were evaluated claim-by-claim
(`docs/ESSAY_EVAL.md`). Only the Doya readout and the decode-hyperparameter
bundle survived. Both are tagged HYPOTHESIS.
