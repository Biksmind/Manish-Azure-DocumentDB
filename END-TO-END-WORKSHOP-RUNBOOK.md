# Azure DocumentDB Workshop Participant Guide

## Workshop Overview

In this workshop, you will provision Azure DocumentDB, connect using VS Code, load sample data, explore full-text and vector search capabilities, run AI-powered agents, and review performance and security best practices.

## Learning Objectives

By the end of this workshop, you will be able to:

- Deploy an Azure DocumentDB cluster
- Connect to Azure DocumentDB using VS Code
- Load and validate workshop datasets
- Run MongoDB to Azure DocumentDB migration workflows
- Execute document queries
- Perform full-text and vector searches
- Explore AI-powered agent scenarios
- Review performance optimization techniques
- Apply security best practices

---

## What you will build

You will build a mobile shopping assistant using Azure DocumentDB with workshop sample data, generated embeddings, migration validation, and AI agents.

The workshop flow is:

```text
Create Azure resources
  -> connect from VS Code
  -> prepare local Python environment
  -> generate embeddings
  -> load mobile catalog data
  -> run basic queries
  -> run migration workflow (assessment, offline, online, cutover)
  -> run full-text search
  -> run vector search
  -> run hybrid search and RAG patterns
  -> run AI agents
  -> review performance and security
  -> cleanup
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
| 17:00-17:15 | Updates | MCP Server plus GitHub Copilot integration and latest updates |
| 17:15-17:30 | Close | Wrap-up and Q&A |

## Module order in this file

1. Module 1: Introduction and cluster setup
2. Module 2: Core data operations and indexing
3. Module 3: Migration (VS Code extension and mongodump/mongorestore)
4. Module 4A: Search and RAG patterns
5. Module 4B: AI workloads and agents
6. Extended module: Performance
7. Extended module: Security

## Before Module 1: Verify prerequisites (install only if missing)

Run these checks in PowerShell:

```powershell
code --version
python --version
mongosh --version
git --version
```

### How to read the result

- If all commands return versions, continue to Module 1.
- If any command shows "not recognized" or "command not found", install prerequisites before continuing.

### Quick install on workshop VM (recommended)

From repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_vm_prerequisites.ps1
```

Then open a new PowerShell terminal and run verification again:

```powershell
code --version
python --version
mongosh --version
git --version
```

### Manual install (if script is not available)

```powershell
winget install --id Microsoft.VisualStudioCode --exact --source winget
winget install --id Python.Python.3.10 --exact --source winget
winget install --id MongoDB.Shell --exact --source winget
winget install --id Git.Git --exact --source winget
```

After manual install, restart terminal and re-run the verification commands.

## Before Module 1: Clone workshop repo from VS Code

1. Open **VS Code**.
2. Click the **Source Control** icon in the Activity Bar (or open the GitHub view if your lab image shows a GitHub icon).
3. Click **Clone Repository**.
4. Paste the public repository URL and press **Enter**:

  ```text
  https://github.com/Biksmind/Azure-DocumentDB-Workshop.git
  ```

5. When prompted for destination, select:

  ```text
  C:\Users\lab1euser4\Azure-DocumentDB-Workshop
  ```

6. Click **Select as Repository Destination**.
7. After clone completes, click **Open** to open the repository in VS Code.

You should now see the workshop files in Explorer before continuing with Module 1.

## Module 1: Create Azure DocumentDB

### 1. Open Azure Portal

1. Open a browser.
2. Go to:

   ```text
   https://portal.azure.com
   ```

3. Sign in with your Azure account.
4. Wait until the Azure Portal home page is fully loaded.

### 2. Start Azure DocumentDB creation directly

1. In Azure Portal, use the top search bar.
2. Type:

  ```text
  Azure DocumentDB
  ```

3. Click **Azure DocumentDB** from the search results.
4. Click **Create**.
5. On the Basics page, for **Resource group**:
  - Select an existing resource group if you already have one.
  - If you do not have one, click **Create new** and create it during this flow in the region that matches your workshop time zone: **Central India** for IST or **East US** for PST. If you are unsure, confirm with the speakers or sponsors.

### 3. Create the Azure DocumentDB cluster

1. If the portal shows multiple options, choose **Azure DocumentDB** or **Azure DocumentDB with MongoDB compatibility**.
2. Fill in the Basics page:

  - Subscription: Select your subscription.
  - Resource group: Select existing, or create new in this flow.
  - Cluster name: Use a globally unique name, for example az-docdb-workshop-yourname.
  - Region: Central India for IST or East US for PST.
  - MongoDB version: Latest available version.
  - High availability: Disabled for the workshop.
  - Cluster tier: Click **Configure** and keep the default compute (2 cores / 8 GB RAM).
  - Storage: Change to **128 GB**.

3. Click **Review + create**.
4. Wait for validation to pass.
5. Click **Create**.
6. Wait for deployment to complete. This can take 10-15 minutes.
7. When deployment is complete, click **Go to resource**.

### 4. Configure networking

1. In the DocumentDB resource page, look at the left navigation.
2. Under **Settings**, click **Networking**.
3. Select the option that allows access from selected IP addresses.
4. Click **+ Add current client IP address**.
5. Confirm your IP address appears in the allowed list.
6. Click **Save**.
7. Wait until the save operation completes.

Do not use a broad IP range such as `0.0.0.0 - 255.255.255.255` unless the instructor explicitly asks you to do it for a temporary lab.

### 5. Copy the connection string

1. In the DocumentDB resource left navigation, under **Settings**, click **Connection strings**.
2. Find the primary or global read-write connection string.
3. Click the copy icon.
4. Paste it into a temporary local note. You will use it later in `.env`.

The connection string looks similar to this:

```text
mongodb+srv://<username>:<password>@<cluster-name>.mongocluster.cosmos.azure.com/?tls=true
```

Do not share the real connection string in screenshots, chat, or slides.

## Module 1: Connect from VS Code

### 1. Install VS Code extension

1. Open **VS Code**.
2. On the left Activity Bar, click **Extensions**.
3. In the search box, type:

   ```text
   DocumentDB for VS Code
   ```

4. Click the Microsoft DocumentDB extension.
5. Click **Install**.
6. If VS Code asks you to reload, click **Reload**.

### 2. Add the DocumentDB connection

1. In VS Code, click the **DocumentDB** icon on the left Activity Bar.
2. Click **Add New Connection**.
3. Select **Connection String**.
4. Paste the DocumentDB connection string.
5. If your connection string does not already include the auth mechanism, add it so the end looks like this:

   ```text
   ?tls=true&authMechanism=SCRAM-SHA-256
   ```

6. Press **Enter**.
7. Wait a few seconds.
8. The cluster should appear in the DocumentDB panel.

### 3. Create the workshop database

1. In the DocumentDB panel, find your cluster.
2. Right-click the cluster.
3. Click **Create Database...**.
4. Enter:

   ```text
   Workshop_DB
   ```

5. Press **Enter**.
6. Right-click the cluster again.
7. Click **Refresh**.
8. Expand the cluster and confirm `Workshop_DB` is visible.

### 4. Verify the connection

1. Right-click **Workshop_DB**.
2. Click **New Query Playground**.
3. Paste this:

   ```javascript
   use('Workshop_DB')
   db.runCommand({ ping: 1 })
   show collections
   db.stats()
   ```

4. Click **Run** above the code block.
5. Confirm the ping output contains:

   ```json
   { "ok": 1 }
   ```

### 5. Import sample documents

The `sample-docs` folder contains small representative JSON files for each collection. Import them now to confirm the database accepts data before you set up the full Python environment in Module 2.

The folder contains:

| File | Collection | Documents |
|---|---|---|
| `sample-docs\mobiles_sample.json` | `mobiles` | 30 mobile phones across Budget, Mid Range, Premium, Foldable, and Gaming segments |
| `sample-docs\support_articles_sample.json` | `supportInc` | 30 knowledge-base articles covering Battery, Camera, Connectivity, Bluetooth, Payments, and more |
| `sample-docs\retail_offers_sample.json` | `retail_offers` | 30 phones with retailer offer details |

#### Step 1: Create the collections

1. In the Query Playground, run the following commands to create the collections:

```javascript
use Workshop_DB

db.createCollection("mobiles")
db.createCollection("supportInc")
db.createCollection("retail_offers")
```

2. Verify the collections are created by running:

```javascript
show collections
```

#### Step 2: Import sample documents

#### Option A: mongosh (quickest)


