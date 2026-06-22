# Module 5: Search, AI Workloads, Agents, and RAG

This module uses `supportInc` for search/RAG and local Agent Framework DevUI agents for the mobile shopping experience.

## Goals

- Compare keyword search, full-text search, and vector search.
- Generate embeddings with Azure OpenAI.
- Create vector indexes on Azure DocumentDB.
- Run semantic vector search.
- Run a simple RAG app.
- Run local Agent Framework DevUI agents from this repository only.
- Review MCP/Copilot, performance, security, and cleanup.

## Main commands

```powershell
python .\scripts\generate_workshop_embeddings.py
python .\scripts\create_workshop_indexes.py
python .\scripts\vector_search_support.py --query "I changed my password and cannot access my account"
python .\rag_app.py
python .\scripts\run_ai_agents.py
```

`generate_workshop_embeddings.py` prepares both:

- `supportInc.embedding` for vector search and RAG
- `mobiles.contentVector` for MobileAdvisor semantic recommendations

`create_workshop_indexes.py` creates vector indexes for both collections.

## Local AI agents

The agent app is self-contained in this repository. It does not clone or reference any external repo.

| Agent | What it does | Tools |
|---|---|---|
| `MobileAdvisor` | Recommends phones from `mobiles` | semantic recommendation, budget search, details lookup |
| `RetailOfferFinder` | Finds offers from `retail_offers` | offer lookup, retailer search |

The flow is:

```text
Prompt
  -> Azure OpenAI chat model chooses a tool
  -> Python tool queries Azure DocumentDB
  -> Tool result returns to the model
  -> Model formats the final answer
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
