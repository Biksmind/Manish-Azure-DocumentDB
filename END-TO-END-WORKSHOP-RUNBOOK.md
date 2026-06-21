# Azure DocumentDB Workshop Participant Guide

## Workshop overview

In this workshop, you will create an Azure DocumentDB cluster, connect from VS Code and `mongosh`, load sample data, run basic CRUD commands, create indexes, run migration steps, explore search and RAG, run local AI agents, review performance/security, and clean up.

This guide is written so a first-time Azure Portal user can follow it step by step.

## Collections used in this workshop

| Collection | Records | How data is loaded | Purpose |
|---|---:|---|---|
| `mobiles` | 5 manual demo records, or 30 sample records | `insertMany` first, script later | CRUD, aggregation, indexing, MobileAdvisor |
| `support_articles` | 30 | Import from `sample-docs` | File import practice |
| `retail_offers` | 30 | Import from `sample-docs` | RetailOfferFinder |
| `supportInc` | 5 | Script or copy/paste | Keyword, full-text, vector search, and RAG |

All scripts use the same `.env` file. You only enter connection details and Azure OpenAI details once.

## Full-day agenda

| Time | Session | Focus |
|---|---|---|
| 09:30-10:15 | Slot 1 | Introduction and Azure DocumentDB overview |
| 10:15-11:15 | Hands-on Lab | Cluster setup and connectivity |
| 11:15-13:00 | Slot 2 | Data modeling, import, CRUD, query planning, aggregation, and indexing |
| 13:00-13:30 | Break | Lunch break |
| 13:30-14:15 | Slot 3 | MongoDB to Azure DocumentDB migration |
| 14:15-15:15 | Hands-on Lab | Migration using VS Code extension; optional `mongodump`/`mongorestore` instructor demo |
| 15:15-16:00 | Slot 4 | Search capabilities, AI workloads, agents, and RAG patterns |
| 16:00-17:00 | Hands-on Lab | Full-text search, vector search, hybrid search, and RAG |
| 17:00-17:15 | Updates | MCP Server plus GitHub Copilot integration and latest updates |
| 17:15-17:30 | Close | Wrap-up and Q&A |

---

# Module 0: Verify prerequisites

Open PowerShell and run:

```powershell
code --version
python --version
mongosh --version
git --version
```

If all commands return versions, continue.

If a command is not found, install the missing tool:

```powershell
winget install --id Microsoft.VisualStudioCode --exact --source winget
winget install --id Python.Python.3.10 --exact --source winget
winget install --id MongoDB.Shell --exact --source winget
winget install --id Git.Git --exact --source winget
```

Close and reopen PowerShell, then run the version checks again.

---

# Module 1: Clone the workshop repository

1. Open **VS Code**.
2. Press `Ctrl+Shift+P`.
3. Type:

   ```text
   Git: Clone
   ```

4. Paste:

   ```text
   https://github.com/Biksmind/Manish-Azure-DocumentDB.git
   ```

5. Choose a local folder on your workshop VM, for example:

   ```text
   C:\Users\<your-user-name>\Documents
   ```

6. Click **Open** when VS Code asks whether to open the cloned repository.
7. Open **Terminal > New Terminal**.
8. Confirm you are in the repository root:

   ```powershell
   Get-ChildItem
   ```

You should see:

```text
END-TO-END-WORKSHOP-RUNBOOK.md
requirements.txt
.env.template
sample-docs
scripts
```

---

# Module 2: Create Azure DocumentDB

## 2.1 Open Azure Portal

1. Open a browser.
2. Go to:

   ```text
   https://portal.azure.com
   ```

3. Sign in.
4. Wait for the Azure Portal home page to load.

## 2.2 Start DocumentDB creation

1. Use the top search bar.
2. Type:

   ```text
   Azure DocumentDB
   ```

3. Click **Azure DocumentDB with MongoDB compatibility**.
4. Click **Create**.

## 2.3 Fill the Basics page

Use the values provided by your instructor or sponsor.

