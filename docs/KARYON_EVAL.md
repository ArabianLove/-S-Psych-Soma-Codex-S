# Valutazione critica di Karyon (dono 10)

Il dono non è stato accettato in toto. Ogni claim è stato confrontato con
(i) le fonti primarie già usate come metro, (ii) il codice già presente in
`psych_soma_codex`, (iii) il protocollo epistemico di `docs/RESEARCH.md` e i
verbali dei doni 1–9. Nessun genoma eseguibile entra nel repository.
Andersen \(h_1/h_2/h_3\) non si tocca. Il piano 0 resta un prior, non una
sequenza.

Data di valutazione: 21 agosto 2026.
Giudice: questo repository. La sorgente è stata letta per intero (incollata
in chat: header «Traslitterazione funzionale (non mera simulazione) del
genoma umano», ~340 righe). Un probe equivalente è stato eseguito *fuori*
dal repo (`/tmp`, seed 42). Il file non è stato copiato in `psych_soma_codex`.

Materiale valutato:

1. *Karyon — Core genomico eseguibile*. Sorgente Python unica. 18 loci
   diploidi (HOX, TP53/MYC, HLA, SNRPN/UBE3A/IGF2, HTT polyQ, SRY,
   MT-ATP6/ND1/CO1, TERT), promoter random 90 bp, CDS random 150 bp, GRN
   Hill + Euler, energia / telomero / etichette di patologia. Header:
   «traslitterazione, non mera simulazione».

## Sintesi esecutiva

Karyon **gira**. Gira ≠ Kodex. È un organismo L1 concorrente al *piano
sbagliato*: un runtime genomico che pretende di *essere* la costituzione.
RESEARCH §3.3 lo vieta già in prosa: «Genetica/epigenetica *non* sono un
genoma: sono il prior del piano 0.» Meaney–Weaver scala \(\mu/\rho\), non
la sequenza di NR3C1. Rothbart / Cloninger / Gray RST sono guadagni e
riposo, non 18 CDS.

Il gesto è lo stesso dello zip NeuroChem-GenAI (dono 8): un eseguibile con
qualche landmark vero, un header che promette translitterazione, e un
lavoro costitutivo invertito. Là dieci serbatoi Euler scrivevano
l'affetto. Qui diciotto proteine Hill scrivono etichette di malattia.
`_diagnose` è Barrett capovolto al DNA: una soglia produce un nome folk
(`myc-dereg`, `PWS-like`, `polyQ-N`). Nel Kodex l'etichetta nasce *dopo*
il corpo; qui il genoma *autora* la diagnosi.

Si **butta come runtime**. Si **tiene come rassegna di ciò che non si fa
al piano 0**. Nessun locus, nessuna cinetica di Hill, nessun telomero,
nessuna etichetta PWS/AS entra in `constitution.py`.

Confidenza: alta sul rifiuto di importare il genoma e di sostituire il
prior costituzionale con una GRN; alta sul fatto che la tabella dei
codoni 1 è corretta e la 2 manca; alta sul fatto che la demo non raggiunge
mai l'età diagnostica e che MYC satura tutti quando la si forza; media
sulle magnitudini di qualunque prior futuro (restano HYPOTHESIS).

## Domanda di questa valutazione

Di Karyon, che cosa si tiene, che cosa si butta, che cosa si tiene in
regalo — e che cosa, pur vero, è già costitutivo e non va reimplementato?

## 1. Cosa c'è già, e perché è il metro

Oltre al metro dei doni 1–9: quattro piani 0/A/B/C, 18 specie, 7 circuiti,
HPA Andersen in µg/dL, RK4 `dt = 0.05 min`, bond per-agente, OT gated da
`in_group`, Doya come readout HYPOTHESIS, decode a segni fissi, packet,
`phenomenology_claim: false`, `immutable_constraints`, costituzione a
identità di default. Zero dipendenze runtime. 60 test. Lövheim, Iovane
\(5^7\), Brian2/NEST, FiLM, NeuroChem-GenAI, MOSAIC, RCAD come L1: già
fuori.

Il piano 0 (`constitution.py`) è un dataclass *frozen*: rest, event gain,
\(\tau\), baseline chimiche, \(\mu/\rho\) HPA, `rest_stress_gain`. Default
= identità. Archetipi nominati: `high_fffs`, `high_bis`, `high_bas`,
`meaney_low_nurture`. Non autorizzano `forbidden`. Non scalano
\(h_1/h_2/h_3\). Non contengono un campo genoma.

Qualunque dono che *sostituisca* il prior con una sequenza, che faccia del
DNA l'autore di un'etichetta folk, o che confonda sintenia nominale con
cinetica HPA, è un regresso.

