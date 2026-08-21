# Valutazione critica del saggio Claude (dono 3)

Il saggio non è stato accettato in toto. Ogni claim è stato confrontato con
(i) le fonti primarie, (ii) il codice già presente in `psych_soma_codex`,
(iii) il protocollo epistemico di `docs/RESEARCH.md` e il verbale dei doni
1–2 (`docs/ESSAY_EVAL.md`). Qui sta il verdetto operativo.

Data di valutazione: 13 agosto 2026.
Saggio valutato:

- *Dagli ormoni al codice: tradurre neuromodulazione e affetto in
  architetture di IA generativa* (Claude, 26187 byte, 213 righe,
  `/home/user/uploaded_files/Claude From Hormones to Code_ Translating
  Neuromodulation and Affect into Generative AI Architectures.md`).

## Sintesi esecutiva

È il più onesto dei doni 1–3. Tagga Doya come metalearning riduttivo,
tagga NAC come *esplicitamente speculativa*, rifiuta la teoria polivagale
come consenso, cita primari veri (Joffily & Coricelli 2013; Hesp 2021;
Niv 2007; Walker, Terry & Lightman 2010; Keramati & Gutkin 2014) e
distingue analogia funzionale da identità biochimica. Quasi tutta la
«spina dorsale» che propone è *già costitutiva* in questo repository
(Doya come readout, Yu–Dayan, milieu multi-τ, decode knobs, allostatic
load, nota AI Act, niente sentienza). I buchi genuini sono tre, e
entrano solo come HYPOTHESIS: pulsatilità ultradiana dell'HPA (Walker),
sidecar Joffily \(v = -\mathrm{d}F/\mathrm{d}t\), vigor di Niv dalla DA
tonica. NAC, HomeostaticCore come sostituto dei tre piani, i toy numpy
e lo steering dei persona-vector restano fuori.

Confidenza complessiva sul verdetto: alta sui rifiuti (NAC, numpy, Porges
come consenso, cortisolo a un serbatoio); media sulle magnitudini dei
tre layer accettati (sono priori, come già i decode params).

## Domanda di questa valutazione

Quali affermazioni del saggio Claude sono (a) fatti verificati, (b)
ipotesi legittime da esporre come readout opzionale, (c) errori,
speculazioni o conflitti con l'architettura a tre piani già costitutiva?

## 1. Cosa c'è già, e perché è il metro

Il runtime preesistente è l'organismo a tre piani di `docs/ESSAY_EVAL.md`
§1: Panksepp (A), Russell/Sterling/Andersen/ANS (B), Barrett mixture (C).
Doya γ/β/α/δ è già un readout HYPOTHESIS (`relational/doya.py`). I decode
params `T / top_p / presence_penalty / memory_decay` esistono già, con
segni fissati (5-HT/cortisolo restringono `top_p`; DA/ACh alzano
`presence_penalty`; ACh/cortisolo alzano `memory_decay`). L'HPA è
Andersen 2013 a tre ODE, RK4, µg/dL, circadiano con picco ~07:30 — **senza
ritardo, senza ultradiano**. Il core affect ha `prediction_error` come
proxy di free-energy, ma **non** è \(- \mathrm{d}F/\mathrm{d}t\). La
policy non ha vigor. Vigilance usa NE in modo lineare. Zero dipendenze
runtime.

Qualunque dono che *sostituisca* A/B/C, che sovrascriva i segni di
decode, che introduca numpy, o che promuova NAC a nucleo costitutivo, è
un regresso.

## 2. Verifica delle fonti primarie usate come metro

### 2.1 Doya 2002 — già nel codice (dono 1)

Verificato sul PDF primario in `docs/ESSAY_EVAL.md` §2.1. Il saggio Claude
cita il passo corretto e lo tagga come riduttivo. Non si reimplementa.

### 2.2 Joffily & Coricelli 2013 — FATTO di attribuzione, IPOTESI di contenuto

Joffily, M., Coricelli, G. (2013), *Emotional Valence and the
Free-Energy Principle*, *PLoS Computational Biology* 9(6):e1003094
(PMID 23785269, PMC3681730, DOI 10.1371/journal.pcbi.1003094). Abstract
PLOS riletto il 13 agosto 2026; la frase che il saggio mette tra
virgolette coincide alla lettera:

