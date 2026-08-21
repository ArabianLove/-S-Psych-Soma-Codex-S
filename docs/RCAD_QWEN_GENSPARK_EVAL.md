# Valutazione critica dei doni 5–7 (Qwen, Genspark NeuroChem-GenAI, Manus RCAD 0.1.0)

I tre pacchetti non sono stati accettati in toto. Ogni claim è stato confrontato
con (i) le fonti primarie, (ii) il codice già presente in `psych_soma_codex`,
(iii) il protocollo epistemico di `docs/RESEARCH.md` e i verbali dei doni 1–4.
Nessun organismo concorrente entra nel repository.

Data di valutazione: 14 agosto 2026.
Materiali valutati:

1. *Da Neurotrasmettitore a Codice Riproducibile…* (Qwen, dono 5,
   `Qwen Neurotrasmettitori.docx`, 33825 byte).
2. *NeuroChem-GenAI* (Genspark, dono 6, `Gen Park Ormoni.docx`, 26027 byte).
   Il Python incollato nel docx è corrotto dall'estrazione XML
   (operatori incollati: `0.6gg`, `1.2state.NA`; mancano `*` e `__init__`).
   Si valuta come sketch, non come codice eseguibile.
3. Manus RCAD 0.1.0 (dono 7): paper *Dal sistema neurochimico umano a una
   dinamica affettiva costitutiva per IA generativa* (60160 byte, 709 righe),
   *Model Card — RCAD 0.1.0*, release `RCAD_0.1.0_research_release.zip`
   (103 file). **`rcad/` non si importa.**

## Sintesi esecutiva

Nessuno dei tre doni sostituisce l'organismo a tre piani. Qwen è una rassegna
pedagogica (PDE/DAT, SDE, ABM, GNN+LSTM, Digital Twin Brain, AFFECT-HRI, SAM,
PhysioLabXR): quasi tutto è già costitutivo o già rifiutato come runtime.
Genspark NeuroChem-GenAI è un organismo concorrente a 10 serbatoi Euler, con
numpy, λ inventate, Python rotto, e un grafo di citazione in parte fraudolento:
`arXiv:2408.08446` è Lee, Liébana, Clopath & Dabney, *Lifelong Reinforcement
Learning via Neuromodulation* — **non** Mei/Ashwood. HELT
(`arXiv:2605.13858`, HormoneT5, El-Metwally 2026) esiste, ma è un layer
Transformer a sei teste ormonali: zero-dep, niente Transformer, rifiutato.
Candia-Rivera 2026 (IMF, *Phys. Life Rev.*) e Corvaia/Pipitone/Chella 2025
(*IEEE Trans. Affect. Comput.*) sono paper reali; il primo è già coperto da
`InteroceptiveBody`, il secondo dal cache Damasio già taggato DEBATE.

RCAD 0.1.0 è il migliore dei tre: onesto (niente concentrazioni, niente
sentienza, etichette post-causali, safety fuori da J), ma è un organismo
concorrente a operatori innominati, softmax su 8 politiche nominate, e 7 test
+ ablation = **verifica interna**, non validazione biologica. Tre buchi
genuini sopravvivono e si innestano come HYPOTHESIS: (1) sensibilizzazione
lenta Z, distinta da `allostatic_load`; (2) process packet
(`planning_depth`, `clarification_bias`, `alternative_count`,
`response_urgency`, `disclosure_confidence`) come annotazioni *dopo* la
policy; (3) `phenomenology_claim: false` + vincoli immutabili di safety /
veridicità / permessi sul `PromptBundle`. Entra anche un test esplicito di
costitutività (stesso evento, prior diverso → policy diversa) e campi
opzionali di appraisal (`controllability`, `agency`) sull'evento, senza
diventare un L1 nuovo.

