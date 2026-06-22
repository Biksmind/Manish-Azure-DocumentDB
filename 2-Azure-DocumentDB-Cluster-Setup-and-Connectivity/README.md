# Module 2: Azure DocumentDB Cluster Setup and Connectivity

This module creates the Azure DocumentDB cluster and connects to it from VS Code and `mongosh`.

## Goals

- Create an Azure DocumentDB cluster in Azure Portal.
- Use a workshop-friendly cluster configuration.
- Configure temporary workshop networking during creation.
- Store connection and Azure OpenAI settings in one `.env` file.
- Connect using the VS Code extension and `mongosh`.

## Portal configuration summary

| Portal field | Workshop value |
|---|---|
| Resource group | Use assigned group. Avoid creating a new resource group without instructor confirmation. |
| Region | `Central India`. Confirm with instructor before choosing any other region. |
| Admin username/password | Choose and save them safely for the session. They are used in the connection string. |
| High availability | Disabled for workshop |
| Cluster tier | Configure and select `M30` |
| Storage | 32 GB |
| Networking | Use instructor-provided workshop access approach |

A broad range may be used only for temporary workshop resources that will be cleaned up. Do not use broad public access for production.

## Environment setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.template .env
notepad .env
python .\scripts\check_env.py
```

## Connect with mongosh

```powershell
python .\scripts\print_mongosh_command.py
```

Copy and run the printed command, then run:

```javascript
use Workshop_DB
db.runCommand({ ping: 1 })
```

## Continue

For detailed screenshots/click-path style instructions, use [the end-to-end runbook](../END-TO-END-WORKSHOP-RUNBOOK.md).