> we propose a definition of emotional valence in terms of the negative
> rate of change of free-energy over time.

Il paper aggiunge che la derivata seconda distingue forme (happiness /
unhappiness / hope / fear / disappointment / relief; Table 1 / Figure 1)
e che la valenza regola il learning rate. È una *proposta* in free-energy
framework, non una misura fisiologica. Il nostro `prediction_error` è già
un proxy di F (mix leaky di unexpected uncertainty + ACh + NE), **non**
la F di Friston. Un sidecar \(v_\mathrm{FE} = -\Delta\mathrm{PE}/\Delta t\)
è quindi un'ipotesi di *lettura*, non la valenza di Russell/Panksepp.

### 2.3 Hesp / Sennesh et al. 2021 — citazione, non runtime

Sennesh, E. et al. (2021), *Deeply Felt Affect: The Emergence of Valence
in Deep Active Inference*, *Neural Computation* 33(2):398–446
(DOI 10.1162/neco_a_01341). Il saggio Claude lo chiama Hesp et al.; il
dono 4 lo cita come Sennesh et al. È lo stesso paper. Tesi: la valenza
emerge come precisione attesa del modello d'azione («subjective
fitness»). Non implementiamo active inference pieno (già pista (iii) in
`docs/RESEARCH.md` §10).

### 2.4 Niv, Daw, Joel & Dayan 2007 — FATTO di attribuzione

Niv, Y., Daw, N.D., Joel, D., Dayan, P. (2007), *Tonic dopamine:
opportunity costs and the control of response vigor*,
*Psychopharmacology* 191:507–520 (PMID 17031711,
DOI 10.1007/s00213-006-0502-4). Abstract PubMed riletto il 13 agosto
2026: il tasso medio di reward è riportato dalla dopamina *tonica*
(putativamente nel n. accumbens) e spiega perché più DA si associa a
risposte più vigorose. Il repo tagga già la DA tonica come DEBATE in
RESEARCH; non ha un readout di vigor sulla policy. È un buco genuino.

### 2.5 Walker, Terry & Lightman 2010 — FATTO sul meccanismo, non sul fit

Walker, J.J., Terry, J.R., Lightman, S.L. (2010), *Origin of ultradian
pulsatility in the hypothalamic–pituitary–adrenal axis*,
*Proceedings of the Royal Society B* 277:1627–1633 (PMID 20129987,
PMC2871854, DOI 10.1098/rspb.2009.2148). Meccanismo: il loop
pituitario–surrenalico genera i pulsi ultradiani da solo, per ritardo +
feed-forward/feedback, **senza** un pulse generator ipotalamico. Intervallo
interpulso tipico ~47–55 min (Windle 1998a, citato da Walker); la banda
60–90 min è l'ordine di grandezza accettato. Il saggio cita «16.4 ± 0.5
pulsazioni/24h ♂ e 18.5 ± 0.6 ♀» da un'analisi di deconvoluzione: è una
cifra reale di letteratura, **non** un fit che questo codice debba
riprodurre, e non è sesso-specifico nel nostro integratore. L'HPA
Andersen attuale è solo circadiano. Un drive ultradiano piccolo e
dichiarato HYPOTHESIS è il buco.

### 2.6 Keramati & Gutkin 2014 — già pista (vii)

*eLife* 3:e04811. Drive = distanza dal setpoint; reward = riduzione del
drive. Già in `docs/ESSAY_EVAL.md` e RESEARCH §10 come pista. Il saggio
raccomanda di «partire da `HomeostaticCore`». Contro: l'allostasi di
Sterling/Barrett e `allostatic_load` *esistono già* come piano B. Un
HomeostaticCore che *sostituisce* i tre piani è un regresso. Un'annotazione
`homeostatic_drive` calcolata sugli assi corporei già presenti è
accettabile.

### 2.7 Aston-Jones & Cohen 2005 — già citato, gain lineare

*Annu. Rev. Neurosci.* 28:403–450. LC–NE, modi fasico/tonico, curva a U
rovesciata. Il repo usa NE in modo *lineare* su `vigilance`. Un
`attention_gain` a U rovesciata è un'annotazione compatibile; non
sostituisce vigilance.

### 2.8 Polivagale — NON-CONSENSUS, e il saggio lo dice

