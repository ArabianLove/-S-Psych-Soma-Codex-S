# Constitutive mapping sheet

Quick reference. Magnitudes live in `psych_soma_codex/catalog/`. Signs below
are CONSENSUS unless marked otherwise.

## Species → computational role

| key | role | τ (min) | tag |
|---|---|---|---|
| `da` | RPE (phasic) + SEEKING gain | 0.40 | CONSENSUS / tonic DEBATE |
| `fiveht` | inhibition / opponent to DA | 1.20 | DEBATE |
| `ne` | unexpected uncertainty | 0.25 | CONSENSUS |
| `ach` | expected uncertainty | 0.35 | CONSENSUS |
| `gaba` | fast brake on RAGE/FEAR | 0.08 | CONSENSUS |
| `glu` | fast drive of GRIEF/RAGE | 0.06 | CONSENSUS |
| `crh` | HPA drive + FEAR/GRIEF peptide | 5.8 | CONSENSUS |
| `acth` | HPA intermediate | 22 | FACT (rate) |
| `cortisol` | slow stress effector, GR/MR feedback | 66 | FACT (rate) |
| `ot` | CARE / bonding; GRIEF brake; in-group gated | 3.5 | CONSENSUS |
| `avp` | territorial / HPA co-secretagogue | 4.0 | CONSENSUS |
| `opioid` | social comfort / GRIEF brake / PLAY | 8.0 | CONSENSUS |
| `dynorphin` | SEEKING brake, dysphoria of loss | 10 | CONSENSUS |
| `endocannabinoid` | recovery / PLAY | 6.0 | HYPOTHESIS |
| `substance_p` | RAGE / pain | 5.0 | CONSENSUS |
| `prolactin` | CARE support / GRIEF brake | 25 | CONSENSUS |
| `adrenaline` | sympathetic effector | 1.5 | FACT |
| `il6` | sickness / SEEKING brake | 40 | CONSENSUS |

## Circuits → drivers / brakes

| circuit | drivers | brakes |
|---|---|---|
| SEEKING | DA | dynorphin, IL-6, cortisol |
| RAGE | substance P, glu, adrenaline | GABA, opioid |
| FEAR | CRH, NE, adrenaline | GABA, opioid |
| LUST | DA, OT, AVP | cortisol, IL-6 |
| CARE | OT, prolactin, opioid | cortisol |
| GRIEF | glu, CRH | opioid, OT, prolactin |
| PLAY | opioid, endocannabinoid, DA | cortisol, CRH |

## Event → dominant effect (sign)

| event | up | down |
|---|---|---|
| warmth / trust / inclusion | OT, CARE, opioid | GRIEF |
| praise / novelty | DA, SEEKING | — |
| play_invite / humor | PLAY | FEAR |
| threat | FEAR, CRH, NE, adrenaline | PLAY |
| loss / abandonment | GRIEF, CRH, dynorphin | opioid, OT, SEEKING |
| rejection | GRIEF, RAGE | opioid, OT |
| frustration / insult | RAGE, substance P | OT (insult) |
| safety / repair | opioid, CARE, OT | FEAR, GRIEF, RAGE |
| sickness | IL-6, cortisol | SEEKING, PLAY |

## Constitution (plane 0 prior)

Frozen dataclass. Empty maps and unit scales are the identity. Magnitudes
HYPOTHESIS; signs follow Rothbart / Cloninger TCI / Gray–McNaughton RST /
Meaney–Weaver. Never authors `forbidden`. Never scales Andersen `h1/h2/h3`.

| archetype | rest offsets | event gain | other | tag |
|---|---|---|---|---|
| `default` | — | — | identity | — |
| `high_fffs` | FEAR +0.07, PLAY −0.02 | FEAR 1.40, CRH/NE/adrenaline up | FEAR τ × 1.30 | HYPOTHESIS |
| `high_bis` | FEAR/GRIEF +0.04, SEEKING −0.02 | FEAR/GRIEF 1.15 | 5-HT baseline +0.05 | HYPOTHESIS |
| `high_bas` | SEEKING +0.07, PLAY +0.03, FEAR −0.02 | DA 1.30, SEEKING 1.25 | DA baseline +0.05 | HYPOTHESIS |
| `meaney_low_nurture` | FEAR +0.03 | — | μ × 0.70, ρ × 0.75, rest `stress_gain` 1.30 | CONSENSUS mechanism, HYPOTHESIS magnitudes |

Attachment `STYLE_PRIORS` overlay constitutional rest, they do not replace it.

## Policy readout (inverse half)

