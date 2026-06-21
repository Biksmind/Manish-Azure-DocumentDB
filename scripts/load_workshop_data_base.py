"""Load mobile workshop data WITHOUT indexes.

This script loads the base data only:
  - mobiles
  - supportInc
  - retail_offers

NO indexes are created. Students create indexes manually during Module 2 exercises.

Use this script:
1. In Module 2 Step 1 to load initial data.
2. After dropping collections to reload for re-exercising.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient, ReplaceOne


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.template to .env in {ROOT_DIR} and fill in the workshop values."
        )
    return value


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required data file not found: {path}"
        )
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {path}")
    return data


def upsert_by_title(collection, documents: list[dict]) -> int:
    operations = []
    for document in documents:
        title = document.get("title")
        if not title:
            raise ValueError(f"Document missing required title field: {document}")
        operations.append(ReplaceOne({"title": title}, document, upsert=True))

    if not operations:
        return 0

    result = collection.bulk_write(operations, ordered=False)
    return result.upserted_count + result.modified_count + result.matched_count


def upsert_by_article_id(collection, documents: list[dict]) -> int:
    operations = []
    for document in documents:
        article_id = document.get("articleId")
        if not article_id:
            raise ValueError(f"Document missing required articleId field: {document}")
        operations.append(ReplaceOne({"articleId": article_id}, document, upsert=True))

    if not operations:
        return 0

    result = collection.bulk_write(operations, ordered=False)
    return result.upserted_count + result.modified_count + result.matched_count


def first_existing_path(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    candidates = "\n".join(f"  - {path}" for path in paths)
    raise FileNotFoundError(
        "No valid data file found. Checked:\n"
        f"{candidates}\n"
        "Ensure the workshop repository is complete, then rerun:\n"
        "  python .\\scripts\\load_workshop_data_base.py"
    )


def main() -> None:
    connection_string = require_env("DOCUMENTDB_CONNECTION_STRING")
    database_name = os.getenv("DOCUMENTDB_DATABASE", "Workshop_DB")

    mobiles_path = first_existing_path(
        ROOT_DIR / "3-AI-Vector-Search" / "mobile-data" / "mobiles_with_vectors.json",
        ROOT_DIR / "sample-docs" / "mobiles_sample.json",
    )
    support_path = first_existing_path(
        ROOT_DIR / "3-AI-Vector-Search" / "support-data" / "support_articles_with_vectors.json",
        ROOT_DIR / "sample-docs" / "support_articles_sample.json",
    )
    offers_path = first_existing_path(
        ROOT_DIR / "4-AI-Agents" / "mobile-agents" / "retail_offers.json",
        ROOT_DIR / "sample-docs" / "retail_offers_sample.json",
    )

    print("Connecting to Azure DocumentDB...")
    client = MongoClient(connection_string)
    db = client[database_name]

    print(f"Loading mobiles from {mobiles_path}...")
    mobiles = load_json(mobiles_path)
    mobiles_written = upsert_by_title(db.mobiles, mobiles)
    print(f"Loaded or updated {mobiles_written} mobile documents in {database_name}.mobiles")

    print(f"Loading support articles from {support_path}...")
    supportInc = load_json(support_path)
    support_written = upsert_by_article_id(db.supportInc, supportInc)
    print(
        f"Loaded or updated {support_written} support articles "
        f"in {database_name}.supportInc"
    )

    print(f"Loading retail offers from {offers_path}...")
    offers = load_json(offers_path)
    offers_written = upsert_by_title(db.retail_offers, offers)
    print(f"Loaded or updated {offers_written} offer documents in {database_name}.retail_offers")

    print("\nVerification:")
    print(f"  Database: {database_name}")
    print(f"  mobiles count: {db.mobiles.count_documents({})}")
    print(f"  supportInc count: {db.supportInc.count_documents({})}")
    print(f"  retail_offers count: {db.retail_offers.count_documents({})}")

    client.close()
    print("\nBase workshop data load complete.")


if __name__ == "__main__":
    main()