| Field | Value |
|---|---|
| Subscription | Select your assigned subscription |
| Resource group | Use the assigned resource group; create one only if sponsor confirms |
| Cluster name | `az-docdb-workshop-<yourname>` |
| Region | Use the instructor-provided region |
| MongoDB version | Latest available |
| High availability | Disabled for workshop |
| Cluster tier | Use instructor-provided tier; vector search may require M30 or higher |
| Storage | 128 GB |

Click **Review + create**, then **Create**.

Wait for deployment to complete, then click **Go to resource**.

## 2.4 Configure networking

1. Open your DocumentDB resource.
2. Click **Networking**.
3. Select access from selected IP addresses.
4. Click **Add current client IP address**.
5. Click **Save**.

Do not use a broad IP range such as `0.0.0.0 - 255.255.255.255` unless the instructor explicitly asks for temporary lab access.

## 2.5 Copy connection string

1. In the DocumentDB resource, click **Connection strings**.
2. Copy the primary or global read-write connection string.
3. Keep it temporarily. You will paste it into `.env`.

Example format:

```text
mongodb+srv://<username>:<password>@<cluster-name>.mongocluster.cosmos.azure.com/?tls=true
```

Do not share real connection strings in screenshots, chat, slides, or commits.

---

# Module 3: One-time local environment setup

Run these commands from the repository root.

## 3.1 Create Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3.2 Create `.env`

```powershell
Copy-Item .env.template .env
notepad .env
```

Fill in the values:

```text
DOCUMENTDB_CONNECTION_STRING=<paste-your-documentdb-connection-string>
DOCUMENTDB_DATABASE=Workshop_DB

AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<paste-your-azure-openai-key>
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4.1-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

Important:

- Do not add quotes.
- Do not add spaces before or after `=`.
- Save the file.
- Do not commit `.env`.

## 3.3 Check `.env`

```powershell
python .\scripts\check_env.py
```

Expected:

```text
Environment check passed.
DOCUMENTDB_DATABASE=Workshop_DB
```

---

# Module 4: Connect to Azure DocumentDB

## 4.1 Connect from VS Code

1. In VS Code, click **Extensions**.
2. Search:

   ```text
   DocumentDB for VS Code
   ```

3. Install the Microsoft DocumentDB extension.
4. Click the **DocumentDB** icon.
5. Click **Add New Connection**.
6. Select **Connection String**.
7. Paste the DocumentDB connection string.
8. Press **Enter**.

## 4.2 Connect from mongosh

Print the command from `.env`:

```powershell
python .\scripts\print_mongosh_command.py
```

Copy and run the printed `mongosh` command.

Inside `mongosh`, run:

```javascript
use Workshop_DB
db.runCommand({ ping: 1 })
```

Expected:

```javascript
{ ok: 1 }
```

---

# Module 5: Create collections

Inside `mongosh`, run:

```javascript
use Workshop_DB

db.createCollection("mobiles")
db.createCollection("support_articles")
db.createCollection("retail_offers")
db.createCollection("supportInc")

show collections
```

Expected:

```text
mobiles
retail_offers
supportInc
support_articles
```

---

# Module 6: Basic query and CRUD using `mobiles`

This first lab uses manual `insertMany` so you can see exactly what is inserted.

## 6.1 Insert records

```javascript
db.mobiles.insertMany([
  {
    productId: "MOB-001",
    title: "Samsung Galaxy S24",
    brand: "Samsung",
    segment: "Premium",
    priceInr: 74999,
    ramGb: 8,
    storageGb: 256,
    cameraMp: 50,
    batteryMah: 4000,
    inStock: true
  },
  {
    productId: "MOB-002",
    title: "OnePlus 12",
    brand: "OnePlus",
    segment: "Premium",
    priceInr: 64999,
    ramGb: 12,
    storageGb: 256,
    cameraMp: 50,
    batteryMah: 5400,
    inStock: true
  },
  {
    productId: "MOB-003",
    title: "iPhone 15",
    brand: "Apple",
    segment: "Premium",
    priceInr: 79999,
    ramGb: 6,
    storageGb: 128,
    cameraMp: 48,
    batteryMah: 3349,
    inStock: true
  },
  {
    productId: "MOB-004",
    title: "Redmi Note 13 Pro",
    brand: "Redmi",
    segment: "Mid Range",
    priceInr: 25999,
    ramGb: 8,
    storageGb: 128,
    cameraMp: 200,
    batteryMah: 5100,
    inStock: true
  },
  {
    productId: "MOB-005",
    title: "Realme Narzo 70",
    brand: "Realme",
    segment: "Budget",
    priceInr: 14999,
    ramGb: 6,
    storageGb: 128,
    cameraMp: 50,
    batteryMah: 5000,
    inStock: false
  }
])
```

## 6.2 Count records

```javascript
db.mobiles.countDocuments()
```

Expected:

```text
5
```

## 6.3 Find records

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, brand: 1, priceInr: 1, segment: 1 }
).limit(5)
```

