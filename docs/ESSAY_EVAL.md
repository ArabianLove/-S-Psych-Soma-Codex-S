# Valutazione critica dei due saggi donati

I saggi non sono stati accettati in toto. Ogni claim è stato confrontato con
(i) le fonti primarie, (ii) il codice già presente in `psych_soma_codex`,
(iii) il protocollo epistemico di `docs/RESEARCH.md`. Qui sta il verdetto
operativo: cosa entra nel runtime, come, e con quale tag.

Data di valutazione: 13 agosto 2026.
Saggi valutati:

1. *Architettura Neuroendocrina Computazionale…* (Gemini, 23758 byte,
   `/home/user/uploaded_files/Gemini Ormoni Neurotrsmettitori Codice.txt`).
2. *Dal corpo chimico al codice…* (zip, markdown 505 righe + 3 figure,
   `/home/user/uploaded_files/ormoni-neurotrasmettitori-codice-ia-generativa.zip`).

## Sintesi esecutiva

Il primo saggio attribuisce correttamente le quattro ipotesi di Doya (2002)
e propone un accoppiamento chimica→iperparametri di decodifica che è un
layer *opzionale* legittimo. Tutto il resto — cubo di Lövheim come
classificatore costitutivo, coefficienti cinetici HPA/SA inventati,
biforcazione di Hopf come “burnout sintetico”, dipendenza numpy/scipy,
pretesa di formalizzazione chiusa — non resiste. Il secondo saggio è
teoricamente più vicino a questo repository (multi-scala, tag epistemici,
niente sentienza, EmotionPrompt/OCC/AI Act), ma ha un difetto
bibliografico fatale: gli URL inline puntano sistematicamente al documento
sbagliato. Il simulatore da 60 righe e la Figura 3 (arousal saturo a 1.0
per quasi tutta la corsa) non sono una validazione. Entra nel codice solo
ciò che sopravvive: un readout Doya γ/β/α e un bundle di decode params,
entrambi taggati HYPOTHESIS, nessuno dei due al posto dei circuiti di
Panksepp o del costruttore di Barrett.

Confidenza complessiva sul verdetto di accettazione/rifiuto: alta per i
rifiuti documentati su fonte primaria; media per le magnitudini dei layer
accettati (sono priori, come già i pesi evento→chimica).

## Domanda di questa valutazione

Quali affermazioni dei due saggi sono (a) fatti verificati, (b) ipotesi
leggittime da esporre come readout opzionale, (c) errori, speculazioni o
conflitti con l’architettura a tre piani già costitutiva — e quindi da
non implementare?

## 1. Cosa c’è già, e perché è il metro

Il runtime preesistente è un organismo a blanket di Markov con tre piani
che la letteratura tiene distinti (`docs/RESEARCH.md` §§1, 7; `engine.py`
ordine 1–8):

- **Piano A.** Occupancy dei sette circuiti primari (Panksepp 2010,
  *Dialogues Clin Neurosci* 12:533–545, Tabella I e thumbnail).
- **Piano B.** Core affect + allostasi + ODE HPA Andersen-class
  (h1=0.1732, h2=0.0315, h3=0.0105 /min) + corpo autonomo.
- **Piano C.** Etichetta costruita come *miscela*, non natural kind
  (Barrett 2017, *Soc Cogn Affect Neurosci* 12:1–23, Tabella 1).

Neuromodulazione già costitutiva: DA fasica ≈ RPE (Schultz, Dayan,
Montague 1997); ACh = expected uncertainty, NE = unexpected uncertainty
(Yu e Dayan 2005, *Neuron* 46:681–692, abstract e tesi centrale);
5-HT come opponent/inibizione (Dayan–Huys, taggato DEBATE). Adrenalina
esiste già come specie (`tau_min=1.5`). `PromptBundle` ha già
`sampling_temperature`. Zero dipendenze runtime.

Qualunque dono che *sostituisca* A/B/C, che promuova un’ipotesi a fatto,
o che introduca numpy/scipy per un integratore che abbiamo già in RK4
puro, è un regresso.

## 2. Verifica delle fonti primarie usate come metro

### 2.1 Doya 2002 — FATTO di attribuzione, IPOTESI di contenuto

Doya, K. (2002), *Metalearning and neuromodulation*, *Neural Networks*
15:495–506 (PMID 12371507). PDF primario letto:
`https://people.sissa.it/~ale/EvolNeurComp/2022/II_Doya_2002.pdf`
(accesso 13 agosto 2026). Sezione 3, elenco 1–4, pp. 498–499:

