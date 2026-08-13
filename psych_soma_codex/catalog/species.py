"""Chemical species: transmitters, neuromodulators, hormones, peptides.

Concentrations in the runtime are *normalized occupancies* in [0, 1] unless
``physical_unit`` is set. Decay rates are envelopes of phasic/tonic signalling
at the affective-episode timescale (minutes), not single-vesicle half-lives.

Mapping column
--------------
Each species carries the computational role used by the engine. These roles
follow Dayan (2012) *Neuron* 76:240-256 for DA/5-HT/ACh/NE, Panksepp (1998,
2010) for peptide-system coupling, and Andersen/Vinther-class HPA models for
CRH/ACTH/cortisol. Roles tagged HYPOTHESIS are constitutive modelling choices.
"""

from __future__ import annotations

from dataclasses import dataclass

from psych_soma_codex.catalog.epistemics import Epistemic


@dataclass(frozen=True)
class SpeciesSpec:
    key: str
    name: str
    kind: str  # transmitter | neuromodulator | hormone | peptide | cytokine
    tau_min: float  # envelope time constant (minutes)
    baseline: float  # resting occupancy in [0, 1]
    floor: float
    ceiling: float
    role: str
    epistemic: Epistemic
    sources: tuple[str, ...]
    notes: str = ""
    physical_unit: str = ""


# Envelope time constants are *order-of-magnitude* affective timescales, not
# synaptic millisecond clearances. Fast amino acids (Glu/GABA) are treated as
# instantaneous gain terms driven by circuit activity (tau ~ seconds).
# Slow hormones use literature half-lives converted as tau = t_half / ln(2).
#
# CRH plasma t½ ≈ 4 min → tau ≈ 5.8 min; we use 5.8.
# ACTH t½ ≈ 22 min → tau ≈ 31.7; Andersen et al. 2013 removal 0.0315 /min
#   implies t½ = ln(2)/0.0315 ≈ 22 min. We expose both the physical HPA
#   integrator (µg/dL, pg/mL) and a normalized occupancy.
# Cortisol t½ ≈ 66 min → tau ≈ 95; Andersen h3 = 0.0105 /min.

