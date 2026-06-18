# EU AI Act Compliance Agent for Microsoft 365 Copilot

> A **Microsoft 365 Declarative Agent** that helps your organization understand and comply with EU AI Act Regulation (EU) 2024/1689 — powered by the [Lexbeam EU AI Act MCP server](https://smithery.ai/servers/lexbeam-software/eu-ai-act).

---

## What this agent does

The agent is available inside **M365 Copilot Chat**, **Microsoft Word** (via the Copilot sidebar), and as a **standalone agent experience**. Colleagues can ask compliance questions in plain language and receive structured, business-readable answers with relevant article references.

The agent uses 9 specialised MCP tools — it never answers EU AI Act questions from generic model knowledge when a relevant tool is available.

### Example questions you can ask

| Question | Tool used |
|---|---|
| "Classify this AI system under the EU AI Act." | Risk classification |
| "Scan this document and identify EU AI Act compliance gaps." | Risk classification |
| "Which obligations apply to us as the deployer?" | Obligations by role |
| "Does this solution qualify as high-risk AI under Annex III?" | Risk classification |
| "Which documentation is still missing for EU AI Act compliance?" | Annex IV checklist |
| "Can we rely on the Article 6(3) no-significant-risk exception?" | Art. 6(3) exception |
| "Which EU AI Act deadlines are relevant for this application?" | Deadlines |
| "What is the maximum fine exposure for non-compliance?" | Penalty calculator |
| "Does this model qualify as GPAI with systemic risk?" | GPAI systemic risk |
| "Summarize Article 9 of the EU AI Act." | Article text |

For ambiguous questions like *"Is this risky?"* or *"Can we launch this in Europe?"*, the agent asks a single clarifying follow-up question before proceeding.

---

## Architecture

```
User (M365 Copilot Chat / Word on the Web)
       │
       ▼
M365 Copilot Orchestrator
(declarativeAgent.json — instructions + routing policy)
       │
       ▼
ai-plugin.json (Plugin Manifest v2.4, RemoteMCPServer)
       │  HTTP POST
       ▼
Lexbeam EU AI Act MCP Server
https://eu-ai-act--lexbeam-software.run.tools
(9 tools, free, no API key required)
```

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram and component details.

---

## Repository structure

```
EU-AI-Act-Agent/
├── appPackage/
│   ├── manifest.json           ← M365 App Manifest (v1.18)
│   ├── declarativeAgent.json   ← Agent manifest + instructions + routing policy
│   ├── ai-plugin.json          ← Plugin manifest (v2.4) — MCP server connection
│   ├── mcp-tools.json          ← MCP tool definitions (static snapshot)
│   ├── color.png               ← App icon 192×192 (replace with your own)
│   └── outline.png             ← App icon 32×32 (replace with your own)
├── .vscode/
│   ├── mcp.json                ← MCP server config for development
│   ├── launch.json             ← Debug configurations (Copilot Chat + Word on Web)
│   └── settings.json           ← JSON schema associations
├── env/
│   ├── .env.dev                ← Environment variables (safe to commit)
│   └── .env.dev.user           ← User-specific vars (gitignored)
├── scripts/
│   └── generate-icons.py       ← Generates placeholder app icons
├── tests/
│   └── test-cases.md           ← 32 test prompts mapped to expected tools
├── docs/
│   ├── architecture.md         ← System architecture and component details
│   └── deployment.md           ← Step-by-step deployment guide
├── teamsapp.yml                ← M365 Agents Toolkit lifecycle config
├── .gitignore
└── README.md
```

---

## MCP Tools

The agent integrates these 9 tools from the [Lexbeam EU AI Act MCP server](https://smithery.ai/servers/lexbeam-software/eu-ai-act):

| Tool | Purpose |
|---|---|
| `euaiact_classify_system` | Classify AI system risk level (Prohibited / High-risk / Limited / Minimal) |
| `euaiact_check_deadlines` | Return all implementation milestones with days remaining |
| `euaiact_get_obligations` | Obligations by role (provider, deployer, importer, distributor) and risk level |
| `euaiact_answer_question` | General EU AI Act FAQ with article references |
| `euaiact_calculate_penalty` | Maximum fine under Article 99, with SME/startup reduction |
| `euaiact_get_article` | Article text and EUR-Lex URL for Articles 3–6, 9–17, 26, 27, 43, 47, 49–51, 53, 55, 72, 73, 99, 100, 113 |
| `euaiact_check_gpai_systemic_risk` | GPAI / foundation model systemic risk under Article 51 |
| `euaiact_assess_art6_3_exception` | Article 6(3) no-significant-risk exception for Annex III systems |
| `euaiact_annex_iv_checklist` | Annex IV technical documentation checklist (Article 11) |

**MCP server:** `https://eu-ai-act--lexbeam-software.run.tools`
**Auth:** None required — free, no API key

---

## Swap in your own MCP server (same functionality)

The current hosted Lexbeam MCP endpoint can be replaced with **your own MCP server** that provides the exact same EU AI Act tools.

Use the official open-source implementation:
- https://github.com/lexbeam-software/eu-ai-act-mcp

If your self-hosted server keeps the same `euaiact_*` tool names and schemas, this agent works the same way. In this repo, you only need to update the MCP endpoint URL in:

- `appPackage/ai-plugin.json` → `runtimes[0].spec.url`
- `.vscode/mcp.json` → `servers.eu-ai-act.url`

Then refresh tool metadata (if needed) and re-provision/re-deploy.

---

## Quick start

### Prerequisites

- VS Code with [Microsoft 365 Agents Toolkit](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.ms-teams-vscode-extension) (v6.3+)
- Microsoft 365 Copilot license
- M365 tenant admin access (for publishing)

### Deploy in 3 steps

```bash
# 1. Clone
git clone https://github.com/your-org/EU-AI-Act-Agent.git
cd EU-AI-Act-Agent
code .

# 2. Sign in to M365 via the Agents Toolkit panel

# 3. Agents Toolkit → Lifecycle → Provision → then F5 to preview
```

See [docs/deployment.md](docs/deployment.md) for the complete step-by-step guide including Microsoft Word setup, SharePoint scoping, and publishing to the org catalog.

---

## Using the agent in Microsoft Word

1. Open any document in **Microsoft Word** (desktop or web)
2. Open the **Copilot** pane
3. Click the **controls/settings icon with two sliders** to open agent selection (**not** the hamburger icon)
4. Select **EU AI Act Compliance Agent**
5. Ask: *"Scan this document and identify EU AI Act compliance gaps."*

> **Note:** The agent uses `OneDriveAndSharePoint` grounding to search your organization's SharePoint and OneDrive content. For the best results on a specific document, upload it to SharePoint/OneDrive first.

---

## Screenshots

### Standalone agent

The agent can also be used as a standalone experience.

![EU AI Act standalone agent](media/stand-alone-agent.png)

### Teams conversations (add-in agent)

Use the agent directly in Teams conversations.

![EU AI Act agent in Teams conversation](media/add-in-agent.png)

### Office apps like Word (agent selection flow)

This screenshot shows how to use/select the agent in Office apps such as Microsoft Word.

![EU AI Act agent in Office apps like Word](media/word-add-in-agent.png)

---

## Testing

See [tests/test-cases.md](tests/test-cases.md) for 32 test prompts covering:
- 22 standard single-tool cases
- 6 ambiguous cases (agent must ask a clarifying question)
- 4 compound multi-tool cases

Use VS Code Developer Mode (F5) to verify tool routing and log results.

---

## Customisation

### Scoping SharePoint grounding

Edit the `OneDriveAndSharePoint` capability in `appPackage/declarativeAgent.json`:

```json
{
  "name": "OneDriveAndSharePoint",
  "items_by_url": [
    { "url": "https://yourorg.sharepoint.com/sites/AIComplianceReviews" }
  ]
}
```

### Updating tool routing rules

Edit the `instructions` field in `appPackage/declarativeAgent.json`.
Max 8,000 characters. See [docs/architecture.md](docs/architecture.md) for the routing policy design.

### Replacing the icons

Replace `appPackage/color.png` (192×192) and `appPackage/outline.png` (32×32) with your own branded icons.
To regenerate the placeholder icons:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install Pillow
python scripts/generate-icons.py
```

---

## About the MCP server

The [Lexbeam EU AI Act MCP server](https://smithery.ai/servers/lexbeam-software/eu-ai-act) is published by [Lexbeam Software](https://www.lexbeam.com) and covers EU AI Act Regulation (EU) 2024/1689 in full, including the Digital Omnibus simplification proposal.

- **Free** — no API key required
- **Quality score:** 97/100 (Smithery)
- **Avg latency:** ~107ms
- **Uptime:** 97.6%

---

## Attribution and credits

This project's MCP integration approach and tool taxonomy are based on the original **Lexbeam EU AI Act MCP server** concept and implementation.

- Original server/author: **Lexbeam Software**
- Smithery listing: https://smithery.ai/servers/lexbeam-software/eu-ai-act

If you fork or reuse this repository, keep this attribution section and credit Lexbeam Software for the MCP server concept and underlying EU AI Act tooling.

---

## License

MIT — see `LICENSE` for details.

---

## Contributing

Pull requests and issues are welcome. If you find a routing failure or a missing test case, open an issue or submit a PR with an update to `tests/test-cases.md` and the relevant `declarativeAgent.json` fix.