## 6.4 Insert temporary records for delete demo

```javascript
db.mobiles.insertMany([
  {
    productId: "TEMP-001",
    title: "Temporary Demo Phone 1",
    brand: "Demo",
    segment: "Demo",
    priceInr: 9999,
    inStock: true
  },
  {
    productId: "TEMP-002",
    title: "Temporary Demo Phone 2",
    brand: "Demo",
    segment: "Demo",
    priceInr: 10999,
    inStock: true
  }
])
```

## 6.5 Update one record

```javascript
db.mobiles.updateOne(
  { productId: "MOB-005" },
  { $set: { inStock: true, updatedBy: "workshop" } }
)
```

Verify:

```javascript
db.mobiles.find(
  { productId: "MOB-005" },
  { _id: 0, productId: 1, title: 1, inStock: 1, updatedBy: 1 }
)
```

## 6.6 Update many records

```javascript
db.mobiles.updateMany(
  { segment: "Premium" },
  { $set: { workshopCategory: "flagship" } }
)
```

Verify:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, segment: 1, workshopCategory: 1 }
)
```

## 6.7 Delete one temporary record

```javascript
db.mobiles.deleteOne({ productId: "TEMP-001" })
```

## 6.8 Delete remaining temporary records

```javascript
db.mobiles.deleteMany({ segment: "Demo" })
```

Verify the count is back to 5:

```javascript
db.mobiles.countDocuments()
```

---

# Module 7: Load full workshop data

The previous module used 5 manual records. Now load the full sample data for the rest of the workshop.

Run from the repository root:

```powershell
python .\scripts\load_workshop_data_base.py
```

This script loads data into:

- `mobiles` from `sample-docs\mobiles_sample.json`
- `support_articles` from `sample-docs\support_articles_sample.json`
- `retail_offers` from `sample-docs\retail_offers_sample.json`
- `supportInc` from `sample-docs\support_inc_search_sample.json`

It does not create indexes.

Verify in `mongosh`:

```javascript
use Workshop_DB
db.mobiles.countDocuments()
db.support_articles.countDocuments()
db.retail_offers.countDocuments()
db.supportInc.countDocuments()
```

Expected:

```text
30
30
30
5
```

---

# Module 8: Import one collection from sample document

This shows how to import a JSON file using a script.

```powershell
python .\scripts\import_sample_collection.py --file .\sample-docs\retail_offers_sample.json --collection retail_offers
```

Verify:

```javascript
db.retail_offers.countDocuments()
db.retail_offers.find({}, { _id: 0, title: 1, offers: 1 }).limit(2)
```

---

# Module 9: Aggregation and indexing

## 9.1 Aggregation

```javascript
db.mobiles.aggregate([
  { $group: { _id: "$segment", avgPrice: { $avg: "$priceInr" }, total: { $sum: 1 } } },
  { $sort: { avgPrice: -1 } }
])
```

## 9.2 Check indexes before creating one

```javascript
db.mobiles.getIndexes()
```

Expected: only `_id_` exists.

## 9.3 Explain plan before index

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Look for `COLLSCAN`.

## 9.4 Create index

```javascript
db.mobiles.createIndex({ segment: 1 }, { name: "idx_segment" })
```

## 9.5 Explain plan after index

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Look for `IXSCAN`.

## 9.6 Create compound index

```javascript
db.mobiles.createIndex(
  { segment: 1, priceInr: -1 },
  { name: "idx_segment_price" }
)
```

Use it:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, brand: 1, priceInr: 1 }
).sort({ priceInr: -1 }).limit(5)
```

