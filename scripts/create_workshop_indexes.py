from __future__ import annotations

import os

from pymongo.errors import OperationFailure

from common import get_database, load_workshop_env


def create_vector_index(db, collection_name: str, vector_field: str, index_name: str, dimensions: int) -> None:
    try:
        db.command(
            {
                "createIndexes": collection_name,
                "indexes": [
                    {
                        "name": index_name,
                        "key": {vector_field: "cosmosSearch"},
                        "cosmosSearchOptions": {
                            "kind": "vector-ivf",
                            "similarity": "COS",
                            "dimensions": dimensions,
                            "numLists": 1,
                        },
                    }
                ],
            }
        )
        print(f"Created vector index: {collection_name}.{index_name}")
    except OperationFailure as error:
        if "already exists" in str(error) or "IndexOptionsConflict" in str(error):
            print(f"Vector index already exists: {collection_name}.{index_name}")
            return
        raise


def main() -> None:
    load_workshop_env()
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    client, db, _ = get_database()
    try:
        db.supportInc.create_index(
            [("title", "text"), ("description", "text"), ("category", "text")],
            name="support_text_idx",
        )
        print("Created or verified text index: supportInc.support_text_idx")

        if db.supportInc.count_documents({"embedding": {"$exists": True}}, limit=1) == 0:
            raise RuntimeError("No supportInc.embedding values found. Run generate_workshop_embeddings.py first.")
        create_vector_index(db, "supportInc", "embedding", "support_vector_idx", dimensions)

        if db.mobiles.count_documents({"contentVector": {"$exists": True}}, limit=1) == 0:
            raise RuntimeError("No mobiles.contentVector values found. Run generate_workshop_embeddings.py first.")
        create_vector_index(db, "mobiles", "contentVector", "vector_index", dimensions)
    finally:
        client.close()


if __name__ == "__main__":
    main()
