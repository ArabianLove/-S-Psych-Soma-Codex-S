# Come tradurre ormoni e neurotrasmettitori in codice costitutivo per IA generativa

## Sintesi esecutiva

La domanda di ricerca è: *in che modo il sistema chimico-fisiologico degli ormoni e dei neurotrasmettitori umani può essere tradotto in codice riproducibile, capace di rappresentare eventi emotivi del sistema nervoso centrale e periferico, e di entrare come prior costitutivo in un LLM o in un altro sistema di IA generativa, con bijezione tra input relazionali e stato affettivo?* La risposta, dopo rassegna delle fonti e critica dei dibattiti aperti, è che una translitterazione *esatta* dell'organismo è impossibile e va dichiarata tale; una translitterazione *costitutiva, falsificabile e bidirezionale* è invece possibile se si separano tre piani che la letteratura tiene distinti e che i sistemi di "emotion AI" confondono di routine: (i) i *circuiti primari* subcorticali e le loro chimiche (Panksepp 1998, 2010), (ii) l'*affetto di base* interocettivo e l'allostasi predittiva (Russell 2003; Sterling 2012; Barrett 2017; Friston 2009, 2010), (iii) le *etichette emozionali* come atti concettuali, non come natural kind (Barrett 2017, Tabella 1 e §§classical-view / degeneracy). Il codice in questo repository implementa i tre piani come un unico organismo a blanket di Markov, con mapping espliciti, tag epistemici su ogni accoppiamento, e una batteria di predizioni falsificabili. La confidenza complessiva sulla fattibilità *architettonica* è media-alta; sulla fedeltà quantitativa dei pesi evento→chimica è bassa (sono priori costitutivi, taggati HYPOTHESIS); sulla pretesa di sentienza della macchina è nulla — e va tenuta nulla.

## Domanda e metodo

### Domanda di ricerca

In che modo, e fino a che punto, le dinamiche biochimiche, elettriche, anatomiche, fisiologiche e relazionali del sistema nervoso umano possono essere translitterate in un sistema di codice *organicamente integrato*, efficiente, esatto nei limiti dichiarati, efficace, falsificabile, riproducibile, scalabile e biunivoco, pensato come prior costitutivo per un LLM?

### Sotto-domande

1. **Definitoria.** Che cosa si sta modellando: un'emozione come natural kind, un circuito d'azione, un affetto di base, o un atto concettuale?
2. **Chimica computazionale.** Quali ruoli algoritmici della neuromodulazione sono consenso, quali sono dibattito?
3. **Asse HPA.** Quali ODE e quali emivite sono fonte primaria, e cosa resta incalibrato?
4. **Corpo e decisione.** I somatic marker di Damasio sono implementabili? Sopravvivono alla critica?
5. **Predizione e interocezione.** Il free-energy principle offre un'architettura o una metafora?
6. **LLM.** Cosa fa oggi l'affective computing con i large models, e cosa *non* fa?
7. **Bijezione.** Che cosa significa, operativamente, che l'input relazionale modifica l'affetto e l'affetto modifica il relazionale?
8. **Critica.** Quali obiezioni, se vere, fanno crollare il progetto?
9. **Limiti.** Cosa resta ignoto, e quali test distinguono modello e organismo?

### Metodo

