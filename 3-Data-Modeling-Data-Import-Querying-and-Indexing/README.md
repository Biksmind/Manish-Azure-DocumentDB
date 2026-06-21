# Module 3: Data Modeling, Data Import, Querying, and Indexing

This module creates collections, runs CRUD commands, imports data, runs aggregation, and creates indexes.

## Collections

| Collection | Purpose |
|---|---|
| `mobiles` | CRUD, aggregation, indexing, MobileAdvisor |
| `support_articles` | Import practice |
| `retail_offers` | RetailOfferFinder |
| `supportInc` | Search and RAG |

## Create collections

```javascript
use Workshop_DB

db.createCollection("mobiles")
db.createCollection("support_articles")
db.createCollection("retail_offers")
db.createCollection("supportInc")
```

## Load full sample data

```powershell
python .\scripts\load_workshop_data_base.py
```

Expected counts:

```text
mobiles: 30
support_articles: 30
retail_offers: 30
supportInc: 5
```

## Key skills practiced

- `insertMany`
- `find`
- projection
- `updateOne`
- `updateMany`
- `deleteOne`
- `deleteMany`
- aggregation with `$group`, `$avg`, `$sum`, `$sort`
- `explain("executionStats")`
- single-field and compound indexes

For update and delete operations, the runbook follows a beginner-safe pattern:

```text
find the record
  -> update or delete the record
  -> run find/count again to verify the result
```


For update and delete operations, the runbook follows a beginner-safe pattern:

```text
find the record
  -> update or delete the record
  -> run find/count again to verify the result
```
## Continue

The full copy/paste command sequence is in [the end-to-end runbook](../END-TO-END-WORKSHOP-RUNBOOK.md).

