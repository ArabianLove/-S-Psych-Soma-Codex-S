---
description: Use when implementing a feature, bugfix, or refactor in the workspace.
---

# Implement a change

1. Read the request and name the acceptance check in one sentence.
2. Call `record_plan` with goal, ordered steps, likely files, and risks.
3. Explore with `glob` / `grep` / `read` before editing. Prefer the smallest
   existing pattern over inventing a new one.
4. Edit with harness tools. Keep diffs focused on the request.
5. Run a targeted verify command when one exists (test, typecheck, lint).
6. Call `record_outcome` with status, files touched, verify commands, and
   follow-ups.
7. Reply with what changed, how to verify, and any open risk.