```javascript
use Workshop_DB

db.mobiles.insertMany([ /* paste contents of mobiles_sample.json here */ ])
db.supportInc.insertMany([
  {
    "articleId": "KB001",
    "title": "Battery drains quickly after software update",
    "product": "Mobile OS",
    "category": "Battery",
    "severity": "Medium",
    "content": "After a software update, background sync and app re-indexing can temporarily increase battery usage. Ask the user to restart the phone, check battery usage by app, disable unused background refresh, and install pending app updates.",
    "tags": ["battery", "software update", "background sync", "power usage"]
  },
  {
    "articleId": "KB002",
    "title": "Phone charges slowly with fast charger",
    "product": "Mobile Hardware",
    "category": "Charging",
    "severity": "Medium",
    "content": "Slow charging can happen when the cable does not support fast charging, the adapter wattage is too low, or the charging port has dust. Ask the user to test a certified cable, clean the port carefully, and verify fast charging is enabled.",
    "tags": ["charging", "fast charging", "cable", "adapter"]
  },
  {
    "articleId": "KB003",
    "title": "5G signal drops indoors",
    "product": "Network",
    "category": "Connectivity",
    "severity": "Low",
    "content": "5G coverage can drop indoors because high-frequency bands are blocked by walls. Ask the user to check carrier coverage, switch airplane mode on and off, update carrier settings, and test LTE fallback.",
    "tags": ["5G", "network", "signal", "connectivity"]
  },
  {
    "articleId": "KB004",
    "title": "Camera photos look blurry in low light",
    "product": "Camera",
    "category": "Camera",
    "severity": "Low",
    "content": "Blurry low-light photos are often caused by motion, dirty lenses, or aggressive digital zoom. Ask the user to clean the lens, hold the phone steady, use night mode, and avoid zooming in dark scenes.",
    "tags": ["camera", "low light", "photos", "night mode"]
  },
  {
    "articleId": "KB005",
    "title": "Apps crash after opening",
    "product": "Mobile Apps",
    "category": "Apps",
    "severity": "High",
    "content": "App crashes can be caused by corrupted cache, incompatible app versions, or low storage. Ask the user to update the app, clear cache, restart the phone, and check available storage.",
    "tags": ["apps", "crash", "cache", "storage"]
  },
  {
    "articleId": "KB006",
    "title": "Phone heats up during gaming",
    "product": "Mobile Hardware",
    "category": "Performance",
    "severity": "Medium",
    "content": "Gaming can heat the device because CPU, GPU, display, and network are active together. Ask the user to lower graphics settings, close background apps, remove thick cases, and avoid charging while gaming.",
    "tags": ["gaming", "heating", "performance", "thermal"]
  },
  {
    "articleId": "KB007",
    "title": "Fingerprint unlock is not working",
    "product": "Security",
    "category": "Authentication",
    "severity": "Medium",
    "content": "Fingerprint unlock can fail because of wet fingers, screen protector issues, or corrupted biometric data. Ask the user to clean the sensor, remove and re-add fingerprints, and check for software updates.",
    "tags": ["fingerprint", "unlock", "biometric", "security"]
  },
  {
    "articleId": "KB008",
    "title": "Face unlock fails in dark room",
    "product": "Security",
    "category": "Authentication",
    "severity": "Low",
    "content": "Face unlock may fail in low light if the device relies on the front camera. Ask the user to improve lighting, clean the front camera area, re-enroll face data, or use PIN/fingerprint fallback.",
    "tags": ["face unlock", "low light", "authentication", "camera"]
  },
  {
    "articleId": "KB009",
    "title": "Wi-Fi connects but internet does not work",
    "product": "Network",
    "category": "Connectivity",
    "severity": "High",
    "content": "If Wi-Fi connects but internet is unavailable, the issue may be DNS, router, captive portal, or IP conflict. Ask the user to forget and reconnect to Wi-Fi, restart router, test another network, and reset network settings.",
    "tags": ["wifi", "internet", "router", "dns"]
  },
  {
    "articleId": "KB010",
    "title": "Bluetooth earbuds disconnect frequently",
    "product": "Accessories",
    "category": "Bluetooth",
    "severity": "Medium",
    "content": "Frequent Bluetooth disconnections may be caused by low earbud battery, interference, old firmware, or pairing corruption. Ask the user to charge earbuds, forget and re-pair, update firmware, and test away from interference.",
    "tags": ["bluetooth", "earbuds", "disconnect", "pairing"]
  },
  {
    "articleId": "KB011",
    "title": "Storage is full and phone is slow",
    "product": "Mobile OS",
    "category": "Storage",
    "severity": "Medium",
    "content": "Low storage can slow the phone and cause app failures. Ask the user to delete large videos, move photos to cloud storage, clear app cache, uninstall unused apps, and keep at least 10 percent storage free.",
    "tags": ["storage", "slow phone", "cache", "cleanup"]
  },
  {
    "articleId": "KB012",
    "title": "Mobile data works but hotspot fails",
    "product": "Network",
    "category": "Hotspot",
    "severity": "Medium",
    "content": "Hotspot may fail because of carrier restrictions, data saver, incorrect APN, or device limit. Ask the user to check hotspot plan support, disable data saver, restart the phone, and verify APN settings.",
    "tags": ["hotspot", "mobile data", "carrier", "apn"]
  },
  {
    "articleId": "KB013",
    "title": "Notifications are delayed",
    "product": "Mobile Apps",
    "category": "Notifications",
    "severity": "Low",
    "content": "Delayed notifications are often caused by battery optimization, data saver, or background restrictions. Ask the user to allow background activity, disable battery optimization for the app, and check notification permissions.",
    "tags": ["notifications", "battery optimization", "background activity", "permissions"]
  },
  {
    "articleId": "KB014",
    "title": "Phone cannot install system update",
    "product": "Mobile OS",
    "category": "Updates",
    "severity": "Medium",
    "content": "System update installation can fail because of low battery, low storage, unstable Wi-Fi, or interrupted downloads. Ask the user to charge above 50 percent, free storage, use stable Wi-Fi, and retry the update.",
    "tags": ["system update", "install failure", "storage", "wifi"]
  },
  {
    "articleId": "KB015",
    "title": "Call audio is not clear",
    "product": "Voice",
    "category": "Calls",
    "severity": "High",
    "content": "Poor call audio can be caused by network signal, blocked microphone, Bluetooth routing, or carrier issues. Ask the user to test speaker mode, clean microphone area, disconnect Bluetooth, and try another location.",
    "tags": ["calls", "audio", "microphone", "network"]
  },
  {
    "articleId": "KB016",
    "title": "Screen touch is not responding properly",
    "product": "Display",
    "category": "Touch",
    "severity": "High",
    "content": "Touch issues can be caused by screen protectors, moisture, software freezes, or hardware damage. Ask the user to clean the screen, remove thick screen protectors, restart the phone, and test safe mode.",
    "tags": ["touch", "screen", "display", "safe mode"]
  },
  {
    "articleId": "KB017",
    "title": "GPS location is inaccurate",
    "product": "Location",
    "category": "GPS",
    "severity": "Low",
    "content": "Location accuracy can be affected by indoor use, battery saver, denied permissions, or poor satellite visibility. Ask the user to enable high accuracy mode, check app permissions, and test outdoors.",
    "tags": ["gps", "location", "permissions", "battery saver"]
  },
  {
    "articleId": "KB018",
    "title": "Payment app fails during checkout",
    "product": "Payments",
    "category": "Payments",
    "severity": "High",
    "content": "Payment failures can be caused by outdated app versions, network issues, disabled NFC, or bank authentication failures. Ask the user to update the app, check network, enable NFC, and retry bank verification.",
    "tags": ["payments", "checkout", "nfc", "bank authentication"]
  },
  {
    "articleId": "KB019",
    "title": "Phone speaker volume is too low",
    "product": "Mobile Hardware",
    "category": "Audio",
    "severity": "Low",
    "content": "Low speaker volume can be caused by dirt in the speaker grille, software volume limits, or Do Not Disturb mode. Ask the user to clean the grille gently, check volume settings, disable DND, and test with headphones to isolate the issue.",
    "tags": ["speaker", "volume", "audio", "do not disturb"]
  },
  {
    "articleId": "KB020",
    "title": "App does not open after install",
    "product": "Mobile Apps",
    "category": "Apps",
    "severity": "Medium",
    "content": "An app that fails to open after installation may have a corrupted download, missing permissions, or incompatible OS version. Ask the user to uninstall and reinstall the app, grant all required permissions, and verify the OS version meets requirements.",
    "tags": ["app install", "permissions", "crash", "os version"]
  },
  {
    "articleId": "KB021",
    "title": "Phone restarts randomly",
    "product": "Mobile OS",
    "category": "Stability",
    "severity": "High",
    "content": "Random restarts can be caused by a faulty app, overheating, low battery health, or a software bug. Ask the user to boot in safe mode to isolate apps, check battery health, and update the OS.",
    "tags": ["restart", "crash", "battery health", "safe mode"]
  },
  {
    "articleId": "KB022",
    "title": "SIM card not detected",
    "product": "Mobile Hardware",
    "category": "SIM",
    "severity": "High",
    "content": "A SIM not detected error may be caused by a loose SIM tray, dirty contacts, or a network issue. Ask the user to re-seat the SIM, clean the tray contacts, test another SIM if available, and check with the carrier.",
    "tags": ["sim", "no signal", "hardware", "carrier"]
  },
  {
    "articleId": "KB023",
    "title": "Screen brightness does not adjust automatically",
    "product": "Display",
    "category": "Display",
    "severity": "Low",
    "content": "Auto-brightness relies on the ambient light sensor. It can fail if the sensor is covered, disabled, or the display calibration is off. Ask the user to uncover the sensor area, enable adaptive brightness, and recalibrate the display.",
    "tags": ["brightness", "auto brightness", "ambient light sensor", "display"]
  },
  {
    "articleId": "KB024",
    "title": "Mobile gets very hot while charging",
    "product": "Mobile Hardware",
    "category": "Charging",
    "severity": "Medium",
    "content": "Excessive heat during charging can happen when using a non-certified charger, charging on a soft surface, or using the phone heavily while charging. Ask the user to use the original charger, charge on a hard flat surface, and avoid using the phone while charging.",
    "tags": ["charging", "heating", "thermal", "charger"]
  },
  {
    "articleId": "KB025",
    "title": "Calls drop in the middle of a conversation",
    "product": "Network",
    "category": "Calls",
    "severity": "High",
    "content": "Call drops are usually caused by poor signal, VoLTE issues, or SIM problems. Ask the user to check signal strength, enable VoLTE if available, re-seat the SIM, and contact the carrier if the problem persists.",
    "tags": ["call drop", "signal", "volte", "sim"]
  },
  {
    "articleId": "KB026",
    "title": "Wireless charging is not working",
    "product": "Mobile Hardware",
    "category": "Charging",
    "severity": "Low",
    "content": "Wireless charging can fail if the phone is misaligned on the pad, a thick case is blocking the coil, or wireless charging is disabled. Ask the user to remove the case, center the phone on the pad, and ensure wireless charging is turned on.",
    "tags": ["wireless charging", "qi", "case", "charging pad"]
  },
  {
    "articleId": "KB027",
    "title": "App draining battery in background",
    "product": "Mobile Apps",
    "category": "Battery",
    "severity": "Medium",
    "content": "Background apps can drain battery by running location, sync, or refresh tasks. Ask the user to check battery usage stats, restrict background activity for the offending app, and consider disabling location access when not needed.",
    "tags": ["battery drain", "background app", "location", "battery optimization"]
  },
  {
    "articleId": "KB028",
    "title": "Phone microphone not working during video calls",
    "product": "Mobile Hardware",
    "category": "Audio",
    "severity": "High",
    "content": "If the microphone works for regular calls but not video calls, the issue is likely app-level permission. Ask the user to check microphone permission for the video call app, restart the app, and test with another video call app to confirm.",
    "tags": ["microphone", "video call", "permissions", "audio"]
  },
  {
    "articleId": "KB029",
    "title": "Display colors look washed out",
    "product": "Display",
    "category": "Display",
    "severity": "Low",
    "content": "Washed-out colors can occur when reading mode, night mode, or a low-saturation color profile is active. Ask the user to disable reading mode, check display color settings, and reset the color profile to the default vivid or natural mode.",
    "tags": ["display", "colors", "reading mode", "night mode"]
  },
  {
    "articleId": "KB030",
    "title": "Phone does not vibrate for notifications",
    "product": "Mobile OS",
    "category": "Notifications",
    "severity": "Low",
    "content": "Missing vibration for notifications can be caused by vibration intensity set to zero, Do Not Disturb mode, or per-app notification settings. Ask the user to check vibration intensity, disable DND, and verify notification vibration is enabled for the specific app.",
    "tags": ["vibration", "notifications", "do not disturb", "haptics"]
  }
])
db.retail_offers.insertMany([ /* paste contents of retail_offers_sample.json here */ ])
```


