from __future__ import annotations

import argparse
import os

from openai import AzureOpenAI

from common import get_database, load_workshop_env, require_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run vector search against supportInc.")
    parser.add_argument("--query", required=True, help="Question or phrase to search for.")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    load_workshop_env()
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    openai_client = AzureOpenAI(
        azure_endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
        api_key=require_env("AZURE_OPENAI_API_KEY"),
        api_version=require_env("AZURE_OPENAI_API_VERSION"),
    )

    response = openai_client.embeddings.create(
        model=require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=args.query,
        dimensions=dimensions,
    )

    pipeline = [
        {
            "$search": {
                "cosmosSearch": {
                    "vector": response.data[0].embedding,
                    "path": "embedding",
                    "k": args.top_k,
                },
                "returnStoredSource": True,
            }
        },
        {
            "$project": {
                "_id": 0,
                "ticketId": 1,
                "title": 1,
                "description": 1,
                "category": 1,
                "score": {"$meta": "searchScore"},
            }
        },
    ]

    client, db, _ = get_database()
    try:
        for document in db.supportInc.aggregate(pipeline):
            print(f"{document.get('ticketId')} | {document.get('title')} | Score: {document.get('score')}")
            print(document.get("description"))
            print("-" * 80)
    finally:
        client.close()


if __name__ == "__main__":
    main()
