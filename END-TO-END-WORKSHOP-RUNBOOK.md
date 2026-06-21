# Azure DocumentDB Workshop Participant Guide

## Workshop overview

In this workshop, you will create an Azure DocumentDB cluster, connect from VS Code and `mongosh`, load sample data, run CRUD commands, create indexes, run a migration workflow, explore full-text and vector search, build a simple RAG flow, run local AI agents, review MCP/Copilot integration, and clean up.

The guide is written for participants who may be new to Azure Portal, VS Code extensions, MongoDB commands, and AI search concepts. Every hands-on step includes what to click, what to paste, and what result to expect.

## Collections used in this workshop

| Collection | Records | How data is loaded | Purpose |
|---|---:|---|---|
| `mobiles` | 5 manual demo records, then 30 sample records | `insertMany` first, script later | CRUD, aggregation, indexing, and MobileAdvisor |
| `support_articles` | 30 | Imported from `sample-docs` using VS Code GUI | File import practice |
| `retail_offers` | 30 | Imported from `sample-docs` using VS Code GUI or loaded by script | RetailOfferFinder |
| `supportInc` | 5 | Loaded by script from `sample-docs` | Keyword search, full-text search, vector search, and RAG |

All scripts use the same `.env` file. You enter DocumentDB and Azure OpenAI details once, then reuse them for the full workshop.

## Full-day agenda

| Time | Session | Focus |
|---|---|---|
| 09:30-10:15 | Slot 1 | Introduction and Azure DocumentDB overview |
| 10:15-11:15 | Hands-on Lab | Cluster setup and connectivity |
| 11:15-13:00 | Slot 2 | Data modeling, import, CRUD, query planning, aggregation, and indexing |
| 13:00-13:30 | Break | Lunch break |
| 13:30-14:15 | Slot 3 | MongoDB to Azure DocumentDB migration |
| 14:15-15:15 | Hands-on Lab | Migration using the Azure DocumentDB VS Code extension |
| 15:15-16:00 | Slot 4 | Search capabilities, AI workloads, agents, and RAG patterns |
| 16:00-17:00 | Hands-on Lab | Full-text search, vector search, hybrid search, and RAG |
| 17:00-17:15 | Updates | MCP Server plus GitHub Copilot integration and latest updates |
| 17:15-17:30 | Close | Wrap-up and Q&A |

## Module map

| Module | Folder | What you do |
|---|---|---|
| 0 | This runbook | Verify prerequisites |
| 1 | `1-Introduction-to-Azure-DocumentDB` | Understand the workshop and clone the repo |
| 2 | `2-Azure-DocumentDB-Cluster-Setup-and-Connectivity` | Create the Azure DocumentDB cluster and connect |
| 3 | `3-Data-Modeling-Data-Import-Querying-and-Indexing` | Create collections, run CRUD, import data, aggregate, and index |
| 4 | `4-Migration-to-Azure-DocumentDB` | Run migration assessment, offline migration, online migration, and cutover |
| 5 | `5-Search-AI-Workloads-Agents-and-RAG` | Run keyword, full-text, vector, hybrid, RAG, agents, MCP/Copilot, performance, security, and cleanup |

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

# Module 1: Introduction and repository setup

## 1.1 Clone the workshop repository

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

## 1.2 What this repository contains

| Item | Purpose |
|---|---|
| `END-TO-END-WORKSHOP-RUNBOOK.md` | Complete participant guide |
| Numbered module folders | Shorter module-specific guides |
| `sample-docs` | JSON data files used in labs |
| `scripts` | Helper scripts that read the same `.env` file |
| `.env.template` | Template for DocumentDB and Azure OpenAI settings |

---

# Module 2: Azure DocumentDB cluster setup and connectivity

## 2.1 Open Azure Portal

1. Open a browser.
2. Go to:

   ```text
   https://portal.azure.com
   ```

3. Sign in with your workshop Azure account.
4. Wait for the Azure Portal home page to load.

## 2.2 Start Azure DocumentDB creation

1. Use the search bar at the top of Azure Portal.
2. Type:

   ```text
   Azure DocumentDB
   ```

3. Click **Azure DocumentDB with MongoDB compatibility**.
4. Click **Create**.

## 2.3 Fill the cluster creation form

Use the instructor-provided subscription and resource group. Create a new resource group only if the sponsor or instructor confirms that you should.

