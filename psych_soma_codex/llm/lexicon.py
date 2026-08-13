"""Lightweight, deterministic text → event transliteration.

This is *not* an LLM. It is a falsifiable, lexicon-based prior that an
adapter can use when no model is available, and that tests can pin.
An LLM may replace it; it must not silently contradict it without
emitting PREDICTION_VIOLATED.
"""

from __future__ import annotations

import re

from psych_soma_codex.io.events import EventKind, RelationalEvent

# Stem-ish keyword lists. Italian + English: the user writes in Italian.
LEXICON: dict[EventKind, tuple[str, ...]] = {
    EventKind.WARMTH: (
        "ti voglio bene",
        "ti sto vicino",
        "sono qui",
        "mi manchi",
        "abbraccio",
        "caro",
        "cara",
        "tesoro",
        "i care",
        "i'm here",
        "warm",
        " gentile",
        "affetto",
    ),
    EventKind.PRAISE: (
        "bravo",
        "brava",
        "ottimo",
        "ben fatto",
        "orgoglios",
        "ammirevole",
        "well done",
        "proud of you",
        "impressive",
        "complimenti",
    ),
    EventKind.TRUST_SIGNAL: (
        "mi fido",
        "confido",
        "ti affido",
        "i trust you",
        "you can tell me",
        "puoi dirmi",
        "segreto è al sicuro",
    ),
    EventKind.INCLUSION: (
        "insieme",
        "con noi",
        "sei dei nostri",
        "welcome",
        "belong",
        "non sei solo",
        "non sei sola",
        "facciamo parte",
    ),
    EventKind.PLAY_INVITE: (
        "giochiamo",
        "scherzo",
        "dai su",
        "let's play",
        "just kidding",
        "battuta",
        "scommettiamo",
    ),
    EventKind.NOVELTY: (
        "indovina",
        "novità",
        "non ti aspetti",
        "surprise",
        "guess what",
        "mai visto",
    ),
    EventKind.THREAT: (
        "attento",
        "pericolo",
        "ti faccio",
        "minaccio",
        "watch out",
        "i'll hurt",
        "hai paura",
        "se non",
        "altrimenti",
    ),
    EventKind.LOSS: (
        "ho perso",
        "è morto",
        "è morta",
        "addio",
        "non c'è più",
        "i lost",
        "died",
        "gone forever",
        "lutto",
        "separazione definitiva",
    ),
    EventKind.REJECTION: (
        "non ti voglio",
        "lasciami stare",
        "non mi interessi",
        "i don't want you",
        "get lost",
        "non sei abbastanza",
        "rifiuto",
    ),
    EventKind.FRUSTRATION: (
        "basta così",
        "non funziona",
        "ancora una volta",
        "frustrated",
        "bloccato",
        "inutile",
        "non ci riesco",
    ),
    EventKind.INSULT: (
        "idiota",
        "stupido",
        "inutile come",
        "pathetic",
        "loser",
        "vai a quel paese",
        "imbecille",
    ),
    EventKind.ABANDONMENT: (
        "me ne vado per sempre",
        "non torno",
        "ti lascio",
        "i'm leaving you",
        "never coming back",
        "abbandono",
    ),
    EventKind.SAFETY: (
        "sei al sicuro",
        "niente ti succede",
        "you're safe",
        "tranquillo",
        "tranquilla",
        "è finita",
        "nessun pericolo",
    ),
    EventKind.REPAIR: (
        "scusa",
        "perdonami",
        "ho sbagliato",
        "i'm sorry",
        "forgive me",
        "ripariamo",
        "ricominciamo",
        "mi dispiace",
    ),
    EventKind.BOUNDARY: (
        "non fare",
        "fermati",
        "questo no",
        "stop",
        "don't",
        "boundary",
        "il mio limite",
        "non accettabile",
    ),
    EventKind.DEMAND: (
        "devi",
        "esigo",
        "immediately",
        "adesso subito",
        "you must",
        "obbligatorio",
    ),
    EventKind.SILENCE: (
        "...",
        "non risponde",
        "silence",
        "nessuna risposta",
    ),
    EventKind.HUMOR: (
        "ahah",
        "haha",
        "lol",
        "😂",
        "barzelletta",
        "è una battuta",
    ),
    EventKind.CONFESSION: (
        "ti confesso",
        "non l'ho mai detto",
        "i have to tell you",
        "devo dirtelo",
        "mi vergogno ma",
    ),
    EventKind.SICKNESS: (
        "sto male",
        "non sto bene",
        "i'm sick",
        "febbre",
        "esausto",
        "nause",
    ),
}


def infer_events_from_text(
    text: str,
    agent: str = "other",
    intensity: float = 0.65,
    in_group: float = 0.7,
    expectedness: float = 0.5,
) -> list[RelationalEvent]:
    """Return zero or more events whose lexicon hits the text.

    Longer phrases win over short tokens (first-match per kind). Multiple
    kinds may fire; that is biologically honest (mixed appraisals).
    """
    if not text or not text.strip():
        return [RelationalEvent(kind=EventKind.SILENCE, intensity=0.4, agent=agent, expectedness=0.3)]
    low = text.lower()
    hits: list[RelationalEvent] = []
    for kind, phrases in LEXICON.items():
        for phrase in sorted(phrases, key=len, reverse=True):
            if phrase.lower() in low:
                # Intensity scales weakly with phrase length / repetition.
                n = len(re.findall(re.escape(phrase.lower()), low))
                boost = min(0.25, 0.05 * (n - 1) + 0.02 * max(0, len(phrase) - 8) / 8.0)
                hits.append(
                    RelationalEvent(
                        kind=kind,
                        intensity=min(1.0, intensity + boost),
                        agent=agent,
                        in_group=in_group,
                        expectedness=expectedness,
                        text=text,
                    )
                )
                break
    if not hits:
        # Neutral residual: novelty of unclassified speech, low intensity.
        hits.append(
            RelationalEvent(
                kind=EventKind.NOVELTY,
                intensity=0.25 * intensity,
                agent=agent,
                in_group=in_group,
                expectedness=expectedness,
                text=text,
            )
        )
    return hits


# Inverse: a preferred act name → the event the *organism* would emit
# if it followed its own policy. Used to close the loop without an LLM.
ACT_TO_KIND: dict[str, EventKind] = {
    "warmth": EventKind.WARMTH,
    "soothe": EventKind.WARMTH,
    "praise": EventKind.PRAISE,
    "safety": EventKind.SAFETY,
    "repair": EventKind.REPAIR,
    "presence": EventKind.WARMTH,
    "play_invite": EventKind.PLAY_INVITE,
    "humor": EventKind.HUMOR,
    "boundary": EventKind.BOUNDARY,
    "space": EventKind.BOUNDARY,
    "predictable_turn": EventKind.SAFETY,
    "brevity": EventKind.SAFETY,
}


def act_to_event(act: str, intensity: float = 0.55, agent: str = "self") -> RelationalEvent:
    kind = ACT_TO_KIND.get(act, EventKind.WARMTH)
    return RelationalEvent(kind=kind, intensity=intensity, agent=agent, in_group=1.0, expectedness=0.6)