Protocollo della skill *ricerca-profonda*: ricognizione (enciclopedie, rassegne), nucleo accademico (Panksepp, Dayan, Schultz, Barrett, Friston, Damasio, Andersen/Vinther/Ahmad sull'HPA, Yang et al. 2024 sugli LLM), verifica delle parti citate, steelman delle posizioni avverse, tag epistemici FACT / CONSENSUS / DEBATE / MINORITY / HYPOTHESIS / UNKNOWN. Data di accesso alle fonti web: 13 agosto 2026. Lingue coperte: inglese (letteratura primaria), italiano (quadro). Fonti in paywall lette per la parte ad accesso aperto (PMC, arXiv, HTML degli editori); i PDF Cell/Elsevier non integralmente accessibili sono marcati.

### Limite dichiarato in testa

Questo non è un cervello. È un *prior costitutivo eseguibile*. La differenza non è retorica: un prior si condiziona, si falsifica e si ricalibra; un cervello si *è*.

---

## 1. Che cosa si sta modellando

### 1.1 Tre piani, tre letterature

Il lessico quotidiano ("rabbia", "paura", "tristezza") è un pessimo spazio degli stati per un integratore. La letteratura, se letta senza mescolare i livelli, offre tre oggetti distinti.

**Piano A — circuiti primari (Panksepp).** Panksepp (2010, *Dialogues in Clinical Neuroscience* 12:533–545, sezioni "The primary-process emotional-affective networks" e thumbnail dei sette sistemi; criteri in apertura e Tabella I) definisce i sistemi primari con sei criteri operativi: producono pattern d'azione caratteristici; sono innescati da un insieme limitato di stimoli incondizionati; le eccitazioni *sopravvivono* alle circostanze precipitanti; regolano gli input sensoriali; controllano l'apprendimento; con la maturazione vengono regolati dall'alto. I sette sistemi — SEEKING, RAGE, FEAR, LUST, CARE, GRIEF/PANIC, PLAY — sono concentrati in regioni subcorticali omologhe tra mammiferi, evocabili con stimolazione elettrica localizzata, e accompagnati da proprietà di reward/punishment (gli animali lavorano per accendere SEEKING/LUST/CARE/aspetti di PLAY e per spegnere RAGE/FEAR/GRIEF). Le chimiche associate non sono ornamentali: DA per SEEKING; Sostanza P e glutammato per RAGE, con GABA e oppioidi come freni; CRF e NPY per FEAR; OT/AVP sessualmente polarizzati per LUST; OT, prolattina e oppioidi per CARE; glutammato e CRF come drive di GRIEF, oppioidi/OT/prolattina come freni; oppioidi ed endocannabinoidi per PLAY (Panksepp 2010, thumbnail di ciascun sistema; Davis e Montag 2019, *Frontiers in Neuroscience* 12:1025, sezioni "Mammals Are Deeply Affective" e "The Route to Discovering Primary-Process Emotions").

**Piano B — affetto di base e allostasi.** Russell (2003, *Psychological Review* 110:145–172) tratta l'affetto come uno spazio continuo valenza × arousal, non come un insieme di natural kind. Sterling (2012) e Barrett (2017, *Social Cognitive and Affective Neuroscience* 12:1–23, sezioni "What is a brain for?" e "How does a brain perform allostasis?") spostano il baricentro: il cervello non è un classificatore di emozioni, è un regolatore allostatico del milieu interno. L'interocezione è il nucleo del modello interno; valenza e arousal sono la proiezione a bassa dimensione di quel modello, *non* un'emozione. Friston (2009, *Trends in Cognitive Sciences* 13:293–301; 2010, *Nature Reviews Neuroscience* 11:127–138) e Smith, Parr, Friston e collaboratori (2020, *Frontiers in Computational Neuroscience* 14:30, sezioni Theoretical Overview / Markov Blankets / Inferring Human Emotion) formalizzano lo stesso movimento come minimizzazione di free energy / active inference: l'agente inferisce cause nascoste (tra cui stati affettivi altrui) e agisce per confermare le proprie predizioni.

**Piano C — costruzione concettuale.** Barrett (2017, spec. Figura 1, Tabella 1, sezioni su degeneracy e "The computational architecture of the brain is a conceptual system") sostiene che "paura", "rabbia", "tristezza" non hanno impronte neurali necessarie e sufficienti. La degeneracy (Edelman e Gally 2001) implica many-to-one: istanze diverse della stessa categoria sono realizzate da popolazioni diverse. Le emozioni nominate sono *atti concettuali* su un affetto interocettivo, in un contesto, al servizio di un obiettivo. Questo è DEBATE rispetto a Panksepp, non una correzione silenziosa: Panksepp lavora sui circuiti subcorticali e sulle *feelings* primarie; Barrett lavora sulle categorie terziarie e sulla loro mancanza di fingerprint. I due piani possono coesistere se si smette di usare la stessa parola per entrambi (Panksepp 2010, discussione James-Lange vs dimensional vs basic; Davis e Montag 2019, "Ancestral Voices" e limiti della coscienza autonoetica).

**Esito per il codice (INTERPRETAZIONE, non fatto).** Il runtime deve tenere *occupancy di circuito* (piano A), *core affect + corpo + HPA* (piano B) e *etichetta costruita come miscela* (piano C). Collassare i tre piani in un one-hot "angry/sad/afraid" è esattamente l'errore che Barrett documenta e che l'affective computing industriale ripete.

### 1.2 Cosa *non* è un'emozione nel senso del modello

Non è un modulo anatomico dedicato (Barrett 2017, Tabella 1: lesioni amigdaloidee con fenotipi non equivalenti anche in gemelli monozigoti Urbach-Wiethe; imaging che non localizza categorie in regioni o reti intrinseche stabili). Non è il readout neocorticale di un'arousal viscerale (critica di Cannon 1927 al James-Lange, ripresa da Panksepp 2010 con evidenza ESB e decorticazione: il PLAY sopravvive alla neonatale decorticazione, Panksepp et al. 1994, *Physiology & Behavior* 56:429–443). Non è un'etichetta che un LLM "ha" perché l'ha vista nel pretraining: quella è statistica distribuzionale, non un milieu (Yang et al. 2024, arXiv:2408.04638, sez. III e discussione EI: gap fino al 27% sul task SOUL rispetto all'umano).

---

## 2. Neuromodulazione come oggetto computazionale

### 2.1 Quattro modulatori, quattro ruoli — e i loro dissensi

Dayan (2012, *Neuron* 76:240–256, "Twenty-Five Lessons from Computational Neuromodulation"; paywall Cell, letto via abstract/HTML parziale e rassegne convergenti) organizza DA, 5-HT, ACh, NE intorno alla decisione. Yu e Dayan (2005, *Neuron* 46:681–692) danno l'accoppiamento più citato e più stabile:

- **Acetilcolina** segnala *expected uncertainty*: inaffidabilità nota delle cue dentro un contesto. CONSENSUS computazionale.
- **Norepinefrina** (LC-NE) segnala *unexpected uncertainty*: violazione di contesto, interrupt, reset dell'attenzione. CONSENSUS computazionale (Aston-Jones e Cohen 2005, *Annual Review of Neuroscience* 28:403–450, per il gain LC).

