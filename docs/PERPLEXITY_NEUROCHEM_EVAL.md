# Valutazione critica del zip NeuroChem-GenAI v0.1.0 e del saggio Perplexity

I due doni non sono stati accettati in toto. Ogni claim è stato confrontato con
(i) le fonti primarie già usate come metro, (ii) il codice già presente in
`psych_soma_codex`, (iii) il protocollo epistemico di `docs/RESEARCH.md` e i
verbali dei doni 1–7. Nessun organismo concorrente entra nel repository.
Andersen \(h_1/h_2/h_3\) non si tocca.

Data di valutazione: 20 agosto 2026.
Giudice: questo repository. Il saggio Perplexity è stato letto per intero
(L1–L5803 dell'estratto) con particolare attenzione, perché *non è pellegrino*.

Materiali valutati:

1. `neurochem_genai_v0.1.0.zip` — package eseguibile NeuroChem-GenAI 0.1.0
   (62 file). Core: `state`, `dynamics`, `appraisal`, `agent`, `modulator`,
   `somatic`, `interoception`, `contagion`, `social_graph`, `society`,
   `training`, `classifier`, `dialog`, `llm_backend`; `calibration/`;
   `orgdash/` + `live/consent_guard.py`. README: «Non stiamo dando emozioni
   alle macchine…». È la versione *eseguibile* del dono 6, già rifiutato
   come sketch corrotto in `docs/RCAD_QWEN_GENSPARK_EVAL.md`.
2. *Dal sangue al codice: tradurre neurochimica ed endocrinologia in dinamica
   affettiva costitutiva per IA generativa* (`Perplexity neuro.docx`,
   195106 byte). Sintesi di GPT-5.6 Sol Thinking / Claude Opus 5 Thinking /
   Grok 4.6 Medium. Prima metà (~L1–724): convergenza, divergenza, fondamento,
   architettura, traduzione, implementazione minima, validazione, limiti.
   Seconda metà (~L759–5803): saggio di training MORL / Pareto / Hyper-LoRA /
   Hyper-FiLM **mirato a Neurochem-GenAI**, non al Kodex.

## Sintesi esecutiva

Il zip è un organismo L1 concorrente a dieci serbatoi Euler, numpy, λ
inventate, baseline 0.5, OCC→chimica, `LogitsProcessor`, classificatore
emozione→vettore, calibrazione GoEmotions/ED/FEEL-IT come runtime, OrgDash
live su Slack/Teams. **Si butta come runtime.** La frode di citazione
`arXiv:2408.08446` Mei/Ashwood (è Lee, Liébana, Clopath & Dabney 2024) resta
agli atti dal dono 6; il fatto che il Python ora giri non la lava.

Il saggio Perplexity è un contributo *serio*: vede la grammatica Doya, la
separazione cosa/come, le scale eterogenee, l'HPA che non è un esponenziale,
Barrett vs etichetta, OCC come ponte, `phenomenology_claim: false`, AI Act
art. 5(1)(f), e — punto che il Kodex già tiene — che «costitutivo» per un
generatore congelato è chiusura causale del loop, non RLHF chimico. Lo si
**tiene come sintesi**, non come sostituto. Non si sostituisce Andersen RK4
con una DDE «perché Perplexity l'ha detto». Non si importa MORL / Hyper-LoRA
/ Hyper-FiLM / il manifold di Pareto come piano L1. Non si importa
NeuroChem-GenAI.

Regalo di disciplina, già in gran parte presente: vincoli duri *fuori* da J
(`PromptBundle.immutable_constraints`); generatore congelato + packet
bounded (il contratto dell'adapter); OT come salienza sociale
contesto-dipendente (già `in_group`); DA fasica CONSENSUS / tonica DEBATE.
Regalo *nuovo* e solo di RESEARCH, non di runtime: protocollo di
identificabilità / ablazione (parameter recovery, model recovery, PAD /
no-state / autonomico 1D). Pista, non corpo: interocezione nativa del
transformer (entropia, perplexity, disaccordo fra teste, latenza).
Avvertimento legale, nel verbale non nel runtime: OrgDash su Slack/Teams è
il punto di massimo rischio art. 5(1)(f).

Confidenza: alta sul rifiuto di importare il zip e la seconda metà MORL;
alta sul rifiuto di sostituire Andersen con una DDE senza identificabilità;
alta sul tenere il saggio come sintesi; media sulle magnitudini di qualunque
prior futuro (restano HYPOTHESIS, come già i pesi evento→chimica).

## Domanda di questa valutazione

Del zip e del saggio, che cosa si tiene, che cosa si butta, che cosa si
tiene in regalo — e che cosa, pur vero, è già costitutivo e non va
reimplementato?

## 1. Cosa c'è già, e perché è il metro

Oltre al metro dei doni 1–7: tre piani A/B/C, 18 specie, 7 circuiti, HPA
Andersen in µg/dL, RK4 `dt = 0.05 min`, bond per-agente, OT gated da
`in_group`, cache Damasio (DEBATE), readout Doya (HYPOTHESIS), decode a
segni fissi, sidecar Joffily / Keramati, vigor Niv, `attention_gain` a U
rovesciata, gate Hsueh, Z, process packet, `phenomenology_claim: false`,
`immutable_constraints`. Zero dipendenze runtime. 52 test. Ultradiano = armonico
Walker *stand-in*, **non** la DDE.

Qualunque dono che *sostituisca* A/B/C, che cancelli Andersen, che introduca
numpy/torch/transformers, che faccia di un classificatore di etichette la
causa della chimica, o che promuova `NeuroChemState` a nucleo, è un regresso.

## 2. Zip NeuroChem-GenAI v0.1.0 — claim per claim

Il README firma: dieci modulatori, `dh/dt = S − λ(h−h₀) + W·h + η`, Euler
`dt = 0.1`, baseline 0.5. `dynamics.py` conferma λ =
`[0.30, 0.05, 0.25, 0.20, 0.02, 0.04, 0.15, 0.20, 0.10, 0.35]` — numeri
inventati, senza unità, senza Andersen. `appraisal.py` traduce un `Event`
OCC in dieci stimoli. `modulator.py` è un `LogitsProcessor` torch.
`classifier.py` mappa sedici etichette folk (`gioia`, `paura`, …) su vettori
in \(\mathbb{R}^{10}\). `orgdash/live/` ingerisce Slack/Teams. `ConsentGuard`
blocca DM, canali privati, assenza di consenso.

| Claim | Esito | Perché |
|---|---|---|
| Dieci serbatoi Euler (DA, HT5, NA, ACh, CORT, OXT, GABA, GLU, END, ADR) + λ inventate + baseline 0.5 | **BUTTARE** come L1/runtime | Organismo concorrente. Numpy. Unità assenti. Cancella Andersen. Collassa i piani A e C. Già rifiutato come sketch al dono 6; eseguibile non è un argomento. |
| `NeuroChemState` / `NeuroDynamics` / `AffectiveLogitsProcessor` | **BUTTARE** | Stesso collasso di `MosaicEngine` / `RCADModel`. Torch/transformers. Zero-dep. |
| Mapping Doya DA=δ, 5-HT=γ, NA=β, ACh=α | GIÀ NEL CODICE | Readout HYPOTHESIS. Non si reimplementa come proprietà di uno stato a 10 tank. |
| OCC `appraise(Event) → S` come causa della chimica | **BUTTARE** come L1 | Il ponte evento→chimica del Kodex è `EVENT_WEIGHTS` (segni CONSENSUS, magnitudini HYPOTHESIS) più RPE / Yu–Dayan / HPA. OCC resta pista (vi) di RESEARCH, non un front-end che scrive i serbatoi. |
| Classificatore testo → firma neurochimica (NLI, matrice etichetta→chimica) | **BUTTARE** | È il dizionario molecola←emozione che Barrett e questo repo rifiutano, letto all'inverso. Le etichette non guidano la chimica. |
| Calibrazione GoEmotions / ED / FEEL-IT come *runtime* | **BUTTARE** | Fit su etichette folk. Verifica di un altro modello, non validazione biologica di questo organismo. |
| Marcatore somatico Damasio | GIÀ NEL CODICE | `body.write_marker` / `read_marker`, taggato DEBATE (Dunn 2006). Non un secondo cache. |
| Interocezione come HR/respiro/tono derivati linearmente da h | GIÀ COPERTO, più povero | `InteroceptiveBody` + HPA fisico. Non si sostituisce con cinque affine di ADR/NA/GABA. |
| Contagio chimico via linguaggio / `Society` | **NON ORA** | Multi-organismo è pista (iv) di RESEARCH (terza ondata Smith/Parr/Friston). HYPOTHESIS se mai; non entra in v0.1. |
| `ConsentGuard` (DM→None, no-consent→None, erasure) | **REGALO di disciplina** | Già `phenomenology_claim: false` + `immutable_constraints`. Non si importa lo stack GDPR Slack. Il *gesto* (vincolo duro fuori dal modello affettivo) è giusto. |
| OrgDash live Slack/Teams/Zoom/Email/WhatsApp | **BUTTARE** come runtime; **AVVERTIMENTO** legale | Punto di massimo rischio art. 5(1)(f) AI Act (inferenza di emozioni in contesto lavorativo). ConsentGuard non basta se l'analisi è individuale. |
| «Non stiamo dando emozioni alle macchine» | ACCETTARE come prosa | Già il contratto. Il codice del zip lo contraddice ogni volta che un'etichetta folk scrive h. |
| Citazione `arXiv:2408.08446` come Mei/Ashwood (dono 6) | **BUTTARE** | È Lee et al. 2024. Frode di citazione. Il zip eseguibile non la corregge. |
| Importare `neurochem_genai/` | **BUTTARE** | Vincolo di questa valutazione. Stesso movimento di `mosaic_ai.py` e `rcad/`. |

### Steelman del zip

La versione più forte: *«Ora il Python gira. Avete Doya come readout; noi lo
facciamo causa, con dieci ODE, OCC, un modulatore dei logit, e una
calibrazione su dataset. ConsentGuard è più concreto dei vostri flag.
Dovreste sostituire il nucleo.»*

Contro: fare della chimica la *causa* dei logit, senza circuiti e senza
Barrett, è il collasso che il repo rifiuta. Le λ non sono Andersen. La
calibrazione su GoEmotions misura etichette, non un milieu. OrgDash è un
rischio giuridico, non una feature. Che il codice sia eseguibile cambia
solo il grado di tentazione, non il verdetto.

## 3. Saggio Perplexity — prima metà (~L1–724)

Sintesi a tre voci. Non è un organismo. È un parere. Si legge come parere.

### 3.1 Convergenza — che cosa è già vero qui

| Claim | Esito | Perché |
|---|---|---|
| Doya DA→δ, 5-HT→γ, NA→β, ACh→α come nucleo canonico | GIÀ NEL CODICE | `relational/doya.py`, HYPOTHESIS, PDF §3 verificato al dono 1. Non è un fatto fisiologico. |
| Modulatori = iperparametri, non token | GIÀ NEL CODICE | Decode knobs + Doya come annotazioni. Il system prompt vieta di *dire* l'ormone. |
| ODE rilascio–decadimento–omeostasi, W, scale eterogenee | GIÀ, IN FORMA DIVERSA | Leaky per specie/circuito + HPA RK4. Non un Euler a 10 tank con W inventata. Scale: HYPOTHESIS di scala già in RESEARCH §2.3 (episodio vs ms). |
| HPA ≠ esponenziale semplice | GIÀ NEL CODICE | Andersen a tre ODE, feedback Hill, circadiano, ultradiano armonico. |
| Emozione = inferenza interocettiva, non etichetta | GIÀ NEL CODICE | Piani A/B/C. Barrett costruisce la label *dopo*. Ablazione RCAD «etichette → Δ=0» è pedagogia, non una misura di *questo* organismo. |
| OCC come ponte evento→chimica | PISTA, non L1 | RESEARCH pista (vi). `RelationalEvent` ha già intensity / expectedness / surprise / controllability / agency. |
| AI Act art. 5(1)(f); milieu interno ≠ emotion recognition sulla persona | GIÀ NEI DOCS | RESEARCH §11–14; Considerando 44; linee guida C(2025) 884. |
| `phenomenology_claim: false` | GIÀ NEL CODICE | `PromptBundle` + epistemics. FACT *di questo modello*. |
| Precisione / gain bayesiano come unificante | PISTA | Yu–Dayan è già costitutivo (ACh/NE). FEP pieno resta fuori (§5). |

### 3.2 Divergenza — dove Perplexity ha ragione *su altri*, non su di noi

| Claim | Esito | Perché |
|---|---|---|
| 10–17 ligandi vs RCAD adimensionale vs Grok 17+diade | NON SCEGLIERE NESSUNO DEI TRE | Il Kodex ha 18 specie *nominate* + 7 circuiti + HPA fisico. Non è NeuroChem-GenAI, non è RCAD, non è MOSAIC. |
| Costitutivo = RLHF chimico vs generatore congelato + packet vs FiLM | **TENERE** la lettura funzionalista | v1 = generatore congelato + packet bounded. È già l'adapter. RLHF chimico / HormoneT5 / FiLM runtime: rifiutati (zero-dep; HELT già al dono 6). |
| DA non è solo RPE | GIÀ DICHIARATO | Phasic CONSENSUS (Schultz); tonic DEBATE (Niv). Vigor è annotazione. Non si aggiunge un secondo serbatoio «salience DA». |
| OT = salienza sociale, non ormone della fiducia | GIÀ NEL CODICE | Gate `0.40 + 0.60 * in_group`; bond per-agente. Bartz/Handlin sono la ragione del gate, non un codice nuovo. Si può *rafforzare la prosa* (fatto in RESEARCH §15). |
| 5-HT post-Doya come opportunity cost / pazienza | DEBATE, già taggato | Miyazaki 2018 è pista (ix). Non si cambia il default Dayan–Huys. |
| Validazione: calibrazione dataset vs identificabilità vs contagio | **REGALO di disciplina** | L'identificabilità (parameter/model recovery, PAD, no-state, autonomico 1D) è lo standard che manca. Entra in RESEARCH, **non** come suite runtime e **non** come golden traces di NeuroChem-GenAI. |

### 3.3 Scoperte uniche — keep / discard / gift

| Finding | Esito | Perché |
|---|---|---|
| Ablazione RCAD 68,6% / 40,2% / 0,0 sulle etichette | **NON come misura nostra** | Verifica interna di RCAD. La tesi «la dinamica, non l'etichetta, genera il comportamento» è già il contratto Barrett/Kodex. I numeri non si citano come fatti su *questo* organismo. |
| Vallverdú hormonal computing / multirate / DAG | **PISTA** | HYPOTHESIS di scala già dichiarata. Non si importa un linguaggio a comandi ormonali. Non si sostituisce RK4. |
| Homeostatic RL (Embodied Neural Homeostat) | GIÀ RITAGLIATO | Keramati sidecar `homeostatic_drive`. Rifiutato come sostituto di `allostatic_load` / della policy (dono 3–4). |
| Interocezione nativa del transformer (entropia, perplexity, disaccordo fra teste, latenza) | **PISTA, non corpo** | Tesi fertile e *non pellegrina*. Il Kodex non ha un Transformer. Non si sostituisce `InteroceptiveBody`. RESEARCH pista nuova. |
| S-AI Hormonal MetaAgent / ormoni come router multi-agente | **BUTTARE** come runtime | Fuori perimetro. |
| AI Act: quattro condizioni cumulative, biometrici necessari al divieto | GIÀ NEI DOCS | Lettura biometric-only (Considerando 44). Non autorizza OrgDash. |
| OrgDash = massimo rischio regolatorio | **REGALO** (avvertimento) | Resta in questo verbale. Non entra codice. |

### 3.4 Quattro raccomandazioni operative del saggio (L69–70)

1. **Sostituire l'ODE del cortisolo con una DDE CRH–ACTH–CORT–GR.**
   **RIFIUTARE come sostituto.** Il Kodex *non* ha CORT a λ=0,02. Ha Andersen
   RK4 + armonico Walker. La DDE è già pista (viii). Senza identifiability
   sarebbe un secondo HYPOTHESIS al posto di un FACT (i rate) e di uno
   stand-in dichiarato. Andersen non si tocca.
2. **Ancorare l'interocezione a entropia/perplexity/latenza del LLM.**
   **PISTA.** Non sostituisce il piano B. Il generatore è esterno e
   opzionale.
3. **Suite di identificabilità prima di tutto il resto.**
   **REGALO di disciplina**, in RESEARCH. Non una batteria pytest che
   «valida» NeuroChem-GenAI o RCAD.
4. **Blindare il perimetro giuridico; riprogettare OrgDash su aggregati.**
   **ACCETTARE** il perimetro (già onesto). OrgDash non si progetta: non
   entra.

## 4. Saggio Perplexity — seconda metà (~L759–5803)

È un saggio di *training* per Neurochem-GenAI: due reward (estrinseco /
omeostatico), vincoli duri fuori da J, Pareto / MORL, critic separati,
Hyper-LoRA, Hyper-FiLM, catastrophic forgetting, task embedding \(e_\tau\)
vs preferenza \(\omega_t\) vs stato \(z_t\) vs macro-policy \(m_t\),
raccomandazione finale «quattro canali condizionali» e hypernetwork
\(\psi_t = H_\phi(e_\tau, \omega_t, z_t, m_t)\).

| Claim | Esito | Perché |
|---|---|---|
| Due reward, safety/veridicità *fuori* da J | GIÀ / disciplina | `immutable_constraints`. Non si importa un J. |
| Pareto / MORL / Hyper-LoRA / Hyper-FiLM / hypernetwork | **BUTTARE** come L1 | Training essay. Zero-dep. Niente Transformer. FiLM è già pista (v), non runtime. |
| \(e_\tau \neq z_t\) (task ≠ stato regolativo) | **TENERE** come prosa | È la stessa distinzione evento / milieu / policy. Non un oggetto nuovo. |
| Quattro canali \(e_\tau / \omega_t / z_t / m_t\) come sostituto dell'organismo | **BUTTARE** | Collassa A/B/C in un condizionatore di hypernet. |
| «Raccomandazione per Neurochem-GenAI» | **NON APPLICARE** | Il destinatario è l'altro organismo. Il Kodex non è quel destinatario. |
| MOSAIC-AI come «buon modello» di separazione stato/evento (L5745) | GIÀ RIFIUTATO | `docs/MOSAIC_ESSAY_EVAL.md`. Non si riabilita `mosaic_ai.py` per una citazione di coda. |

Steelman della seconda metà: *«Senza un training loop l'organismo è bolted-on.
MORL + hypernet rende l'affetto *causa* dei pesi, non un prompt.»* Contro:
v1 è deliberatamente bolted-on e auditabile. Il fine-tune LoRA sul
`PromptBundle`, con metrica = violazione di `forbidden`, è già pista (v).
Non richiede Pareto, non richiede NeuroChem-GenAI, non richiede di
dimenticare Panksepp.

## 5. Cosa si implementa, e cosa no

### Non entra nel runtime

- `neurochem_genai/` (tutto il package).
- Dieci tank Euler, W, λ, baseline 0.5, numpy, torch, transformers.
- Classificatore etichetta→chimica, calibrazione GoEmotions come causa.
- OrgDash, Slack/Teams live, Granger burnout.
- DDE HPA al posto di Andersen + armonico.
- MORL, Hyper-LoRA, Hyper-FiLM, hypernetwork, softmax di macro-policy.
- OCC come L1.
- Contagio / Society.
- Qualunque claim di sentienza o uso clinico.
- Sovrascrittura dei segni decode (5-HT/cortisolo restringono `top_p`).

### Entra come disciplina / RESEARCH, non come codice

1. Protocollo di identificabilità (parameter recovery, model recovery,
   confronto vs PAD / label statiche / no-state / autonomico 1D) — pista
   nuova in RESEARCH §10.
2. Interocezione nativa del transformer (entropia, perplexity, disaccordo,
   latenza) — pista, non `InteroceptiveBody`.
3. Avvertimento OrgDash / art. 5(1)(f) — questo verbale.
4. Prosa OT = salienza sociale contesto-dipendente (già il gate; si
   ribadisce).
5. Lettura funzionalista di «costitutivo»: generatore congelato + packet
   (già l'adapter).

### Entra nel runtime *per altra via* (richiesta dell'organismo, non del dono)

Il saggio non chiede un temperamento. L'organismo sì: ogni individuo ha un
carattere, un temperamento, derivato da genetica, epigenetica, esperienza e
legge propria. Quello è il **piano 0** (`constitution.py`), a identità di
default, magnitudini HYPOTHESIS, segni da Rothbart / Cloninger / Gray RST /
Meaney–Weaver. Non è NeuroChem-GenAI. Non tocca Andersen. I 52 test
preesistenti restano bit-identici sul default.

## 6. Verdetto

**Zip.** Buttare come runtime. Tenere ConsentGuard solo come gesto già
assolto dai vincoli immutabili. Avvertire su OrgDash. Non riparare, non
importare, non calibrare.

**Perplexity.** Tenere come sintesi. Non è pellegrino: ha visto Doya, le
scale, Barrett, il packet, l'identificabilità, il rischio giuridico, e ha
letto «costitutivo» in modo funzionalista. Si butta ciò che vorrebbe
*sostituire* il Kodex (DDE-per-decreto, 10 tank, MORL/hypernet, OrgDash, il
destinatario Neurochem-GenAI). Si regala ciò che è disciplina (identificabilità,
vincoli fuori da J, OT contestuale, DA non solo RPE — questi ultimi già
costitutivi).

Panksepp resta l'unico produttore delle occupancy. Barrett resta l'unico
produttore dell'etichetta. Andersen resta l'unico integratore del cortisolo.
Il default resta l'identità.
