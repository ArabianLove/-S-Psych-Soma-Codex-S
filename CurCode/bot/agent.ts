import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { defineAgent } from "@grok/agent-sdk";

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "..", "..");

export default defineAgent({
  name: "CurCode",
  description:
    "Coding agent for Psych-Soma-Codex: implements features, fixes bugs, and explains diffs in this repo.",
  local: {
    // Live inside this checkout: every session shares the repo tree.
    workspaceDir: repoRoot,
  },
  model: {
    id: "grok-4.7",
    params: [
      { id: "reasoning_effort", value: "high" },
      { id: "fast", value: "true" },
    ],
  },
});
