# Valutazione critica di MOSAIC-AI (dono 4)

Il pacchetto non è stato accettato in toto. Ogni claim è stato confrontato
con (i) le fonti primarie, (ii) il codice già presente in
`psych_soma_codex`, (iii) il verbale dei doni 1–3. Il simulatore
`mosaic_ai.py` **non entra nel repository**.

Data di valutazione: 13 agosto 2026.
Materiali valutati:

1. *Dalla neurochimica umana a un'architettura generativa affettiva
   riproducibile / Proposta MOSAIC-AI* (ChatGPT, 33720 byte, 490 righe,
   `/home/user/uploaded_files/ricerca_mosaic_ai ChatGPT.md`).
2. `mosaic_ai ChatGPT.py` (17225 byte, 477 righe) — simulatore
   deterministico stdlib-only. **Non si importa.**

## Sintesi esecutiva

È la specifica ingegneristica più pulita dei quattro doni: stdlib,
deterministico, tabella L0/L1/L2, caveat di equifinalità, niente
sentienza, niente uso clinico, Hsueh 2023 usato nel segno giusto,
NE a U rovesciata, self-test di ordine temporale. Ma è un **organismo
L1 concorrente**, non una patch. Questo repository è già un organismo
più biologicamente nominato: tre piani, 18 specie, 7 circuiti Panksepp,
miscela Barrett, bond per-agente, OT gated, HPA Andersen in µg/dL, RK4
a `dt = 0.05 min`. Importare `MosaicEngine` collasserebbe i piani A e C
in 17 proxy adimensionali e un `tanh` di valenza omeostatica. La luce
nuova che non era già nel dono 3 è una sola, e si innesta in tre righe:
il gate moltiplicativo corpo × contesto rischioso (Hsueh et al. 2023
*Nature* 615:292–299). L'`attention_gain` a U rovesciata è più onesta
del lineare di Claude e si prende insieme al vigor di Niv. Tutto il
resto — cascata HPA inventata, `drive()` come sostituto di
`allostatic_load`, i dieci `GenerativeControls` come blocco, FiLM/LoRA,
i tre scenari, il file Python — resta fuori.

Confidenza complessiva: alta sul rifiuto di importare il motore; alta
sull'accettazione del gate Hsueh (abstract + testo Nature verificati);
media sulle magnitudini del gate e della U-rovesciata.

## Domanda di questa valutazione

MOSAIC è un soprainsieme, un sottoinsieme, o un concorrente? E, dei
pezzi che propone, quali sopravvivono al confronto con un organismo che
ha già Panksepp, Barrett e Andersen?

## 1. Cosa c'è già, e perché è il metro

Oltre al metro dei doni 1–3: `InteroceptiveBody.arousal()` e
`valence_body()` alimentano già `CoreAffect`, ma **senza** un termine
moltiplicativo corpo × minaccia. `EventInputs` di MOSAIC (threat,
novelty, reward, expected_reward, expected/unexpected uncertainty,
controllability, safety, social_salience, affiliation, rejection, pain,
effort, …) è coperto, sotto altri nomi, da `RelationalEvent` +
`EVENT_WEIGHTS` + `LearningState`. MOSAIC **non** ha circuiti Panksepp,
**non** ha la miscela Barrett, **non** ha bond per-agente, **non** ha
il gate OT in-group, **non** ha cortisolo in µg/dL. Il suo self-test
verifica solo ordinamenti di picco (DA dopo reward; NE/adrenalina prima
del cortisolo; OT dopo affiliazione) — segni che questo repo testa già
in forma più stretta (`tests/test_falsifiable.py`).

## 2. Verifica delle fonti primarie usate come metro

### 2.1 Hsueh et al. 2023 — FATTO sul claim, IPOTESI sul gate

Hsueh, B. et al. (2023), *Cardiogenic control of affective behavioural
state*, *Nature* 615:292–299 (PMID 36859543, PMC9995271,
DOI 10.1038/s41586-023-05748-8). Abstract e testo principale riletti il
13 agosto 2026. Claim verificato alla lettera:

> optically evoked tachycardia potently enhanced anxiety-like behaviour,
> but crucially only in risky contexts