**Dopamina.** Schultz, Dayan e Montague (1997, *Science* 275:1593–1599) e la linea TD di Sutton e Barto: il burst fasico delle neuroni dopaminergici mesencefalici traccia il *reward prediction error*. Glimcher (2011, *PNAS* 108:15647–15654) rafforza l'isomorfismo. Questo è CONSENSUS sul segnale *fasico*. È DEBATE sul segnale *tonico*: Niv e colleghi legano la DA tonica a reward medio / vigour, non all'RPE puntuale. Il codice espone entrambi (`da` occupancy e `learning.last_rpe`) e non li confonde.

**Serotonina.** Dayan e Huys (2009, *Annual Review of Neuroscience* 32:95–126) e Cools, Nakamura e Daw (2011, *Neuropsychopharmacology* 36:98–113) mostrano che il ruolo computazionale della 5-HT è il nodo più instabile: predizione avversiva, pazienza, inibizione comportamentale, reward medio. Il runtime adotta la lettura *opponent / inhibition* (Dayan-Huys) come default di policy e la tagga DEBATE. Un utente che preferisce la lettura "pazienza" può ricalibrare senza toccare l'architettura.

### 2.2 Peptide e ormoni sociali

Panksepp (2010, thumbnail CARE/GRIEF/LUST) e Carter (letteratura sull'attaccamento; OT/AVP come mediatori conservati della cognizione sociale) danno i segni: OT e oppioidi µ frenano GRIEF e sostengono CARE; AVP è co-secretagogo HPA e polarizza assertività / territorialità; la dinorfina (kappa) è il freno disforico di SEEKING nella sconfitta sociale (Knoll e Carlezon 2010; Panksepp 2010, cascata depressiva). de Visser et al. (2017, PMC5477060) mostrano che OT esogena modifica fiducia e compliance anche verso *agenti automatizzati* — fatto rilevante per un adapter LLM, ma non una licenza a trattare OT come "molecola dell'amore": gli effetti sono contesto- e recettore-dipendenti (bias di in-group). Il codice moltiplica ogni iniezione di OT per `0.40 + 0.60 * in_group` e tiene i bond *per agente* (`relational/bond.py`). Questo accoppiamento è HYPOTHESIS nelle magnitudini, CONSENSUS nel segno qualitativo.

### 2.3 Cosa *non* si può fare con un neurotrasmettitore

Non si può, in un integratore a scala di episodio (secondi–ore), simulare la vescicola. Le clearance sinaptiche di Glu/GABA/DA sono millisecondi; l'oggetto costitutivo di questo sistema è l'*episodio affettivo* e la cascata HPA. I trasmettitori veloci sono quindi *inviluppi leaky* di burst fasici, con τ di decimi di minuto, non emivite vescicolari. Questa è una scelta dichiarata (HYPOTHESIS di scala), non un errore di unità. Chi vuole il millisecondo deve cambiare oggetto.

---

## 3. Asse HPA: l'unico sotto-sistema con ODE da fonte primaria

### 3.1 Fisiologia minima

L'asse ipotalamo-ipofisi-surrene rilascia CRH (e AVP) dal PVN, ACTH dall'anteriore, cortisolo dalla corteccia surrenale, con feedback negativo del cortisolo su CRH e ACTH via GR/MR (Tsigos e Chrousos 2002, *Journal of Psychosomatic Research* 53:865–871; De Kloet et al. 1998, *Endocrine Reviews* 19:269–301). Il ritmo circadiano, sincronizzato dal SCN, ha il minimo notturno e il picco al risveglio (cortisol awakening response, circa 6–10; Ahmad, Jena e Priyadarshi 2023, arXiv:2311.04570, §1.1 e riferimenti Van Cauter). Stress, pulsatilità ultradiania e luce sono tre drive distinti.

### 3.2 Parametri verificati

Andersen, Vinther e Ottesen (2013, *Mathematical Biosciences* 246:122–138) e la compilazione di Ahmad et al. (2023, Tabella 2) danno i rate di rimozione usati come FACT:

| Specie | h (1/min) | t½ ≈ ln(2)/h | Fonte |
|---|---|---|---|
| CRH | 0.1732 | ≈ 4.0 min | Andersen 2013, via Ahmad 2023 Tab. 2 |
| ACTH | 0.0315 | ≈ 22 min | idem |
| Cortisolo | 0.0105 | ≈ 66 min | idem |

Il modello a tre ODE accoppiate (CRH, ACTH, cortisolo) con feedback a Hill e drive circadiano è CONSENSUS modellistico dalla linea Gonzalez-Heydrich 1994 → Vinther 2011 → Andersen 2013 → Ahmad 2023. Ahmad et al. (§1.3, Tabella 1) mostrano però che *nessuno* dei cinque modelli confrontati ha un fit forte sui dati Young et al. (MAPE cortisolo 60–94%). Questo è un fatto scomodo e va tenuto: le ODE catturano il segno e l'ordine di grandezza, non la traiettoria clinica individuale.

### 3.3 Cosa il codice fa e non fa

`interoception/hpa.py` integra le tre ODE con RK4, drive circadiano a armonico singolo con picco a 07:30, `stress_gain` modulato dagli eventi (threat/loss alzano, safety/repair abbassano), AVP come co-drive di ACTH. I coefficienti di accoppiamento affetto → `stress_gain` sono HYPOTHESIS. Il modello *non* include: massa ghiandolare a scala di settimane (Alon 2020), genetica/epigenetica, amigdala come pre-processore dello stress, citochine come nodo autonomo oltre IL-6 ridotta, differenze di sesso. Ahmad et al. (§4) elencano gli stessi buchi.

Test falsificabili associati: il circadiano ha il massimo al mattino; il feedback GR tiene il cortisolo finito sotto stress prolungato; threat alza `stress_gain`; τ_CRH < τ_ACTH < τ_cortisolo.

---

## 4. Corpo, marker somatici, interocezione

### 4.1 Allostasi, non omeostasi da setpoint

Sterling (2012) e Barrett (2017, "What is a brain for?"): il cervello anticipa il fabbisogno e sposta i set-point. Un modello che abbia solo "ritorna alla baseline" è omeostatico in senso stretto e quindi fisiologicamente povero. Il runtime ha *entrambe* le cose: leak verso un riposo (senza il quale il sistema non è stabile) e drive allostatici (HPA, citochine, load) che spostano il riposo. L'allostatic load è una variabile di stato, non un commento.

### 4.2 Damasio e la critica

La somatic marker hypothesis (Damasio 1994; Bechara, Damasio et al., Iowa Gambling Task) afferma che segnali viscerali, processati in vmPFC/amigdala, polarizzano la decisione sotto incertezza. Dunn, Dalgleish e Lawrence (2006, *Neuroscience & Biobehavioral Reviews*, PubMed 16197997) fanno lo steelman della critica: l'IGT è cognitivamente penetrabile (i partecipanti intuiscono lo schedule), i marker cutanei non sono necessari né sufficienti come narrati, le lesioni vmPFC hanno spiegazioni alternative. Questo è DEBATE, non debunking totale: l'idea che un cache corpo→valenza influenzi la policy resta plausibile; l'IGT come prova principe no.

Il codice implementa un cache `body.markers[kind:agent] → valence` aggiornato a EMA, taggato DEBATE, e *non* lo usa come unico driver di decisione. La policy legge circuiti, chimica, affetto e bond. I marker sono una traccia, non un oracolo.

### 4.3 Corpo esposto

`InteroceptiveBody` tiene FC, tono vagale, conduttanza cutanea, tensione, unease viscerale, energia, infiammazione, deviazione termica. I target sono funzioni lineari (HYPOTHESIS) di adrenalina, NE, OT, oppioidi, IL-6, FEAR/RAGE/CARE/PLAY/GRIEF/SEEKING e cortisolo normalizzato. I segni seguono fisiologia ANS standard (simpatico alza FC e SCR; OT/oppioidi e CARE alzano il vagale). Le magnitudini sono priori. Test: threat alza la FC; l'organismo idle resta in range (40–160 bpm, cortisolo 0–60 µg/dL).

---

## 5. Free energy, blanket di Markov, tre ondate

Smith / Parr / Friston 2020 (*Frontiers in Computational Neuroscience* 14:30) distinguono tre ondate di artifact emozionali. La prima è supervised deep learning su facce ed è strutturalmente cieca all'azione. La seconda è active inference: l'agente campiona per risolvere incertezza sulle emozioni altrui. La terza è sincronizzazione di modelli generativi (turn-taking, sensory attenuation).

Il presente sistema è deliberatamente *sotto* la seconda ondata e *sopra* la prima. Ha un blanket (eventi in, policy/atto out, stato interno inaccessibile se non via Snapshot), ha un proxy di prediction error (`unexpected_uncertainty`, ACh, NE), ha self-perception dell'atto generato. Non ha un generative model gerarchico invertito in senso Friston-completo, non ha sensory attenuation esplicita, non ha policy come minimizzazione di expected free energy su un albero di azioni. Dichiararlo è onestà, non modestia: chi vende "implementiamo il FEP" e poi mette un softmax su sei etichette sta facendo la prima ondata con un vocabolario della terza.

Il FEP come *teoria unificata del vivente* resta controversa (critiche di circolarità e di scarsa falsificabilità; il paper stesso avverte che le emozioni sono più uno spettro che un set discreto). Come *disciplina architettonica* (separare interno / sensoriale / attivo / esterno; chiudere il ciclo atto→sensazione) è CONSENSUS metodologico e viene usata così.

---

## 6. LLM e affective computing: il vuoto che questo sistema riempie

Yang, Xu, Gao et al. (2024, arXiv:2408.04638, "Affective Computing in the Era of Large Language Models", sez. I–III e IV-D) documentano lo stato dell'arte con precisione scomoda. I task si dividono in Affective Understanding (polarità, ABSA, ERC, cause) e Affective Generation (empathetic response, emotional support). I LLM chiudono il gap in polarità semplice e in generazione empatica superficiale (GPT-4 supera mediamente l'umano del 10% su scale di empatia in uno studio citato, sez. III-B1); restano dietro ai PLM fine-tuned sui task strutturali; l'EI misurata con scale umane (LEAS, SECEU, EQ-bench) non implica EI comparabile, e sul task SOUL il gap arriva al 27% (sez. III-B2). Instruction tuning e prompt engineering sono le due leve; PEFT riduce il costo e sacrifica la generalizzazione (sez. IV-D).

