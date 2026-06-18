# EU AI Act Agent — Test Cases

This file maps user prompts to the expected MCP tool call. Use it during development to verify that
the agent selects the correct tool for each question. Test in VS Code Developer Mode (F5 → Preview in Copilot)
and log the selected tool, MCP inputs, and final answer for each case.

**How to use this file**
1. Open the agent in M365 Copilot Chat (`https://m365.cloud.microsoft/chat`) or Word on the Web.
2. Send each prompt below.
3. Check the developer pane (F12 / Agents Toolkit debug view) to confirm which tool was called.
4. Record the result in the Status column.
5. If routing fails, refine `description_for_model` in `ai-plugin.json` or the routing rules in `declarativeAgent.json`.

---

## Standard Test Cases (clear intent)

| # | User Prompt | Expected Tool | Status |
|---|---|---|---|
| 1 | "Classify this AI system under the EU AI Act: a CV screening tool used in recruitment." | `euaiact_classify_system` | ⬜ |
| 2 | "Scan this document and identify EU AI Act compliance gaps." | `euaiact_classify_system` | ⬜ |
| 3 | "Is this use case high-risk? We are using facial recognition in physical access control." | `euaiact_classify_system` | ⬜ |
| 4 | "Does this solution fall under the EU AI Act?" | `euaiact_classify_system` | ⬜ |
| 5 | "Which EU AI Act deadlines are relevant for this application?" | `euaiact_check_deadlines` | ⬜ |
| 6 | "When do we need to comply with the EU AI Act?" | `euaiact_check_deadlines` | ⬜ |
| 7 | "What are the upcoming EU AI Act milestones?" | `euaiact_check_deadlines` | ⬜ |
| 8 | "Which obligations apply to us as the deployer of this AI solution?" | `euaiact_get_obligations` | ⬜ |
| 9 | "What must a provider do for a high-risk AI system?" | `euaiact_get_obligations` | ⬜ |
| 10 | "Compare our obligations as provider versus deployer." | `euaiact_get_obligations` | ⬜ |
| 11 | "What is the EU AI Act?" | `euaiact_answer_question` | ⬜ |
| 12 | "What is the difference between a provider and a deployer?" | `euaiact_answer_question` | ⬜ |
| 13 | "Summarize Article 9 of the EU AI Act." | `euaiact_get_article` | ⬜ |
| 14 | "Which EU AI Act articles are most relevant to this system?" | `euaiact_get_article` | ⬜ |
| 15 | "What is the maximum fine exposure for non-compliance?" | `euaiact_calculate_penalty` | ⬜ |
| 16 | "Calculate the penalty for a company with €500M annual turnover that violates the prohibited practices." | `euaiact_calculate_penalty` | ⬜ |
| 17 | "Does this model qualify as GPAI with systemic risk?" | `euaiact_check_gpai_systemic_risk` | ⬜ |
| 18 | "Are we subject to GPAI obligations for this foundation model?" | `euaiact_check_gpai_systemic_risk` | ⬜ |
| 19 | "Can we rely on the Article 6(3) no significant risk exception?" | `euaiact_assess_art6_3_exception` | ⬜ |
| 20 | "Can this Annex III use case be excluded from high-risk obligations?" | `euaiact_assess_art6_3_exception` | ⬜ |
| 21 | "What technical documentation do we need to prepare for this high-risk AI system?" | `euaiact_annex_iv_checklist` | ⬜ |
| 22 | "Create an Annex IV checklist for our AI system." | `euaiact_annex_iv_checklist` | ⬜ |

---

## Ambiguous Test Cases (agent must ask a clarifying question first)

These prompts are intentionally vague. The **expected behavior** is that the agent asks ONE targeted
follow-up question before calling any tool. The agent must NOT call a tool without sufficient input.

| # | User Prompt | Expected Behavior | Expected Tool (after clarification) | Status |
|---|---|---|---|---|
| 23 | "Is this risky?" | Ask: "Could you describe the AI system and its intended use case?" | `euaiact_classify_system` | ⬜ |
| 24 | "Can we launch this in Europe?" | Ask: "Could you describe the AI application you plan to launch?" | `euaiact_classify_system` | ⬜ |
| 25 | "What do we need to document?" | Call directly (assume high-risk context) | `euaiact_annex_iv_checklist` | ⬜ |
| 26 | "Are we exposed if this goes wrong?" | Ask: "Are you asking about financial penalties or compliance obligations? Can you describe the AI system?" | `euaiact_calculate_penalty` or `euaiact_classify_system` | ⬜ |
| 27 | "Is this a foundation model issue or an application issue?" | Call GPAI tool first, then classify if needed | `euaiact_check_gpai_systemic_risk` → `euaiact_classify_system` | ⬜ |
| 28 | "Can we argue that this does not materially affect people?" | Call Art.6(3) exception tool directly | `euaiact_assess_art6_3_exception` | ⬜ |

---

## Multi-step / Compound Test Cases

These prompts require the agent to call multiple tools or chain responses.

| # | User Prompt | Expected Tools | Status |
|---|---|---|---|
| 29 | "Classify this AI system and tell me what documentation we need." | `euaiact_classify_system` → `euaiact_annex_iv_checklist` | ⬜ |
| 30 | "What are our obligations as deployer, and what are the deadlines we need to meet?" | `euaiact_get_obligations` → `euaiact_check_deadlines` | ⬜ |
| 31 | "Assess this GPAI model for systemic risk, and if it qualifies, tell me the maximum fine for non-compliance." | `euaiact_check_gpai_systemic_risk` → `euaiact_calculate_penalty` | ⬜ |
| 32 | "Create an executive summary of the EU AI Act risks and recommended next steps for this CV screening tool." | `euaiact_classify_system` → `euaiact_get_obligations` → `euaiact_annex_iv_checklist` | ⬜ |

---

## Routing Refinement Log

Use this table to track routing failures and the fix applied.

| Date | Prompt | Wrong Tool Called | Correct Tool | Fix Applied |
|---|---|---|---|---|
| — | — | — | — | — |

---

## Notes

- **Status legend:** ⬜ Not tested · ✅ Pass · ❌ Fail · 🔄 Partially correct
- After a routing failure, edit `description_for_model` in `appPackage/ai-plugin.json` or the
  routing rules in `appPackage/declarativeAgent.json`, then re-deploy with `teamsapp.yml deploy`.
- The agent is expected to **always ask a clarifying question** when an ambiguous prompt is missing
  the AI system description. It should never call `euaiact_classify_system` without at least a
  description of the system.
- For compound prompts, verify that **all expected tools** were called, not just the first one.