L'insula posteriore media l'effetto. RTPP: il pacing *non* è
intrinsecamente avversivo. MOSAIC lo implementa come

```
contextual_body_alarm = interoceptive_arousal * (0.15 + 0.85 * threat)
```

È il pezzo più difendibile del dono. Nel repo il contesto rischioso
*esiste già* come occupancy FEAR (e come `EventKind.THREAT`). Non serve
un nuovo campo `interoceptive_arousal` sugli eventi: si moltiplica
`body.arousal()` per un fattore di FEAR, in `CoreAffect.step`. Esperimento
animale (topo, optogenetica): la generalizzazione all'umano e a un
organismo simbolico è HYPOTHESIS, e va taggata così.

### 2.2 Aston-Jones & Cohen 2005 — U rovesciata

Già nel verbale Claude. MOSAIC scrive
`gaussian_optimum(NE, optimum=0.46, width=0.28)` e la chiama
`attention_gain`. Più onesta del `1 + 1.5·NE` lineare di Claude.
Entra come annotazione, non al posto di `vigilance`.

### 2.3 Keramati & Gutkin 2014 — già pista; `drive()` è un concorrente

`MosaicEngine.drive() = √Σ w_i (h − h*)²` su energy/safety/affiliation
è la formula di Keramati. Il repo ha `allostatic_load`. Sostituire
l'uno con l'altro è un reset del piano B. Un sidecar
`homeostatic_drive` calcolato su energia / load / vagale *già presenti*
è l'unica forma accettabile (stesso verdetto del dono 3).

### 2.4 Churilov & Milton 2022 / Kim, D'Orsogna & Chou 2016 — stessa famiglia di Walker

DDE impulsive per HPA pulsatile. Fonti reali. Il prototipo MOSAIC
**non le implementa**: implementa una cascata leaky CRH→ACTH→cortisolo
verso target sigmoidi, circadiano `0.04·sin(2π t / 86400)`, **senza**
rate Andersen, **senza** µg/dL, **senza** ritardo. È un HPA inventato,
come quello del Gemini (dono 1), solo più onesto sulle unità
(dichiara i proxy adimensionali). Non sostituisce Andersen. L'ultradiano
che accettiamo viene da Walker via dono 3, non da questa cascata.

### 2.5 Yu & Dayan, Schultz, Miyazaki, Handlin, Nummenmaa, Allen 2022

- Yu–Dayan, Schultz: già costitutivi.
- Miyazaki et al. 2018 (*Nat Commun* 9:2048): 5-HT e pazienza
  contestuale. Compatibile col dibattito Dayan–Huys già taggato DEBATE.
  Non si cambia il ruolo della 5-HT in questo giro.
- Handlin et al. 2023 (*eLife* 12:e81197): OT contestuale. Il repo ha
  già il gate in-group su OT. Citazione utile, non codice nuovo.
- Nummenmaa et al. 2014 (*PNAS* 111:646–651): mappe corporee. Già
  allineato a Barrett (distribuzioni, non impronte). Non si implementa
  una mappa somatica nuova.
- Allen et al. 2022 (*PLoS Comput Biol* 18:e1010490): POMDP
  interocettivo. Pista, non runtime (FEP pieno già escluso).

### 2.6 FiLM / AdaLN / LoRA / Backpropamine

Perez et al. 2018; Hu et al. 2021; Miconi ICLR 2019. Meccanismi reali
di condizionamento. Questo repo è zero-dep e non ha un Transformer.
Restano piste (v) di RESEARCH.

## 3. Il simulatore come organismo concorrente

Superficie di `mosaic_ai.py` (non si copia):