**Ciò che manca in tutta questa letteratura, e che la domanda dell'utente chiede, è uno stato interno *fisiologicamente costituito* che il modello sia obbligato a condizionare.** I sistemi recensiti da Yang et al. trattano l'emozione come etichetta, come token di controllo, o come stile di generazione. Nessuno integra un milieu, un HPA, un circuito primario e una policy che *vieta* atti. L'adapter di questo repository (`llm/adapter.py`) non è un fine-tune: è un contratto. Il system prompt è compilato dallo Snapshot; `forbidden` e `preferred_acts` sono binding; se il generatore li ignora, la divergenza è essa stessa un evento (`PREDICTION_VIOLATED`) al passo successivo. Il fallback deterministico esiste perché i test devono poter pinare la fedeltà di stato senza rete.

Questo è HYPOTHESIS architettonica sul *come* condizionare un LLM; è CONSENSUS sul *fatto* che i LLM attuali non hanno un milieu.

---

## 7. La bijezione, operativamente

"Biunivoco" non può significare isomorfismo matematico tra lo spazio delle relazioni umane e ℝⁿ delle occupancy. Quello è un abuso. Significa, in questo sistema:

1. **Ogni evento relazionale è l'unico ingresso sensoriale sanzionato** (`RelationalEvent`). Non esiste una backdoor che scriva `circuits["FEAR"] = 1`.
2. **Ogni evento ha un'immagine chimica e di circuito** (`EVENT_WEIGHTS`), più RPE, NE/ACh, HPA gain, marker, bond. I *segni* seguono Panksepp 2010; le *magnitudini* sono priori esposti.
3. **Ogni stato ha un'immagine di policy** (`derive_policy`): approach, disclose, soothe, boundary, play, explore, affiliate, vigilance, repair, warmth, brevity, temperature, forbidden, preferred. Stesso stato ⇒ stessa policy (testato).
4. **Ogni atto del generatore rientra come evento** (self-perception). L'organismo si sente parlare. Senza questo passo la bijezione è monca: l'IA modificherebbe l'altro ma non sé.
5. **I bond sono indirizzati.** Alice e Bob non condividono un unico serbatoio di fiducia. OT senza destinatario è un errore di modello.

