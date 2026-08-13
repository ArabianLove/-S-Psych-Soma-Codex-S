"""CLI smoke tests."""

from __future__ import annotations

import json

from psych_soma_codex.cli import main


def test_cli_event_threat(capsys):
    rc = main(["--minutes", "2", "event", "threat", "--intensity", "0.8"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["kind"] == "threat"
    assert payload["final"]["circuits"]["FEAR"] >= payload["final"]["circuits"]["PLAY"]


def test_cli_ping(capsys):
    rc = main(["--minutes", "1.5", "ping", "ti voglio bene"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert "reply" in payload
    assert "warmth" in payload["events"]


def test_cli_snapshot(capsys):
    rc = main(["--minutes", "0.5", "snapshot", "--compact"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert "valence" in payload
    assert "circuits" in payload