| Oggetto MOSAIC | Oggetto repo | Rapporto |
|---|---|---|
| 17 proxy adimensionali | 18 specie nominate + 7 circuiti + bond | MOSAIC è più povero |
| Euler `dt ∈ (0, 1]` secondi | RK4 `dt = 0.05` min | scale diverse |
| HPA leaky verso sigmoidi | Andersen h1/h2/h3, C in µg/dL | MOSAIC è inventato |
| `valence = tanh(18·r_homeo + 0.80·rpe + …)` | Russell da circuiti+chimica+corpo | formule concorrenti |
| niente Panksepp | 7 occupancy | MOSAIC collassa A |
| niente Barrett | miscela su CONCEPTS | MOSAIC collassa C |
| `GenerativeControls` (10 knobs) | policy + decode + Doya | sovrapposizione parziale |
| `top_p = 0.90 + 0.08·expl − 0.22·arousal` | `top_p = 0.94 − 0.22·5HT − 0.16·CORT` | **segni diversi** |
| 3 scenari + self-test qualitativo | 38+ test di segno e ordine | il repo è più stretto |

Il self-test di MOSAIC è onesto e piccolo. Non è una validazione del
*nostro* organismo, e non è una ragione per sostituirlo.

Equifinalità (saggio §8.3): «se un modello latente generico predice
ugualmente bene, il nome biologico non è giustificato». Principio
accettato come disciplina, già implicito nei tag FACT/CONSENSUS/
HYPOTHESIS. Non richiede codice.

## 4. Claim per claim

| Claim | Esito | Perché |
|---|---|---|
| Niente dizionario molecola → emozione | ACCETTARE come cornice | Già il contratto del repo. |
| Tabella L0 / L1 / L2 | ACCETTARE come pedagogia | L1 è dove stiamo; L2 è Andersen (già più L2 del loro L1). Non si adotta la tabella come architettura. |
| Stato, non etichetta | ACCETTARE | Già Panksepp occupancy + Barrett mixture. |
| Molti-a-molti, più scale, contesto | ACCETTARE come cornice | Già costitutivo. |
| Proxy ≠ concentrazione | ACCETTARE | Le 18 specie sono occupancy; il cortisolo Andersen è l'eccezione nominata (µg/dL). |
| MOSAIC-AI come architettura a 8 moduli | RIFIUTARE come sostituto | Event encoder / world model / generative core / meta-controller non esistono e non si inventano in questo giro. I moduli 2–4 (body, neuromod, affect) *esistono già* sotto altri nomi. |
| `MosaicEngine` + `EventInputs` + 17 state vars | RIFIUTARE | Organismo concorrente. Collassa A e C. |
| Cascata HPA leaky + `0.04·sin` | RIFIUTARE | Non Andersen. Non µg/dL. Non ritardo. |
| `drive()` Keramati come ricompensa primaria | RIFIUTARE come sostituto; annotazione sì | Vedi dono 3. |
| Valenza `tanh(18·homeostatic_reward + …)` | RIFIUTARE | Concorre con Russell/Panksepp. |
| Gate Hsueh `body × (0.15 + 0.85·threat)` | ACCETTARE, ritagliato | Moltiplicare `body.arousal()` per FEAR, in `CoreAffect`. Niente nuovo campo evento. |
| `gaussian_optimum` → `attention_gain` | ACCETTARE come annotazione | Più onesta del lineare di Claude. Non tocca vigilance. |
| `GenerativeControls` come blocco (plasticity_gate, memory_write_gate, threat_retrieval_bias, interrupt_sensitivity, …) | RIFIUTARE come dump | `T` e `top_p` ci sono già. `memory_decay` copre parte di memory_write. I restanti sono piste di decode, non un dataclass da copiare. |
| `top_p` che scende con arousal / sale con exploration | RIFIUTARE i segni | I nostri segni (5-HT, cortisolo) restano. |
| FiLM / AdaLN / LoRA condizionati | PISTA | Zero-dep; niente Transformer. |
| Sei esperimenti falsificabili (§9) | ACCETTARE come programma | Specie esp. 2 (corpo × contesto) diventa un test di questo giro. Gli altri restano piste. |
| Equifinalità / identificabilità | ACCETTARE come disciplina | Docs, non codice. |
| Niente sentienza, niente clinico | ACCETTARE | Contratto. |
| Allen 2022 POMDP, Miyazaki 2018, Handlin 2023 | CITAZIONI / piste | Non runtime. |
| Importare `mosaic_ai.py` nel repo | RIFIUTARE | Vincolo esplicito di questa valutazione e della richiesta utente («il giudizio è il tuo»). |