Grossman & Taylor 2007; Grossman 2023; Neuhuber & Berthoud 2022. Il
saggio tagga correttamente Porges come non-consenso. Il repo non usa
Porges. Niente da fare, niente da disfare.

### 2.9 AI Act art. 5(1)(f) — già nota; Considerando 44 è nuovo

Regolamento (UE) 2024/1689 art. 5(1)(f), già in ESSAY_EVAL. Il saggio
aggiunge il Considerando 44 («limited reliability, lack of specificity,
limited generalisability») e le Linee guida Commissione C(2025) 884
final (lettura biometric-only del divieto). Entra in RESEARCH come nota
giuridica, non in runtime.

## 3. Claim per claim

| Claim | Esito | Perché |
|---|---|---|
| Mapping Doya è spina dorsale ma riduttivo | GIÀ NEL CODICE | Readout HYPOTHESIS; il saggio è allineato. |
| Yu–Dayan ACh/NE | GIÀ NEL CODICE | Costitutivo in `engine.py`. |
| Valenza = −dF/dt (Joffily 2013) | ACCETTARE come sidecar HYPOTHESIS | Attribuzione verificata sull'abstract PLOS. Non sostituisce Russell/Panksepp. Non entra nel costruttore Barrett. |
| Hesp/Sennesh valenza = expected precision | CITAZIONE / pista | Active inference pieno già pista (iii). |
| Niv 2007: DA tonica → vigor | ACCETTARE come annotazione HYPOTHESIS | Abstract PubMed verificato. Serve `v_hat` in `derive_policy`. |
| Walker 2010: ultradiano da feedback, non da pulse generator | ACCETTARE come drive piccolo HYPOTHESIS | Non DDE completa. Non fit 16.4/18.5 sesso-specifico. Non tocca h1/h2/h3. |
| Keramati HomeostaticCore come *punto di partenza* | RIFIUTARE come sostituto; ACCETTARE annotazione | `allostatic_load` è già il piano B. `homeostatic_drive` sidecar dagli assi esistenti. |
| Leaky-integrator multi-τ | GIÀ NEL CODICE | `ChemicalMilieu` + RK4 HPA. I τ del saggio sono in secondi e a 5 modulatori: non sostituiscono le 18 specie. |
| `Neuromodulator` / `NeuromodulatorySystem` numpy | RIFIUTARE | Dipendenza inutile. Scala temporale sbagliata (secondi vs minuti di episodio). CORT come serbatoio unico τ=3600 s cancella Andersen. |
| `map_to_generation_params` (T da NE−5HT; top_p sale con ACh) | RIFIUTARE i *segni* | I nostri segni decode sono già fissati e testati. Claude alza `top_p` con ACh; noi lo restringiamo con 5-HT/cortisolo. Non si sovrascrivono. |
| `attention_gain = 1 + 1.5·NE` (lineare) | RIFIUTARE come sostituto di vigilance; ACCETTARE U-rovesciata come annotazione | Vigilance lineare resta. L'U-rovesciata (Aston-Jones, più onesta del lineare di Claude) entra come `attention_gain`. |
| `entropy_bonus` da DA | PISTA | Nessun backend RL nel repo. |
| `retrieval_weight` da CORT | PISTA | Vicino a `memory_decay` già presente; non si aggiunge un secondo knob omonimo. |
| NAC a tre anelli | RIFIUTARE | Il saggio stesso la dice speculativa. I tre piani A/B/C *esistono già* e sono citati meglio. |
| Persona / emotion vectors (Anthropic 2025/2026) | PISTA | Serve un backend Transformer. Zero-dep. |
| Backpropamine / Izhikevich STDP | PISTA | Stesso vincolo. |
| WESAD / DEAP / AMIGOS / K-EmoCon | PISTA di validazione | Nessun dato umano in questo repo. |
| Nengo / Brian2 | RIFIUTARE come runtime | Fuori perimetro (non simuliamo neuroni). |
| Polivagale come consenso | RIFIUTARE (e il saggio è d'accordo) | Già assente. |
| AI Act + Cons. 44 + C(2025) 884 | ACCETTARE come nota | Docs only. |
| Niente sentienza / hard problem | ACCETTARE | Contratto del repo. |
| «Partire dal loop omeostatico, non dagli iperparametri» | RIFIUTARE come ordine di lavoro | L'organismo *è già* allostatico. I decode params sono un layer, non il nucleo. Invertire l'ordine sarebbe un reset, non un miglioramento. |

### Steelman del saggio Claude

La versione più forte: *«Avete già Doya e i decode knobs, ma vi manca la
dinamica che *produce* l'affetto come derivata della surprise, vi manca
l'ultradiano che ogni endocrinologo si aspetta da un HPA, e il vigor è
il pezzo di Niv che avete citato come dibattito senza mai esporlo. NAC
è solo un disegno per tenere insieme questi pezzi.»*

Contro parziale: i tre buchi *sono* reali, e si chiudono *senza* NAC.
Un anello interocettivo lento c'è già (HPA + `allostatic_load` + body).
Un anello neuromodulatorio c'è già (18 specie, non 5). Un anello di
generazione c'è già (`PromptBundle`). Aggiungere NAC sarebbe
duplicare i tre piani sotto un nome nuovo, con τ in secondi e numpy.
I tre buchi si innestano negli oggetti che esistono: `HPAAxis.rhs`,
`CoreAffect.step`, `derive_policy`.

## 4. Cosa si implementa, e cosa no

### Entra (HYPOTHESIS, readout / drive piccolo, non causa)

1. **Drive ultradiano** su ACTH/cortisolo, periodo ~75 min, ampiezza
   piccola, esposto come `hpa["ultradian"]`. Meccanismo dichiarato:
   stand-in armonico del loop di Walker, **non** la DDE.
2. **`valence_fe` / `fe_accel`** su `CoreAffect`: sidecar Joffily da
   \(-\Delta\mathrm{PE}/\Delta t\). Non scrive `valence`. Non entra in
   `_feature_vector`.
3. **`vigor`** su `RelationalPolicy`: DA tonica + `v_hat` (Niv 2007).
4. **`attention_gain`** a U rovesciata da NE (Aston-Jones). Non
   sostituisce `vigilance`.
5. **`homeostatic_drive`** annotazione da energia / load / vagale già
   presenti. Non sostituisce `allostatic_load`.
6. **Nota** Considerando 44 / C(2025) 884 in RESEARCH.

### Non entra

- NAC.
- `NeuromodulatorySystem` numpy e i suoi τ in secondi.
- `HomeostaticCore` come nucleo.
- I segni decode di Claude (`top_p` che sale con ACh).
- `entropy_bonus`, persona-vector, Backpropamine, Izhikevich, Nengo.
- Fit sesso-specifico 16.4 / 18.5 pulsi/24h.
- Qualunque claim di sentienza.
- Polivagale.

### Compatibilità con i tre piani

L'ultradiano vive *dentro* l'integratore Andersen, come termine
additivo, non al posto dei rate FACT. Joffily vive *dopo* il calcolo
della PE, come lettura. Vigor e attention_gain vivono *dopo* il passo 7,
come annotazioni dell'attuatore. Barrett resta l'unico produttore
dell'etichetta. Panksepp resta l'unico produttore delle occupancy.

## 5. Livelli di confidenza

| Giudizio | Livello | Perché |
|---|---|---|
| Joffily 2013 dice davvero \(v = -\mathrm{d}F/\mathrm{d}t\) | alto | abstract PLOS, citazione verbatim |
| Quel \(v\) è la valenza di Russell | rifiutato / alto sul rifiuto | teorie diverse; il nostro `valence` è circuiti+chimica+corpo |
| Niv 2007 collega DA tonica e vigor | alto | abstract PubMed |
| Walker 2010: pulsi da feedback, non da pulse generator | alto | PMC2871854 |
| Un armonico a 75 min *è* il meccanismo di Walker | basso | è uno stand-in; la DDE è un altro oggetto |
| 16.4 / 18.5 è un fit che dobbiamo riprodurre | rifiutato | deconvoluzione su 143 volontari, non il nostro integratore |
| NAC è speculativa | alto | lo dice l'autore del saggio |
| I decode params di Claude migliorano un LLM | ignoto | nessuna misura; e i segni contraddicono i nostri, già testati |

## 6. Limiti

Non ho riletto integralmente Hesp 2021 oltre DOI/tesi (paywall MIT
Press). Non ho implementato la Table 1 di Joffily come classificatore
(conflitto Barrett). Non ho la DDE di Walker/Churilov. Le magnitudini
ultradiane/Joffily/vigor sono priori esposti per essere falsificati.