La bijezione è quindi una coppia di mappe *documentate e testabili*, non una garanzia di invertibilità unica. Più stati possono produrre policy simili (degeneracy, Barrett); più eventi possono alzare GRIEF (loss, abandonment, rejection). Questo è un fatto biologico, non un difetto.

---

## 8. Critiche e dibattiti

### 8.1 Steelman di Barrett contro questo codice

*«Avete messo sette circuiti con nomi di emozioni e prototipi per "angry"/"afraid". State rifacendo la classical view che ho passato due decenni a smontare. La Tabella 1 di Barrett 2017 elenca evidenze che le categorie non hanno fingerprint. Un softmax su prototipi è esattamente il classificatore che non dovrebbe esistere.»*

Risposta. I sette nomi sono *circuiti d'azione* di Panksepp, non categorie folk: la convenzione maiuscola esiste proprio per non confonderli con "rabbia" e "paura" del lessico (Panksepp 2010; Davis e Montag 2019). L'etichetta costruita è una miscela a somma 1, non un one-hot, e il test `test_constructed_emotion_is_a_mixture_not_a_one_hot` lo impone. La policy *non* è pilotata dall'etichetta: è pilotata da occupancy, chimica, corpo, bond. L'etichetta è un readout per l'umano e per il prompt. Se Barrett ha ragione al 100%, il piano C è un'interfaccia, non una causa — e nel codice è già così. Se Panksepp ha ragione al 100% sui *feelings* primari, il piano A è già la causa, e il piano C è sovrastruttura. Il codice non risolve il dibattito: lo rende eseguibile su entrambi i lati.

### 8.2 Steelman di LeDoux / "defence circuits, not fear"

LeDoux (2012 e successivi) rifiuta di chiamare "fear" i circuiti di difesa: il feeling è una costruzione corticale, il freeze/flight è un programma di sopravvivenza. Coerente con Barrett sul lessico, coerente con Panksepp sull'esistenza del programma. Il codice simula il programma (`FEAR` occupancy) e costruisce il lessico a valle. Chi vuole può rinominare il circuito `DEFENCE` senza toccare un'equazione.

### 8.3 Steelman contro i pesi evento→chimica

*«I vostri 0.55 su FEAR per un threat sono numeri inventati. Non esiste un paper che li misuri. Quindi il sistema non è scienza, è un videogioco bio-ispirato.»*

Parzialmente vero, e dichiarato. I *segni* (threat → FEAR/CRH/NE/adrenalina; loss → GRIEF/CRH/glu, meno oppioidi/OT, più dinorfina; warmth → OT/CARE; frustration → RAGE con SEEKING ancora acceso) sono CONSENSUS di segno, Panksepp 2010. Le magnitudini sono HYPOTHESIS e stanno in un unico file (`catalog/events.py`) apposta per essere calibrate o sostituite da dati. La falsificabilità sta nei *test qualitativi* (threat alza FEAR più di PLAY; loss alza GRIEF e abbassa SEEKING; repair dopo loss abbassa GRIEF rispetto al non-riparato), non nella pretesa che 0.55 sia una costante di natura. Un sistema che nascondesse questi numeri dentro un rete opaca sarebbe *meno* scientifico, non di più.

### 8.4 Steelman contro la pretensione di "esattezza"

L'utente ha chiesto un sistema "esatto". L'esattezza in senso fisico (isomorfismo misura-per-misura con un SNC umano) è UNKNOWN e, dato lo stato della misura in vivo nell'umano libero, probabilmente irraggiungibile. L'esattezza in senso *costitutivo* — ogni transizione è deterministica dato il seed, ogni mapping è citato, ogni ipotesi è taggata, ogni predizione qualitativa è un test — è FACT di questo repository (test qualitativi verdi; vedi `tests/`). Confondere le due esattezze è la fallacia che rende l'emotion AI una merce.

