# Module 2: Azure DocumentDB Cluster Setup and Connectivity

Duration: 10:15-11:15

This module sets up the Azure DocumentDB cluster and validates connectivity from VS Code and `mongosh`.

## Learning outcomes

By the end of this module, you will be able to:

- Provision an Azure DocumentDB cluster.
- Configure firewall/network access.
- Connect from VS Code and create `Workshop_DB`.
- Validate connectivity and basic database health.

## Step-by-step hands-on

### Step 1: Create Azure DocumentDB cluster

1. Open `https://portal.azure.com`.
2. Search for **Azure DocumentDB**.
3. Create a new cluster with:
   - MongoDB version: latest available
   - Tier: M30 or higher
   - High availability: off for workshop
4. Wait until deployment completes.

### Step 2: Configure network access

1. Open the cluster in Azure Portal.
2. Go to **Networking**.
3. Add current client IP.
4. Save settings and wait for update completion.

### Step 3: Copy connection string

1. Open **Connection strings** in the Azure DocumentDB resource.
2. Copy primary/global read-write connection string.
3. Keep it ready for `.env` and VS Code connection.

### Step 4: Connect from VS Code

1. Install **DocumentDB for VS Code** extension.
2. Add new connection using connection string.
3. Ensure the connection string has `authMechanism=SCRAM-SHA-256`.
4. Confirm cluster appears in the extension panel.

### Step 5: Create `Workshop_DB`

1. Right-click cluster in VS Code extension.
2. Select **Create Database...**
3. Enter `Workshop_DB`.
4. Refresh the cluster tree.

### Step 6: Validate in Query Playground

Run:

```javascript
use('Workshop_DB')
db.runCommand({ ping: 1 })
show collections
db.stats()
```

Expected: ping response includes `{ ok: 1 }`.

### Step 7: Validate in mongosh

```powershell
mongosh "<your_connection_string>"
```

Then run:

```javascript
use Workshop_DB
db.runCommand({ ping: 1 })
exit
```

## Expected result

Azure DocumentDB cluster is provisioned, reachable from your machine, and `Workshop_DB` is ready for data load.

## Next module

Continue to:

- `../3-Data-Modeling-Data-Import-Querying-and-Indexing/README.md`
