# Valutazione critica del rapporto Mistral (*Mistral neuro.docx*)

Il dono non è stato accettato in toto. Ogni claim è stato confrontato con
(i) le fonti primarie già usate come metro, (ii) il codice già presente in
`psych_soma_codex`, (iii) il protocollo epistemico di `docs/RESEARCH.md` e i
verbali dei doni 1–8. Nessun simulatore a spike, nessuna griglia \(5^7\),
nessun layer PyTorch entra nel repository. Andersen \(h_1/h_2/h_3\) non si
tocca. Lövheim resta rifiutato come classificatore (già dono 1).

Data di valutazione: 21 agosto 2026.
Giudice: questo repository. Il rapporto è stato letto per intero
(L1–L998 dell'estratto, 37646 caratteri).

Materiale valutato:

1. *Traduzione del Sistema Chimico-Fisiologico degli Ormoni e
   Neurotrasmettitori Umani in Codice Riproducibile per IA Generativa*
   (`Mistral neuro.docx`, 39554 byte). Autore dichiarato: «Dan (con supporto
   Vibe Work)», 20 agosto 2026. Domanda di ricerca coincidente con quella
   del Kodex. Non è un organismo eseguibile. È una rassegna + tre sketch
   (Brian2 STDP, `NeuroModulationLayer` PyTorch, `EmotionEngine` a sette
   interi 0–5).

## Sintesi esecutiva

Il rapporto *non è un organismo concorrente* nel senso dello zip
NeuroChem-GenAI. È più povero, e in un punto più pericoloso: propone di
*scrivere* la chimica a partire da un'etichetta folk (`set_emotion('joy')`)
e di *dire* l'ormone nel prompt (`[NEURO_STATE: cortisol=1, …]`). Quello è
il dizionario molecola←emozione che Barrett e questo repo rifiutano, più il
gesto che l'adapter vieta.

Le sette «insight» da 5 stelle sono, nell'ordine: il cubo di Lövheim
(già rifiutato, e qui *disegnato storto*); il motore Iovane & Di Pasquale
2025 (78.125 «stati mentali» = \(5^7\) interi, non fisiologia); NEUCOGAR /
Talanov (metafora von Neumann, non Doya); Brian2 + STDP di Izhikevich
(scala del millisecondo, già rifiutata); di nuovo NEUCOGAR; un layer
FiLM-like su Mistral-7B; NEST/NEURON/PyNN. Nessuna di queste è L1. Tre
sono già agli atti come scarti (Lövheim, Iovane come «sede debole»,
Brian2/Nengo al dono 3).

Si **tiene come rassegna di ciò che non si fa**, non come sintesi al livello
di Perplexity. Perplexity aveva visto Doya, le scale, Barrett, il packet,
l'identificabilità, l'AI Act. Mistral non cita Panksepp, non cita Barrett,
non cita Andersen, non cita Doya. Il cortisolo è un intero 0–5. L'HPA non
esiste.

Regalo, solo di disciplina e già in gran parte costitutivo: la domanda
aperta sulla *scala temporale* (ms vs minuti) è esattamente RESEARCH §2.3;
la «individual variability» è il piano 0. Non si implementa niente di
nuovo. Avvertimento: EEG da cuffia commerciale → neurotrasmettitori è il
punto in cui Iovane stesso ammette «feasibility only», e dove un DSS
«emotivo» sull'umano tocca art. 5(1)(f).

Confidenza: alta sul rifiuto di Lövheim, della griglia \(5^7\), di
Brian2/NEST come runtime, del `NeuroModulationLayer`, del
`set_emotion('joy')`; alta sul fatto che Iovane 2025 *esiste* (MDPI
*Electronics* 14(6):1093) e resta combinatoria, non biologia; media sulle
magnitudini di qualunque prior futuro (restano HYPOTHESIS).

## Domanda di questa valutazione

Del rapporto, che cosa si tiene, che cosa si butta, che cosa si tiene in
regalo — e che cosa, pur vero, è già costitutivo e non va reimplementato?

## 1. Cosa c'è già, e perché è il metro

Oltre al metro dei doni 1–8: quattro piani 0/A/B/C, 18 specie, 7 circuiti,
HPA Andersen in µg/dL, RK4 `dt = 0.05 min`, bond per-agente, OT gated da
`in_group`, Doya come readout HYPOTHESIS, decode a segni fissi, packet,
`phenomenology_claim: false`, `immutable_constraints`, costituzione a
identità di default. Zero dipendenze runtime. 60 test. Lövheim è già
rifiutato come classificatore (RESEARCH §9, §11). Iovane 2025 era già in
bibliografia come «non verificato, sede debole». Brian2/Nengo/Izhikevich
sono già rifiutati al dono 3. La scala del millisecondo è già dichiarata
fuori oggetto (§2.3). FiLM / LoRA / HormoneT5 sono già pista (v), non
runtime.

Qualunque dono che *sostituisca* A/B/C con una griglia di interi, che
faccia di un'etichetta folk la causa della chimica, che importi un
simulatore a spike, o che inietti `[NEURO_STATE: cortisol=…]` nel prompt,
è un regresso.

## 2. Errori di fatto, prima dei claim

Quattro sbagli stanno nel testo *prima* di qualunque raccomandazione. Non
sono stile. Sono il metro.

| Errore | Cosa c'è | Cosa è |
|---|---|---|
| Cubo «Lövheim» disegnato come Russell | Assi *valence × arousal*, «disgust» come terza, «dominance» come quarta. Euforia/gioia/paura/tristezza/rabbia/calma disposti su un piano 2D. | Lövheim 2012 (*Medical Hypotheses* 78:341–348, PMID 22153577) è un cubo **DA × 5-HT × NA**, angoli = otto affetti di Tomkins, ipotesi di *ortogonalità* dei monoamini. Non è Russell 2003. Il disegno del rapporto è un PAD con un nome sbagliato. |
| \(7^5 = 78\,125\) | Diagramma del motore: «STATO GLOBALE → \(7^5 = 78{,}125\) stati». Testo: «6 livelli discreti (0–5)». | \(7^5 = 16\,807\). \(6^7 = 279\,936\). \(5^7 = 78\,125\). Iovane 2025, §2, scrive \(5^7\) su \(\{1,2,3,4,5\}\). Il rapporto sbaglia la base, l'esponente, e l'intervallo, e ottiene per coincidenza il numero giusto. |
| Cortisolo come intero 0–5, «livello normale = 3» | Tabelle 4.1.1–4.1.2. | Il Kodex ha Andersen in µg/dL, \(h_3 = 0.0105\,\mathrm{min}^{-1}\), circadiano, feedback Hill. Un ordinale 0–5 cancella l'unico sotto-sistema con ODE da fonte primaria. |
| Citazione Picard | «La vera intelligenza artificiale non sarà quella che supera l'uomo in logica, ma quella che lo eguaglia in emozione e creatività.» — *Adattamento libero da Rosalind Picard*. | Non è una citazione. È una didascalia. Picard 1997 resta un libro vero; questa frase no. |

Il DOI Springer `10.1007/s11042-026-21288-5` non è stato risolto a una
landing page dell'editore. Esiste su ResearchGate un lavoro Iovane dal
titolo affine (*A novel neuromorphic engine… bioliquid intelligence*). Non
si cita il DOI del rapporto come prova. Non si accusa frode di citazione
senza il PDF: si marca **URL non verificato**.

## 3. Claim per claim

### 3.1 Lövheim + NEST

| Claim | Esito | Perché |
|---|---|---|
| Cubo di Lövheim come validazione che DA/5-HT/NA mappano stati emotivi 3D | **BUTTARE** come classificatore | Già dono 1. Sede *Medical Hypotheses*. L'autore chiede studi ulteriori. Confligge con Barrett (degeneracy: niente fingerprint). RESEARCH §9: «rifiutato / alto sul rifiuto». Il disegno del rapporto, in più, non è Lövheim. |
| NEST come simulazione del cubo (Talanov et al. 2019) | **BUTTARE** come runtime | Simulatore a spike, cervello di ratto, 1000 ms. Scala sbagliata (§2.3). Zero-dep. Non è un HPA. Non è Panksepp. |
| Talanov: DA ↑ risorse computazionali, 5-HT ↓, NA modula DA | **NON COME L1** | È NEUCOGAR: metafora von Neumann (attenzione = CPU). Doya 2002 è già readout (δ, γ, β, α), HYPOTHESIS, e *non* dice «risorse». Non si reimplementa una CPU ormonale. |

### 3.2 Iovane & Di Pasquale 2025

Il paper **esiste**: Iovane, G. & Di Pasquale, R. (2025), *A Complexity
Theory-Based Novel AI Algorithm for Exploring Emotions and Affections by
Utilizing Artificial Neurotransmitters*, *Electronics* 14(6):1093,
https://doi.org/10.3390/electronics14061093. RESEARCH lo teneva come «non
verificato, sede debole». Ora è verificato come esistente. Resta fuori dai
pilastri.

Cosa fa, in concreto (abstract + §2–4 del HTML MDPI):

- Sette assi \(X_1\ldots X_7\) (cortisolo, adrenalina, GABA, DA, 5-HT, OT,
  endorfine), ciascuno in \(\{0,1,2,3,4,5\}\).
- \(5^7 = 78\,125\) n-tuple. Proiezione su un piano energia–entropia
  \(f_1 = (E, S)\) con medie pesate. Dodici algoritmi su reticolo 8-connesso
  che «minimizzano l'entropia». Cinque attrattori. Otto «operational
  strategies» che sono *permutazioni dell'ordine* in cui si toccano gli
  \(X_i\).
- Mapping su Ekman. EEG da cuffia *commerciale / entertainment* (marca
  omessa), ~100 prove, stimoli audio/video da 5 min, gli autori stessi:
  feasibility, niente misura diretta di neurotrasmettitore, campione non
  statistico.
- Obiettivo dichiarato: DSS per «liquid intelligence»; tra i futuri, «AI
  con un genere definito» via ormoni.

| Claim | Esito | Perché |
|---|---|---|
| 78.125 stati mentali distinti | **BUTTARE** come fenotipo | È il cardinale di \(\{1,2,3,4,5\}^7\). Ogni 7-upla di interi è uno «stato». Non è uno spazio di circuiti, non è un milieu, non è un HPA. Contare le tuple non è modellare. |
| Livello 3 = equilibrio / conservazione dell'energia; 2/4 implosivo-esplosivo; 1/5 anarmonico | **BUTTARE** | Termodinamica nominale su ordinali. Non c'è una misura, non c'è un'unità, non c'è Andersen. |
| EEG → neurotrasmettitore (misura indiretta) | **BUTTARE** come validazione; **AVVERTIMENTO** | Gli autori lo dicono feasibility. Cuffia non medica. Inferire DA/OT/cortisolo da bande EEG e poi chiamarlo «causa» dell'emozione è il dizionario molecola←segnale, due volte. Su un umano è il punto di rischio art. 5(1)(f). |
| Mapping emozione ↔ \(X_i\) (euforia = endorfine 5, DA 5, …) | **BUTTARE** | Classical view. Barrett Tab. 1. Lo stesso collasso del `classifier.py` NeuroChem-GenAI. |
| Codice `EmotionEngine.set_emotion('joy')` | **BUTTARE** | L'etichetta *scrive* i sette interi. Nel Kodex l'etichetta nasce *dopo* (piano C). Questo inverte A/B/C. |
| Iovane come paper da citare in bibliografia di quadro | **TENERE il puntatore, scartare il pilastro** | Esiste. MDPI *Electronics*, computer science, non neuroscienza computazionale. Aggiorna la voce «non verificato». Non entra nei segni, non entra nei test. |

### 3.3 Brian2 / NEURON / NEST / PyNN / Izhikevich 2007

| Claim | Esito | Perché |
|---|---|---|
| Brian2 + dopamine-modulated STDP come «codice pronto all'uso» per l'IA generativa | **BUTTARE** come runtime | Già dono 3 (Nengo/Brian2/Izhikevich). τ in ms, vescicola, rete spiking. RESEARCH §2.3: l'oggetto costitutivo è l'episodio, non la sinapsi. Zero-dep. |
| Izhikevich 2007 (*Cerebral Cortex* 17:2443–2452) | **TENERE** come paper | Esiste. Risolve il distal reward problem legando STDP e DA. Non è un argomento per importare Brian2 nel Kodex. |
| NEURON / NEST / PyNN | **BUTTARE** come runtime | Stessa scala, stesse dipendenze. Tutorial, non organismo. |
| Hardware neuromorfico (Loihi, TrueNorth) | **BUTTARE** | Fuori perimetro. |

### 3.4 Layer di neuromodulazione su LLM

| Claim | Esito | Perché |
|---|---|---|
| `NeuroModulationLayer`: stato 7D (0–5) → bias additivo sugli embedding di Mistral-7B | **BUTTARE** come runtime | Famiglia FiLM / AdaLN / HormoneT5, già pista (v) e già rifiutata come L1 (zero-dep, niente Transformer). HELT esiste e resta fuori. Questo sketch è più povero: un `Linear` + `Tanh` + somma. |
| Condizionamento del prompt `[NEURO_STATE: cortisol=1, dopamine=5, …]` | **BUTTARE** | L'adapter *vieta di dire l'ormone*. Il system prompt porta policy, circuiti, vincoli; non un vettore da leggere ad alta voce. EmotionPrompt (Li 2023) è già pista, non un dizionario di interi. |
| `EmotionMemory` con `np.random.rand(128)` come embedding del contesto | **BUTTARE** | Toy. Il Kodex ha bond per-agente e marker Damasio (DEBATE). Non un secondo cache a cosine similarity. |
| `emotion_to_neuro["joy"] = {dopamine: 5, …}` | **BUTTARE** | Stesso inversione Barrett del classificatore NeuroChem e di `set_emotion`. |
| Integrazione «(a) layer, (b) memoria episodica, (c) prompt» come stato dell'arte | **NON SCEGLIERE NESSUNO DEI TRE** | v1 = generatore congelato + `PromptBundle` bounded. È già l'adapter. Non un fine-tune, non un FiLM, non un vettore detto nel testo. |

### 3.5 Raccomandazioni operative (sezione 6)

| Raccomandazione | Esito | Perché |
|---|---|---|
| Implementare `NeuroModulationLayer` in 2–4 settimane | **RIFIUTARE** | Vedi 3.4. |
| Dataset testi annotati con emozioni *e* neurotrasmettitori | **RIFIUTARE** come causa | Fit su etichette folk. Stesso vizio di GoEmotions nel dono 8. |
| Validare con EEG reale | **RIFIUTARE** come misura *nostra*; **AVVERTIMENTO** se su persone | Iovane è feasibility. Su un umano, emotion recognition. |
| Demo Brian2 | **RIFIUTARE** | Scala sbagliata. |
| Loihi | **RIFIUTARE** | Fuori perimetro. |
| Casi d'uso «chatbot empatici, assistenza sanitaria» | **AVVERTIMENTO** | Il contratto vieta uso clinico. Yang et al. 2024 già chiude sull'etica; questo la rende più acuta. |
| «Il futuro dell'IA è emotivo, e il codice per costruirlo esiste già» | **RIFIUTARE** come prosa | Slogan. Il codice che «esiste già» nel rapporto è Brian2 + sette interi + un `Linear`. Il Kodex esiste già, e non è quello. |

### 3.6 Domande aperte del rapporto — che cosa è già risposto

| Domanda (loro §5) | Esito | Perché |
|---|---|---|
| Validazione biologica dei modelli NT | GIÀ DICHIARATA | Magnitudini HYPOTHESIS, segni CONSENSUS, test qualitativi, niente dati umani nuovi (RESEARCH §10). Iovane non chiude il buco: lo rinomina EEG. |
| Scala temporale ms vs minuti/ore | GIÀ RISPOSTA | §2.3: episodio + HPA. Chi vuole il millisecondo cambia oggetto. |
| Interazioni non lineari DA × 5-HT | GIÀ, IN FORMA DIVERSA | Driver/brake sui circuiti; Doya come readout; niente W inventata a 10 tank (dono 8). |
| Individual variability | GIÀ NEL CODICE | Piano 0, identità di default, archetipi nominati. Non una griglia 0–5. |
| Layer vs prompt vs fine-tune | GIÀ SCELTO | Generatore congelato + packet. Pista (v) per LoRA sul bundle, metrica = violazione di `forbidden`. |
| Manipolazione emotiva / privacy / bias / responsabilità | GIÀ NEI DOCS | §8.6, §11–15, `phenomenology_claim: false`, AI Act. Il rapporto alza la domanda e poi raccomanda chatbot sanitari. |

## 4. Steelman, e il contro

La versione più forte: *«Avete un milieu continuo e dei circuiti. Noi vi
diamo (i) un cubo monoaminico con una simulazione NEST alle spalle, (ii)
78.125 stati discreti già pubblicati su MDPI, (iii) STDP dopaminergico in
Brian2, (iv) un layer che *modula i pesi* del transformer invece di un
prompt. Dovreste sostituire il piano C con Ekman, il piano B con la
griglia, e l'adapter con FiLM.»*

Contro:

1. Lövheim non è un fatto, e il cubo nel rapporto non è Lövheim.
2. \(5^7\) è un cardinale, non un organismo. Ekman è la classical view.
3. STDP è la scala che il Kodex ha dichiarato fuori. Izhikevich 2007 non
   autorizza a cancellare Andersen.
4. FiLM/HormoneT5 è già pista (v). v1 è deliberatamente bolted-on e
   auditabile. Un `Linear` su Mistral-7B non rende l'affetto *causa*: rende
   l'affetto un bias sugli embedding, senza circuiti, senza Barrett, senza
   HPA.
5. `set_emotion('joy')` è il collasso che i doni 6–8 hanno già incarnato in
   tre organismi diversi. Non diventa vero perché gli interi sono sette
   invece di dieci.

Che il paper Iovane esista cambia il grado di tentazione, non il verdetto.
Che Brian2 sia software vero cambia il grado di tentazione, non la scala.

## 5. Cosa si implementa, e cosa no

### Non entra nel runtime

- `EmotionEngine`, `NeurotransmitterState`, `NeuroModulationLayer`,
  `EmotionMemory`, gli sketch Brian2/NEST/NEURON/PyNN.
- Griglia \(5^7\) / \(6^7\), piano energia–entropia, attrattori Iovane,
  operational strategies OS_1–OS_7.
- Cubo di Lövheim come classificatore o come disegno Russell.
- Mapping etichetta folk → vettore NT (`emotion_to_neuro`, `set_emotion`).
- Prompt `[NEURO_STATE: cortisol=…]`.
- EEG come misura di questo organismo; cuffie; Loihi.
- numpy / torch / transformers / sklearn / brian2 / nest / neuron.
- Qualunque claim di sentienza o uso clinico / sanitario.
- Sovrascrittura di Andersen, di Panksepp, di Barrett, dei segni decode.

### Entra come disciplina / RESEARCH, non come codice

1. Aggiornare la voce Iovane 2025: da «non verificato» a **esiste, scartato
   come pilastro** (combinatoria + EEG entertainment + Ekman).
2. Ribadire Lövheim: rifiuto confermato; il dono 9 in più *sbaglia il
   disegno*.
3. Ribadire §2.3 (scala) e il piano 0 (variabilità individuale) come
   risposte già date alle «domande aperte» del rapporto.
4. Avvertimento: EEG → NT su persona, e «assistenza sanitaria», sono il
   punto di rischio art. 5(1)(f) — stesso gesto OrgDash, altra superficie.

### Non entra neanche come pista nuova

Izhikevich 2007, Picard 1997, Talanov/NEUCOGAR, FiLM-on-embeddings sono già
citati o già rifiutati. Non si apre una pista (xi) «griglia Iovane» o
«NEST come validazione».

## 6. Verdetto

**Mistral.** Tenere come rassegna di ciò che non si fa. Non è pellegrino
nel senso di Perplexity: non ha visto i tre piani, non ha visto Andersen,
non ha visto Barrett, ha disegnato Lövheim come Russell, ha sbagliato
\(7^5\), ha proposto `set_emotion('joy')` e `[NEURO_STATE:]`. Si butta ciò
che vorrebbe *sostituire* il Kodex (griglia, spike, FiLM, Ekman come causa,
EEG come validazione). Si tiene Izhikevich 2007 come paper già noto, Iovane
2025 come puntatore verificato e scartato, la domanda sulla scala e sulla
variabilità come già risposte. Si avverte sul sanitario e sull'EEG.

Panksepp resta l'unico produttore delle occupancy. Barrett resta l'unico
produttore dell'etichetta. Andersen resta l'unico integratore del
cortisolo. Il default resta l'identità. Lövheim resta fuori.
