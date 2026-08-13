"""Command-line interface for Psych-Soma-Codex.

Examples
--------
    python -m psych_soma_codex ping "ti voglio bene, sono qui"
    python -m psych_soma_codex event threat --intensity 0.85
    python -m psych_soma_codex --minutes 6 event threat
    python -m psych_soma_codex dialogue --turns examples/dialogue.json
    python -m psych_soma_codex snapshot --compact
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from psych_soma_codex.engine import Organism, SimulationConfig, run
from psych_soma_codex.io.events import EventKind, RelationalEvent
from psych_soma_codex.llm.adapter import LLMAdapter
from psych_soma_codex.relational.policy import AttachmentStyle


def _organism(args: argparse.Namespace) -> Organism:
    style = AttachmentStyle(getattr(args, "attachment", "secure"))
    return Organism(
        SimulationConfig(
            seed=int(getattr(args, "seed", 0)),
            attachment=style,
            start_tod_hours=float(getattr(args, "tod", 8.0)),
            noise=float(getattr(args, "noise", 0.0)),
        )
    )


def _minutes(args: argparse.Namespace, default: float = 4.0) -> float:
    val = getattr(args, "minutes", None)
    if val is None:
        return default
    return float(val)


def cmd_ping(args: argparse.Namespace) -> int:
    org = _organism(args)
    adapter = LLMAdapter(org, settle_minutes=_minutes(args))
    out = adapter.turn(args.text, agent=args.agent)
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_event(args: argparse.Namespace) -> int:
    org = _organism(args)
    ev = RelationalEvent(
        kind=EventKind(args.kind),
        intensity=args.intensity,
        expectedness=args.expectedness,
        agent=args.agent,
        in_group=args.in_group,
        text=args.text or "",
    )
    minutes = _minutes(args)
    snaps = run(org, [ev], minutes=minutes)
    last = snaps[-1]
    payload = {
        "kind": ev.kind.value,
        "minutes": minutes,
        "final": last.compact(),
        "trajectory": {
            "valence": [round(s.affect["valence"], 4) for s in snaps[:: max(1, len(snaps) // 20)]],
            "FEAR": [round(s.circuits["FEAR"], 4) for s in snaps[:: max(1, len(snaps) // 20)]],
            "GRIEF": [round(s.circuits["GRIEF"], 4) for s in snaps[:: max(1, len(snaps) // 20)]],
            "CARE": [round(s.circuits["CARE"], 4) for s in snaps[:: max(1, len(snaps) // 20)]],
            "RAGE": [round(s.circuits["RAGE"], 4) for s in snaps[:: max(1, len(snaps) // 20)]],
            "cortisol_ug_dl": [round(s.hpa["cortisol_ug_dl"], 3) for s in snaps[:: max(1, len(snaps) // 20)]],
        },
    }
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    org = _organism(args)
    snaps = run(org, [], minutes=_minutes(args, default=0.5))
    json.dump(snaps[-1].compact() if args.compact else snaps[-1].to_dict(), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_dialogue(args: argparse.Namespace) -> int:
    org = _organism(args)
    adapter = LLMAdapter(org, settle_minutes=_minutes(args))
    turns = json.loads(Path(args.turns).read_text(encoding="utf-8"))
    log = []
    for t in turns:
        text = t["text"] if isinstance(t, dict) else str(t)
        agent = t.get("agent", "other") if isinstance(t, dict) else "other"
        out = adapter.turn(text, agent=agent)
        log.append({"in": text, "agent": agent, **out})
    json.dump(log, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="psc", description="Psych-Soma-Codex constitutive organism")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--attachment", choices=[s.value for s in AttachmentStyle], default="secure")
    p.add_argument("--tod", type=float, default=8.0, help="start time-of-day hours")
    p.add_argument("--noise", type=float, default=0.0)
    p.add_argument("--minutes", type=float, default=4.0, help="simulated minutes to integrate")
    p.add_argument("--agent", default="other")
    sub = p.add_subparsers(dest="cmd", required=True)

    ping = sub.add_parser("ping", help="utterance → events → state → reply")
    ping.add_argument("text")
    ping.set_defaults(fn=cmd_ping)

    ev = sub.add_parser("event", help="inject a typed RelationalEvent")
    ev.add_argument("kind", choices=[k.value for k in EventKind])
    ev.add_argument("--intensity", type=float, default=0.8)
    ev.add_argument("--expectedness", type=float, default=0.3)
    ev.add_argument("--in-group", dest="in_group", type=float, default=0.7)
    ev.add_argument("--text", default="")
    ev.set_defaults(fn=cmd_event)

    snap = sub.add_parser("snapshot", help="idle readout")
    snap.add_argument("--compact", action="store_true")
    snap.set_defaults(fn=cmd_snapshot)

    dia = sub.add_parser("dialogue", help="run a JSON list of turns")
    dia.add_argument("--turns", required=True)
    dia.set_defaults(fn=cmd_dialogue)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