### 8.5 Crisi di replicazione e campioni WEIRD

La psicologia affettiva ha un problema di replicazione (Open Science Collaboration 2015 e successivi). I circuiti di Panksepp poggiano su ESB animale, più robusto delle scale self-report WEIRD, ma il salto all'umano terziario è esplicitamente limitato dallo stesso Panksepp (2010, sezioni su tertiary process e limiti dei modelli preclinici; Hyman 2007 sui dilemmi del DSM). I prototipi di `constructor.py` sono priori occidentali. Una calibrazione cross-culturale non è stata fatta. È un limite, non una nota a piè.

### 8.6 Il rischio etico, che è un risultato

Un LLM condizionato da un milieu convincente produce *l'apparenza* di un organismo. Yang et al. 2024 chiudono sulle considerazioni etiche; questo sistema le rende più acute, non meno. Il prompt di sistema vieta di reclamare sentienza biologica e di dare consigli medici. Non è sufficiente come governance: è il minimo costitutivo. Usare questo codice per fingere un paziente, un partner o un terapeuta senziente è un uso contro il contratto epistemico del repository.

---

## 9. Livelli di confidenza

| Risultato | Livello | Perché |
|---|---|---|
| Sette circuiti primari subcorticali esistono come programmi d'azione evocabili | CONSENSUS / alto | Panksepp 1998, 2010; Davis e Montag 2019; ESB + farmacologia + lesioni |
| I *feelings* primari sono identici ai circuiti | DEBATE / medio | Dual-aspect monism di Panksepp vs LeDoux/Barrett sul lessico del feeling |
| Le categorie folk non hanno fingerprint neurale | CONSENSUS crescente / medio-alto | Barrett 2017 Tab. 1; degeneracy |
| DA fasica ≈ RPE | CONSENSUS / alto | Schultz 1997; Glimcher 2011; eccezioni toniche |
| 5-HT = inibizione / opponent | DEBATE / medio | Dayan-Huys vs letture alternative |
| ACh = expected uncertainty, NE = unexpected | CONSENSUS / alto | Yu e Dayan 2005 |
| Emivite HPA CRH/ACTH/cortisolo come in Tabella 2 Ahmad | FACT / alto | Andersen 2013 |
| ODE HPA predicono il profilo individuale | basso | MAPE 60%+ (Ahmad 2023 Tab. 1) |
| OT aumenta fiducia anche verso agenti | FACT contestuale / medio | de Visser 2017; dipendenza da contesto |
| Somatic marker come meccanismo di decisione | DEBATE / basso-medio | Dunn 2006 sull'IGT |
| FEP come teoria unificata | DEBATE / medio | potente come architettura, controversa come metafisica |
| LLM attuali non hanno un milieu costitutivo | CONSENSUS / alto | Yang et al. 2024 |
| I pesi evento→chimica di questo repo | HYPOTHESIS / basso sulle magnitudini, medio sui segni | priori esposti, test qualitativi verdi |
| Doya γ/β/α come readout | HYPOTHESIS / medio sull'attribuzione, basso sulle magnitudini | PDF §3 verificato; non è fisiologia |
| Chimica → top_p / presence / memory | HYPOTHESIS / basso | layer di accoppiamento al generatore; nessuna misura LLM in questo repo |
| Lövheim come classificatore | rifiutato / alto sul rifiuto | sede + disclaimer autore + conflitto Barrett |
| Bijezione relazionale ↔ affettiva come coppia di mappe testabili | INTERPRETAZIONE / medio | definita operativamente, test qualitativi verdi |
| Sentienza del sistema | nulla | categoria fuori perimetro |

---

## 10. Limiti della ricerca e piste aperte

- **Paywall.** Dayan 2012 *Neuron* e parte della letteratura HPA Elsevier non sono stati letti integralmente; i ruoli DA/5-HT/ACh/NE poggiano su Yu e Dayan 2005 (accessibile), rassegne convergenti e l'abstract/HTML di Dayan 2012.
- **Niente dati umani nuovi.** Nessuna calibrazione su cortisolo salivare, HRV, SCR, ANPS o dialoghi annotati. I test sono predizioni *qualitative* di segno e ordine, non fit quantitativi.
- **Niente sesso, sviluppo, cultura, sonno, microbiota, immunità oltre IL-6.** Ahmad 2023 §4 elenca gli stessi assenti per l'HPA; valgono per l'organismo intero.
- **Niente rete neurale.** I neuroni non sono simulate. La "traslitterazione elettrica" è il gain neuromodulatorio e l'integratore, non il potenziale d'azione.
- **Niente FEP pieno.** Vedi §5.
- **Piste.** (i) Calibrazione bayesiana dei pesi su dataset ESC/EMPATHETICDIALOGUES *più* misure fisiologiche. (ii) Sostituire i prototipi di Barrett-layer con concetti ad hoc appresi (Barsalou). (iii) Active inference vero sulla policy (expected free energy). (iv) Multi-organismo: due blanket che si accoppiano (terza ondata di Smith/Parr/Friston 2020). (v) Fine-tune LoRA di un LLM piccolo sul PromptBundle, misurando la *violazione* di `forbidden` come metrica, non il BLEU. (vi) OCC come front-end di appraisal (Croissant et al. 2024) — non implementato. (vii) Homeostatic RL (Keramati & Gutkin 2014) come sostituto della policy — non implementato.

