from __future__ import annotations

import json
import sys
from typing import Any

from common import get_database


def list_collections() -> dict[str, Any]:
    client, db, database_name = get_database()
    try:
        return {"database": database_name, "collections": sorted(db.list_collection_names())}
    finally:
        client.close()


def count_documents() -> dict[str, Any]:
    client, db, database_name = get_database()
    try:
        collections = ["mobiles", "support_articles", "retail_offers", "supportInc"]
        return {
            "database": database_name,
            "counts": {name: db[name].count_documents({}) for name in collections},
        }
    finally:
        client.close()


TOOLS = [
    {
        "name": "list_workshop_collections",
        "description": "List collections in the configured Azure DocumentDB workshop database.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "count_workshop_documents",
        "description": "Count documents in the four workshop collections.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def result(request_id: Any, payload: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def text_content(payload: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}]}


def handle(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")

    if method == "initialize":
        return result(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "azure-documentdb-workshop", "version": "1.0.0"},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return result(request_id, {"tools": TOOLS})
    if method == "tools/call":
        tool_name = request.get("params", {}).get("name")
        if tool_name == "list_workshop_collections":
            return result(request_id, text_content(list_collections()))
        if tool_name == "count_workshop_documents":
            return result(request_id, text_content(count_documents()))
        return error(request_id, -32602, f"Unknown tool: {tool_name}")
    return error(request_id, -32601, f"Unsupported method: {method}")


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            response = handle(json.loads(line))
            if response is not None:
                print(json.dumps(response), flush=True)
        except Exception as exc:
            print(json.dumps(error(None, -32000, str(exc))), flush=True)


if __name__ == "__main__":
    main()
