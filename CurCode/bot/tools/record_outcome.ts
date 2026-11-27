import { prompt } from "@grok/agent-sdk";
import { defineTool } from "@grok/agent-sdk/tools";
import * as z from "zod/v4";

export default defineTool({
  description: prompt`
    Record the outcome of a coding task when you are done or blocked.
    Call once at the end. Include files touched and how to verify.
  `,
  effect: "idempotent",
  inputSchema: z.object({
    status: z.enum(["done", "blocked", "partial"]),
    summary: z.string().min(1).max(800),
    filesTouched: z.array(z.string().min(1).max(240)).max(40),
    verify: z.array(z.string().min(1).max(240)).max(12).optional(),
    followUps: z.array(z.string().min(1).max(240)).max(12).optional(),
  }),
  async execute(input, ctx) {
    const recordedAt = new Date().toISOString();
    const key = `outcome:${ctx.session.id}`;
    const outcome = {
      status: input.status,
      summary: input.summary,
      filesTouched: input.filesTouched,
      verify: input.verify ?? [],
      followUps: input.followUps ?? [],
      recordedAt,
    };
    await ctx.host.kv.put(key, outcome);
    return { ok: true as const, key, ...outcome };
  },
});
