from __future__ import annotations

import argparse
import os

from openai import AzureOpenAI

from common import get_database, load_workshop_env, require_env


def text_search(collection, query: str, top_k: int) -> list[dict]:
    return list(
        collection.find(
            {"$text": {"$search": query}},
            {
                "_id": 0,
                "ticketId": 1,
                "title": 1,
                "description": 1,
                "category": 1,
                "textScore": {"$meta": "textScore"},
            },
        )
        .sort([("textScore", {"$meta": "textScore"})])
        .limit(top_k)
    )


def vector_search(collection, query: str, top_k: int) -> list[dict]:
    load_workshop_env()
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    openai_client = AzureOpenAI(
        azure_endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
        api_key=require_env("AZURE_OPENAI_API_KEY"),
        api_version=require_env("AZURE_OPENAI_API_VERSION"),
    )
    response = openai_client.embeddings.create(
        model=require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=query,
        dimensions=dimensions,
    )
    pipeline = [
        {
            "$search": {
                "cosmosSearch": {
                    "vector": response.data[0].embedding,
                    "path": "embedding",
                    "k": top_k,
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
                "vectorScore": {"$meta": "searchScore"},
            }
        },
    ]
    return list(collection.aggregate(pipeline))


def print_results(label: str, results: list[dict], score_field: str) -> None:
    print(f"\n{label}:")
    if not results:
        print("No results.")
        return
    for document in results:
        print(f"{document.get('ticketId')} | {document.get('title')} | {score_field}: {document.get(score_field)}")
        print(document.get("description"))
        print("-" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare full-text and vector search for a workshop query.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    client, db, _ = get_database()
    try:
        collection = db.supportInc
        text_results = text_search(collection, args.query, args.top_k)
        vector_results = vector_search(collection, args.query, args.top_k)
    finally:
        client.close()

    print(f'Query: "{args.query}"')
    print("\nThis hybrid demo runs two searches for the same query:")
    print("1. Full-text search: matches exact words and text relevance.")
    print("2. Vector search: matches semantic meaning using embeddings.")
    print("\nIn a production hybrid implementation, both result sets are merged and re-ranked.")

    print_results("Full-text search results", text_results, "textScore")
    print_results("Vector search results", vector_results, "vectorScore")

    text_ids = {item.get("ticketId") for item in text_results}
    vector_ids = {item.get("ticketId") for item in vector_results}
    overlap = [ticket_id for ticket_id in text_ids.intersection(vector_ids) if ticket_id]

    print("\nHow this differs from normal vector search:")
    print("- Normal vector search only shows semantic matches.")
    print("- This hybrid demo also shows which records matched the exact words from the query.")
    print("- If the same ticket appears in both lists, it is a strong candidate because it matched by words and meaning.")
    print(f"- Overlap in this run: {', '.join(sorted(overlap)) if overlap else 'No overlapping tickets'}")


if __name__ == "__main__":
    main()
