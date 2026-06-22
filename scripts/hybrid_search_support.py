from __future__ import annotations

import argparse
import os

from openai import AzureOpenAI

from common import get_database, load_workshop_env, require_env


def normalize_scores(results: list[dict], score_field: str) -> dict[str, float]:
    scores = {item["ticketId"]: float(item.get(score_field, 0) or 0) for item in results}
    max_score = max(scores.values(), default=0)
    if max_score <= 0:
        return {ticket_id: 0.0 for ticket_id in scores}
    return {ticket_id: score / max_score for ticket_id, score in scores.items()}


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
    for index, document in enumerate(results, 1):
        print(f"{index}. {document.get('ticketId')} | {document.get('title')} | {score_field}: {document.get(score_field)}")
        print(document.get("description"))
        print("-" * 80)


def merge_hybrid_results(text_results: list[dict], vector_results: list[dict]) -> list[dict]:
    text_normalized = normalize_scores(text_results, "textScore")
    vector_normalized = normalize_scores(vector_results, "vectorScore")

    by_ticket: dict[str, dict] = {}
    for item in [*text_results, *vector_results]:
        by_ticket.setdefault(item["ticketId"], item)

    merged = []
    for ticket_id, item in by_ticket.items():
        text_score = text_normalized.get(ticket_id, 0.0)
        vector_score = vector_normalized.get(ticket_id, 0.0)
        hybrid_score = (0.6 * text_score) + (0.4 * vector_score)
        if text_score and vector_score:
            reason = "matched by exact words and semantic meaning"
        elif text_score:
            reason = "matched by full-text words only"
        else:
            reason = "matched by semantic vector meaning only"
        merged.append(
            {
                **item,
                "normalizedTextScore": text_score,
                "normalizedVectorScore": vector_score,
                "hybridScore": hybrid_score,
                "reason": reason,
            }
        )
    return sorted(merged, key=lambda item: item["hybridScore"], reverse=True)


def print_hybrid_results(results: list[dict]) -> None:
    print("\nFinal hybrid-ranked results:")
    if not results:
        print("No results.")
        return
    for index, item in enumerate(results, 1):
        print(f"{index}. {item.get('ticketId')} | {item.get('title')}")
        print(f"   Text contribution: {item['normalizedTextScore']:.3f}")
        print(f"   Vector contribution: {item['normalizedVectorScore']:.3f}")
        print(f"   Hybrid score: {item['hybridScore']:.3f}")
        print(f"   Why selected: {item['reason']}")
        print(f"   {item.get('description')}")
        print("-" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run vector, full-text, and hybrid search for a workshop query.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    client, db, _ = get_database()
    try:
        collection = db.supportInc
        vector_results = vector_search(collection, args.query, args.top_k)
        text_results = text_search(collection, args.query, args.top_k)
    finally:
        client.close()

    print(f'Query: "{args.query}"')
    print("\nStep 1 - Vector search")
    print("Vector search uses embeddings to find records with similar meaning, even when words differ.")
    print_results("Vector search results", vector_results, "vectorScore")

    print("\nStep 2 - Full-text search")
    print("Full-text search uses exact words, tokenization, and text relevance scoring.")
    print_results("Full-text search results", text_results, "textScore")

    print("\nStep 3 - Hybrid search")
    print("Hybrid search merges both result sets and re-ranks them.")
    print("Workshop formula: hybridScore = 0.6 * normalizedTextScore + 0.4 * normalizedVectorScore")
    print_hybrid_results(merge_hybrid_results(text_results, vector_results))

    print("\nWhy this is different:")
    print("- Vector-only search may include semantically related but weaker matches.")
    print("- Full-text-only search may miss records that use different words.")
    print("- Hybrid search promotes records that are strong in both word match and meaning match.")


if __name__ == "__main__":
    main()