#### Option B: VS Code DocumentDB extension

1. In VS Code, click the **DocumentDB** icon in the Activity Bar.
2. In the DocumentDB explorer, expand your connected cluster.
3. Expand **Databases** and click **Workshop_DB** to select the workshop database.
4. Expand **Workshop_DB** so you can see the collections created in Step 1:
  - `mobiles`
  - `supportInc`
  - `retail_offers`

5. Import records into `supportInc`:
  - Right-click **supportInc**.
  - Click **Import Documents...**.
  - Select `sample-docs\support_articles_sample.json`.
6. Import records into `retail_offers`:
  - Right-click **retail_offers**.
  - Click **Import Documents...**.
  - Select `sample-docs\retail_offers_sample.json`.
7. Right-click **Workshop_DB** and click **Refresh**.

#### Verify the import

In `mongosh`:

```javascript
use Workshop_DB
db.mobiles.countDocuments()           // expect 30
db.supportInc.countDocuments()        // expect 30
db.retail_offers.countDocuments()     // expect 30
```

You should see 30 documents in each collection.

If any count is not 30, reset and import again:

```javascript
use Workshop_DB
db.mobiles.drop()
db.supportInc.drop()
db.retail_offers.drop()
```

Then re-create/import from Option A or Option B and verify counts again.

> **Note:** The sample documents match the complete workshop dataset (30 mobiles, 30 support articles, 30 retail offers). You can skip the Module 3 data load script if you have already imported these files. If you run the script anyway, it will re-insert documents and may create duplicates.
>
> To avoid duplicates, drop these collections before running the full load:
>
> ```javascript
> use Workshop_DB
> db.mobiles.drop()
> db.supportInc.drop()
> db.retail_offers.drop()
> ```

## Module 2: Prepare local environment

### 1. Open PowerShell/Terminal

Open PowerShell and go to the folder where you cloned this repository.

Example:

```powershell
cd C:\Users\lab1euser4\Azure-DocumentDB-Workshop
```

Check that you are in the right folder:

```powershell
Get-ChildItem
```

You should see:

```text
README.md
END-TO-END-WORKSHOP-RUNBOOK.md
1-Introduction-to-Azure-DocumentDB
2-Azure-DocumentDB-Cluster-Setup-and-Connectivity
3-Data-Modeling-Data-Import-Querying-and-Indexing
4-Migration-to-Azure-DocumentDB
5-Search-AI-Workloads-Agents-and-RAG
sample-docs
scripts
```

### 2. Create Python virtual environment

Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

You should see `(.venv)` at the beginning of your PowerShell prompt.

If activation is blocked, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Create `.env`

Run:

```powershell
Copy-Item .env.template .env
notepad .env
```

Fill in the values:

```text
DOCUMENTDB_CONNECTION_STRING=<paste your DocumentDB connection string>
DOCUMENTDB_DATABASE=Workshop_DB
AZURE_OPENAI_ENDPOINT=<optional: required for Slot 4 agents and support app vector mode>
AZURE_OPENAI_API_KEY=<optional: required for Slot 4 agents and support app vector mode>
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4.1-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
EMBEDDING_DIMENSIONS=256
```

Important:

- Do not add quotes around values.
- Do not add spaces before or after `=`.
- Save the file before closing Notepad.
- Do not commit `.env`.

### 4. Check `.env`