---

# Module 10: Migration using VS Code extension

Use this module during Slot 3.

The instructor or sponsor will provide the temporary MongoDB source connection string during the workshop. Do not commit source credentials into this repository.

## 10.1 Connect to source MongoDB

1. Open VS Code.
2. Open the DocumentDB extension.
3. Click **Add New Connection**.
4. Select **Connection String**.
5. Paste the source MongoDB connection string provided by the instructor.
6. Confirm the source cluster appears.

## 10.2 Run pre-migration assessment

1. Right-click the source MongoDB connection.
2. Select **Data Migration**.
3. If prompted, install the migration extension.
4. Select **Pre-Migration Assessment for Azure DocumentDB**.
5. Click **Run Validation**.
6. Start the assessment.
7. Review unsupported features, warnings, and recommendations.

## 10.3 Run offline migration

1. Right-click the source MongoDB connection.
2. Select **Migrate to Azure DocumentDB**.
3. Select **Offline** migration.
4. Select **Public** connectivity for this workshop.
5. Select your subscription, resource group, and DocumentDB cluster.
6. Create or reuse Azure Database Migration Service when prompted.
7. Select databases and collections.
8. Start migration.
9. Wait for status `Succeeded`.

## 10.4 Validate migrated data

```javascript
use <your_database_name>
db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

## 10.5 Online migration and cutover

For online migration, repeat the migration wizard and choose **Online**. Wait for:

```text
Ready To Cutover
```

Stop the workload generator, then click **Cutover**.

Final status should be:

```text
Succeeded
```

---

# Module 11: Keyword search on `supportInc`

`supportInc` has 5 simple records so the search behavior is easy to understand.

## 11.1 Keyword search works for exact words

```javascript
db.supportInc.find(
  { title: /login/i },
  { _id: 0, ticketId: 1, title: 1 }
)
```

Expected:

```text
SUP-1001
```

## 11.2 Keyword search fails for different wording

```javascript
db.supportInc.find(
  { title: /logins/i },
  { _id: 0, ticketId: 1, title: 1 }
)
```

Expected: no records.

Keyword search compares text literally.

---

# Module 12: Full-text search

## 12.1 Create text index

```javascript
db.supportInc.createIndex(
  { title: "text", description: "text", category: "text" },
  { name: "support_text_idx" }
)
```

## 12.2 Search with text index

```javascript
db.supportInc.find(
  { $text: { $search: "password login" } },
  {
    _id: 0,
    ticketId: 1,
    title: 1,
    score: { $meta: "textScore" }
  }
).sort({ score: { $meta: "textScore" } })
```

Full-text search is better than keyword search, but it is still mostly word based.

---

# Module 13: Embeddings and vector search

An embedding is a list of numbers that represents meaning.

Example:

```text
"Unable to login"
"Cannot access my account"
```

These sentences use different words, but their meanings are similar. Embeddings help the database find that similarity.

## 13.1 Generate embeddings

Run:

```powershell
python .\scripts\generate_workshop_embeddings.py
```

Verify:

```javascript
db.supportInc.findOne(
  { ticketId: "SUP-1001" },
  { _id: 0, ticketId: 1, embedding: { $slice: 5 } }
)
```

The `embedding` field stores the vector for each support record.

## 13.2 Create vector index

Run:

```powershell
python .\scripts\create_workshop_indexes.py
```

The script creates:

- `support_text_idx`
- `support_vector_idx`

## 13.3 Run vector search

```powershell
python .\scripts\vector_search_support.py --query "I changed my password and cannot access my account"
```

Expected top result:

```text
SUP-1001 | Login failure after password reset
```

Vector search works because it compares meaning, not just exact words.

---

# Module 14: Hybrid search

Hybrid search means using both:

- text search for exact/relevant words
- vector search for semantic meaning

Run:

```powershell
python .\scripts\hybrid_search_support.py --query "password reset login problem"
```

The script prints the text-search command and then runs vector search.

---

# Module 15: RAG application

RAG means Retrieval Augmented Generation.

Flow:

```text
User question
  -> Azure OpenAI creates question embedding
  -> Azure DocumentDB searches supportInc vectors
  -> Python builds context from matching tickets
  -> Azure OpenAI generates an answer from that context