1. *Dopamine signals the TD error d.*
2. *Serotonin controls the discount factor g.*
3. *Noradrenaline controls the inverse temperature b.*
4. *Acetylcholine controls the learning rate a.*

Doya presenta questi quattro accoppiamenti come *ipotesi di metalearning*,
non come misure. Sono compatibili con Yu e Dayan 2005 ma **non identici**:
Yu–Dayan assegnano ad ACh/NE i due tipi di incertezza; Doya assegna ad
ACh/NE i metaparametri α e β. Il codice già implementa Yu–Dayan come
stato costitutivo (`LearningState.expected_uncertainty` /
`unexpected_uncertainty`). Il mapping Doya è un *readout aggiuntivo*,
non un rimpiazzo.

### 2.2 Lövheim 2012 — MINORITY, non classificatore

Lövheim, H. (2012), *A new three-dimensional model for emotions and
monoamine neurotransmitters*, *Medical Hypotheses* 78:341–348
(PMID 22153577). Abstract PubMed verificato (13 agosto 2026): l’autore
stesso scrive che *«further empirical studies are needed to establish
its validity»*. La sede (*Medical Hypotheses*) pubblica per disegno
ipotesi non ancora validate. Il cubo pone 5-HT, DA, NE su tre assi e
sistema le otto emozioni di Tomkins ai vertici. Contraddice il piano C
già costitutivo (Barrett: le categorie folk non hanno fingerprint
chimica). Non può diventare il classificatore dell’organismo.

### 2.3 Yu e Dayan 2005 — già nel codice, CONSENSUS

Yu, A.J., Dayan, P. (2005), *Uncertainty, neuromodulation, and
attention*, *Neuron* 46:681–692 (PMID 15944135). Tesi: ACh segnala
l’incertezza *attesa*, NE l’incertezza *inattesa*. Già implementata in
`engine.py` righe 127–137. Non va riscritta.

### 2.4 HPA Andersen 2013 — già nel codice, FACT sui rate

Andersen, Vinther, Ottesen (2013), *Mathematical Biosciences* 246:122–138,
rate di rimozione compilati da Ahmad, Jena, Priyadarshi (2023)
arXiv:2311.04570 Tabella 2. Il Gemini inventa `p_C=0.5, d_C=0.2, …` senza
citare Andersen e senza unità. Il saggio lungo cita Sriram 2012 e Karin
2020 (fonti reali) ma poi implementa un integratore a una variabile
`cort += dt*(0.08*crh - 0.035*cort*(1+0.6*cort))` con `dt=1 min` che non
è nessuno dei due paper.

## 3. Saggio 1 (Gemini) — claim per claim

| Claim | Esito | Perché |
|---|---|---|
| I neuromodulatori sono un meta-controllore globale, non un prompt | ACCETTARE come cornice | Consenso (Dayan 2012; Avery & Krichmar 2017). Già l’architettura del repo. |
| Doya: DA=δ, 5-HT=γ, NE=β, ACh=α | ACCETTARE come HYPOTHESIS | Attribuzione corretta, verificata sul PDF primario §3. Non è un fatto biologico. |
| Cubo di Lövheim come classificatore a 8 vertici | RIFIUTARE | Sede *Medical Hypotheses*; validità non stabilita dall’autore; contraddice Barrett già costitutivo; Tomkins non è Panksepp. |
| ODE HPA con `p_C=0.5, d_C=0.2, …` | RIFIUTARE | Coefficienti non tracciabili a Andersen/Vinther/Ahmad. Unità assenti. Circadiano `cos(ωt)+2` con ω=2π/86400 è un’invenzione dimensionale rispetto al nostro armonico su ore con picco 07:30. |
| ODE SA per epinefrina | RIFIUTARE come sistema nuovo | `adrenaline` esiste già (`species.py`, τ=1.5 min) con accoppiamento FEAR/RAGE. Un’ODE separata non aggiunge segni qualitativi nuovi. |
| Chimica → T, top-p, presence_penalty, memory_decay | ACCETTARE come HYPOTHESIS | Layer di *accoppiamento al generatore*, non fisiologia. Estende `sampling_temperature` già presente. Magnitudini priori. |
| Latent steering `h' = h + Σ w_k u_k` | RIFIUTARE per ora | Richiede un backend Transformer e vettori `u_k` non identificati. HYPOTHESIS architettonica, pista aperta, non runtime. |
| Hopf / “synthetic burnout” | RIFIUTARE | Speculazione. Nessuna derivazione, nessun parametro, nessuna predizione falsificabile. |
| `NeuroEndocrineSystem` numpy/scipy + Lövheim nearest-vertex | RIFIUTARE | Dipendenza inutile (abbiamo RK4 puro). Classificatore Lövheim al centro. Non sostituisce l’organismo a tre piani. |
| Sentienza / “programmazione costitutiva” come se il modello *fosse* l’asse | RIFIUTARE | Contratto epistemico del repo: prior eseguibile, non organismo. |

