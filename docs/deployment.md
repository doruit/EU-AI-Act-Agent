# Deployment Guide

## Prerequisites

| Requirement | Details |
|---|---|
| **VS Code** | Latest stable version |
| **Microsoft 365 Agents Toolkit** | VS Code extension v6.3 or later — [install](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.ms-teams-vscode-extension) |
| **M365 Copilot license** | Required for the user testing the agent (Microsoft 365 Copilot or Microsoft 365 Copilot Chat license) |
| **M365 tenant admin access** | Required for publishing to the org catalog |
| **Python 3.x** | Only needed to regenerate placeholder icons via `scripts/generate-icons.py` |
| **Node.js 18+** | Recommended for Agents Toolkit CLI features |

---

## Step 1 — Clone the repository

```bash
git clone https://github.com/your-org/EU-AI-Act-Agent.git
cd EU-AI-Act-Agent
```

---

## Step 2 — Open in VS Code

```bash
code .
```

Install the **Microsoft 365 Agents Toolkit** extension if not already installed:
- Open the Extensions panel (`Cmd+Shift+X`)
- Search for `Microsoft 365 Agents Toolkit`
- Install it

---

## Step 3 — Sign in to your M365 tenant

1. Open the **Agents Toolkit** panel in VS Code (puzzle piece icon in the Activity Bar)
2. Under **Accounts**, click **Sign in to Microsoft 365**
3. Complete the browser authentication flow
4. Confirm your tenant appears under **Microsoft 365 account**

---

## Step 4 — (Optional) Refresh MCP tool definitions

If you want to re-fetch the latest tool definitions from the Lexbeam MCP server:

1. Open `.vscode/mcp.json` in VS Code
2. Click the **Start** button that appears above the `eu-ai-act` server entry
3. In the Agents Toolkit panel, select **ATK: Fetch action from MCP**
4. Select all 9 `euaiact_*` tools
5. Choose auth type: **None**
6. The toolkit will update `appPackage/ai-plugin.json` and `appPackage/mcp-tools.json`

> ℹ️ This step is optional — the repository already contains the correct tool definitions. Only needed if the MCP server changes its tool list.

---

## Step 5 — Provision the app

This step creates the Teams app registration in the M365 Developer Portal and generates a `TEAMS_APP_ID`.

1. Open the **Agents Toolkit** panel
2. Under **Lifecycle**, click **Provision**
3. Select environment: **dev**
4. Confirm the prompts — the toolkit will:
   - Create a Teams app registration
   - Zip the app package to `appPackage/build/appPackage.dev.zip`
   - Validate the package
   - Update `env/.env.dev` with the generated `TEAMS_APP_ID`

---

## Step 6 — Test locally (Developer Mode)

1. Press **F5** in VS Code (or select **Run → Start Debugging**)
2. Choose **Preview in Microsoft 365 Copilot (Edge)**
3. Your browser opens `https://m365.cloud.microsoft/chat`
4. Find **EU AI Act Compliance Agent** in the Copilot sidebar (☰ → agent list)
5. Test with prompts from `tests/test-cases.md`
6. Use the browser DevTools or Agents Toolkit output panel to inspect which tool was called

**Test in Word on the Web:**
1. Use the **Preview in Word on the Web (Edge)** launch configuration
2. Open any Word document (or create a new one)
3. Click **Copilot** in the ribbon → ☰ → **EU AI Act Compliance Agent**
4. Try: *"Scan this document and identify EU AI Act compliance gaps"*

---

## Step 7 — Publish to your organization

This step submits the app to the M365 Admin Center for internal distribution.

1. Open the **Agents Toolkit** panel
2. Under **Lifecycle**, click **Publish**
3. The toolkit submits `appPackage/build/appPackage.dev.zip` to your org's app catalog

**Approve in the M365 Admin Center:**
1. Go to [https://admin.microsoft.com](https://admin.microsoft.com)
2. Navigate to **Settings → Integrated apps**
3. Find **EU AI Act Agent** in the pending apps list
4. Click **Deploy** → approve for all users (or specific groups)

After approval, the agent appears automatically in:
- M365 Copilot Chat (`https://m365.cloud.microsoft/chat`)
- Word on the Web (`https://word.cloud.microsoft`)
- Teams, Outlook, PowerPoint (same deployment, no extra steps)

---

## Step 8 — (Optional) Scope SharePoint grounding

By default, the `OneDriveAndSharePoint` capability is unscoped — the agent can search all SharePoint sites and OneDrive content the user has access to. To scope it to a specific site (recommended for production):

1. Open `appPackage/declarativeAgent.json`
2. Replace the `OneDriveAndSharePoint` capability entry:

```json
{
  "name": "OneDriveAndSharePoint",
  "items_by_url": [
    {
      "url": "https://yourorg.sharepoint.com/sites/AIComplianceReviews"
    }
  ]
}
```

3. Re-run **Provision** and **Publish**.

---

## Step 9 — (Optional) Swap Lexbeam hosted MCP with your own server

You can run your own EU AI Act MCP backend with the same functionality using:

- https://github.com/lexbeam-software/eu-ai-act-mcp

Then point this agent to your endpoint:

1. Update `appPackage/ai-plugin.json`:
  - `runtimes[0].spec.url` → your MCP server URL
2. Update `.vscode/mcp.json`:
  - `servers.eu-ai-act.url` → the same URL
3. (Recommended) Re-fetch MCP actions/tools in Agents Toolkit
4. Re-run **Provision** (if required by your environment) and **Deploy/Publish**

If your server keeps the same `euaiact_*` tool names and schemas, no routing logic changes are required in `declarativeAgent.json`.

---

## Updating the agent

After making changes to `declarativeAgent.json`, `ai-plugin.json`, or `mcp-tools.json`:

1. In the Agents Toolkit panel, click **Deploy** (not Provision — this skips app registration)
2. Test in Developer Mode (F5)
3. Re-publish if satisfied

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Agent not appearing in Word | Wait 5–10 min for M365 cache to refresh, then reload Word |
| Tool not being called | Check `description_for_model` in `ai-plugin.json`; see routing log in `tests/test-cases.md` |
| App package validation fails | Run `teamsApp/validateAppPackage` step manually in `teamsapp.yml`; check icon sizes (192×192 and 32×32 required) |
| `TEAMS_APP_ID` empty | Re-run **Provision** — the toolkit populates this automatically |
| MCP server unreachable | Check status at `https://smithery.ai/servers/lexbeam-software/eu-ai-act` |
| Instructions not followed | The `instructions` field has an 8,000-char limit; verify content is not truncated |
| SharePoint content not found | Ensure the target documents are indexed by Microsoft Search; check user permissions |

---

## Regenerating Icons

```bash
# From the repo root:
python3 -m venv .venv
source .venv/bin/activate
pip install Pillow
python scripts/generate-icons.py
```

Replace the generated placeholder icons with your own branded versions before publishing to production.
The icons must be:
- `appPackage/color.png` — 192 × 192 px, full color, PNG
- `appPackage/outline.png` — 32 × 32 px, monochrome (white on transparent), PNG

---

## Attribution requirement

When publishing a forked or modified version of this project, keep attribution to the original **Lexbeam Software** MCP server concept and EU AI Act tooling source:

- https://smithery.ai/servers/lexbeam-software/eu-ai-act
- https://www.lexbeam.com
