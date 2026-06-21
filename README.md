# Azure DocumentDB Workshop

This repository contains a beginner-friendly Azure DocumentDB workshop.

Start here:

```text
END-TO-END-WORKSHOP-RUNBOOK.md
```

The workshop uses one `.env` file for all scripts.

```powershell
Copy-Item .env.template .env
notepad .env
```

Main collections:

| Collection | Purpose |
|---|---|
| `mobiles` | CRUD, aggregation, indexing, and mobile advisor demos |
| `support_articles` | Import-from-file practice |
| `retail_offers` | Import-from-file practice and retail offer agent |
| `supportInc` | Five-record search, vector search, and RAG learning collection |

No script clones or depends on another repository.