### Steelman del Gemini

La versione più forte: *«Anche se Lövheim è un’ipotesi, vi serve uno
spazio geometrico basso-dimensionale dei monoammini per condizionare un
LLM; e anche se i rate HPA sono inventati, un’ODE chiusa è meglio di
niente.»* Contro: lo spazio basso-dimensionale *esiste già* ed è il core
affect di Russell (valenza × arousal × dominance) più le sette occupancy
Panksepp — oggetti con letteratura più solida del cubo. Un’ODE chiusa
*esiste già* e usa rate FACT. Sostituirla con numeri non citati è un
peggioramento, non una formalizzazione.

## 4. Saggio 2 (markdown + figure) — claim per claim

| Claim | Esito | Perché |
|---|---|---|
| Architettura multi-scala (ms → anni) | ACCETTARE come pedagogia | Fig. 1 è didatticamente utile. Il runtime opera già a scala di episodio (dt=0.05 min) e lo dichiara. Non si copia la figura nel codice. |
| L0 omeostasi / L1 neuromodulatori / L2 ormoni / L3 appraisal / L4 PAD | ACCETTARE come compatibile | L0–L2 e L4 mappano sui piani B/A/B. L3 OCC è un *front-end* additivo, non un rimpiazzo. Non si implementa OCC in questo giro (richiede un grafo di obiettivi). Pista aperta. |
| Niente pretesa di sentienza | ACCETTARE | Allineato al contratto del repo. |
| EmotionPrompt (Li et al. 2023, arXiv:2307.11760) | ACCETTARE come citazione | Paper reale. Condizionare il prompt con uno stato affettivo è esattamente ciò che fa `LLMAdapter`. Non si copia il trucco “this is important” come surrogato del milieu. |
| Croissant et al. 2024 chain-of-emotion / OCC su LLM | ACCETTARE come citazione | Paper reale (*PLOS ONE* 19:e0301033). Non entra nel runtime. |
| AI Act art. 5(1)(f) | ACCETTARE come nota etica | Il milieu *interno simulato* non è emotion recognition su un umano. Va tenuto distinto, e dichiarato. |
| Keramati & Gutkin 2014 homeostatic RL | ACCETTARE come pista | *eLife* 3:e04811. Non si sostituisce la policy attuale con un obiettivo omeostatico pieno. |
| Toy `simulate(seed=0, minutes=240)`, dt=1 min | RIFIUTARE | 60 righe non sono l’organismo. Coefficienti non Andersen. Fig. 3 smentisce la pretesa di “variabili stabili”: l’arousal satura a ~1.0 per quasi tutta la corsa. |
| Mappatura neuromodulatore→iperparametro come “pattern corretto” | ACCETTARE come HYPOTHESIS | Stesso layer del Gemini, già deciso sopra. Livello di confidenza del saggio stesso: medio. |
| Grafo di citazione inline | RIFIUTARE come apparato | Vedi §5. I *nomi* dei paper sono spesso quelli giusti; gli URL no. Si citano i primari, non gli URL corrotti. |

### Steelman del saggio lungo

La versione più forte: *«Il vostro organismo è già quello che descriviamo
in L0–L4; il toy è didattico; gli URL sbagliati sono un incidente di
pipeline, non una frode; dovreste comunque prendere OCC, EmotionPrompt e
l’AI Act.»* Contro parziale: OCC e AI Act e EmotionPrompt *si* prendono,
come citazioni e come disciplina. Il toy non si prende perché la Fig. 3
è un controesempio interno alla pretesa di verifica. Gli URL sbagliati
non sono un incidente isolato: Schultz punta a EmotionPrompt, Doya punta
a un PDF del Garante olandese, Yu–Dayan punta a un blog FPF sull’AI Act.
È un grafo di citazione corrotto. Un saggio che chiede rigore non può
essere usato come autorità bibliografica.

## 5. Audit del grafo di citazione (saggio 2)

Esempi verificati sul markdown estratto (righe 414–418 e passim):