### Steelman di MOSAIC

La versione più forte: *«Il vostro organismo è un L2 nominato e
sotto-identificato. Il nostro L1 è più onesto (proxy, non µg/dL ovunque),
più piccolo, più testabile contro un latente innominato, e ha il gate
Hsueh che voi non avete. Dovreste *sostituire* il nucleo con MosaicEngine
e tenere Panksepp/Barrett come readout, non come produttori.»*

Contro: l'onestà dimensionale di MOSAIC è reale, ma il nostro HPA
Andersen *è* L2 su un sottoinsieme (rate FACT, unità dichiarate), e le
occupancy delle altre specie sono già dichiarate proxy. Invertire
produttore e readout — fare di Panksepp un'etichetta sopra 17 leaky
tanks — è esattamente il collasso che il repo è stato scritto per
rifiutare (Barrett 2017 contro i natural kind; Panksepp 2010 contro
l'affetto come solo core affect). Il gate Hsueh e la U-rovesciata non
hanno bisogno di quel collasso: si innestano in `CoreAffect` e in
`derive_policy`.

## 5. Cosa si implementa, e cosa no

### Entra (HYPOTHESIS, ritagliato)

1. **Gate Hsueh** in `CoreAffect.step`: contributo extra di
   `body.arousal()` all'arousal (e una piccola spinta negativa alla
   valenza) *moltiplicato* per l'occupancy FEAR. A FEAR ≈ 0 il passo è
   identico a prima (nessuna regressione). Tag: Hsueh et al. 2023.
2. **`attention_gain`** a U rovesciata da NE, insieme al vigor di Niv
   (dono 3). Helper `gaussian_optimum` in `core/mathutil.py`.
3. **Citazioni** Hsueh 2023, Churilov 2022, Kim 2016, Handlin 2023,
   Miyazaki 2018, Allen 2022, Perez 2018, principio di equifinalità,
   in RESEARCH. Non il codice di MOSAIC.

### Non entra

- `mosaic_ai.py`, `MosaicEngine`, `EventInputs`, `NeuroAffectiveState`,
  `GenerativeControls`.
- La cascata HPA inventata e il circadiano `0.04·sin`.
- La valenza `tanh` omeostatica.
- `drive()` come sostituto di `allostatic_load`.
- I segni decode di MOSAIC.
- FiLM / AdaLN / LoRA runtime.
- I tre scenari e il self-test come «golden traces» di *questo* repo.
- Qualunque claim di sentienza o uso clinico.

### Compatibilità con i tre piani

Hsueh vive *dentro* il passo 5 (core affect), come termine extra
gated da FEAR (passo 3). Non tocca il costruttore (passo 6). Non tocca
Andersen (passo 4). Non introduce un `interoceptive_arousal` sugli
eventi (passo 1).

## 6. Livelli di confidenza

| Giudizio | Livello | Perché |
|---|---|---|
| Hsueh 2023: tachicardia → anxiety-like solo in contesto rischioso | alto | Nature / PubMed, testo principale |
| Quel claim si trasferisce 1-1 a un organismo simbolico gated da FEAR | basso–medio | topo, optogenetica; FEAR ≠ «risky context» sperimentale |
| MOSAIC è un L1 concorrente, non un soprainsieme | alto | ispezione del file: 0 circuiti, 0 Barrett, 0 µg/dL |
| I rate HPA di MOSAIC sono Andersen | rifiutato / alto | numeri e forma diversi |
| Equifinalità è un rischio reale | alto | consenso di system identification; il saggio lo formula bene |
| I dieci GenerativeControls migliorano un LLM | ignoto | nessuna misura; dump rifiutato |

## 7. Limiti

Non ho eseguito `mosaic_ai.py --self-test` dentro questo repository
(non si importa). Non ho riletto integralmente Churilov 2022 oltre DOI
e tesi. Non ho dati WESAD/DEAP su cui fare l'esperimento 2 del saggio
nella forma umana: il test che aggiungiamo è la versione *interna*
(stesso `body.arousal()`, FEAR alto vs basso).
