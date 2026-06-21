"""Load mobile workshop data and create required indexes.

This is the copy-paste friendly setup path for attendees.

It loads (first available source):
    - mobiles: pre-generated vectors file, else sample-docs/mobiles_sample.json
    - support articles: pre-generated vectors file, else sample-docs/support_articles_sample.json
    - retail offers: 4-AI-Agents/mobile-agents/retail_offers.json, else sample-docs/retail_offers_sample.json

It creates:
  - mobile_text_index on title, brand, segment, description, features, useCases
  - vector_index on contentVector
  - support_text_index on support article title, category, content, and tags
  - support_vector_index on support article contentVector
  - lookup indexes for retail_offers
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient, ReplaceOne
from pymongo.errors import OperationFailure


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


def create_vector_index(db, collection_name: str, field_name: str, index_name: str, dimensions: int) -> None:
    try:
        db.command(
            {
                "createIndexes": collection_name,
                "indexes": [
                    {
                        "name": index_name,
                        "key": {field_name: "cosmosSearch"},
                        "cosmosSearchOptions": {
                            "kind": "vector-diskann",
                            "dimensions": dimensions,
                            "similarity": "COS",
                        },
                    }
                ],
            }
        )
        print(f"Created vector index: {collection_name}.{index_name}")
    except OperationFailure as error:
        message = str(error)
        if "already exists" in message or "IndexOptionsConflict" in message:
            print(f"Vector index already exists: {collection_name}.{index_name}")
            return
        raise


def first_existing_path(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    candidates = "\n".join(f"  - {path}" for path in paths)
    raise FileNotFoundError(
        "No valid data file found. Checked:\n"
        f"{candidates}\n"
        "Ensure the workshop repository is complete, then rerun:\n"
        "  python .\\scripts\\load_workshop_data.py"
    )


def has_field(documents: list[dict], field_name: str) -> bool:
    return any(field_name in document and document[field_name] is not None for document in documents)


def main() -> None:
    connection_string = require_env("DOCUMENTDB_CONNECTION_STRING")
    database_name = os.getenv("DOCUMENTDB_DATABASE", "Workshop_DB")
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "256"))

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
    mobiles_have_vectors = has_field(mobiles, "contentVector")
    mobiles_written = upsert_by_title(db.mobiles, mobiles)
    print(f"Loaded or updated {mobiles_written} mobile documents in {database_name}.mobiles")

    print("Creating full-text index on mobiles...")
    db.mobiles.create_index(
        [
            ("title", "text"),
            ("brand", "text"),
            ("segment", "text"),
            ("description", "text"),
            ("features", "text"),
            ("useCases", "text"),
        ],
        name="mobile_text_index",
    )
    print("Created text index: mobiles.mobile_text_index")

    print("Skipping filter indexes on mobiles (students will create these during Module 2 indexing exercise)")

    if mobiles_have_vectors:
        print("Creating DiskANN vector index on mobiles.contentVector...")
        create_vector_index(db, "mobiles", "contentVector", "vector_index", dimensions)
    else:
        print("Skipping mobiles vector index: contentVector not present in loaded data.")

    print(f"Loading support articles from {support_path}...")
    supportInc = load_json(support_path)
    support_have_vectors = has_field(supportInc, "contentVector")
    support_written = upsert_by_article_id(db.supportInc, supportInc)
    print(
        f"Loaded or updated {support_written} support articles "
        f"in {database_name}.supportInc"
    )

    print("Creating full-text index on supportInc...")
    db.supportInc.create_index(
        [
            ("title", "text"),
            ("product", "text"),
            ("category", "text"),
            ("content", "text"),
            ("tags", "text"),
        ],
        name="support_text_index",
    )
    print("Created text index: supportInc.support_text_index")

    print("Skipping support article filter indexes (students will create these during hands-on exercises)")

    if support_have_vectors:
        print("Creating DiskANN vector index on supportInc.contentVector...")
        create_vector_index(
            db,
            "supportInc",
            "contentVector",
            "support_vector_index",
            dimensions,
        )
    else:
        print("Skipping supportInc vector index: contentVector not present in loaded data.")

    print(f"Loading retail offers from {offers_path}...")
    offers = load_json(offers_path)
    offers_written = upsert_by_title(db.retail_offers, offers)
    print(f"Loaded or updated {offers_written} offer documents in {database_name}.retail_offers")

    print("Creating retail offer lookup indexes...")
    db.retail_offers.create_index("title", name="offer_title_index", unique=True)
    db.retail_offers.create_index("offers.retailer", name="offer_retailer_index")
    db.retail_offers.create_index("offers.availability", name="offer_availability_index")
    print("Skipping retail offer indexes (students will create these during hands-on exercises)_documents({})}")
    print(f"  supportInc count: {db.supportInc.count_documents({})}")
    print(f"  retail_offers count: {db.retail_offers.count_documents({})}")
    print("  mobile indexes:")
    for index in db.mobiles.list_indexes():
        print(f"    - {index['name']}")

    client.close()
    print("\nMobile workshop data load complete.")


if __name__ == "__main__":
    main()

