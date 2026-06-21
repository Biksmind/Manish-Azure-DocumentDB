# Azure DocumentDB Workshop

A beginner-friendly, end-to-end Azure DocumentDB workshop for participants who may be new to Azure Portal, MongoDB commands, vector search, and RAG.

## Start here

Open the full participant guide:

[END-TO-END-WORKSHOP-RUNBOOK.md](END-TO-END-WORKSHOP-RUNBOOK.md)

## What you will build

You will create an Azure DocumentDB workshop environment with sample mobile catalog data, support articles, retail offers, a five-record search/RAG collection, vector search, a simple RAG app, and local AI agents.

## Workshop modules

| Module | Link | Focus |
|---|---|---|
| 1 | [Introduction to Azure DocumentDB](1-Introduction-to-Azure-DocumentDB/README.md) | Workshop overview and repo clone |
| 2 | [Cluster Setup and Connectivity](2-Azure-DocumentDB-Cluster-Setup-and-Connectivity/README.md) | Azure Portal setup, `.env`, VS Code, `mongosh` |
| 3 | [Data Modeling, Import, Querying, and Indexing](3-Data-Modeling-Data-Import-Querying-and-Indexing/README.md) | Collections, CRUD, import, aggregation, indexes |
| 4 | [Migration to Azure DocumentDB](4-Migration-to-Azure-DocumentDB/README.md) | Assessment, offline migration, online migration, cutover |
| 5 | [Search, AI Workloads, Agents, and RAG](5-Search-AI-Workloads-Agents-and-RAG/README.md) | Keyword, full-text, vector, hybrid, RAG, agents, MCP/Copilot |

## Repository structure

```text
Manish-Azure-DocumentDB
├── END-TO-END-WORKSHOP-RUNBOOK.md
├── README.md
├── requirements.txt
├── .env.template
├── sample-docs
├── scripts
├── 1-Introduction-to-Azure-DocumentDB
├── 2-Azure-DocumentDB-Cluster-Setup-and-Connectivity
├── 3-Data-Modeling-Data-Import-Querying-and-Indexing
├── 4-Migration-to-Azure-DocumentDB
└── 5-Search-AI-Workloads-Agents-and-RAG
```

## One-time environment file

All scripts use the same `.env` file:

```powershell
Copy-Item .env.template .env
notepad .env
python .\scripts\check_env.py
```

Do not commit `.env`.

## Collections

| Collection | Purpose |
|---|---|
| `mobiles` | CRUD, aggregation, indexing, and MobileAdvisor demos |
| `support_articles` | Import-from-file practice |
| `retail_offers` | Retail offer import and RetailOfferFinder demos |
| `supportInc` | Five-record keyword/full-text/vector/RAG learning collection |

No script clones or depends on another repository.