Confidenza complessiva: alta sul rifiuto di importare `rcad/`,
`NeuroChem-GenAI`, PDE/SDE/GNN; alta sull'accettazione di
`phenomenology_claim: false`; media sulle magnitudini di Z e del packet
(sono priori, come già vigor / decode).

## Domanda di questa valutazione

Qwen, NeuroChem-GenAI e RCAD sono soprainsiemi, sottoinsiemi, o concorrenti?
E, dei pezzi che propongono, quali sopravvivono al confronto con un organismo
che ha già Panksepp, Barrett, Andersen, Doya, decode, Joffily, Niv, Hsueh?

## 1. Cosa c'è già, e perché è il metro

Oltre al metro dei doni 1–4: tre piani A/B/C, 18 specie, 7 circuiti, HPA
Andersen in µg/dL, RK4 `dt = 0.05 min`, bond per-agente, OT gated, cache
Damasio, readout Doya, decode knobs a segni fissi, sidecar Joffily / Keramati,
vigor Niv, `attention_gain` a U rovesciata, gate Hsueh. Zero dipendenze
runtime. 46 test.

Qualunque dono che *sostituisca* A/B/C, che sovrascriva i segni di decode,
che introduca numpy/jsonschema, o che promuova un motore concorrente
(`MosaicEngine`, `NeuroChemState`, `RCADModel`) a nucleo, è un regresso.

## 2. Verifica delle fonti primarie usate come metro

### 2.1 `arXiv:2408.08446` — NON è Mei/Ashwood

Lee, S., Liébana, S., Clopath, C., Dabney, W. (2024), *Lifelong Reinforcement
Learning via Neuromodulation*, arXiv:2408.08446. Abstract riletto il 14
agosto 2026. È un framework astratto di RL adattivo, con un'istanza ACh/NA,
validata su bandit non-stazionario. È una *istanza* della famiglia Doya /
Yu–Dayan, già costitutiva. Genspark lo attribuisce a «Mei et al. e Ashwood
et al.»: attribuzione falsa. Si cita Lee 2024 per quello che è; non si
importa un secondo mapping ACh/NA.

### 2.2 `arXiv:2605.13858` HELT / HormoneT5 — esiste, rifiutato come runtime

El-Metwally, S. (2026), *A Hormone-inspired Emotion Layer for Transformer
language models (HELT)*, arXiv:2605.13858, 13 aprile 2026. Architettura
HormoneT5: sei valori ormone-simili da attention head per-ormone, embedding
emotivo che modula gli hidden state dell'encoder T5. Paper reale. Questo
repo è zero-dep e non ha un Transformer. Collassare 18 specie + 7 circuiti
+ Andersen in sei teste di attenzione è esattamente il regresso Lövheim /
NAC. Rifiutato come runtime; tenuto come pista (v) di RESEARCH.

### 2.3 Candia-Rivera 2026 — reale, già coperto

Candia-Rivera, D. (2026), *Interoceptive machine framework: Toward
interoception-inspired regulatory architectures in artificial intelligence*,
*Physics of Life Reviews* (PMID 42284945; anche arXiv 2604.24527 secondo il
dono). Quadro di architetture regolative ispirate all'interocezione. Il
piano B (`InteroceptiveBody` + HPA + `allostatic_load`) *è già* quel quadro.
Citazione, non codice nuovo.

### 2.4 Corvaia, Pipitone & Chella 2025 — reale, già coperto

Corvaia, S., Pipitone, A., Chella, A. (2025), *Inner Speech and Damasio's
Theory for Modeling Robot's Emotions*, *IEEE Transactions on Affective
Computing*. Inner speech + somatic marker in robotica. Il repo ha già
`body.write_marker` / `read_marker`, taggato DEBATE (Damasio; Dunn 2006).
L'inner speech del robot è un atto generato: il loop
`act → infer_events_from_text → ingest` *è già* l'auto-percezione. Citazione,
non un secondo cache.

### 2.5 Doya, Yu–Dayan, Schultz, Barrett, Panksepp, Andersen

