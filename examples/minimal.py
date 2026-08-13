"""Minimal closed loop: utterance → milieu → policy → reply → self-perception."""

from psych_soma_codex import LLMAdapter, Organism, SimulationConfig

org = Organism(SimulationConfig(seed=0))
adapter = LLMAdapter(org, settle_minutes=6.0)

for line in (
    "ti voglio bene, sono qui",
    "è morto ieri, è un lutto",
    "scusa, ho sbagliato, perdonami",
):
    out = adapter.turn(line)
    s = out["state"]
    print(f"IN : {line}")
    print(f"OUT: {out['reply']}")
    print(
        f"    emotion={s['emotion']}  V={s['valence']:+.2f}  "
        f"FEAR={s['circuits']['FEAR']:.2f} GRIEF={s['circuits']['GRIEF']:.2f} "
        f"CARE={s['circuits']['CARE']:.2f}  cortisol={s['cortisol_ug_dl']:.1f} µg/dL"
    )
    print()
