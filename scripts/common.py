from __future__ import annotations

import json
import os
import warnings
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pymongo import MongoClient


ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT_DIR / ".env"


def load_workshop_env() -> None:
    load_dotenv(ENV_PATH)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.template to .env in {ROOT_DIR} and fill it in."
        )
    stripped = value.strip()
    if "<" in stripped or ">" in stripped:
        raise RuntimeError(f"{name} is still a placeholder in .env.")
    return stripped


def get_database():
    load_workshop_env()
    warnings.filterwarnings(
        "ignore",
        message="You appear to be connected to a CosmosDB cluster.*",
        category=UserWarning,
    )
    client = MongoClient(require_env("DOCUMENTDB_CONNECTION_STRING"))
    database_name = os.getenv("DOCUMENTDB_DATABASE", "Workshop_DB")
    return client, client[database_name], database_name


def load_json_array(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {path}")
    return data


def replace_collection(db, collection_name: str, documents: list[dict[str, Any]]) -> int:
    collection = db[collection_name]
    collection.delete_many({})
    if not documents:
        return 0
    collection.insert_many(documents, ordered=False)
    return len(documents)


def support_inc_documents() -> list[dict[str, Any]]:
    return load_json_array(ROOT_DIR / "sample-docs" / "support_inc_search_sample.json")