## 2. Errori di fatto, prima dei claim

Sei sbagli stanno nel codice *prima* di qualunque raccomandazione. Non
sono stile. Sono il metro.

| Errore | Cosa c'è | Cosa è |
|---|---|---|
| Codice mitocondriale assente | `CODON_TABLE` = NCBI `transl_table=1` (64/64, verificato). MT-ATP6, MT-ND1, MT-CO1 usano la stessa tabella. `translate` è definita e **mai chiamata** dal runtime. | NCBI `transl_table=2` (vertebrate mitochondrial): ATA = M non I, TGA = W non \*, AGA/AGG = \* non R. I tre loci «energia» sono nucleari di fatto. |
| TERT come fattore di transcrizione | `SINTENIA`: TERT `is_tf=True`, `motif="MYC"`. Nove TF. TERT entra in `tf_levels` e cerca CACGTG su ogni promoter. | TERT è la subunità catalitica della telomerasi (reverse transcriptase, cromosoma 5). Il promoter di TERT *è* un bersaglio di MYC (E-box): vero. La *proteina* TERT non è un TF che legge E-box. Il dono inverte bersaglio e fattore, e chiude un feedback positivo MYC↔TERT. |
| Motivo HOX = TAAT | 4-mer inserito + conteggio del reverse-complement. Su 1000 promoter random 90 bp a GC 0.55: **337** contengono TAAT o ATTA. Sul genoma seed 42 di K-000 il 4-mer colpisce anche MYC, HLA-DRB1, SNRPN, UBE3A, IGF2, SRY, MT-\*, TERT. | Il core homeodomain è TAAT, ma è promiscuo. Non è sintenia. Non è un sito HOX. |
| Motivo TP53 = AGGCATGT | Inserito come «da letteratura». | Il consensus p53 è RRRCWWGYYY (el-Deiry 1992; due half-site). AGGCATGT non è un half-site pulito. |
| PolyQ = `str.count("CAG")` | HTT inserisce 15–28 CAG (soglia ≥ 36: vera). Poi conta ogni occorrenza nel CDS random. Seed 42: 20 inseriti → 22 contati; 27 → 30. | La lunghezza polyQ è il tratto *consecutivo* dopo ATG, non il conteggio di sottostringhe. Il CDS random contiene CAG per caso. |
| Demo che non diagnostica | `__main__`: 15 × `dt=0.4` → età 6.0. `_diagnose` ritorna se `age < 12`. Energia satura al cap 22.0. Patologia stampata: `-`. | Il teatro «gira». La patologia della demo **non scatta mai**. Forzando `age=13`, tutti e sei gli organismi sono `myc-dereg` (MYC 4.7–11.4 vs soglia 2.8). |

Altri fatti, non errori di battitura:

- HOX cluster sui cromosomi 7 / 17 / 12 / 2: vero (Bhatlekar 2018 e rassegne HOX).
- SNRPN espresso dal paterno, UBE3A dal materno, IGF2 dal paterno: segni
  parentali corretti (PWS / AS, Nature Scitable; cromosoma 15q11–q13).
- SRY AACAAT: approssimazione HMG nota in vitro (mouse Sry / SOX).
- MYC CACGTG, CREB TGACGTCA, SP1 GGGCGG, NF-κB GGGACTTTCC: motivi cis
  recogniti. CREB è nel dizionario e **mai assegnato** a un locus.
- GC default 0.42: ordine di grandezza di Piovesan 2019 (genoma umano
  40.9%). I promoter HOX a 0.55 sono un'altra cosa.
- mtDNA umano è aplotipo materno, non diploide. Karyon dà a MT-ATP6 due
  alleli attivi, materno e paterno, diversi. SRY è diploide sul Y.
- Campo `dev` (ordine collineare HOX): scritto, mai letto.
- `math`, `copy`, `Tuple`: importati, mai usati.

## 3. Claim per claim

### 3.1 «Traslitterazione, non mera simulazione»