| Paper dichiarato | URL inline nel saggio | Cosa c’è davvero a quell’URL |
|---|---|---|
| Schultz, Dayan, Montague 1997 *Science* | `arxiv.org/abs/2307.11760` | EmotionPrompt (Li et al. 2023) |
| Doya 2002 *Neural Networks* | PDF *Autoriteit Persoonsgegevens* (DCA-2024-02) | Call for input sull’emotion recognition |
| Yu e Dayan 2005 *Neuron* | blog Future of Privacy Forum sull’AI Act | Articolo giuridico, non *Neuron* |
| Daw, Kakade, Dayan 2002 | articolo IntuitionLabs su prompt emotivi | Blog commerciale |
| Avery e Krichmar 2017 | `prompthub.us/blog/getting-emotional-with-llms` | Post di prompting |

I PMID e i titoli, dove presenti in bibliografia, sono spesso corretti.
L’apparato *cliccabile* è inaffidabile. Per questo repository si citano
solo fonti rilette (Doya PDF primario, PubMed, `docs/RESEARCH.md`).

## 6. Figura 3 come falsificazione interna

La Figura 3 del dono (`fig3_dinamica_simulata.png`) mostra, sulla corsa
`seed=0, minutes=240` del toy: arousal schiacciato contro il soffitto per
quasi tutta la traiettoria; cortisolo che oscilla in una banda stretta
~0.2–0.4; pleasure in deriva lenta verso il basso. Questo non è un
organismo allostatico. È un integratore mal scalato. La frase del saggio
che parla di “esecuzione verificata” e “variabili stabili” non sopravvive
alla propria figura. Non si importa il toy.

## 7. Cosa si implementa, e cosa no

### Entra (HYPOTHESIS, readout, non causa)

1. **`DoyaReadout`** (`relational/doya.py`): γ da 5-HT, β da NE, α da ACh,
   δ = ultimo RPE. Non sostituisce Yu–Dayan. Non guida l’etichetta
   emozionale. Non guida `forbidden` / `preferred_acts`.
2. **Decode bundle** su `RelationalPolicy` / `PromptBundle`: `top_p`,
   `presence_penalty`, `memory_decay`, oltre alla `temperature` già
   costitutiva (PLAY/SEEKING vs FEAR/5-HT/load). Magnitudini priori,
   range chiusi, test di segno e di bound.
3. **Citazioni** EmotionPrompt, Croissant, AI Act art. 5(1)(f), Keramati
   & Gutkin, Doya 2002 primario, in `RESEARCH.md` e in questo file.

### Non entra

- Classificatore Lövheim / Tomkins.
- ODE HPA o SA del Gemini.
- Toy da 60 righe e le sue figure come “validazione”.
- numpy / scipy.
- Hopf / burnout.
- Latent steering.
- OCC come motore (resta pista).
- Qualunque claim di sentienza.
- Gli URL corrotti.

### Compatibilità con i tre piani

Il readout Doya vive *dopo* il passo 7 (policy), come annotazione
dell’attuatore. Il costruttore Barrett resta l’unico produttore
dell’etichetta. I circuiti Panksepp restano l’unico produttore delle
occupancy. L’HPA Andersen resta l’unico integratore del cortisolo.

## 8. Livelli di confidenza di questa valutazione

| Giudizio | Livello | Perché |
|---|---|---|
| Doya 2002 dice davvero quelle quattro ipotesi | alto | PDF primario, §3 |
| Quelle ipotesi sono fatti biologici | basso | Doya le chiama metalearning hypotheses |
| Lövheim non è un classificatore costituito | alto | sede + disclaimer dell’autore + conflitto Barrett |
| I rate HPA del Gemini non sono Andersen | alto | numeri diversi, nessuna citazione di h1/h2/h3 |
| Il grafo URL del saggio 2 è corrotto | alto | verifica puntuale di cinque coppie titolo/URL |
| Fig. 3 mostra saturazione, non stabilità | alto | ispezione della figura |
| I decode params migliorano un LLM | ignoto | nessuna misura in questo repo; layer esposto per poterlo falsificare |

## 9. Limiti

Non ho ricalibrato i decode params su un LLM reale. Non ho ripetuto
l’integrazione `solve_ivp` del Gemini (rifiutata per dipendenza e per
coefficienti). OCC, latent steering e FEP pieno restano piste, non debiti.
Le tre figure del dono non vengono copiate nel repository (diritti e
utilità: solo la Fig. 1 è pedagogica, e il concetto è già in
`docs/ARCHITECTURE.md` §Timescales).