```

Run:

```powershell
python .\rag_app.py
```

Ask:

```text
Why am I unable to access my account after changing password?
```

Expected retrieved ticket:

```text
SUP-1001 | Login failure after password reset
```

Type `exit` to stop.

---

# Module 16: Local AI agents

No external repository is used. The agent app runs from this repository only and reads the same `.env`.

Run:

```powershell
python .\scripts\run_ai_agents.py
```

Open:

```text
http://localhost:8080
```

Try `MobileAdvisor`:

```text
Recommend a phone under 50000 for camera and battery
```

Try `RetailOfferFinder`:

```text
Where can I buy OnePlus 12?
```

Stop the app with:

```text
Ctrl+C
```

---

# Module 17: MCP Server and GitHub Copilot update

This is an instructor-led update module.

Key points:

1. MCP exposes tools to AI assistants in a structured way.
2. GitHub Copilot can use configured tools to help with repeatable developer workflows.
3. Do not paste secrets into Copilot prompts.
4. Keep connection strings in `.env` or approved secret stores.

Safe prompt example:

```text
Using the configured workshop environment, show me which collections exist in my database.
```

---

# Module 18: Performance review

Use these habits:

## Use projection

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, brand: 1, priceInr: 1 }
)
```

## Use limit

```javascript
db.mobiles.find({}).limit(5)
```

## Use compound indexes for filter plus sort

```javascript
db.mobiles.createIndex(
  { segment: 1, priceInr: -1 },
  { name: "idx_segment_price" }
)
```

## Check query plan

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Look for `IXSCAN`. If you see `COLLSCAN`, the query is scanning the collection.

---

# Module 19: Security review

Before finishing:

1. Open Azure Portal.
2. Open your DocumentDB resource.
3. Click **Networking**.
4. Remove broad or temporary IP ranges.
5. Save changes.

Check that `.env` is not committed:

```powershell
git status --short
```

Rules:

- Do not commit `.env`.
- Do not paste real connection strings into docs.
- Do not share screenshots that show passwords or keys.
- For production, use least-privilege users and Azure Key Vault.
- For production, enable HA based on business requirements.

---

# Module 20: Cleanup

Stop any running local app:

```text
Ctrl+C
```

Deactivate Python:

```powershell
deactivate
```

If the Azure resource group was created only for this workshop:

1. Open Azure Portal.
2. Search **Resource groups**.
3. Open the workshop resource group.
4. Review resources.
5. Click **Delete resource group**.
6. Confirm the resource group name.

Only delete the resource group if you are sure nothing important is inside it.

---

# Troubleshooting

## `.env` missing

```powershell
Copy-Item .env.template .env
notepad .env
```

## Authentication failed

Copy the connection string again from Azure Portal and update `.env`.

## Network timeout

Add your current IP address in DocumentDB **Networking** and save.

## Python package missing

```powershell
pip install -r requirements.txt
```

## Vector dimension mismatch

Check:

```text
EMBEDDING_DIMENSIONS=1536
```

If you change dimensions, regenerate embeddings and recreate the vector index:

```powershell
python .\scripts\generate_workshop_embeddings.py
python .\scripts\create_workshop_indexes.py
```

## Port 8080 already in use

Close the previous app instance or restart PowerShell and run:

```powershell
python .\scripts\run_ai_agents.py
```

---

# Final validation commands

Run these before the workshop:

```powershell
python .\scripts\check_env.py
python .\scripts\load_workshop_data_base.py
python .\scripts\validate_workshop_setup.py
```

For AI/RAG modules:

```powershell
python .\scripts\generate_workshop_embeddings.py
python .\scripts\create_workshop_indexes.py
python .\scripts\vector_search_support.py --query "password login issue"
python .\rag_app.py
```