| Claim | Esito | Perché |
|---|---|---|
| 18 loci = genoma umano in unità relazionali | **BUTTARE** | 18 promoter random da 90 bp non sono sintenia. Non c'è collinearità, non c'è un asse, non c'è un cis-regulatory landscape. I nomi dei geni sono etichette su stringhe casuali. |
| Codice degenerato reale | **TENERE il fatto, non il runtime** | Tabella 1 corretta. Tabella 2 assente. `translate` morta: il proteoma non passa dai codoni. La degeneracy è un commento. |
| GRN Hill + Euler = espressione | **BUTTARE** come L1 | \(n=2.2\), \(k=0.45\), decay 0.09, `dt` 0.2–0.4: numeri inventati, come le λ dello zip. Nove TF senza saturazione di proteina. MYC a fine demo: 4.7–11.4; a morte: 19.9. Non è un HPA. Non è Panksepp. |
| Epigenoma (cromatina, metilazione, acetilazione) | **NON COME L1** | Tre float uniformi per allele. Meaney–Weaver nel Kodex è \(\mu/\rho\), meccanismo CONSENSUS, magnitudini HYPOTHESIS. Non è NR3C1, non è un promoter di 90 bp. |
| Organismo con metabolismo, patologie, senescenza | **BUTTARE** | Energia con cap 22, costo lineare in età, telomero −0.0012/unità. Morte a 230 passi, età 92, **E = 0.25**, telomero ancora 0.890. Il telomero non uccide. La patologia è un'etichetta post-hoc. |

### 3.2 Patologia come produttore

| Claim | Esito | Perché |
|---|---|---|
| `myc-dereg` se MYC > 2.8 | **BUTTARE** | Soglia inventata. MYC è illimitato. Forzando l'età, *tutti* sono `myc-dereg`. È un classificatore, non un fenotipo. |
| `PWS-like` / `AS-like` se SNRPN / UBE3A < 0.035 | **BUTTARE** come diagnosi | I segni parentali dell'imprinting sono corretti. La diagnosi è una soglia di proteoma, non la perdita dell'impronta. Nel probe, SNRPN 0.6–3.8 e UBE3A 0.55–3.7: PWS/AS non scattano *perché Euler spinge in su*, non perché l'imprinting tiene. |
| `guardian-loss` se TP53 < 0.04 e età > 18 | **BUTTARE** | TP53 a fine demo è 1.9–6.8. Non scatta. Stesso gesto: nome clinico da soglia. |
| `polyQ-N` se `cds.count("CAG") ≥ 36` | **BUTTARE** il conteggio; **TENERE** la soglia ≥ 36 come fatto noto | Donaldson / Faquih: CAG ≥ 36 è la soglia HD. Il dono inserisce 15–28 (normale) e poi sbaglia la misura. Non entra. |
| `_diagnose` gated a età 12 | **NOTARE** | La demo (`age=6`) non chiama mai il diagnostico. Gira ≠ mostra ciò che pretendi di mostrare. |

### 3.3 Accoppiamento al piano 0

| Claim | Esito | Perché |
|---|---|---|
| Un genoma *fonda* la costituzione | **BUTTARE** | RESEARCH §3.3: genetica/epigenetica sono il prior, non un genoma. `Constitution` è frozen, identità di default, senza campi di sequenza. Inserire 18 loci invertirebbe il lavoro: il DNA scriverebbe il carattere *e* l'etichetta. |
| TERT / telomero come senescenza costituzionale | **BUTTARE** | Il Kodex non ha un orologio di repliche. La costituzione è a vita dell'organismo (Rothbart / Cloninger / Gray / Meaney), non un float che scende di 0.0012. |
| HLA come self/non-self relazionale | **NON COME L1** | I bond del Kodex sono per-agente, OT gated da `in_group`. HLA-A / HLA-DRB1 come stringhe random con motivo NF-κB non aggiungono un self. |
| SRY come sesso costituzionale | **BUTTARE** | Il Kodex non ha un sesso genomico. Differenze di sesso HPA sono già dichiarate fuori (§3.3: «Il modello *non* include … differenze di sesso»). SRY diploide sul Y è, in più, sbagliato. |

## 4. Steelman, e il contro

La versione più forte: *«Avete un piano 0 che ammette genetica ed
epigenetica. Noi vi diamo i landmark veri (codoni, HOX sui cromosomi
giusti, imprinting parentale, soglia HTT, motivi cis). Un prior senza
sequenza è un commento. Dovreste sostituire `Constitution` con un
diploide, e far nascere il carattere — e le patologie — dal GRN.»*

Contro:

1. Il piano 0 è già la risposta. Esistenza CONSENSUS, numeri HYPOTHESIS,
   identità di default, Meaney su \(\mu/\rho\). Una sequenza *non è
   richiesta* perché il prior sia costitutivo. È richiesta perché sia un
   altro oggetto.
2. 18 promoter random non sono un genoma. I landmark veri sono nomi
   attaccati a stringhe casuali. La tabella 1 corretta non lava la
   tabella 2 assente, TERT-TF, TAAT promiscuo, `count("CAG")`.
