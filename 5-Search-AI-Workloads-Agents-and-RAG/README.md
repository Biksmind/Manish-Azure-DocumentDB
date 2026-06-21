# Module 5: Search, AI Workloads, Agents, and RAG

This module uses `supportInc` for search/RAG and local scripts for AI demos.

## Goals

- Compare keyword search, full-text search, and vector search.
- Generate embeddings with Azure OpenAI.
- Create a vector index on Azure DocumentDB.
- Run semantic vector search.
- Run a simple RAG app.
- Run local AI agents from this repository only.
- Review MCP/Copilot, performance, security, and cleanup.

## Main commands

```powershell
python .\scripts\generate_workshop_embeddings.py
python .\scripts\create_workshop_indexes.py
python .\scripts\vector_search_support.py --query "I changed my password and cannot access my account"
python .\rag_app.py
python .\scripts\run_ai_agents.py
```

## MCP/Copilot demo

The repository includes a local MCP server:

```text
scripts\mcp_documentdb_server.py
```

VS Code can load an MCP JSON configuration that starts this script. Copilot can then call tools such as:

- `list_workshop_collections`
- `count_workshop_documents`

The MCP server reads the same local `.env` configuration and talks to Azure DocumentDB without requiring users to paste secrets into Copilot prompts.


## MCP/Copilot demo

The repository includes a local MCP server:

```text
scripts\mcp_documentdb_server.py
```

VS Code can load an MCP JSON configuration that starts this script. Copilot can then call tools such as:

- `list_workshop_collections`
- `count_workshop_documents`

The MCP server reads the same local `.env` configuration and talks to Azure DocumentDB without requiring users to paste secrets into Copilot prompts.
## Search concept summary

| Search type | Best for |
|---|---|
| Keyword search | Exact word or pattern matching |
| Full-text search | Word-based relevance and variations |
| Vector search | Meaning-based similarity |
| Hybrid search | Combining exact terms with semantic meaning |
| RAG | Retrieval from DocumentDB plus answer generation with Azure OpenAI |

## Continue

Use [the end-to-end runbook](../END-TO-END-WORKSHOP-RUNBOOK.md) for detailed copy/paste steps and explanations.