| Portal field | Workshop value | Explanation |
|---|---|---|
| Subscription | Select your assigned subscription | This controls where the resource is billed |
| Resource group | Use assigned group, or create one only if confirmed | Keeps workshop resources together |
| Cluster name | `az-docdb-workshop-<yourname>` | Must be globally unique |
| Region | `Central US`, or the region provided by instructor | Use the same region for related resources when possible |
| MongoDB version | Latest available | Use the default latest version |
| High availability | Disabled | This is a temporary workshop environment |
| Cluster tier | Click **Configure**, select **M30**, keep default cores/RAM shown by portal | M30 is used so vector-search labs work consistently |
| Storage | 32 GB | Enough for this workshop |

When you reach the networking section during creation, select the workshop-friendly option that allows public access for the lab. Because this is a temporary workshop environment and will be cleaned up, the instructor may ask you to use a broad range. If asked, enter:

```text
0.0.0.0 - 255.255.255.255
```

Important: this broad range is only for the temporary workshop. In production, use selected IPs, private networking, and least-privilege access.

Click **Review + create**, then **Create**.

Wait for deployment to complete, then click **Go to resource**.

## 2.4 Copy connection string

1. In the DocumentDB resource, click **Connection strings**.
2. Copy the primary or global read-write connection string.
3. Keep it temporarily. You will paste it into `.env`.

Example format:

```text
mongodb+srv://<username>:<password>@<cluster-name>.mongocluster.cosmos.azure.com/?tls=true
```

Do not share real connection strings in screenshots, chat, slides, or commits.

## 2.5 One-time local environment setup

Run these commands from the repository root:

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

Create `.env`:

```powershell
Copy-Item .env.template .env
notepad .env
```

Fill in the values. The database does not need to exist before you set this value. `Workshop_DB` is the database name that the next modules and scripts will create/use when they first create collections and load data.

```text
# Azure DocumentDB connection string copied from Azure Portal.
DOCUMENTDB_CONNECTION_STRING=<paste-your-documentdb-connection-string>

# Database name used by all workshop scripts.
# It will be created automatically when you create collections or load data.
DOCUMENTDB_DATABASE=Workshop_DB

# Azure OpenAI resource endpoint.
# Keep the format exactly like this: https://<resource-name>.openai.azure.com/
AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com/

# Azure OpenAI key from the Azure OpenAI resource.
AZURE_OPENAI_API_KEY=<paste-your-azure-openai-key>

# API version used by the OpenAI Python SDK.
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Chat model deployment name used by the RAG app to generate final answers.
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4.1-mini

# Embedding model deployment name used to convert text into vectors.
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small

# Number of values in each embedding vector.
# This must match the embedding model output and the vector index dimensions.
EMBEDDING_DIMENSIONS=1536
```

Rules:

- Do not add quotes.
- Do not add spaces before or after `=`.
- Save the file.
- Do not commit `.env`.

Check `.env`:

```powershell
python .\scripts\check_env.py
```

## 2.6 Connect from VS Code

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

## 2.7 Connect from mongosh

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

# Module 3: Data modeling, import, querying, and indexing

## 3.1 Create collections

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

## 3.2 Insert records into `mobiles`

This first lab uses manual `insertMany` so you can see exactly what is inserted.

```javascript
db.mobiles.insertMany([
  { productId: "MOB-001", title: "Samsung Galaxy S24", brand: "Samsung", segment: "Premium", priceInr: 74999, ramGb: 8, storageGb: 256, cameraMp: 50, batteryMah: 4000, inStock: true },
  { productId: "MOB-002", title: "OnePlus 12", brand: "OnePlus", segment: "Premium", priceInr: 64999, ramGb: 12, storageGb: 256, cameraMp: 50, batteryMah: 5400, inStock: true },
  { productId: "MOB-003", title: "iPhone 15", brand: "Apple", segment: "Premium", priceInr: 79999, ramGb: 6, storageGb: 128, cameraMp: 48, batteryMah: 3349, inStock: true },
  { productId: "MOB-004", title: "Redmi Note 13 Pro", brand: "Redmi", segment: "Mid Range", priceInr: 25999, ramGb: 8, storageGb: 128, cameraMp: 200, batteryMah: 5100, inStock: true },
  { productId: "MOB-005", title: "Realme Narzo 70", brand: "Realme", segment: "Budget", priceInr: 14999, ramGb: 6, storageGb: 128, cameraMp: 50, batteryMah: 5000, inStock: false }
])
```

Count records:

```javascript
db.mobiles.countDocuments()
```

Expected: `5`.

## 3.3 Find records