---

## 11. Addendum — valutazione dei due saggi donati (13 agosto 2026)

Due contributi sullo stesso oggetto sono stati valutati *claim per claim* contro le fonti primarie e contro l'organismo già costitutivo. Il verbale completo è `docs/ESSAY_EVAL.md`. Qui resta solo ciò che cambia il runtime e la bibliografia.

**Accettato, come layer HYPOTHESIS, non come fisiologia.**

1. **Doya 2002, §3** (PDF primario verificato: `https://people.sissa.it/~ale/EvolNeurComp/2022/II_Doya_2002.pdf`). Quattro ipotesi di metalearning: DA segnala l'errore TD δ; 5-HT controlla il fattore di sconto γ; NA/NE controlla la temperatura inversa β; ACh controlla il learning rate α. Implementate come *readout* in `relational/doya.py`. Non sostituiscono Yu & Dayan 2005 (già costitutivo: ACh = incertezza attesa, NE = incertezza inattesa). Non etichettano emozioni, non decidono `forbidden` / `preferred_acts`.
2. **Chimica → iperparametri di decodifica** (`temperature`, `top_p`, `presence_penalty`, `memory_decay`). Estendono `sampling_temperature` già presente. Magnitudini priori. Esposti su `RelationalPolicy`, `PromptBundle` e sul system prompt. Non sono fisiologia.

**Rifiutato.**