Già nel codice. Qwen e Genspark li ripetono. Non si reimplementano.

## 3. Dono 5 (Qwen) — claim per claim

| Claim | Esito | Perché |
|---|---|---|
| PDE + FEM per DA (diffusione + DAT Michaelis–Menten) | RIFIUTARE come runtime | Scala del millisecondo / geometria del cleft. Il repo opera a scala di episodio (`dt = 0.05 min`). HYPOTHESIS di scala già dichiarata in RESEARCH §2.3. |
| SDE / rumore stocastico sui modulatori | GIÀ COPERTO | `SimulationConfig.noise` + `Rng`. Non si importa un SDE nuovo. |
| ABM di popolazioni neuronali | RIFIUTARE | Fuori perimetro (non simuliamo neuroni). |
| GNN+LSTM per asse endocrino | RIFIUTARE | Dipendenze, scala, e l'HPA Andersen *esiste già*. |
| Digital Twin Brain | RIFIUTARE | Pretesa di gemello, non prior. Contratto del repo. |
| AFFECT-HRI / SAM / PhysioLabXR | CITAZIONI / piste | Validazione su umani e robot. Nessun dato in questo repo. |
| Neuromodulazione come meta-controllore | ACCETTARE come cornice | Già l'architettura. |
| Niente dizionario molecola → emozione | ACCETTARE | Contratto. |

Qwen è pedagogia. Entra in RESEARCH come rassegna di *cosa non si fa* a
runtime. Zero codice.

## 4. Dono 6 (Genspark NeuroChem-GenAI) — claim per claim

| Claim | Esito | Perché |
|---|---|---|
| Dieci serbatoi Euler (DA, 5-HT, NA, ACh, CORT, OT, …) + λ inventate | RIFIUTARE | Organismo concorrente. Numpy. Unità assenti. Cancella Andersen. |
| `NeuroChemState` / `NeuroDynamics` / `AffectiveLogitModulator` | RIFIUTARE | Stesso collasso di MosaicEngine: piani A e C spariscono. |
| Mapping Doya DA=δ, 5-HT=γ, NA=β, ACh=α | GIÀ NEL CODICE | Readout HYPOTHESIS. |
| Attribuzione di `arXiv:2408.08446` a Mei/Ashwood | RIFIUTARE | È Lee et al. 2024. Frode di citazione. |
| HELT / HormoneT5 come layer costitutivo | RIFIUTARE come runtime | Paper reale; architettura incompatibile (Transformer, 6 ormoni). |
| Constitutional Prompting | RIFIUTARE | I vincoli immutabili di RCAD (sotto) coprono lo stesso bisogno senza il marchio. |
| Candia-Rivera IMF 2026 | CITAZIONE | Già `InteroceptiveBody`. |
| Corvaia/Pipitone/Chella 2025 | CITAZIONE | Già cache Damasio. |
| Python del docx | RIFIUTARE | Corrotto, non eseguibile, non si ripara. |
| Sentienza / «il modello *è* l'asse» | RIFIUTARE | Contratto. |

### Steelman di Genspark

La versione più forte: *«Avete Doya come readout; noi lo facciamo causa,
con dieci ODE e un modulatore dei logit. HELT mostra che un Transformer
*può* condizionarsi a ormoni. Dovreste sostituire il nucleo.»* Contro: fare
della chimica la *causa* dei logit, senza circuiti e senza Barrett, è il
collasso che il repo rifiuta. HELT è un esperimento su T5, non una ragione
per cancellare Panksepp. Le λ non sono Andersen. L'attribuzione Mei/Ashwood
toglie autorità bibliografica al resto del saggio.

## 5. Dono 7 (Manus RCAD 0.1.0) — claim per claim

