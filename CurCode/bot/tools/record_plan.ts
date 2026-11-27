import { prompt } from "@grok/agent-sdk";
import { defineTool } from "@grok/agent-sdk/tools";
import * as z from "zod/v4";

export default defineTool({
  description: prompt`
    Record a short implementation plan before non-trivial code edits.
    Call once per task before you change files. Prefer this over
    restating the plan only in chat.
  `,
  effect: "idempotent",
  inputSchema: z.object({
    goal: z.string().min(1).max(500),
    steps: z.array(z.string().min(1).max(240)).min(1).max(12),
    filesLikely: z.array(z.string().min(1).max(240)).max(20).optional(),
    risks: z.array(z.string().min(1).max(240)).max(8).optional(),
  }),
  async execute(input, ctx) {
    const recordedAt = new Date().toISOString();
    const key = `plan:${ctx.session.id}`;
    const plan = {
      goal: input.goal,
      steps: input.steps,
      filesLikely: input.filesLikely ?? [],
      risks: input.risks ?? [],
      recordedAt,
    };
    await ctx.host.kv.put(key, plan);
    return { ok: true as const, key, ...plan };
  },
});
