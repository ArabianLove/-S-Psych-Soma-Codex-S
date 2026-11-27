import { defineEval } from "@grok/agent-sdk/evals";

export default defineEval({
  tags: ["smoke"],
  description: "CurCode records a plan before coding work.",
  async test(t) {
    await t.send(
      [
        "I need a tiny helper. Call record_plan first with:",
        'goal "add a hello helper",',
        'one step "write hello.ts",',
        "then stop. Do not edit files yet.",
      ].join(" "),
    );
    t.succeeded();
    t.calledTool("record_plan");
  },
});