Find premium phones and show only useful fields:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, brand: 1, priceInr: 1, segment: 1 }
).limit(5)
```

This command filters by `segment`, hides `_id`, returns only selected fields, and limits output.

## 3.4 Insert, update, and delete demo records

Insert temporary demo records:

```javascript
db.mobiles.insertMany([
  { productId: "TEMP-001", title: "Temporary Demo Phone 1", brand: "Demo", segment: "Demo", priceInr: 9999, inStock: true },
  { productId: "TEMP-002", title: "Temporary Demo Phone 2", brand: "Demo", segment: "Demo", priceInr: 10999, inStock: true }
])
```

Before updating one record, find the current value:

```javascript
db.mobiles.find(
  { productId: "MOB-005" },
  { _id: 0, productId: 1, title: 1, inStock: 1, updatedBy: 1 }
)
```

Now update one record:

```javascript
db.mobiles.updateOne(
  { productId: "MOB-005" },
  { $set: { inStock: true, updatedBy: "workshop" } }
)
```

Verify the update:

```javascript
db.mobiles.find(
  { productId: "MOB-005" },
  { _id: 0, productId: 1, title: 1, inStock: 1, updatedBy: 1 }
)
```

Before updating many records, find the records that match:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, productId: 1, title: 1, segment: 1, workshopCategory: 1 }
)
```

Now update many records:

```javascript
db.mobiles.updateMany(
  { segment: "Premium" },
  { $set: { workshopCategory: "flagship" } }
)
```

Verify the update:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, productId: 1, title: 1, segment: 1, workshopCategory: 1 }
)
```

Before deleting one temporary record, find it:

```javascript
db.mobiles.find(
  { productId: "TEMP-001" },
  { _id: 0, productId: 1, title: 1, segment: 1 }
)
```

Now delete one temporary record:

```javascript
db.mobiles.deleteOne({ productId: "TEMP-001" })
```

Verify it is gone:

```javascript
db.mobiles.find({ productId: "TEMP-001" })
```

Before deleting the remaining temporary records, find them:

```javascript
db.mobiles.find(
  { segment: "Demo" },
  { _id: 0, productId: 1, title: 1, segment: 1 }
)
```

Now delete remaining temporary records:

```javascript
db.mobiles.deleteMany({ segment: "Demo" })
```

Verify the count is back to 5:

```javascript
db.mobiles.countDocuments()
```

## 3.5 Load full workshop data

The previous step used 5 manual records. Now load full sample data for the rest of the workshop:

```powershell
python .\scripts\load_workshop_data_base.py
```

This loads:

- `mobiles` from `sample-docs\mobiles_sample.json`
- `support_articles` from `sample-docs\support_articles_sample.json`
- `retail_offers` from `sample-docs\retail_offers_sample.json`
- `supportInc` from `sample-docs\support_inc_search_sample.json`

It does not create indexes.

Verify:

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

## 3.6 Aggregation

This aggregation answers: "How many phones are in each segment, and what is the average price per segment?"

```javascript
db.mobiles.aggregate([
  { $group: { _id: "$segment", avgPrice: { $avg: "$priceInr" }, total: { $sum: 1 } } },
  { $sort: { avgPrice: -1 } }
])
```

What to notice:

- `$group` groups phones by segment.
- `$avg` calculates average price.
- `$sum` counts phones.
- `$sort` shows the highest average price first.

## 3.7 Indexing

Check indexes before creating one:

```javascript
db.mobiles.getIndexes()
```

Expected: only `_id_` exists.

Explain plan before index:

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Look for `COLLSCAN`, which means the database scanned the collection.

Create index:

```javascript
db.mobiles.createIndex({ segment: 1 }, { name: "idx_segment" })
```

Explain plan after index:

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Look for `IXSCAN`, which means the database used the index.

Create compound index for filter plus sort:

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

# Module 4: Migration to Azure DocumentDB

Use this module during Slot 3.

The instructor or sponsor will provide the temporary source MongoDB connection string during the workshop. Do not commit source credentials into this repository.

## 4.1 Connect to source MongoDB

1. Open VS Code.
2. Open the DocumentDB extension.
3. Click **Add New Connection**.
4. Select **Connection String**.
5. Paste the source MongoDB connection string provided by the instructor.
6. Confirm the source cluster appears.

## 4.2 Run pre-migration assessment

1. Right-click the source MongoDB connection.
2. Select **Data Migration**.
3. If prompted, install the migration extension.
4. Select **Pre-Migration Assessment for Azure DocumentDB**.
5. Click **Run Validation**.
6. Start the assessment.
7. Review unsupported features, warnings, and recommendations.

## 4.3 Run offline migration

1. Right-click the source MongoDB connection.
2. Select **Migrate to Azure DocumentDB**.
3. Select **Offline** migration.
4. Select **Public** connectivity for this workshop.
5. Select your subscription, resource group, and DocumentDB cluster.
6. Create or reuse Azure Database Migration Service when prompted.
7. Select databases and collections.
8. Start migration.
9. Wait for status `Succeeded`.

Validate migrated data:

```javascript
use <your_database_name>
db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

