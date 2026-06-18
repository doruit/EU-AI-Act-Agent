# Architecture

## Overview

The EU AI Act Compliance Agent is a **Microsoft 365 Declarative Agent** that integrates the [Lexbeam EU AI Act MCP server](https://smithery.ai/servers/lexbeam-software/eu-ai-act) as its primary knowledge and reasoning source.

It is surfaced inside:
- **M365 Copilot Chat** (`https://m365.cloud.microsoft/chat`)
- **Microsoft Word** (desktop and web) — via the Copilot sidebar

```
User (M365 Copilot Chat / Microsoft Word)
       │
       ▼
┌──────────────────────────────────────────────┐
│       M365 Copilot Orchestrator              │
│  (GPT-4o / M365 foundation model)            │
│                                              │
│  declarativeAgent.json                       │
│  ├── instructions (tool routing policy)      │
│  ├── conversation_starters (6)               │
│  ├── capabilities                            │
│  │   ├── OneDriveAndSharePoint               │
│  │   └── WebSearch                           │
│  └── actions → ai-plugin.json               │
└──────────────────────┬───────────────────────┘
                       │ Plugin selected via description_for_model
                       ▼
┌──────────────────────────────────────────────┐
│       ai-plugin.json (Plugin Manifest v2.4)  │
│       runtime: RemoteMCPServer               │
│       auth: None                             │
│       spec.url: https://eu-ai-act--           │
│                lexbeam-software.run.tools     │
└──────────────────────┬───────────────────────┘
                       │ MCP tool call (HTTP POST)
                       ▼
┌──────────────────────────────────────────────┐
│  Lexbeam EU AI Act MCP Server                │
│  (Smithery-hosted, free, no API key)         │
│                                              │
│  Tools:                                      │
│  ├── euaiact_classify_system                 │
│  ├── euaiact_check_deadlines                 │
│  ├── euaiact_get_obligations                 │
│  ├── euaiact_answer_question                 │
│  ├── euaiact_calculate_penalty               │
│  ├── euaiact_get_article                     │
│  ├── euaiact_check_gpai_systemic_risk        │
│  ├── euaiact_assess_art6_3_exception         │
│  └── euaiact_annex_iv_checklist              │
└──────────────────────────────────────────────┘
```

---

## Component Details

### 1. `appPackage/manifest.json` — M365 App Manifest

The root Teams/M365 application manifest (schema v1.18). Registers the application in the M365 ecosystem and references the declarative agent. Also declares `validDomains` for the MCP server host.

**Key field:**
```json
"copilotAgents": {
  "declarativeAgents": [{ "id": "euAiActComplianceAgent", "file": "declarativeAgent.json" }]
}
```

The `TEAMS_APP_ID` value is templated and filled in by the M365 Agents Toolkit during provisioning.

---

### 2. `appPackage/declarativeAgent.json` — Declarative Agent Manifest (v1.5)

Defines the agent's identity, behaviour, and capabilities. The most critical field is `instructions` — an 8,000-character system prompt that implements the **tool routing policy**.

**Routing policy summary:**

| User intent | Tool called |
|---|---|
| Classify AI system / assess risk / scan document | `euaiact_classify_system` |
| Deadlines / milestones / when to comply | `euaiact_check_deadlines` |
| Obligations by role (provider/deployer/etc.) | `euaiact_get_obligations` |
| General questions / definitions / FAQ | `euaiact_answer_question` |
| Specific article text / EUR-Lex reference | `euaiact_get_article` |
| Fines / penalties / sanctions / fine exposure | `euaiact_calculate_penalty` |
| GPAI / foundation model / systemic risk | `euaiact_check_gpai_systemic_risk` |
| Article 6(3) no-significant-risk exception | `euaiact_assess_art6_3_exception` |
| Technical documentation / Annex IV checklist | `euaiact_annex_iv_checklist` |
| Ambiguous / unclear intent | Ask ONE clarifying question |

**Capabilities configured:**
- `OneDriveAndSharePoint` — unscoped (accesses all SharePoint/OneDrive the user has permission to). Enables grounding on internal policy documents and uploaded compliance materials.
- `WebSearch` — fallback for publicly available EU AI Act updates not yet in the MCP server.

---

### 3. `appPackage/ai-plugin.json` — Plugin Manifest (v2.4)

Wires the M365 Copilot orchestrator to the Lexbeam MCP server via the `RemoteMCPServer` runtime type (introduced in plugin schema v2.4). Key fields:

| Field | Value |
|---|---|
| `schema_version` | `v2.4` |
| `runtime.type` | `RemoteMCPServer` |
| `runtime.auth.type` | `None` (no API key required) |
| `runtime.spec.url` | `https://eu-ai-act--lexbeam-software.run.tools` |
| `runtime.spec.mcp_tool_description.file` | `mcp-tools.json` |

The `description_for_model` field (~2,048 chars max) is the primary signal that tells the orchestrator to select this plugin. It lists all 9 tool domains explicitly.

### Swappable MCP backend

The hosted Lexbeam MCP endpoint is not hard-wired. You can replace it with your own deployment built from:

- https://github.com/lexbeam-software/eu-ai-act-mcp

As long as your server preserves the same `euaiact_*` tool names and input/output contracts, the declarative agent routing logic remains unchanged and behaviour is functionally equivalent.

---

### 4. `appPackage/mcp-tools.json` — MCP Tool Descriptions

A static snapshot of the MCP server's `tools/list` response, bundled into the app package. This allows the orchestrator to understand the available tools without calling `tools/list` at runtime. Each tool includes `name`, `description`, and `inputSchema`.

> **Tip:** Re-run the Agents Toolkit *ATK: Fetch action from MCP* command to regenerate this file if the MCP server adds or changes tools.

---

### 5. Microsoft Word Integration

No extra manifest configuration is required for Word. Once the agent is deployed to your M365 tenant, it appears in the **Copilot sidebar** in Microsoft Word.

1. Open any document in **Microsoft Word** (desktop or web)
2. Open the **Copilot** pane
3. Click the **controls/settings icon with two sliders** (not the hamburger menu)
4. Select **EU AI Act Compliance Agent**

**Document workflow (demo):**
For predictable results, the recommended workflow for the demo is:
1. Upload the document to OneDrive/SharePoint
2. Open it in Microsoft Word
3. Copy the relevant sections and paste into the agent, or reference the document URL
4. The agent uses `OneDriveAndSharePoint` grounding to retrieve the document content

---

### 6. Ambiguity Protocol

When user intent is unclear (e.g., "Is this risky?"), the agent follows this protocol:

```
1. Do NOT call any tool yet.
2. Ask ONE targeted follow-up question, e.g.:
   "Could you describe the AI system and its intended use case?
    This will help me give you a precise EU AI Act classification."
3. Use the user's answer to determine the correct tool.
4. Call the tool with the enriched input.
5. Return the result in plain business language with article references.
```

---

### 7. Response Format

Every agent response follows this structure:

1. **Finding summary** — 2–3 sentences, plain business language
2. **Relevant articles and risk level** — where applicable
3. **Key obligations or compliance gaps**
4. **Recommended next steps**
5. **Disclaimer:** *"⚠️ This is an initial compliance assessment, not formal legal advice. Consult qualified legal counsel for binding decisions."*

---

### 8. Security and Data Privacy

- The MCP server is **read-only** — it returns regulatory content, not user data.
- No user data is stored by the MCP server. All inputs are transient.
- The Lexbeam MCP server is publicly hosted and free; no API key is transmitted.
- SharePoint grounding respects the **authenticated user's M365 permissions** — the agent cannot access files the user cannot access.
- The agent is deployed for **internal use only** via the M365 Admin Center org catalog.

---

## Attribution

The MCP server concept used in this agent implementation is credited to the original **Lexbeam Software** EU AI Act MCP server project.

- Source listing: https://smithery.ai/servers/lexbeam-software/eu-ai-act
- Author/publisher: https://www.lexbeam.com