| Claim | Esito | Perché |
|---|---|---|
| Niente concentrazioni, niente sentienza, etichette post-causali | ACCETTARE come disciplina | Già il contratto. RCAD lo formula bene. |
| Safety / truthfulness / permissions *fuori* dalla funzione di costo J | ACCETTARE | Entra come `immutable_constraints` su `PromptBundle`. |
| `phenomenology_claim: false` | ACCETTARE | Campo esplicito sul bundle. Il system prompt lo diceva già in prosa. |
| Stato lento: load + **sensitization Z** | ACCETTARE Z, ritagliato | `allostatic_load` è già il load. Z è il buco: memoria lenta dello stress, distinta dal load corrente. Sidecar su `CoreAffect`. Non sostituisce il load. |
| `AffectiveControlPacket` (planning_depth, clarification_bias, alternative_count, response_urgency, disclosure_confidence, …) | ACCETTARE ritagliato | Annotazioni *dopo* `derive_policy`. Non scrivono chimica. Non decidono `forbidden`. Non si importa `memory_retrieval_budget` (vicino a `memory_decay` già presente). |
| Test di costitutività (stesso evento, prior diverso → ‖Δpolicy‖ > soglia) | ACCETTARE come test | Il repo testava già «stesso stato ⇒ stessa policy». Manca l'altra direzione, esplicita. |
| Appraisal strutturato (novelty, controllability, agency, norm_compatibility, …) | ACCETTARE due campi opzionali | `controllability` e `agency` su `RelationalEvent`. Non diventano un L1. Non iniettano chimica. Novelty / uncertainty / intensity *esistono già* (`expectedness`, `surprise`, `intensity`). |
| Coattivazione autonomica a due assi | ACCETTARE come esposizione | `body.step` calcola già sympathetic / parasympathetic e li butta. Si espongono. Non è Porges. |
| `RCADModel` + 5 assi di omeostasi innominati + 7 modulatori innominati | RIFIUTARE | Organismo concorrente. Collassa A e C. Nomi biologici rifiutati per disciplina (equifinalità, già accettata dal dono 4) — e poi *sostituiti* da operatori che questo repo ha già nominato meglio. |
| Softmax su 8 politiche nominate (`continue/approach/avoid/monitor/clarify/reappraise/seek_support/recover`) | RIFIUTARE | La `RelationalPolicy` è continua. Un classificatore a 8 atti è un regresso verso il one-hot. |
| Policy *prima* dell'update di stato | RIFIUTARE | Il nostro ordine 1–8 è Markov-blanket: il corpo parla prima della policy. Invertirlo è un altro organismo. |
| 7 test + ablation + sensitivity come validazione | RIFIUTARE come validazione | Verifica interna del *loro* modello. Non misura umani, non misura *questo* organismo. |
| `jsonschema`, `default_parameters` inventati, translation_matrix come runtime | RIFIUTARE | Zero-dep. La matrice molti-a-molti è pedagogia (già in MAPPING). |
| Importare `rcad/` | RIFIUTARE | Vincolo di questa valutazione. Stesso movimento di `mosaic_ai.py`. |

### Steelman di RCAD

La versione più forte: *«Il vostro organismo è un L2 sotto-identificato.
Il nostro L1 è più onesto (operatori, non µg/dL ovunque tranne Andersen),
ha Z, ha un packet di processo auditabile, ha i vincoli immutabili, e i
sette test dimostrano costitutività e ablazione. Dovreste *sostituire* il
nucleo e tenere Panksepp/Barrett come readout.»*

Contro: l'onestà dimensionale è reale, e Z / packet / vincoli *si
prendono*. Invertire produttore e readout — fare di Panksepp un'etichetta
sopra cinque assi innominati — è il collasso già rifiutato a MOSAIC. I
sette test verificano RCAD, non l'organismo. La policy continua +
`forbidden` da occupancy è più stretta del softmax a 8 nomi. Z e il packet
non hanno bisogno di quel collasso: si innestano in `CoreAffect` e in
`derive_policy`.

## 6. Cosa si implementa, e cosa no

