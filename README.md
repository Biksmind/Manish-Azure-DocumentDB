# Azure DocumentDB Workshop (V2)

This repository is organized as an end-to-end, slot-wise workshop path.

## Start here

If you are attending or running the workshop, start with the end-to-end runbook:

- [END-TO-END-WORKSHOP-RUNBOOK.md](END-TO-END-WORKSHOP-RUNBOOK.md)

This runbook covers all modules with step-by-step hands-on details from setup to migration, search, agents, and wrap-up.

## What we are building

You will build and validate this complete flow:

```text
Introduction and architecture
  -> Azure DocumentDB cluster setup and connectivity
  -> data modeling, data import, querying, query planning, aggregation, and indexing
  -> MongoDB to Azure DocumentDB migration
  -> full-text, vector, and hybrid search
  -> AI workloads, agents, and RAG patterns
  -> MCP Server + GitHub Copilot updates
```

## Full-day agenda

| Time | Session | Focus |
|---|---|---|
| 09:30-10:15 | Slot 1 | Introduction and Azure DocumentDB overview |
| 10:15-11:15 | Hands-on Lab | Cluster setup and connectivity |
| 11:15-13:00 | Slot 2 | Data modeling, data import, querying, query planning, aggregation framework, and indexing |
| 13:00-13:30 | Break | Lunch break |
| 13:30-14:15 | Slot 3 | MongoDB to Azure DocumentDB migration |
| 14:15-15:15 | Hands-on Lab | Migration using VS Code extension and mongodump/mongorestore |
| 15:15-16:00 | Slot 4 | Search capabilities, AI workloads and agents, and RAG patterns |
| 16:00-17:00 | Hands-on Lab | Full-text search, vector search, hybrid search, and RAG patterns |
| 17:00-17:15 | Updates | MCP Server + GitHub Copilot integration and latest updates |
| 17:15-17:30 | Close | Wrap-up and Q&A |

## Module structure (agenda-aligned)

1. [Module 1: Introduction to Azure DocumentDB](1-Introduction-to-Azure-DocumentDB/README.md)
2. [Module 2: Azure DocumentDB Cluster Setup and Connectivity](2-Azure-DocumentDB-Cluster-Setup-and-Connectivity/README.md)
3. [Module 3: Data Modeling, Data Import, Querying, Query Planning, Aggregation Framework and Indexing](3-Data-Modeling-Data-Import-Querying-and-Indexing/README.md)
4. [Module 4: Migration to Azure DocumentDB](4-Migration-to-Azure-DocumentDB/README.md)
5. [Module 5: Search Capabilities, AI Workloads, Agents and RAG Patterns](5-Search-AI-Workloads-Agents-and-RAG/README.md)

Each module includes a step-by-step hands-on README.

> Note: The primary learning path is the 5 modules listed above.

## End-to-end run order

Follow modules in this exact order:

1. Module 1
2. Module 2
3. Module 3
4. Module 4
5. Module 5

## Prerequisites

- Azure subscription
- VS Code
- Python 3.10 or later
- Git
- MongoDB Shell (`mongosh`)
- Access to Azure AI Foundry or Azure OpenAI (for Slot 4)

For vector search, use Azure DocumentDB M30 or higher.

## Existing technical asset folders

The repository also contains implementation assets used by module steps:

- `scripts/`
- `sample-docs/`

These are used by the module READMEs as part of the hands-on path.

## Cleanup after workshop

1. Stop local applications.
2. Remove temporary firewall rules.
3. Delete or scale down workshop resources if no longer needed.
4. Keep secrets out of commits.
