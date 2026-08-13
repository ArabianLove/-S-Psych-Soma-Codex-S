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

Lövheim 2012 is **not** a mapping in this sheet.
