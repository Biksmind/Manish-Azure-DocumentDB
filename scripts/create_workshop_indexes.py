"""Create workshop indexes after data load and embedding generation."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Update .env in {ROOT_DIR} and rerun."
        )
    return value


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


def main() -> None:
    connection_string = require_env("DOCUMENTDB_CONNECTION_STRING")
    database_name = os.getenv("DOCUMENTDB_DATABASE", "Workshop_DB")
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "256"))

    mongo_client = MongoClient(connection_string)
    db = mongo_client[database_name]

    print("Creating text index on mobiles...")
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

    print("Creating text index on supportInc...")
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

    if db.mobiles.count_documents({"contentVector": {"$exists": True}}, limit=1) > 0:
        create_vector_index(db, "mobiles", "contentVector", "vector_index", dimensions)
    else:
        raise RuntimeError(
            "No mobiles.contentVector found. Run: python .\\scripts\\generate_workshop_embeddings.py"
        )

    if db.supportInc.count_documents({"contentVector": {"$exists": True}}, limit=1) > 0:
        create_vector_index(db, "supportInc", "contentVector", "support_vector_index", dimensions)
    else:
        raise RuntimeError(
            "No supportInc.contentVector found. Run: python .\\scripts\\generate_workshop_embeddings.py"
        )

    print("Creating retail offer lookup indexes...")
    db.retail_offers.create_index("title", name="offer_title_index", unique=True)
    db.retail_offers.create_index("offers.retailer", name="offer_retailer_index")
    db.retail_offers.create_index("offers.availability", name="offer_availability_index")

    mongo_client.close()
    print("Index creation complete.")


if __name__ == "__main__":
    main()

