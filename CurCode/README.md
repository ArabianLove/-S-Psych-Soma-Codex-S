# CurCode

Coding agent for **Psych-Soma-Codex**, built with `@grok/agent-sdk`. Lives in
this repo (`CurCode/`). Sessions share the repository root as workspace.

## Quick start

```bash
cd CurCode
npm install
npx @grok/agent-sdk login
npx @grok/agent-sdk dev
# playground: http://127.0.0.1:3000/playground
```

One-shot turn (from `CurCode/`):

```bash
npx @grok/agent-sdk run --dir . --message "Spiega circuits/primary.py in tre frasi."
```

## Layout

| Path | Role |
| --- | --- |
| `bot/agent.ts` | Model + identity |
| `bot/instructions.md` | Always-on coding prompt |
| `bot/tools/record_plan.ts` | Persist the implementation plan |
| `bot/tools/record_outcome.ts` | Persist the task outcome |
| `bot/skills/implement-change.md` | Feature / fix workflow |
| `evals/smoke.eval.ts` | Smoke: calls `record_plan` |

## Checks

```bash
npx @grok/agent-sdk validate --dir .
npx tsc --noEmit -p .
npx @grok/agent-sdk tool call record_plan --dir . --input '{"goal":"demo","steps":["inspect"]}'
npx @grok/agent-sdk eval --dir .
```