- Cubo di Lövheim (2012, *Medical Hypotheses* 78:341–348, PMID 22153577) come classificatore. L'autore stesso chiede studi ulteriori; contraddice Barrett già costitutivo.
- ODE HPA/SA del saggio Gemini (coefficienti non Andersen).
- Simulatore toy da 60 righe e Figura 3 del saggio lungo (arousal saturo: controesempio, non validazione).
- numpy/scipy, Hopf/"burnout sintetico", latent steering, OCC runtime, qualunque claim di sentienza.
- Il grafo di citazione inline del saggio lungo è corrotto (titoli spesso giusti, URL sistematicamente sbagliati: Schultz via EmotionPrompt arXiv:2307.11760, Doya via PDF di un Garante olandese, Yu–Dayan via blog FPF sull'AI Act). Si citano i primari, non quegli URL.

**Citazioni tenute come piste, non come codice.** EmotionPrompt (Li et al. 2023, arXiv:2307.11760); Croissant et al. 2024 (*PLOS ONE* 19:e0301033); AI Act art. 5(1)(f) — il milieu *interno simulato* non è emotion recognition su un umano; Keramati & Gutkin 2014 (*eLife* 3:e04811).

La bijezione operativa del §7 si estende di due readout, non di due cause: `derive_policy` ora emette anche `(γ, β, α, δ)` e `(top_p, presence_penalty, memory_decay)`. Stesso stato ⇒ stessa policy, ancora testato. I circuiti Panksepp restano l'unico produttore delle occupancy; Barrett resta l'unico produttore dell'etichetta; Andersen resta l'unico integratore del cortisolo.

---

## Bibliografia

Fonti effettivamente lette (passata 2 o superiore) e usate. Data di accesso per il web: 13 agosto 2026.

### Accademiche e preprint

- Ahmad, I., Jena, I., Priyadarshi, A. (2023), *Mathematical Modelling of Hypothalamus-Pituitary-Adrenal Axis Dynamics: A Review, a Novel Approach and Future Directions*, arXiv:2311.04570, spec. §1.1, §1.3 Tab. 1, §2 eq. (2.1)–(2.3), Tab. 2, §4.
- Andersen, M., Vinther, F., Ottesen, J.T. (2013), *Mathematical modeling of the hypothalamic-pituitary-adrenal axis*, *Mathematical Biosciences* 246:122–138 (rate h1, h2, h3 via compilazione Ahmad).
- Aston-Jones, G., Cohen, J.D. (2005), *An integrative theory of locus coeruleus-norepinephrine function*, *Annual Review of Neuroscience* 28:403–450.
- Barrett, L.F. (2017), *The theory of constructed emotion: an active inference account of interoception and categorization*, *Social Cognitive and Affective Neuroscience* 12(1):1–23, PMC5390700, spec. Figura 1, Tabella 1, sezioni allostasi, degeneracy, predictive coding.
- Cannon, W.B. (1927), *The James-Lange theory of emotions: a critical examination and an alternative theory*, *American Journal of Psychology* 39:106–124.
- Cools, R., Nakamura, K., Daw, N.D. (2011), *Serotonin and dopamine: unifying affective, activational, and decision functions*, *Neuropsychopharmacology* 36:98–113.
- Damasio, A.R. (1994), *Descartes' Error*, Putnam / Grosset. (SMH; letto come quadro, non come pagina-per-pagina.)
- Damasio, A.R. et al. (2000), *Subcortical and cortical brain activity during the feeling of self-generated emotions*, *Nature Neuroscience* 3:1049–1056.
- Davis, K.L., Montag, C. (2019), *Selected Principles of Pankseppian Affective Neuroscience*, *Frontiers in Neuroscience* 12:1025, spec. sezioni sui sette sistemi, decorticazione, ANPS, predizioni psichiatriche.
- Croissant, M., Schofield, G., & McCallum, S. (2024), *Emotion design for video games: A framework for affective interaction based on the OCC model*, *PLOS ONE* 19(4):e0301033.
- Dayan, P. (2012), *Twenty-Five Lessons from Computational Neuromodulation*, *Neuron* 76:240–256. (Paywall; ruoli via abstract e rassegne convergenti — marcato lettura parziale.)
- Dayan, P., Huys, Q.J.M. (2009), *Serotonin in affective control*, *Annual Review of Neuroscience* 32:95–126.
- De Kloet, E.R., Vreugdenhil, E., Oitzl, M.S., Joëls, M. (1998), *Brain corticosteroid receptor balance in health and disease*, *Endocrine Reviews* 19:269–301.
- de Visser, E.J. et al. (2017), *A little anthropomorphism goes a long way*, PMC5477060.
- Doya, K. (2002), *Metalearning and neuromodulation*, *Neural Networks* 15:495–506 (PMID 12371507). PDF primario letto 13 agosto 2026: sezione 3, elenco 1–4. Quattro *ipotesi* di metalearning, non fatti. Implementate come readout opzionale.
- Dunn, B.D., Dalgleish, T., Lawrence, A.D. (2006), *The somatic marker hypothesis: a critical evaluation*, *Neuroscience & Biobehavioral Reviews* (PubMed 16197997).
- Edelman, G.M., Gally, J.A. (2001), *Degeneracy and complexity in biological systems*, *PNAS* 98:13763–13768.
- Friston, K. (2009), *The free-energy principle: a rough guide to the brain?*, *Trends in Cognitive Sciences* 13:293–301.
- Friston, K. (2010), *The free-energy principle: a unified brain theory?*, *Nature Reviews Neuroscience* 11:127–138.
- Glimcher, P.W. (2011), *Understanding dopamine and reinforcement learning: The dopamine reward prediction error hypothesis*, *PNAS* 108:15647–15654.
- Keramati, M., Gutkin, B. (2014), *Homeostatic reinforcement learning for integrating reward collection and physiological stability*, *eLife* 3:e04811.
- Hyman, S.E. (2007), *Can neuroscience be integrated into the DSM-V?*, *Nature Reviews Neuroscience* 8:725–732.
- Li, C. et al. (2023), *Large Language Models Understand and Can Be Enhanced by Emotional Stimuli*, arXiv:2307.11760 (EmotionPrompt). Citato come evidenza che uno stato affettivo nel prompt cambia la generazione; non come surrogato del milieu.
- Lövheim, H. (2012), *A new three-dimensional model for emotions and monoamine neurotransmitters*, *Medical Hypotheses* 78:341–348 (PMID 22153577). MINORITY / ipotesi non validata; rifiutata come classificatore.
- Panksepp, J. (1998), *Affective Neuroscience: The Foundations of Human and Animal Emotions*, Oxford University Press.
- Panksepp, J. (2010), *Affective neuroscience of the emotional BrainMind*, *Dialogues in Clinical Neuroscience* 12:533–545, PMC3181986, spec. Tabella I, thumbnail dei sette sistemi, cascata GRIEF→SEEKING nella depressione.
- Panksepp, J., Normansell, L.A., Cox, J.F., Siviy, S. (1994), *Effects of neonatal decortication on the social play of juvenile rats*, *Physiology & Behavior* 56:429–443.
- Russell, J.A. (2003), *Core affect and the psychological construction of emotion*, *Psychological Review* 110:145–172.
- Schultz, W., Dayan, P., Montague, P.R. (1997), *A neural substrate of prediction and reward*, *Science* 275:1593–1599.
- Smith, R., Parr, T., Friston, K.J. et al. (2020), *An Investigation of the Free Energy Principle for Emotion Recognition*, *Frontiers in Computational Neuroscience* 14:30, sezioni Theoretical Overview, Markov Blankets, Wave One–Three.
- Sterling, P. (2012), *Allostasis: a model of predictive regulation*, *Physiology & Behavior* 106:5–15.
- Tsigos, C., Chrousos, G.P. (2002), *Hypothalamic–pituitary–adrenal axis, neuroendocrine factors and stress*, *Journal of Psychosomatic Research* 53:865–871.
- Yang, X. et al. (2024), *Affective Computing in the Era of Large Language Models: A Survey from the NLP Perspective*, arXiv:2408.04638v1, sez. I–IV.
- Yu, A.J., Dayan, P. (2005), *Uncertainty, neuromodulation, and attention*, *Neuron* 46:681–692.
- Yovell, Y. et al. (2016), ultra-low-dose buprenorphine and suicidal ideation (cit. da Davis e Montag 2019 come predizione pankseppiana confermata).

### Di quadro, lette in ricognizione e usate con cautela

- MacLean, P. (1990), *The Triune Brain in Evolution*, Plenum. (Quadro storico; il "triune brain" è oggi considerato semplificazione — non è un pilastro.)
- Bowlby, J., lavori sull'attaccamento (via Panksepp 2010 sulla cascata protest→despair).

### Scartate come pilastro

- Wikipedia / blog / thread Reddit e Facebook comparsi in ricognizione: usati solo per trovare nomi, mai citati come prova.
- Paper "Complexity Theory-Based Novel AI Algorithm … Artificial Neurotransmitters" (ResearchGate 2025): non verificato, rischio di sede debole; non entra nei pilastri.