## 4.4 Start live workload for online migration

Before online migration, the instructor will start or share a small workload application that continuously changes source data. This helps demonstrate change replication.

Participants should observe that the source data changes while migration is running:

- inserts are added
- updates modify existing records
- deletes remove records
- collection counts may change

## 4.5 Online migration stages and cutover

Repeat the migration wizard and choose **Online**.

You will see these stages:

| Stage | Meaning |
|---|---|
| `Provisioning` | Azure prepares migration resources |
| `Bulk Copy In Progress` | Existing source data is copied to Azure DocumentDB |
| `Replication In Progress` | New source inserts, updates, and deletes are replicated |
| `Ready To Cutover` | Target is caught up and ready for final switch |
| `Completing` | Cutover is being finalized |
| `Succeeded` | Migration completed successfully |

When status becomes `Ready To Cutover`:

1. Stop the workload generator.
2. Wait for remaining changes to replicate.
3. Click **Cutover**.
4. Wait for `Succeeded`.

Validate target data again after cutover.

---

# Module 5: Search, AI workloads, agents, and RAG

## 5.1 Keyword search on `supportInc`

`supportInc` has 5 simple records so the search behavior is easy to understand.

Keyword search works when the user knows the exact word stored in the document.

```javascript
db.supportInc.find(
  { title: /login/i },
  { _id: 0, ticketId: 1, title: 1 }
)
```

Expected: `SUP-1001`.

Keyword search can fail when the word is different:

```javascript
db.supportInc.find(
  { title: /logins/i },
  { _id: 0, ticketId: 1, title: 1 }
)
```

Expected: no records.

Why it failed: `login` and `logins` are related for humans, but a regular expression keyword search compares characters. To handle word variations and ranking, use full-text search.

## 5.2 Full-text search

Create a text index:

```javascript
db.supportInc.createIndex(
  { title: "text", description: "text", category: "text" },
  { name: "support_text_idx" }
)
```

Search with relevance scoring:

```javascript
db.supportInc.find(
  { $text: { $search: "password login" } },
  { _id: 0, ticketId: 1, title: 1, score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })
```

Full-text search is better than simple keyword search because it tokenizes text and ranks matches. It is still mostly word based. If a user asks with different wording, such as "I cannot access my account after changing my password," vector search is a better fit because it compares meaning.

## 5.3 Embeddings explained simply

An embedding is a numeric fingerprint of meaning.

Analogy: imagine placing sentences on a map. Sentences with similar meaning are placed near each other, even if they use different words.

| Sentence | Meaning |
|---|---|
| `Unable to login` | Account access problem |
| `Cannot access my account` | Account access problem |
| `Database ran out of storage` | Capacity problem |

The first two are close together on the meaning map. Vector search uses this closeness to find relevant records.

Generate embeddings:

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

## 5.4 Create vector index

The script can create the vector index:

```powershell
python .\scripts\create_workshop_indexes.py
```

If you want to see the full command, this is what it creates:

```javascript
db.runCommand({
  createIndexes: "supportInc",
  indexes: [
    {
      name: "support_vector_idx",
      key: { embedding: "cosmosSearch" },
      cosmosSearchOptions: {
        kind: "vector-ivf",
        similarity: "COS",
        dimensions: 1536,
        numLists: 1
      }
    }
  ]
})
```

The `dimensions` value must match `EMBEDDING_DIMENSIONS` in `.env`.

## 5.5 Run vector search

```powershell
python .\scripts\vector_search_support.py --query "I changed my password and cannot access my account"
```

Expected top result:

```text
SUP-1001 | Login failure after password reset
```

Vector search works because it compares meaning, not just exact words.

## 5.6 Hybrid search

Hybrid search combines two strengths:

| Search type | Strength | Example |
|---|---|---|
| Full-text search | Exact words and relevance scoring | `password login` |
| Vector search | Similar meaning with different words | `cannot access my account` |

Run:

```powershell
python .\scripts\hybrid_search_support.py --query "password reset login problem"
```