Run:

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DOCUMENTDB_DATABASE')); print(os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT'))"
```

Expected output:

```text
Workshop_DB
gpt-4.1-mini
```

If you see `None`, the `.env` file is missing, not saved, or not in the repository root.

## Module 2: Basic DocumentDB checks

Install `mongosh` if you have not already installed it.

Windows:

```powershell
winget install MongoDB.Shell
```

Check:

```powershell
mongosh --version
```

Connect:

```powershell
mongosh "<paste DOCUMENTDB_CONNECTION_STRING here>"
```

Inside `mongosh`, run:

```javascript
use Workshop_DB
db.runCommand({ ping: 1 })
```

You should see `{ ok: 1 }`.

### 1. Load workshop data (required before query checks)

If you dropped collections earlier, load data again before running queries.

Run from the repository root (with your virtual environment active):

```powershell
python .\scripts\load_workshop_data_base.py
```

This script loads data only, without any indexes. You will create indexes manually in Steps 5–6.

This script loads or updates:

- `mobiles`
- `supportInc`
- `retail_offers`

### 2. Confirm data is present

Run:

```javascript
show collections
db.mobiles.countDocuments()
db.supportInc.countDocuments()
db.retail_offers.countDocuments()
```

Expected:

- Collections include `mobiles`, `supportInc`, and `retail_offers`.
- Each collection should have records (typically 30 each when sample data is loaded).

### 3. Run a basic `find` query

Run:

```javascript
db.mobiles.find(
  { segment: "Premium" },
  { _id: 0, title: 1, brand: 1, priceInr: 1, segment: 1 }
).limit(5)
```

This validates that filtering and projection are working.

### 4. Run an `aggregate` query

Run:

```javascript
db.mobiles.aggregate([
  { $group: { _id: "$segment", avgPrice: { $avg: "$priceInr" }, total: { $sum: 1 } } },
  { $sort: { avgPrice: -1 } }
])
```

This validates aggregation, grouping, and sorting behavior.

### 5. Reset `mobiles` indexes for this exercise

If you previously ran an older loader or already created indexes, remove secondary indexes first.

Run:

```javascript
db.mobiles.getIndexes()
db.mobiles.dropIndexes()
db.mobiles.getIndexes()
```

Expected:

- Only the default `_id_` index should remain.

### 6. Capture explain plan before index

Run:

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Check in the output:

- Query plan shape should show collection scan before creating index.
- `totalDocsExamined` should be close to the full collection size (typically 30).
- `nReturned` should be lower than `totalDocsExamined` because only matching documents are returned.

### 7. Create index and validate impact

Create index:

```javascript
db.mobiles.createIndex({ segment: 1 }, { name: "idx_segment" })
```

Run explain again:

```javascript
db.mobiles.find({ segment: "Premium" }).explain("executionStats")
```

Verify:

- Plan now uses index scan for the filter.
- `totalDocsExamined` should reduce compared to pre-index run.

List indexes:

```javascript
db.mobiles.getIndexes()
```

Exit `mongosh` for now:

```javascript
exit
```

## Module 3: MongoDB to Azure DocumentDB migration

Use this module during Slot 3.

## Objective

In this exercise, you will migrate data from an existing MongoDB environment to Azure DocumentDB using the Azure DocumentDB Migration extension in Visual Studio Code.

You will perform:

1. Pre-Migration Assessment
2. Offline Migration
3. Online Migration
4. Application Cutover Validation

---

## Prerequisites

### MongoDB Source Connection

Connect to the MongoDB source using the following connection string:

```text
mongodb://readonly:drinkchaidaily123@20.71.118.158:27017/?directConnection=true
```

> Note: If credentials are not provided during the workshop, please obtain them from the workshop sponsors.

---

## Part 1: Connect to MongoDB using VS Code

1. Open Visual Studio Code.
2. Open the DocumentDB for VS Code Extension.
3. Create a new MongoDB connection using the provided connection string.
4. Verify that the MongoDB cluster appears in the Connections pane.

Once connected successfully, proceed to the migration workflow.

---

## Part 2: Pre-Migration Assessment

Before performing any migration, run a compatibility assessment against Azure DocumentDB.

### Launch Assessment

1. Right-click the MongoDB cluster.
2. Select **Data Migration**.
3. If prompted, install the **Azure DocumentDB Migration** extension.
4. After installation completes, right-click the MongoDB cluster again.
5. Select **Data Migration** again.
6. Select **Pre-Migration Assessment for Azure DocumentDB**.

### Validate Source Environment

1. Verify the MongoDB source connection.
2. Click **Run Validation**.
3. Wait for validation to complete.

### Create Assessment

1. Enter an Assessment Name.
2. Optionally specify:
   - Report Path
   - Log Path
3. Click **Start Assessment**.

The assessment process will analyze your MongoDB deployment and identify compatibility considerations.

### Review Assessment Results

1. Open the completed assessment.
2. Download the assessment report.
3. Review:
   - Compatibility findings
   - Unsupported features
   - Migration recommendations

After reviewing the report, close the assessment window.

---

## Part 3: Offline Migration

Now perform a full offline migration.

### Create Migration Job

1. Right-click the MongoDB cluster again.
2. Select **Migrate to Azure DocumentDB**.
3. The Create Migration Job wizard opens.

### Configure Migration Job

Provide:

- Migration Job Name
- Migration Mode: **Offline**
- Network Connectivity: **Public**

For this workshop use:

- Offline Migration
- Public Connectivity

> Source connection string is optional because the extension can use the existing connection.

Click **Next**.

### Configure Target Environment

Provide Azure DocumentDB target details:

- Subscription
- Resource Group
- Azure DocumentDB Cluster

Click **Next**.

### Configure Azure DMS

Migration uses Azure Database Migration Service (DMS).

If DMS already exists:

- Select the existing DMS instance.

Otherwise:

- Create a new DMS instance in the same subscription and resource group.

Click **Next**.

### Firewall Configuration

Update source and target firewall rules when prompted.

Ensure:

- MongoDB source is reachable
- Azure DocumentDB target is reachable

Click **Next**.

### Select Databases and Collections

Choose:

- Database(s)
- Collection(s)

Select the migration action.

Click **Start Migration**.

### Monitor Migration

Azure will provision migration resources in the background.

This may take several minutes.

Monitor the migration status.

Wait until the migration status becomes:

```text
Succeeded
```

### Validate Migrated Data

Connect to Azure DocumentDB and run:

```javascript
use <your_database_name>

db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

Verify collection counts between source and target.

---

## Part 4: Generate Live Workload

Before performing Online Migration, generate ongoing database activity.

### Launch Sample Application

Open:

```text
https://mongocsgen-app1.azurewebsites.net/
```

### Generate Activity

The workshop administrator will start the workload generator.

Participants should observe:

- Continuous inserts
- Updates
- Deletes
- Increasing document counts

This workload helps demonstrate Azure DMS change replication during Online Migration.

---

## Part 5: Online Migration

Complete Part 4 before starting Part 5.

Repeat the migration steps performed earlier.

Navigate again to:

```text
MongoDB Cluster
→ Data Migration
→ Migrate to Azure DocumentDB
```

### Configure Online Migration

Provide:

- Migration Job Name
- Migration Mode: Online
- Network Connectivity: Public

Since DMS was already created during Offline Migration:

- Reuse the existing DMS instance.

Proceed through:

- Target Configuration
- Firewall Updates
- Database Selection
- Collection Selection

Start Migration.

### Monitor Migration Progress

You will observe the following migration states:

```text
Provisioning
```

↓

```text
Bulk Copy In Progress
```

↓

```text
Replication In Progress
```

↓

```text
Ready To Cutover
```

During Replication:

- New inserts are copied continuously.
- Updates are synchronized.
- Deletes are synchronized.

This keeps Azure DocumentDB in sync with the source MongoDB environment.

---

## Part 6: Cutover

Once migration reaches `Ready To Cutover`, perform the following steps.

### Stop Application Workload

Before cutover:

1. Stop the workload generator.
2. Allow remaining changes to synchronize.

This ensures no new writes occur during final synchronization.

### Perform Cutover

Click:

```text
Cutover
```

Migration status changes through:

```text
Ready To Cutover
```

↓

```text
Completing
```

↓

```text
Succeeded
```

---

## Part 7: Final Data Validation

Run the same validation query against Azure DocumentDB:

