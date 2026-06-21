# Module 1: Introduction to Azure DocumentDB

Duration: 09:30-10:15

This module introduces the workshop architecture, outcomes, and dataset so participants have the full context before starting hands-on setup.

## Learning outcomes

By the end of this module, you will be able to:

- Explain where Azure DocumentDB fits in application architecture.
- Understand the workshop scenario and data flow.
- Identify the required tools and Azure resources.

## Step-by-step hands-on

### Step 1: Open the workshop repository

1. Open VS Code.
2. If you have not cloned the repo yet:
   - Click the Source Control (or GitHub) icon.
   - Click **Clone Repository**.
   - Paste: `https://github.com/Biksmind/Azure-DocumentDB-Workshop.git`
   - Choose destination: `C:\Users\lab1euser4\Azure-DocumentDB-Workshop`
   - Click **Open** after clone completes.
3. Open the following files in separate tabs:
   - `README.md`
   - `END-TO-END-WORKSHOP-RUNBOOK.md`

### Step 2: Review the workshop scenario

1. Read the architecture flow in `README.md`.
2. Confirm the data entities used in this workshop:
   - `mobiles`
   - `supportInc`
   - `retail_offers`

### Step 3: Review the day agenda

1. Open `README.md`.
2. Confirm Slot 1, Slot 2, Slot 3, and Slot 4 timings.
3. Confirm that migration is included as Slot 3.

### Step 4: Confirm prerequisites

1. Verify you have:
   - Azure subscription
   - VS Code
   - Python 3.10+
   - `mongosh`
   - Git

If these tools are missing on your VM, run this setup script in an elevated PowerShell terminal:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_vm_prerequisites.ps1
```

After the script completes, open a new terminal and verify:

```powershell
code --version
python --version
mongosh --version
git --version
```

### Step 5: Understand module flow

1. Review the five module folders in this repository.
2. Confirm the execution order:
   1. Introduction
   2. Cluster Setup and Connectivity
   3. Data Modeling, Import, Querying, Query Planning, Aggregation, Indexing
   4. Migration to Azure DocumentDB
   5. Search, AI Workloads, Agents, and RAG

## Expected result

You have a clear understanding of workshop scope, sequence, and required setup before starting configuration steps in Module 2.

## Next module

Continue to:

- `../2-Azure-DocumentDB-Cluster-Setup-and-Connectivity/README.md`