What the output means:

- The text-search command shows how a word-based query would run.
- The vector-search results show semantic matches.
- A production hybrid app usually combines both scores into one ranked list.

Why hybrid is useful: if a query contains important exact terms like product names, error codes, or ticket IDs, text search helps preserve precision. If the query uses different wording, vector search helps preserve recall.

## 5.7 RAG application

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

## 5.8 Local AI agents

No external repository is used. The agent app runs from this repository only and reads the same `.env`.

Run:

```powershell
python .\scripts\run_ai_agents.py
```

Open:

```text
http://localhost:8080
```

What happens between prompt and response:

1. Browser sends your prompt to the local Python app.
2. The app reads DocumentDB connection details from `.env`.
3. `MobileAdvisor` queries the `mobiles` collection.
4. `RetailOfferFinder` queries the `retail_offers` collection.
5. The app formats matching database records into a simple response.
6. The browser displays the answer.

Try `MobileAdvisor`:

```text
Recommend a phone under 50000 for camera and battery
```

Try `RetailOfferFinder`:

```text
Where can I buy OnePlus 12?
```

Stop the app with `Ctrl+C`.

## 5.9 MCP Server and GitHub Copilot demo

This is an instructor-led demo that shows something special: VS Code can load MCP server definitions from JSON, and Copilot can use those MCP tools to talk to Azure DocumentDB through a controlled local tool layer.

Important idea:

- Copilot does not need the connection string in the prompt.
- The MCP server reads configuration from local files or environment variables.
- The MCP tool performs the database action.
- Copilot receives only the tool result that the MCP server returns.

### Demo flow

1. Open this repository in VS Code.
2. Confirm `.env` exists locally and is ignored by Git:

   ```powershell
   git status --short
   ```

3. Open or create the MCP configuration JSON used by the instructor. The exact location may vary by lab image, but the JSON shape is similar to this:

   ```json
   {
     "servers": {
       "azure-documentdb-workshop": {
         "type": "stdio",
         "command": "python",
         "args": [
           "./scripts/mcp_documentdb_server.py"
         ],
         "env": {
           "DOCUMENTDB_DATABASE": "Workshop_DB"
         }
       }
     }
   }
   ```

4. Explain the JSON:

   | JSON field | Meaning |
   |---|---|
   | `servers` | List of MCP servers VS Code can start |
   | `azure-documentdb-workshop` | Friendly name of this workshop MCP server |
   | `type: stdio` | VS Code talks to the MCP server over standard input/output |
   | `command: python` | Starts the MCP server with Python |
   | `args` | Points to the local MCP server script |
   | `env` | Passes safe configuration such as database name |

5. Start or enable the MCP server from VS Code.
6. Ask Copilot a safe prompt:

   ```text
   Using the Azure DocumentDB workshop MCP tool, list the collections in my workshop database.
   ```

7. Copilot calls the MCP tool. The MCP server connects to Azure DocumentDB using local configuration and returns collection names.
8. Ask another prompt:

   ```powershell
   Using the Azure DocumentDB workshop MCP tool, count documents in mobiles, support_articles, retail_offers, and supportInc.
   ```

9. Show that the result matches the validation script:

   ```powershell
   python .\scripts\validate_workshop_setup.py
   ```

### What participants should understand

MCP is useful because it gives Copilot a safe, repeatable way to use tools. Instead of pasting secrets or manually copying commands, the user asks a natural-language question and Copilot calls an approved tool.

Safe prompt example:

```text
Using the configured workshop environment, show me which collections exist in my database.
```

Do not paste connection strings, keys, or passwords into Copilot prompts.

## 5.10 Performance review

Use projection to return only needed fields:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, brand: 1, priceInr: 1 }
)
```

Use `limit()` to bound results:

```javascript
db.mobiles.find({}).limit(5)
```

Use compound indexes for filter plus sort:

```javascript
db.mobiles.createIndex(
  { segment: 1, priceInr: -1 },
  { name: "idx_segment_price" }
)
```

Check query plan:

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Look for `IXSCAN`. If you see `COLLSCAN`, the query is scanning the collection.

## 5.11 Security review

Before finishing:

1. Open Azure Portal.
2. Open your DocumentDB resource.
3. Click **Networking**.
4. Remove broad or temporary IP ranges if your instructor asks you to keep the cluster after the workshop.
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

## 5.12 Cleanup

Stop any running local app with `Ctrl+C`.

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

For the workshop, confirm the portal networking settings match the instructor-provided access approach.

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