```javascript
use <your_database_name>

db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

Verify:

- Collection counts match source.
- No pending replication items remain.
- Migration status is successful.

---

## Part 8: Application Migration Validation

One of the key benefits of Azure DocumentDB is MongoDB compatibility.

No application code changes are required.

### Test Application Connectivity

Update only the application connection string.

#### Before

```text
MongoDB Connection String
```

#### After

```text
Azure DocumentDB Connection String
```

No code modifications are necessary.

### Verify Application Functionality

Perform the following operations:

- Create Records
- Read Records
- Update Records
- Delete Records

Observe that the application continues to function normally against Azure DocumentDB.

---

## Expected Outcome

At the end of this lab, you will have successfully:

✅ Assessed MongoDB compatibility

✅ Performed Offline Migration

✅ Performed Online Migration

✅ Executed Production Cutover

✅ Validated Data Consistency

✅ Connected Existing MongoDB Application to Azure DocumentDB

✅ Verified Application Functionality without Code Changes

This demonstrates a complete MongoDB to Azure DocumentDB migration workflow using Azure Database Migration Service (DMS) and the Azure DocumentDB VS Code Migration Extension.

# Azure DocumentDB Search Workshop - Deep Self Learning Guide

# Introduction

Modern applications store millions of records. Finding the right information quickly is a challenge.

Traditionally, databases relied on exact word matching. Today, AI-powered applications use semantic understanding to find information based on meaning rather than exact words.

In this lab, you will learn the evolution of search:

1. Keyword Search
2. Full Text Search
3. Vector Search
4. Why RAG applications use Vector Search

This guide is intentionally descriptive. After every exercise you will learn not only what happened, but why it happened.

---

# Module 1 - Create Sample Dataset

We will simulate a customer support system.

Create a collection named:

```javascript
supportInc
```

Insert the following data:

```javascript
db.supportInc.insertMany([
{
    _id: 1,
    ticketId: "SUP-1001",
    title: "Login failure after password reset",
    description: "User is unable to login after changing account password. Authentication keeps failing.",
    category: "Authentication",
    priority: "High"
},
{
    _id: 2,
    ticketId: "SUP-1002",
    title: "Storage quota exceeded during migration",
    description: "Database migration process stopped because available storage space was exhausted.",
    category: "Migration",
    priority: "Critical"
},
{
    _id: 3,
    ticketId: "SUP-1003",
    title: "Application timeout while uploading files",
    description: "Users experience connection timeout errors when transferring large documents.",
    category: "Networking",
    priority: "Medium"
},
{
    _id: 4,
    ticketId: "SUP-1004",
    title: "Email notifications not delivered",
    description: "System generated emails are not reaching customer inboxes due to mail delivery issues.",
    category: "Notifications",
    priority: "High"
},
{
    _id: 5,
    ticketId: "SUP-1005",
    title: "High CPU utilization on database server",
    description: "Database server is experiencing unusually high processor consumption during peak workload.",
    category: "Performance",
    priority: "Critical"
}
])
```

---

# Module 2 - Keyword Search

## What is Keyword Search?

Keyword Search is the simplest form of search.

The database looks for the exact text supplied by the user.

It does not understand:

- Meaning
- Context
- Synonyms
- Word variations

It simply compares characters.

Think of it as:

> "Find me documents containing exactly this word."

---

## Exercise 1

```javascript
db.supportInc.find({
  title: /login/i
})
```

Expected Result:

```text
SUP-1001
```

### Why did this work?

The document contains:

```text
Login failure after password reset
```

The query searched for:

```text
login
```

The exact word exists in the title.

Keyword Search performs direct pattern matching and therefore returns the document.

### Key Learning

Keyword Search works well when the user knows the exact word stored in the database.

---

## Exercise 2

```javascript
db.supportInc.find({
  title: /logins/i
})
```

Expected Result:

```text
[]
```

### Why did this fail?

The document contains:

```text
login
```

The query contains:

```text
logins
```

Humans understand that both words are related.

The database does not.

To the database:

```text
login != logins
```

Because the exact word is not present, no results are returned.

### Key Learning

Keyword Search compares text literally.

It does not understand grammar or language.

---

# Module 3 - Full Text Search

## What is Full Text Search?

Full Text Search is more intelligent than Keyword Search.

Instead of comparing raw text, it performs linguistic analysis.

Common capabilities:

- Tokenization
- Stemming
- Relevance Ranking

Full Text Search attempts to understand how words relate to each other.

However, it is still fundamentally a word-based search system.

---

## Create Full Text Index

```javascript
db.runCommand({
  createIndexes: "supportInc",
  indexes: [
    {
      key: {
        title: "text",
        description: "text"
      },
      name: "support_text_idx"
    }
  ]
})
```

---

## Exercise 3

```javascript
db.supportInc.find({
  $text: {
    $search: "logins"
  }
})
```

Expected Result:

```text
SUP-1001
```

### Why did this work?

Document:

```text
login
```

Query:

```text
logins
```

Full Text Search analyzes language.

Internally it recognizes that:

```text
login
logins
```

share the same root.

The search engine reduces both words to a common form and performs matching.

### Key Learning

Full Text Search understands word variations.

---

## Exercise 4

```javascript
db.supportInc.find({
  $text: {
    $search: "procesor"
  }
})
```

Expected Result:

```text
[]
```

### Why did this fail?

Document contains:

```text
processor
```

Query contains:

```text
procesor
```

This is not a variation of the word.

This is a spelling mistake.

Full Text Search understands:

```text
processor
processors
processing
```

because these share a linguistic relationship.

However:

```text
procesor
```

is treated as an entirely different token.

### Key Learning

Full Text Search understands language.

It does not automatically understand spelling mistakes.

---

# Module 4 - Why Full Text Search Is Still Not Enough

Imagine a user searches:

```text
I changed my password and cannot access my account
```

Our document says:

```text
User unable to login after changing account password
```

Humans immediately understand both statements describe the same issue.

Traditional search engines may not.

The words are different.

The meaning is the same.

This is the problem Vector Search solves.

---

# Module 5 - Understanding Embeddings

## What is an Embedding?

An embedding is a numerical representation of meaning.

Text:

```text
User unable to login
```

may become:

```text
[0.124, -0.451, 0.778, ...]
```

The actual numbers are not important.

What matters is:

Documents discussing similar topics generate vectors that are close together.

---

## Example

Sentence 1:

```text
Unable to login
```

Sentence 2:

```text
Cannot access my account
```

The words are different.

However, their embeddings will be very similar because their meaning is similar.

---

# Module 6 - Generate Embeddings

Generate embeddings for every document using Azure OpenAI.

Run the standalone script from the repository root:

```powershell
python .\embeddinggene.py
```

Before running it, make sure `.env` contains:

- `DOCUMENTDB_CONNECTION_STRING`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`

Replace any placeholder values like `<your-documentdb-connection-string>` before running the script.

Store the vector in:

```text
embedding
```

field.

After completion verify:

```javascript
db.supportInc.findOne(
  {_id:1},
  {
    ticketId:1,
    embedding:{$slice:5}
  }
)
```

### What happened?

Your document now contains:

1. Human-readable text
2. AI-readable vectors

DocumentDB can now perform semantic search.

---

# Module 7 - Create Vector Index

```javascript
db.runCommand({
  createIndexes: "supportInc",
  indexes: [
    {
      name: "support_vector_idx",
      key: {
        embedding: "cosmosSearch"
      },
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

### Why do we need a vector index?

Without a vector index, DocumentDB would need to compare every vector against every document.

This becomes expensive at scale.

The vector index allows DocumentDB to quickly find the nearest vectors.

---

# Module 8 - Vector Search

User Query:

```text
I changed my password and now I cannot access my account
```

Generate an embedding for the query.

Run vector search.

Expected Top Result:

```text
SUP-1001
```

---

## Why did this work?

Document:

```text
User unable to login after changing account password
```

Query:

```text
I changed my password and now I cannot access my account
```

Notice:

| Document | Query |
|-----------|--------|
| unable to login | cannot access account |
| changing account password | changed my password |

Very few words overlap.

Keyword Search struggles.

Full Text Search struggles.

Vector Search succeeds because it compares meaning.

---

# Module 9 - The Big Picture

## Keyword Search

Question:

```text
login
```

Database asks:

> Do I see this exact word?

---

## Full Text Search

Question:

```text
logins
```

Database asks:

> Is this a linguistic variation of a known word?

---

## Vector Search

Question:

```text
I changed my password and now I cannot access my account
```

Database asks:

> Which stored documents have a similar meaning?

---

# Final Comparison

| Capability | Keyword | Full Text | Vector |
|------------|----------|-----------|---------|
| Exact Match | Yes | Yes | No |
| Word Variations | No | Yes | Yes |
| Understand Meaning | No | Limited | Yes |
| AI Ready | No | Limited | Yes |
| Best For RAG | No | No | Yes |

# Final Takeaway

Keyword Search matches words.

Full Text Search matches smarter words.

Vector Search matches meaning.

This shift from matching words to matching meaning is what enables modern AI applications, copilots, chatbots, semantic search engines, and Retrieval Augmented Generation (RAG) systems.

---

# Module 10 - Introduction to RAG

## What is RAG?

RAG stands for:

```text
Retrieval Augmented Generation
```

This may sound complex, but the idea is simple.

A normal LLM answers from what it already knows.

A RAG application first searches your private data, retrieves relevant information, and then asks the LLM to answer using that retrieved data.

---

## Normal LLM Flow

```text
User Question
      ↓