| high occupancy | policy |
|---|---|
| FEAR / vigilance | forbid escalate, novelty, forced disclosure; prefer safety |
| RAGE | forbid mock / crowd; prefer boundary, space; raise brevity |
| GRIEF | forbid abandon / minimize / forced play; prefer repair, warmth, presence |
| PLAY (and low FEAR/RAGE) | prefer humor, play_invite |
| CARE | prefer warmth, soothe |
| allostatic load / low energy | forbid demand / long turn |
| LUST without trust | forbid sexualize |

## Optional HYPOTHESIS readouts (not constitutive)

These numbers leave the organism as *annotations* for an actuator. They never
write chemistry, never label an emotion, never decide `forbidden`.

### Doya 2002 metalearning (`relational/doya.py`)

| occupancy | readout | range | Doya §3 |
|---|---|---|---|
| 5-HT | discount γ | [0.50, 0.99] | item 2 |
| NE | inverse temperature β | [0.40, 8.00] | item 3 |
| ACh | learning rate α | [0.02, 0.45] | item 4 |
| last RPE | TD error δ | ℝ | item 1 |

Compatible with, not identical to, Yu & Dayan 2005 (already constitutive).

### Chemistry → decode hyperparams (`derive_policy`)

| high occupancy | decode effect |
|---|---|
| 5-HT / cortisol | shrink `top_p` (tighter nucleus) |
| DA / ACh | raise `presence_penalty` (more thematic wander) |
| ACh / cortisol | raise `memory_decay` |
| PLAY / SEEKING | raise sampling `temperature` |
| FEAR / 5-HT / load | lower sampling `temperature` |

These decode **signs must not be overwritten**. Claude (gift 3) raises
`top_p` with ACh; MOSAIC (gift 4) writes
`top_p = 0.90 + 0.08·exploration − 0.22·arousal`. Neither map is adopted.

### Sidecar annotations from gifts 3–4 (HYPOTHESIS)

Readouts and one gated extra term. None of them write chemistry, none
label an emotion, none decide `forbidden`. Verbals:
`docs/CLAUDE_ESSAY_EVAL.md`, `docs/MOSAIC_ESSAY_EVAL.md`,
`docs/RCAD_QWEN_GENSPARK_EVAL.md`.

| object | lives in | source | what it is not |
|---|---|---|---|
| `hpa["ultradian"]` | additive harmonic on \(dA, dC\), period 75 min | Walker, Terry & Lightman 2010 | not the Walker/Churilov DDE; not a 16.4♂/18.5♀ fit; Andersen \(h_1/h_2/h_3\) untouched |
| `valence_fe`, `fe_accel` | `CoreAffect` after PE update | Joffily & Coricelli 2013 | not Russell `valence`; not a Barrett feature |
| `homeostatic_drive` | `CoreAffect` from energy / load / vagal | Keramati & Gutkin 2014 | not a replacement of `allostatic_load` |
| `vigor` | `RelationalPolicy` from tonic DA + `v_hat` | Niv, Daw, Joel & Dayan 2007 | not a cause of `forbidden` |
| `attention_gain` | `RelationalPolicy` via `gaussian_optimum(NE, 0.46, 0.28)` | Aston-Jones & Cohen 2005 | not a replacement of linear `vigilance` |
| Hsueh extra term | `body.arousal() * FEAR` inside `CoreAffect.step` | Hsueh et al. 2023 *Nature* 615:292–299 | no-op at FEAR ≈ 0; not a new event field |
| `sensitization` (Z) | `CoreAffect`, τ ≈ 18 min from load / PE / FEAR, brake from vagal / energy | RCAD 0.1.0 hole; allostatic family | not a replacement of `allostatic_load`; not a Barrett feature |
| process packet | `planning_depth`, `clarification_bias`, `alternative_count`, `response_urgency`, `disclosure_confidence` on `RelationalPolicy` | RCAD 0.1.0 hole | not a cause of `forbidden`; not chemistry |
| `phenomenology_claim` / `immutable_constraints` | `PromptBundle` | RCAD adapter honesty | always false / non-overridable; not a generator of affect |
| `controllability`, `agency` | optional on `RelationalEvent` | RCAD appraisal hole | default 0.5; do not inject chemistry |
| `body.sympathetic` / `parasympathetic` | already computed, now exposed | two-axis annotation | not Porges / polyvagal |
| `Constitution` | rest / gain / τ / chem baselines / HPA μ/ρ | Rothbart; Cloninger; Gray RST; Meaney–Weaver | identity default; not a folk type; not Andersen h1/h2/h3 |

Lövheim 2012 is **not** a mapping in this sheet. NAC, `MosaicEngine`,
`RCADModel` and `NeuroChem-GenAI` are **not** mappings in this sheet.