SPECIES: dict[str, SpeciesSpec] = {
    "da": SpeciesSpec(
        key="da",
        name="dopamine",
        kind="neuromodulator",
        tau_min=0.4,
        baseline=0.22,
        floor=0.02,
        ceiling=1.0,
        role="reward_prediction_error + SEEKING gain + incentive salience",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Schultz, Dayan, Montague 1997 Science 275:1593-1599",
            "Glimcher 2011 PNAS 108:15647-15654",
            "Dayan 2012 Neuron 76:240-256 §§decision-making",
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545 SEEKING",
        ),
        notes=(
            "Phasic DA ≈ RPE is majority consensus (Schultz lineage) but not "
            "uncontested: tonic DA also tracks average reward / vigour "
            "(Niv et al.). We expose both phasic (rpe) and tonic (da) terms."
        ),
    ),
    "fiveht": SpeciesSpec(
        key="fiveht",
        name="serotonin",
        kind="neuromodulator",
        tau_min=1.2,
        baseline=0.40,
        floor=0.05,
        ceiling=1.0,
        role="punishment / behavioural inhibition / opponent to DA; mood tone",
        epistemic=Epistemic.DEBATE,
        sources=(
            "Dayan & Huys 2009 Neural Comput / Annu Rev Neurosci 32:95-126",
            "Cools, Nakamura, Daw 2011 Neuropsychopharmacology 36:98-113",
            "Dayan 2012 Neuron 76:240-256",
        ),
        notes=(
            "5-HT computational role is actively debated (aversive prediction, "
            "patience, inhibition, average reward). We adopt the Dayan-Huys "
            "opponent / inhibition reading as the *default policy*, flagged DEBATE."
        ),
    ),
    "ne": SpeciesSpec(
        key="ne",
        name="norepinephrine",
        kind="neuromodulator",
        tau_min=0.25,
        baseline=0.28,
        floor=0.04,
        ceiling=1.0,
        role="unexpected uncertainty + phasic interrupt / LC-NE gain",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Yu & Dayan 2005 Neuron 46:681-692",
            "Dayan 2012 Neuron 76:240-256",
            "Aston-Jones & Cohen 2005 Annu Rev Neurosci 28:403-450",
        ),
    ),
    "ach": SpeciesSpec(
        key="ach",
        name="acetylcholine",
        kind="neuromodulator",
        tau_min=0.35,
        baseline=0.30,
        floor=0.04,
        ceiling=1.0,
        role="expected uncertainty + learning-rate boost / cue unreliability",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Yu & Dayan 2005 Neuron 46:681-692",
            "Dayan 2012 Neuron 76:240-256",
        ),
    ),
    "gaba": SpeciesSpec(
        key="gaba",
        name="GABA",
        kind="transmitter",
        tau_min=0.08,
        baseline=0.45,
        floor=0.10,
        ceiling=1.0,
        role="fast inhibition / RAGE-FEAR brake",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545 (RAGE/FEAR chemistries)",
            "standard fast-inhibitory transmission",
        ),
    ),
    "glu": SpeciesSpec(
        key="glu",
        name="glutamate",
        kind="transmitter",
        tau_min=0.06,
        baseline=0.35,
        floor=0.08,
        ceiling=1.0,
        role="fast excitation / GRIEF & RAGE drive",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545 (GRIEF: glu+CRF)",
        ),
    ),
    "crh": SpeciesSpec(
        key="crh",
        name="corticotropin-releasing hormone",
        kind="peptide",
        tau_min=5.8,
        baseline=0.18,
        floor=0.02,
        ceiling=1.0,
        role="HPA drive + FEAR/GRIEF peptide",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Andersen, Vinther, Ottesen 2013 Math Biosci 246:122-138 (h1=0.1732/min)",
            "Ahmad, Jena, Priyadarshi 2023 arXiv:2311.04570 Table 2",
            "Panksepp 2010 (FEAR: NPY+CRF; GRIEF: glu+CRF)",
        ),
        physical_unit="normalized; physical integrator in interoception.hpa",
    ),
    "acth": SpeciesSpec(
        key="acth",
        name="adrenocorticotropic hormone",
        kind="hormone",
        tau_min=22.0,
        baseline=0.16,
        floor=0.02,
        ceiling=1.0,
        role="HPA intermediate",
        epistemic=Epistemic.FACT,
        sources=(
            "Andersen et al. 2013 Math Biosci 246:122-138 h2=0.0315/min",
            "Ahmad et al. 2023 arXiv:2311.04570 Table 2",
        ),
        physical_unit="pg/mL in HPA integrator",
    ),
    "cortisol": SpeciesSpec(
        key="cortisol",
        name="cortisol",
        kind="hormone",
        tau_min=66.0,
        baseline=0.22,
        floor=0.04,
        ceiling=1.0,
        role="slow stress effector + GR/MR feedback + energy mobilisation",
        epistemic=Epistemic.FACT,
        sources=(
            "Andersen et al. 2013 Math Biosci 246:122-138 h3=0.0105/min",
            "Ahmad et al. 2023 arXiv:2311.04570 Table 2, circadian profile §1.1",
            "Tsigos & Chrousos 2002 J Psychosom Res 53:865-871",
        ),
        physical_unit="µg/dL in HPA integrator",
    ),
    "ot": SpeciesSpec(
        key="ot",
        name="oxytocin",
        kind="peptide",
        tau_min=3.5,
        baseline=0.24,
        floor=0.03,
        ceiling=1.0,
        role="CARE / bonding / trust gain; GRIEF brake",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545 CARE/GRIEF",
            "Carter 2014 / 2017 attachment reviews",
            "de Visser et al. 2017 (OT and trust toward automated agents)",
        ),
        notes=(
            "OT is not a universal 'love molecule': effects are context- and "
            "receptor-dependent (in-group bias). We model a *prosocial gain* "
            "modulated by perceived in-group membership (HYPOTHESIS coupling)."
        ),
    ),
    "avp": SpeciesSpec(
        key="avp",
        name="arginine vasopressin",
        kind="peptide",
        tau_min=4.0,
        baseline=0.18,
        floor=0.03,
        ceiling=1.0,
        role="territorial / pair-bond assertiveness; HPA co-secretagogue",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 LUST/CARE chemistries",
            "Ahmad et al. 2023 arXiv:2311.04570 (AVP→ACTH pathway)",
            "Carter attachment literature",
        ),
    ),
    "opioid": SpeciesSpec(
        key="opioid",
        name="mu-opioid / beta-endorphin tone",
        kind="peptide",
        tau_min=8.0,
        baseline=0.32,
        floor=0.04,
        ceiling=1.0,
        role="social comfort / GRIEF brake / PLAY hedonics / pain",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 1980 opioid hypothesis of social attachment",
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545 GRIEF/PLAY",
            "Yovell et al. 2016 (ultra-low-dose buprenorphine, suicidality)",
        ),
    ),
    "dynorphin": SpeciesSpec(
        key="dynorphin",
        name="dynorphin / kappa-opioid",
        kind="peptide",
        tau_min=10.0,
        baseline=0.12,
        floor=0.02,
        ceiling=1.0,
        role="SEEKING brake / dysphoria of loss and social defeat",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Panksepp 2010 Dialogues Clin Neurosci 12:533-545 (depression cascade)",
            "Knoll & Carlezon 2010 Brain Res kappa-opioid dysphoria",
        ),
    ),
    "endocannabinoid": SpeciesSpec(
        key="endocannabinoid",
        name="endocannabinoid tone",
        kind="transmitter",
        tau_min=6.0,
        baseline=0.30,
        floor=0.05,
        ceiling=1.0,
        role="recovery / extinction / PLAY facilitation",
        epistemic=Epistemic.HYPOTHESIS,
        sources=(
            "Panksepp & Biven 2012 Archaeology of Mind (PLAY chemistries)",
        ),
        notes="Included as a slow recovery reservoir; coupling is HYPOTHESIS.",
    ),
    "substance_p": SpeciesSpec(
        key="substance_p",
        name="substance P",
        kind="peptide",
        tau_min=5.0,
        baseline=0.10,
        floor=0.02,
        ceiling=1.0,
        role="RAGE / pain peptide",
        epistemic=Epistemic.CONSENSUS,
        sources=("Panksepp 2010 Dialogues Clin Neurosci 12:533-545 RAGE chemistries",),
    ),
    "prolactin": SpeciesSpec(
        key="prolactin",
        name="prolactin",
        kind="hormone",
        tau_min=25.0,
        baseline=0.16,
        floor=0.03,
        ceiling=1.0,
        role="CARE support / GRIEF brake",
        epistemic=Epistemic.CONSENSUS,
        sources=("Panksepp 2010 CARE/GRIEF chemistries",),
    ),
    "adrenaline": SpeciesSpec(
        key="adrenaline",
        name="adrenaline (epinephrine)",
        kind="hormone",
        tau_min=1.5,
        baseline=0.12,
        floor=0.02,
        ceiling=1.0,
        role="sympathetic effector / arousal / FEAR-RAGE periphery",
        epistemic=Epistemic.FACT,
        sources=("standard adrenal medulla physiology",),
    ),
    "il6": SpeciesSpec(
        key="il6",
        name="interleukin-6 (inflammatory tone)",
        kind="cytokine",
        tau_min=40.0,
        baseline=0.08,
        floor=0.01,
        ceiling=0.9,
        role="sickness / SEEKING brake / interoceptive load",
        epistemic=Epistemic.CONSENSUS,
        sources=(
            "Dantzer et al. 2008 Nat Rev Neurosci cytokine-induced sickness",
            "Panksepp 2010 (cytokines diminish SEEKING)",
        ),
    ),
}
