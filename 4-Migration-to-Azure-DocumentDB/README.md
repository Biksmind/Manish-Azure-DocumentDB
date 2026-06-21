# Module 4: Migration to Azure DocumentDB

This module uses the Azure DocumentDB VS Code migration experience.

## Goals

- Connect to a source MongoDB environment.
- Run pre-migration assessment.
- Run offline migration.
- Observe online migration stages.
- Perform cutover after source workload stops.
- Validate target data.

## Migration stages

| Stage | Meaning |
|---|---|
| `Provisioning` | Azure prepares migration resources |
| `Bulk Copy In Progress` | Existing source data is copied |
| `Replication In Progress` | Source inserts, updates, and deletes are replicated |
| `Ready To Cutover` | Target is caught up |
| `Completing` | Cutover is finishing |
| `Succeeded` | Migration completed |

## Validation command

```javascript
use <your_database_name>
db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

## Security note

The instructor or sponsor provides temporary source connection details during the workshop. Do not commit source credentials to this repository.

## Continue

Use [the end-to-end runbook](../END-TO-END-WORKSHOP-RUNBOOK.md) for the detailed step-by-step migration flow.