3. `_diagnose` è il dizionario molecola→malattia, stessa famiglia di
   `set_emotion('joy')` (dono 9) e del classificatore NeuroChem (doni
   6–8). Barrett Tab. 1: niente fingerprint. Un nome clinico da soglia
   di proteina è classical view al DNA.
4. Hill+Euler a 18 proteine non è l'HPA. Andersen resta l'unico
   integratore del cortisolo. Importare Karyon collasserebbe il piano 0
   *e* il piano C.
5. Che il Python giri cambia il grado di tentazione, non il piano. Stesso
   insegnamento dello zip: eseguibile ≠ organismo di *questo* Kodex.

## 5. Cosa si implementa, e cosa no

### Non entra nel runtime

- `Allele`, `GeneLocus`, `SINTENIA`, `Organism` di Karyon, `genesis`,
  `euler_proteome`, `transcription_rate`, `hill` di Karyon.
- Qualunque campo genoma / promoter / CDS / telomero / patologia su
  `Constitution` o su `psych_soma_codex.Organism`.
- Motivi cis come causa di occupancy Panksepp o di etichetta Barrett.
- Diagnosi PWS / AS / guardian-loss / myc-dereg / polyQ.
- Codice mitocondriale, TERT come TF, HOX come 4-mer.
- numpy / scipy / un secondo integratore Euler.
- Qualunque claim di sentienza, di «traslitterazione del genoma umano»,
  o uso clinico / diagnostico.

### Entra come disciplina / RESEARCH, non come codice

1. Ribadire §3.3: genetica/epigenetica **non** sono un genoma. Il dono 10
   è l'istanza eseguibile di quella tentazione.
2. Stesso gesto del dono 8: *gira ≠ Kodex*. Un toy con landmark veri non
   autorizza a cambiare piano.
3. `_diagnose` come anti-pattern: l'etichetta folk non si scrive dal DNA
   più di quanto non si scriva da un intero 0–5 (`set_emotion`) o da
   dieci serbatoi (NeuroChem).
4. Meaney resta \(\mu/\rho\). Non si apre una pista «NR3C1 sequence».

### Non entra neanche come pista nuova

NCBI `transl_table=1/2`, Piovesan 2019, el-Deiry 1992, i cluster HOX, la
soglia HTT ≥ 36, l'imprinting PWS/AS sono fatti veri usati come *metro
del giudice*. Non diventano pilastri del Kodex. Non si apre una pista
(xii) «genoma a 18 loci».

## 6. Probe (osservazionale, fuori repo)

Eseguito su copia in `/tmp`, seed 42, `n=6`, `warmup=22`, 15 × `dt=0.4`,
`food=1.05`. Non è una test suite del Kodex.

- Tabella 1: 64/64 vs NCBI. Diff. tabella 2: ATA, TGA, AGA, AGG.
- Demo: 6 vivi, energia al cap 22.0 da `t=11`, età finale 6.0, patologia
  `-` per tutti. TP53 1.94–6.78, MYC 4.74–11.44.
- `age=13` forzata: sei su sei `myc-dereg`. PWS/AS / guardian-loss: no.
- HTT: CAG inseriti 15–27, contati sempre ≥ inseriti (extra 0–4).
- TAAT∨ATTA in 90 bp GC 0.55: 337/1000.
- Morte (K-000 fresco, stesso cibo): 230 passi, età 92, tel 0.890,
  E 0.25, path `myc-dereg`, MYC 19.92. Uccide l'energia, non il telomero.

## 7. Verdetto

**Karyon.** Buttare come runtime. Tenere come rassegna di ciò che non si
fa al piano 0. Non è pellegrino nel senso di Perplexity: non ha visto i
tre piani, non ha visto Andersen, non ha visto Barrett, ha chiamato
traslitterazione un toy a 18 stringhe random, ha messo TERT tra i TF, ha
usato il codice nucleare sui geni mitocondriali, ha fatto della patologia
un classificatore, e la demo non raggiunge l'età in cui il classificatore
parlerebbe. Si tiene la lezione già scritta in §3.3 e il richiamo
*gira ≠ Kodex* del dono 8. Si tiene, come fatti di metro e non come
codice, la tabella 1, i cromosomi HOX, i segni parentali dell'imprinting,
la soglia HTT ≥ 36, alcuni motivi cis. Si butta ciò che vorrebbe
*sostituire* la costituzione.

Panksepp resta l'unico produttore delle occupancy. Barrett resta l'unico
produttore dell'etichetta. Andersen resta l'unico integratore del
cortisolo. Il default resta l'identità. Lövheim resta fuori. Il piano 0
resta un prior, non un genoma.