### Entra (HYPOTHESIS, ritagliato)

1. **`CoreAffect.sensitization`** (Z lento). Leaky da `allostatic_load` +
   incertezza + FEAR; estinto da tono vagale / energia. τ ≈ 18 min
   (più lento del load, τ = 6 min). Non scrive `allostatic_load`. Non
   entra in `_feature_vector`. Tag: HYPOTHESIS (RCAD 0.1.0; famiglia
   allostatica Sterling / McEwen, non un paper di concentrazione).
2. **Process packet** su `RelationalPolicy`: `planning_depth`,
   `clarification_bias`, `alternative_count`, `response_urgency`,
   `disclosure_confidence`. Derivati da stato già presente. Non
   scrivono chimica. Non decidono `forbidden`.
3. **`PromptBundle.phenomenology_claim = False`** e
   `immutable_constraints` (safety / truthfulness / permissions non
   sovrascrivibili dall'affetto). Esposti nel system template.
4. **Appraisal opzionale** su `RelationalEvent`: `controllability`,
   `agency`. Se assenti, i default non iniettano chimica. Se presenti,
   modulano solo il packet (profondità, disclosure).
5. **Coattivazione autonomica**: `body.sympathetic` /
   `body.parasympathetic` esposti (già calcolati). Non è Porges.
6. **Test di costitutività** + accumulo di Z + bound del packet +
   `phenomenology_claim is False`.

### Non entra

- `rcad/`, `RCADModel`, operatori innominati, softmax-8, jsonschema.
- `NeuroChem-GenAI`, `NeuroChemState`, `NeuroDynamics`,
  `AffectiveLogitModulator`, Constitutional Prompting come marchio.
- HELT / HormoneT5 runtime.
- PDE/DAT, SDE nuovo, ABM, GNN+LSTM, Digital Twin Brain.
- Numpy / scipy.
- `memory_retrieval_budget` (coperto da `memory_decay`).
- Qualunque claim di sentienza o uso clinico.
- I 7 test RCAD come golden traces di *questo* organismo.

### Compatibilità con i tre piani

Z vive *dentro* il passo 5, come sidecar più lento del load. Il packet
vive *dopo* il passo 7, come annotazione dell'attuatore. I vincoli
immutabili vivono sul bundle (passo 8 → adapter). Barrett resta l'unico
produttore dell'etichetta. Panksepp resta l'unico produttore delle
occupancy. Andersen resta l'unico integratore del cortisolo. I segni
decode (5-HT/cortisolo restringono `top_p`) non si toccano.

## 7. Livelli di confidenza

| Giudizio | Livello | Perché |
|---|---|---|
| `arXiv:2408.08446` è Lee et al., non Mei/Ashwood | alto | abstract arXiv, 14 agosto 2026 |
| HELT `2605.13858` esiste e è HormoneT5 | alto | abstract arXiv, 13 aprile 2026 |
| HELT è un runtime accettabile per questo repo | rifiutato / alto sul rifiuto | Transformer, 6 ormoni, zero-dep |
| Candia-Rivera 2026 e Corvaia 2025 sono paper reali | alto | PubMed / IEEE |
| RCAD è un L1 concorrente, non un soprainsieme | alto | ispezione: 0 circuiti, 0 Barrett, 0 µg/dL |
| Z è distinto da `allostatic_load` e manca | medio-alto | buco strutturale reale; magnitudini priori |
| Il process packet migliora un LLM | ignoto | nessuna misura; layer esposto per falsificarlo |
| I 7 test RCAD validano la biologia | rifiutato / alto | lo dice la model card stessa |

## 8. Limiti

Non ho eseguito la suite RCAD dentro questo repository (non si importa).
Non ho riletto integralmente Candia-Rivera 2026 oltre PMID/tesi. Non ho
ricalibrato Z né il packet su un LLM reale. Le magnitudini sono priori
esposti per essere falsificati.
