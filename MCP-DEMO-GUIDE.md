# Azure DocumentDB MCP Demo Guide

This is a standalone instructor-led demo for showing how an MCP server can connect to Azure DocumentDB and expose safe database tools.

Participants do **not** need GitHub Copilot access for this demo. The instructor can show the flow using VS Code MCP configuration and a simple manual PowerShell trigger.

## What this demo shows

You already created:

- Azure DocumentDB cluster
- `Workshop_DB`
- workshop collections
- `.env` file with connection details

This demo shows:

1. How to define an MCP server in `mcp.json`.
2. How the MCP server starts from VS Code or command line.
3. How authentication works through the existing `.env` file.
4. How an MCP client can call tools that talk to Azure DocumentDB.
5. How the MCP server returns database results such as collection names and document counts.

## Demo architecture

```text
MCP client or manual trigger
        |
        v
mcp.json starts Python MCP server
        |
        v
scripts\mcp_documentdb_server.py
        |
        v
Reads .env
        |
        v
Authenticates to Azure DocumentDB
        |
        v
Queries Workshop_DB collections
        |
        v
Returns tool results
```

## Files used

| File | Purpose |
|---|---|
| `.env` | Stores DocumentDB connection string and database name |
| `scripts\mcp_documentdb_server.py` | Local MCP server |
| `.vscode\mcp.json` | VS Code MCP server definition |

## Important security point

Do not paste the DocumentDB connection string into prompts, screenshots, or markdown files.

The MCP server authenticates by reading:

```text
DOCUMENTDB_CONNECTION_STRING
DOCUMENTDB_DATABASE
```

from the local `.env` file.

That means the MCP client only asks for an action, such as:

```text
List my workshop collections.
```

It does not need the password or connection string in the prompt.

---

# Part 1: Confirm `.env` exists

From the repository root, run:

```powershell
Get-ChildItem .env
python .\scripts\check_env.py
```

Expected:

```text
Environment check passed.
DOCUMENTDB_DATABASE=Workshop_DB
```

If `.env` is missing:

```powershell
Copy-Item .env.template .env
notepad .env
```

Fill in the DocumentDB connection details and save.

---

# Part 2: Confirm the MCP server file exists

Run:

```powershell
Get-ChildItem .\scripts\mcp_documentdb_server.py
```

The server exposes two demo tools:

| Tool | What it does |
|---|---|
| `list_workshop_collections` | Lists collections in `Workshop_DB` |
| `count_workshop_documents` | Counts documents in `mobiles`, `support_articles`, `retail_offers`, and `supportInc` |

---

# Part 3: Create VS Code MCP configuration

Create a folder named `.vscode` if it does not already exist:

```powershell
New-Item -ItemType Directory -Force .vscode
```

Create this file:

```text
.vscode\mcp.json
```

Paste this JSON:

```json
{
  "servers": {
    "azure-documentdb-workshop": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${workspaceFolder}\\scripts\\mcp_documentdb_server.py"
      ],
      "env": {
        "DOCUMENTDB_DATABASE": "Workshop_DB"
      }
    }
  }
}
```

## Explain the JSON

| JSON field | Meaning |
|---|---|
| `servers` | List of MCP servers VS Code can start |
| `azure-documentdb-workshop` | Friendly name for this MCP server |
| `type: stdio` | Client talks to the MCP server over standard input/output |
| `command: python` | Starts the MCP server with Python |
| `args` | Path to the local MCP server script |
| `env` | Optional environment values passed to the MCP server |

## What happens when this starts

```text
VS Code reads .vscode\mcp.json
  -> starts python scripts\mcp_documentdb_server.py
  -> MCP server reads .env
  -> MCP server connects to Azure DocumentDB
  -> tools become available to the MCP client
```

---

# Part 4: Trigger the MCP server manually without Copilot

Because participants may not have GitHub Copilot access, use this PowerShell trigger to demonstrate the MCP protocol directly.

Run from the repository root:

```powershell
$messages = @(
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"manual-demo","version":"1.0.0"}}}',
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}',
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}',
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_workshop_collections","arguments":{}}}',
  '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"count_workshop_documents","arguments":{}}}'
)

$messages | python .\scripts\mcp_documentdb_server.py
```

## What each message does

| Message | Purpose |
|---|---|
| `initialize` | Starts the MCP handshake |
| `notifications/initialized` | Tells the server initialization is complete |
| `tools/list` | Lists available tools |
| `tools/call: list_workshop_collections` | Calls the tool that lists DocumentDB collections |
| `tools/call: count_workshop_documents` | Calls the tool that counts workshop documents |

## Expected output

You should see JSON-RPC responses. The exact IDs and formatting may vary, but the important parts look like this:

```json
{
  "tools": [
    {
      "name": "list_workshop_collections"
    },
    {
      "name": "count_workshop_documents"
    }
  ]
}
```

For collection listing:

```json
{
  "database": "Workshop_DB",
  "collections": [
    "mobiles",
    "retail_offers",
    "supportInc",
    "support_articles"
  ]
}
```

For document counts:

```json
{
  "database": "Workshop_DB",
  "counts": {
    "mobiles": 30,
    "support_articles": 30,
    "retail_offers": 30,
    "supportInc": 5
  }
}
```

## How to explain this to participants

Say:

> This is the same idea as an AI assistant calling a tool. Instead of giving the assistant our connection string, we define a safe local MCP server. The MCP server reads `.env`, authenticates to Azure DocumentDB, runs approved operations, and returns only the result.

---

# Part 5: Optional VS Code MCP demo

If the instructor has an MCP-capable VS Code setup, open the MCP tools panel or MCP-capable chat surface and select the `azure-documentdb-workshop` server.

Use prompts like:

```text
List the collections in my Azure DocumentDB workshop database.
```

```text
Count documents in the workshop collections.
```

Expected behavior:

```text
Prompt
  -> MCP client chooses a tool
  -> MCP server runs the tool
  -> Tool connects to Azure DocumentDB using .env
  -> Tool returns collection names or counts
```

## What not to do

Do not ask participants to paste:

- DocumentDB connection string
- username
- password
- Azure OpenAI key

into any prompt.

---

# Troubleshooting

## `DOCUMENTDB_CONNECTION_STRING` missing

Fix `.env`:

```powershell
notepad .env
```

Then rerun:

```powershell
python .\scripts\check_env.py
```

## Authentication failed

Copy the connection string again from Azure Portal and update `.env`.

## Network timeout

Confirm the DocumentDB firewall/networking settings allow the workshop VM.

## Tool returns zero documents

Load workshop data:

```powershell
python .\scripts\load_workshop_data_base.py
```

Then rerun the manual MCP trigger.

## Python package missing

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# Demo summary

The MCP demo proves this:

```text
MCP can expose controlled database tools.
The server can authenticate using local configuration.
The user can ask for database actions without seeing or sharing secrets.
Azure DocumentDB returns real collection and document data through the MCP tool.
```