LLM
      ↓
Answer
```

This is simple, but it has some problems:

- The LLM may not know your company data
- The LLM may give a generic answer
- The LLM may hallucinate
- The answer may not be grounded in your database

---

## RAG Flow

```text
User Question
      ↓
Generate Query Embedding
      ↓
Search Azure DocumentDB
      ↓
Retrieve Relevant Tickets
      ↓
Send Tickets + Question to GPT
      ↓
Generate Final Answer
```

In this flow, Azure DocumentDB acts as the retrieval layer.

Azure OpenAI acts as:

1. Embedding generator
2. Answer generator

---

## Why RAG is Useful

Suppose the user asks:

```text
Why am I unable to access my account after changing password?
```

The LLM alone may not know your support ticket data.

But with RAG, the application first retrieves this ticket:

```text
SUP-1001 - Login failure after password reset
```

Then GPT answers using that ticket.

This makes the answer more grounded and useful.

---

# Module 11 - RAG Architecture Using Azure DocumentDB

## Components Used

This mini RAG application uses:

| Component | Purpose |
|----------|---------|
| Azure DocumentDB | Stores support tickets and embeddings |
| Azure OpenAI Embedding Model | Converts user question into vector |
| Azure DocumentDB Vector Search | Finds relevant tickets |
| Azure OpenAI Chat Model | Generates final answer |
| Python | Connects all components together |

---

## End-to-End Flow

```text
User asks question
      ↓
Python app receives question
      ↓
Azure OpenAI creates embedding for question
      ↓
Azure DocumentDB vector search finds matching tickets
      ↓
Python builds context from retrieved tickets
      ↓
Azure OpenAI chat model generates answer
      ↓
User receives final response
```

---

## Important Concept

Azure DocumentDB does not generate embeddings by itself.

Azure DocumentDB stores vectors and searches vectors.

Azure OpenAI generates embeddings.

So the responsibility is split like this:

| Responsibility | Service |
|---------------|---------|
| Store documents | Azure DocumentDB |
| Store embeddings | Azure DocumentDB |
| Generate embeddings | Azure OpenAI |
| Search similar vectors | Azure DocumentDB |
| Generate natural language answer | Azure OpenAI GPT model |

---

# Module 12 - Build Your First RAG Application

## Prerequisites

Before running the RAG app, make sure you have already completed:

1. Inserted the `supportInc` sample data
2. Generated embeddings for all support tickets
3. Created the vector index on the `embedding` field
4. Confirmed that vector search works

The checked-in `rag_app.py` reads configuration from `.env`. Replace any template values like `<your-documentdb-connection-string>` and `<your-openai-resource>` before running it.

You also need these Python packages:

```bash
pip install pymongo openai
```

---

## Create Python File

Create a file named:

```text
rag_app.py
```

Paste the following code:

```python
from pymongo import MongoClient
from openai import AzureOpenAI

# -----------------------------
# Azure OpenAI Configuration
# -----------------------------
AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your-azure-openai-key>"
AZURE_OPENAI_API_VERSION = "2024-02-01"

EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
CHAT_DEPLOYMENT = "<your-chat-model-deployment-name>"
# Example: gpt-4o-mini or gpt-4o

# -----------------------------
# Azure DocumentDB Configuration
# -----------------------------
MONGO_URI = "mongodb+srv://<user>:<password>@<cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

DB_NAME = "Workshop_DB"
COLLECTION_NAME = "supportInc"

# -----------------------------
# Clients
# -----------------------------
openai_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]


def generate_embedding(text: str):
    response = openai_client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding


def vector_search(user_question: str, top_k: int = 3):
    query_vector = generate_embedding(user_question)

    pipeline = [
        {
            "$search": {
                "cosmosSearch": {
                    "vector": query_vector,
                    "path": "embedding",
                    "k": top_k
                },
                "returnStoredSource": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "ticketId": 1,
                "title": 1,
                "description": 1,
                "category": 1,
                "priority": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def build_context(search_results):
    context = ""

    for item in search_results:
        context += f\"\"\"
Ticket ID: {item.get("ticketId")}
Title: {item.get("title")}
Description: {item.get("description")}
Category: {item.get("category")}
Priority: {item.get("priority")}
Score: {item.get("score")}
---
\"\"\"

    return context.strip()


def generate_answer(user_question: str, context: str):
    system_prompt = \"\"\"
You are a support assistant.
Answer the user's question using only the provided support ticket context.
If the answer is not present in the context, say that you do not have enough information.
Keep the answer simple and clear.
\"\"\"

    user_prompt = f\"\"\"
User Question:
{user_question}

Support Ticket Context:
{context}

Answer:
\"\"\"

    response = openai_client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


def main():
    print("\\nAzure DocumentDB RAG Demo")
    print("Type 'exit' to stop.\\n")

    while True:
        user_question = input("Ask your question: ")

        if user_question.lower() == "exit":
            break

        print("\\nSearching Azure DocumentDB...\\n")

        results = vector_search(user_question)

        print("Retrieved Tickets:")
        for item in results:
            print(f"- {item['ticketId']} | {item['title']} | Score: {item.get('score')}")

        context = build_context(results)

        print("\\nGenerating answer using Azure OpenAI...\\n")

        answer = generate_answer(user_question, context)

        print("\\nAnswer:")
        print(answer)
        print("\\n" + "-" * 80 + "\\n")


if __name__ == "__main__":
    main()
```

---

# Module 13 - Understanding the RAG Code

This section explains the code step by step.

The goal is not just to run the script, but to understand how the RAG flow works.

---

## Step 1 - Import Libraries

```python
from pymongo import MongoClient
from openai import AzureOpenAI
```

### Why do we need these?

`pymongo` is used to connect to Azure DocumentDB using the MongoDB-compatible API.

`AzureOpenAI` is used to call Azure OpenAI for:

1. Creating embeddings
2. Generating the final answer

---

## Step 2 - Configure Azure OpenAI

```python
AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your-azure-openai-key>"
AZURE_OPENAI_API_VERSION = "2024-02-01"

EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
CHAT_DEPLOYMENT = "<your-chat-model-deployment-name>"
```

### What does this mean?

The embedding deployment converts text into vectors.

The chat deployment generates the final natural language answer.

Both deployments are required because RAG has two AI tasks:

| Task | Model Type |
|------|------------|
| Convert question into vector | Embedding model |
| Generate final answer | Chat model |

---

## Step 3 - Configure Azure DocumentDB

```python
MONGO_URI = "mongodb+srv://<user>:<password>@<cluster-name>.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

DB_NAME = "Workshop_DB"
COLLECTION_NAME = "supportInc"
```

### What does this mean?

This connects the Python app to your Azure DocumentDB cluster.

The application will search inside:

```text
Workshop_DB.supportInc
```

This is the same collection used earlier for Keyword Search, Full Text Search, and Vector Search.

---

## Step 4 - Create Clients

```python
openai_client = AzureOpenAI(...)
mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]
```

### Why do we create clients?

A client is the object that allows Python to communicate with an external service.

Here we create:

1. One client for Azure OpenAI
2. One client for Azure DocumentDB

---

## Step 5 - Generate Embedding

```python
def generate_embedding(text: str):
    response = openai_client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input=text
    )
    return response.data[0].embedding
```

### What does this function do?

It takes text as input.

Example:

```text
I changed my password and now I cannot access my account
```

It sends this text to Azure OpenAI.

Azure OpenAI returns a vector.

Example:

```text
[0.123, -0.456, 0.789, ...]
```

This vector represents the meaning of the question.

---

## Step 6 - Perform Vector Search

```python
def vector_search(user_question: str, top_k: int = 3):
    query_vector = generate_embedding(user_question)
```

### What happens here?

The user question is converted into a vector.

This is required because DocumentDB vector search compares vectors, not raw text.

---

```python
pipeline = [
    {
        "$search": {
            "cosmosSearch": {
                "vector": query_vector,
                "path": "embedding",
                "k": top_k
            },
            "returnStoredSource": True
        }
    }
]
```

### What does this pipeline do?

It asks Azure DocumentDB:

> Compare this query vector with the stored vectors in the `embedding` field.

The field:

```text
embedding
```

contains vectors generated earlier for each support ticket.

The parameter:

```text
k: 3
```

means:

> Return the top 3 most similar tickets.

---

## Step 7 - Project Useful Fields

```python
"$project": {
    "_id": 0,
    "ticketId": 1,
    "title": 1,
    "description": 1,
    "category": 1,
    "priority": 1,
    "score": {"$meta": "searchScore"}
}
```

### Why do we use projection?

The full document may contain many fields, including the large embedding vector.

We do not want to send the full embedding to the LLM.

We only need useful readable information:

- Ticket ID
- Title
- Description
- Category
- Priority
- Search score

This keeps the context clean and efficient.

---

## Step 8 - Build Context

```python
def build_context(search_results):
    context = ""

    for item in search_results:
        context += f\"\"\"
Ticket ID: {item.get("ticketId")}
Title: {item.get("title")}
Description: {item.get("description")}
Category: {item.get("category")}
Priority: {item.get("priority")}
Score: {item.get("score")}
---
\"\"\"

    return context.strip()
```

### What is context?

Context is the retrieved information that we give to the LLM.

Instead of asking GPT to answer blindly, we say:

> Use these retrieved support tickets to answer the user.

This is the "Augmented" part of RAG.

The answer is augmented with your database content.

---

## Step 9 - Generate Final Answer

```python
def generate_answer(user_question: str, context: str):
```

This function sends two things to the chat model:

1. User question
2. Retrieved support ticket context

---

```python
system_prompt = \"\"\"
You are a support assistant.
Answer the user's question using only the provided support ticket context.
If the answer is not present in the context, say that you do not have enough information.
Keep the answer simple and clear.
\"\"\"
```

### Why is the system prompt important?

The system prompt controls the assistant behavior.

It tells the model:

- Do not answer from imagination
- Use only supplied context
- Be clear and simple
- Admit when context is insufficient

This reduces hallucination.

---

```python
temperature=0.2
```

### Why use low temperature?

Lower temperature makes responses more focused and deterministic.

For support and enterprise applications, we usually want stable answers, not creative answers.

---

# Module 14 - Run the RAG Application

Run the script:

```powershell
python .\rag_app.py
```

You should see:

```text
Azure DocumentDB RAG Demo
Type 'exit' to stop.
```

Ask:

```text
Why am I not able to access my account after changing password?
```

Expected retrieved ticket:

```text
SUP-1001 | Login failure after password reset
```

Expected answer should mention that the issue is related to login/authentication failure after password change.

---

# Module 15 - What Happened Internally?

When you asked:

```text
Why am I not able to access my account after changing password?
```

The application performed these steps:

## Step 1

Converted the question into an embedding.

```text
Question Text
↓
Query Vector
```

## Step 2

Searched Azure DocumentDB using vector similarity.

```text
Query Vector
↓
Compare with stored ticket vectors
↓
Find nearest tickets
```

## Step 3

Retrieved the most relevant ticket.

```text
SUP-1001
Login failure after password reset
```

## Step 4

Built a context block.

```text
Ticket ID: SUP-1001
Title: Login failure after password reset
Description: User is unable to login after changing account password.
```

## Step 5

Sent the context and question to GPT.

```text
Question + Retrieved Context
↓
GPT
↓
Answer
```

This is RAG.

---

# Module 16 - Why This Is Better Than Asking GPT Directly

If you ask GPT directly:

```text
Why am I unable to access my account?
```

GPT may give a generic answer.

But with RAG:

1. The application retrieves your actual support ticket
2. GPT answers using that retrieved ticket
3. The answer is grounded in your DocumentDB data

This is why RAG is useful for:

- Internal support bots
- Knowledge base search
- Customer service assistants
- Enterprise copilots
- Developer support tools
- Document search systems

---

# Module 17 - Try More RAG Questions

Try the following questions:

## Question 1

```text
Why am I not able to access my account after changing password?
```

Expected retrieved ticket:

```text
SUP-1001
```

---

## Question 2

```text
Why did my database migration stop due to lack of space?
```

Expected retrieved ticket:

```text
SUP-1002
```

---

## Question 3

```text
Why are customers not receiving emails from the system?
```

Expected retrieved ticket:

```text
SUP-1004
```

---

## Question 4

```text
Why is the database server slow during peak usage?
```

Expected retrieved ticket:

```text
SUP-1005
```

---

## Question 5

```text
Why does file upload fail for large documents?
```

Expected retrieved ticket:

```text
SUP-1003
```

---

# Module 18 - Common Issues and Fixes

## Issue 1 - PowerShell says `from` keyword is not supported

### Cause

You pasted Python code directly into PowerShell.

PowerShell is not Python.

### Fix

Create a `.py` file and run it:

```powershell
python .\rag_app.py
```

Or start Python shell first:

```powershell
python
```

---

## Issue 2 - Azure OpenAI endpoint error

### Cause

The endpoint may include an incorrect suffix.

Incorrect:

```text
https://<resource>.openai.azure.com/openai/v1
```

Correct:

```text
https://<resource>.openai.azure.com/
```

---

## Issue 3 - Vector dimension mismatch

### Cause

The vector index dimension must match the embedding model output.

For `text-embedding-3-small`, commonly used dimension is:

```text
1536
```

### Fix

Ensure your vector index has:

```javascript
dimensions: 1536
```

---

## Issue 4 - Vector search returns poor results

### Possible Causes

- Embeddings were not generated correctly
- Query is too vague
- Wrong field used in vector index
- Vector index not created
- Documents contain too little descriptive text

### Fix

Verify embeddings exist:

```javascript
db.supportInc.findOne(
  {_id:1},
  {
    ticketId:1,
    embedding:{$slice:5}
  }
)
```

---

# Module 19 - Final End-to-End Summary

You have now built the complete learning path:

```text
Keyword Search
    ↓
Exact word matching

Full Text Search
    ↓
Language-aware word matching

Embeddings
    ↓
Text converted into numerical meaning

Vector Search
    ↓
Meaning-based search

RAG Application
    ↓
Vector Search + GPT-generated answer
```

---

# Final Architecture

```text
User Question
      ↓
Azure OpenAI Embedding Model
      ↓
Query Vector
      ↓
Azure DocumentDB Vector Search
      ↓
Relevant Support Tickets
      ↓
Prompt Construction
      ↓
Azure OpenAI Chat Model
      ↓
Final Answer
```

---

# Final Takeaway

Keyword Search helps when the user knows the exact word.

Full Text Search helps when the user uses word variations.

Vector Search helps when the user describes the same meaning using different words.

RAG uses Vector Search to retrieve relevant business data and then uses an LLM to generate a grounded answer.

This is the foundation for building modern AI-native applications on Azure DocumentDB.

## Module 4B: Run AI agents

From this repository root, run:

```powershell
python .\scripts\run_ai_agents.py
```

Or if you prefer PowerShell script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_ai_agents.ps1
```

These scripts will clone `DocumentDB_Workshop_0906` automatically (if missing) and start the agents app.
On first run, the Python launcher also installs required companion repo dependencies.

If the browser opens automatically, use it.

If not, open:

```text
http://localhost:8080
```

You should see two agents:

- `MobileAdvisor`
- `RetailOfferFinder`

### Test MobileAdvisor

1. Click **MobileAdvisor**.
2. Paste:

  ```text
  Recommend a phone under 50000 for camera and battery
  ```

3. Press **Enter**.
4. Try:

  ```text
  I need a gaming phone with fast charging
  ```

5. Try:

  ```text
  Tell me about Samsung Galaxy S24 Ultra
  ```

### Test RetailOfferFinder

1. Go back to the agent list.
2. Click **RetailOfferFinder**.
3. Paste:

  ```text
  Where can I buy OnePlus 12?
  ```

4. Press **Enter**.
5. Try:

  ```text
  What mobiles are available from Flipkart?
  ```

To stop the app, go to PowerShell and press:

```text
Ctrl+C
```

Return to the repository root:

```powershell
# If you changed directories manually, return to repository root.
cd C:\Users\lab1euser4\Azure-DocumentDB-Workshop
```

## Extended Module 5: Performance checks

This module demonstrates how indexes dramatically improve query performance using a dedicated `headsets` collection.

### 5.1 Create headsets collection

Connect with `mongosh` again:

```powershell
mongosh "<paste DOCUMENTDB_CONNECTION_STRING here>"
```

Inside `mongosh`:

```javascript
use Workshop_DB
```

Create the `headsets` collection explicitly:

```javascript
// Create the headsets collection.
// This collection will hold 30 headsets across different categories.
db.createCollection("headsets")

// Verify the collection was created.
show collections
```

You should see `headsets` in the output.

### 5.2 Import headsets sample data

Now import the headset documents into the newly created collection.

**Option A: Direct import via mongosh**

```javascript
// Import 30 headsets for performance testing.
// This collection has brand, priceInr, type, and other fields.
// We will query it to demonstrate the impact of indexes.
db.headsets.insertMany([
  // Copy all 30 headsets from sample-docs\headsets_sample.json here
  // For quick import, use VS Code DocumentDB extension (see Option B below)
])

// Verify import.
db.headsets.countDocuments()  // expect 30
```

**Option B: Use VS Code DocumentDB extension (recommended)**

1. In the DocumentDB panel, expand **Workshop_DB**.
2. Right-click the **headsets** collection (now visible).
3. Click **Import Documents...**.
4. Select `sample-docs\headsets_sample.json`.
5. Wait for the import to complete.

Verify the import in mongosh:

```javascript
// Confirm 30 documents imported.
db.headsets.countDocuments()  // expect 30

// View a sample document.
db.headsets.findOne({}, { _id: 0 })
```

### 5.3 Demonstrate query performance WITHOUT an index

First, run a query **before creating an index** to see poor performance:

```javascript
// Query: Find all gaming headsets under 20000 INR.
// This query will perform a full collection scan (COLLSCAN) because no index exists.
db.headsets.find(
  {
    type: "Gaming Over-ear",
    priceInr: { $lte: 20000 }
  },
  {
    _id: 0,
    name: 1,
    brand: 1,
    type: 1,
    priceInr: 1,
    rating: 1
  }
)
```

Now check the **execution plan** to see the performance cost:

```javascript
// View the execution statistics BEFORE indexing.
// Look for "stage": "COLLSCAN" in the output — this means every document is scanned.
db.headsets.find(
  {
    type: "Gaming Over-ear",
    priceInr: { $lte: 20000 }
  }
).explain("executionStats")
```

**What to notice (WITHOUT index):**
- `executionStats.executionStages.stage` = `COLLSCAN` (full collection scan)
- `executionStats.totalDocsExamined` = ~30 (every document checked)
- `executionStats.executionStats.nReturned` = a few results (only 2 or 3 match the criteria)
- This is inefficient: the database scans ALL 30 documents to find a handful of matches.

### 5.4 Create a compound index

Now create an index on the fields used in the query:

```javascript
// Create a compound index on type and priceInr.
// This allows the database to jump directly to matching documents instead of scanning all.
db.headsets.createIndex(
  {
    type: 1,           // Field 1: type (ascending order)
    priceInr: 1        // Field 2: priceInr (ascending order)
  },
  { name: "headset_type_price_index" }
)
```

Verify the index was created:

```javascript
// List all indexes on the headsets collection.
db.headsets.getIndexes()
```

You should see:
- `_id_` (default)
- `headset_type_price_index` (newly created)

### 5.5 Demonstrate query performance WITH an index

Now run the **same query again** after creating the index:

```javascript
// Run the exact same query as before.
// This time, the database will use the index instead of scanning all documents.
db.headsets.find(
  {
    type: "Gaming Over-ear",
    priceInr: { $lte: 20000 }
  },
  {
    _id: 0,
    name: 1,
    brand: 1,
    type: 1,
    priceInr: 1,
    rating: 1
  }
)
```

Check the **execution plan** to see the improvement:

```javascript
// View the execution statistics AFTER indexing.
// Look for "stage": "IXSCAN" in the output — this means the index was used.
db.headsets.find(
  {
    type: "Gaming Over-ear",
    priceInr: { $lte: 20000 }
  }
).explain("executionStats")
```

**What to notice (WITH index):**
- `executionStats.executionStages.stage` = `IXSCAN` (index scan, not collection scan)
- `executionStats.totalDocsExamined` = ~4 (only relevant documents examined)
- `executionStats.nReturned` = ~4 (matches found)
- **Result: Much faster!** The database jumps to the index, finds matches, and returns them immediately.

### 5.6 Compare performance side-by-side

Run both queries and observe the difference:

```javascript
// Query 1: Complex price-based filter.
// With index, this scans only documents in the price range.
db.headsets.find(
  {
    priceInr: { $gte: 10000, $lte: 20000 }
  }
).explain("executionStats")

// Query 2: Multiple filter conditions.
// With index, both type and price conditions are resolved via the index.
db.headsets.find(
  {
    type: "Over-ear",
    noiseCancel: true,
    priceInr: { $lte: 30000 }
  }
).explain("executionStats")
```

### 5.7 Create additional indexes for other queries

Create indexes for other common filter patterns:

```javascript
// Index for brand searches.
db.headsets.createIndex(
  { brand: 1 },
  { name: "headset_brand_index" }
)

// Index for connectivity type searches.
db.headsets.createIndex(
  { connectivity: 1 },
  { name: "headset_connectivity_index" }
)

// Index for high-rated headsets (sorted by rating).
db.headsets.createIndex(
  { rating: -1 },
  { name: "headset_rating_index" }
)

// Verify all indexes.
db.headsets.getIndexes()
```

### 5.8 Run optimized queries with indexes

Now run queries that leverage the indexes:

```javascript
// Find premium headsets by Bose.
db.headsets.find(
  { brand: "Bose" },
  { _id: 0, name: 1, brand: 1, priceInr: 1, rating: 1 }
).explain("executionStats")

// Find highly-rated gaming headsets.
db.headsets.find(
  { type: "Gaming Over-ear", rating: { $gte: 4.5 } },
  { _id: 0, name: 1, type: 1, rating: 1, priceInr: 1 }
).explain("executionStats")

// Find wireless headsets sorted by price (highest first).
db.headsets.find(
  { connectivity: "Bluetooth 5.3" },
  { _id: 0, name: 1, connectivity: 1, priceInr: 1 }
).sort({ priceInr: -1 }).limit(5).explain("executionStats")
```

### 5.9 Key takeaways

| Aspect | WITHOUT Index | WITH Index |
|---|---|---|
| **Stage** | COLLSCAN | IXSCAN |
| **Docs Examined** | All (~30) | Only matching (~4) |
| **Speed** | Slower (scans all) | Faster (index lookup) |
| **Use Case** | One-time queries | Frequent queries |

**When to index:**
- Frequently queried fields (brand, type, price, rating)
- Filter conditions (`find({ brand: "X" })`)
- Sort operations (`.sort({ rating: -1 })`)
- Compound conditions (`type: "Gaming", priceInr: { $lte: 20000 }`)

**Exit mongosh:**

```javascript
exit
```

## Extended Module 6: Security review

Before you finish, review these checks:

1. In Azure Portal, open the DocumentDB resource.
2. Click **Networking**.
3. Confirm you did not leave broad public IP ranges open.
4. If you added temporary broad access, remove it.
5. Click **Save** if you changed anything.
6. Check that `.env` is not committed:

   ```powershell
   git status --short
   ```

7. Confirm `.env` does not appear in the output.

For production, do not use the workshop admin connection string directly in application code. Use least-privilege access and store secrets in an approved secret store such as Azure Key Vault.

## Final cleanup

Stop local app if it is still running:

```text
Ctrl+C
```

Deactivate Python environment:

```powershell
deactivate
```

If you created Azure resources only for this workshop and no longer need them:

1. Open Azure Portal.
2. Search for **Resource groups**.
3. Open:

   ```text
   rg-az-documentdb-workshop
   ```

4. Review the resources.
5. If you are sure you no longer need them, click **Delete resource group**.
6. Follow the confirmation prompts.

Only delete the resource group if you are sure nothing important is inside it.

## Troubleshooting quick list

### `DOCUMENTDB_CONNECTION_STRING not set`

Open `.env` and confirm the value is present and saved.

### Authentication failed

Check the username/password in the DocumentDB connection string. Copy it again from Azure Portal if needed.

### Network timeout

Add your current IP address under DocumentDB **Networking**.

### Missing embedding files

Make sure these files exist before running data load:

- `3-AI-Vector-Search\mobile-data\mobiles_with_vectors.json`
- `3-AI-Vector-Search\mobile-data\query_embeddings.json`
- `3-AI-Vector-Search\support-data\support_articles_with_vectors.json`

### Vector index creation fails

Check:

- Cluster tier is M30 or higher.
- `EMBEDDING_DIMENSIONS=256`.
- `mobiles_with_vectors.json` exists.

### DevUI does not open

Open manually:

```text
http://localhost:8080
```

### Port 8080 already in use

Close the previous app instance or restart PowerShell and run `python app.py` again.


