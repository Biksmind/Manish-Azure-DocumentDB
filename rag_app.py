from __future__ import annotations

import os

from openai import AzureOpenAI

from scripts.common import get_database, load_workshop_env, require_env


def generate_embedding(openai_client: AzureOpenAI, deployment: str, text: str, dimensions: int) -> list[float]:
    response = openai_client.embeddings.create(
        model=deployment,
        input=text,
        dimensions=dimensions,
    )
    return response.data[0].embedding


def vector_search(collection, query_vector: list[float], top_k: int = 3) -> list[dict]:
    pipeline = [
        {
            "$search": {
                "cosmosSearch": {
                    "vector": query_vector,
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
                "priority": 1,
                "score": {"$meta": "searchScore"},
            }
        },
    ]
    return list(collection.aggregate(pipeline))


def build_context(results: list[dict]) -> str:
    parts = []
    for item in results:
        parts.append(
            "\n".join(
                [
                    f"Ticket ID: {item.get('ticketId')}",
                    f"Title: {item.get('title')}",
                    f"Description: {item.get('description')}",
                    f"Category: {item.get('category')}",
                    f"Priority: {item.get('priority')}",
                ]
            )
        )
    return "\n---\n".join(parts)


def generate_answer(openai_client: AzureOpenAI, deployment: str, question: str, context: str) -> str:
    response = openai_client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a workshop support assistant. Answer only from the provided "
                    "support ticket context. If the context does not contain the answer, "
                    "say you do not have enough information."
                ),
            },
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nSupport ticket context:\n{context}\n\nAnswer:",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def main() -> None:
    load_workshop_env()
    endpoint = require_env("AZURE_OPENAI_ENDPOINT")
    api_key = require_env("AZURE_OPENAI_API_KEY")
    api_version = require_env("AZURE_OPENAI_API_VERSION")
    embedding_deployment = require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    chat_deployment = require_env("AZURE_OPENAI_CHAT_DEPLOYMENT")
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))

    openai_client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    mongo_client, db, database_name = get_database()
    collection = db.supportInc

    print(f"\nAzure DocumentDB RAG Demo using {database_name}.supportInc")
    print("Type 'exit' to stop.\n")

    try:
        while True:
            question = input("Ask your question: ").strip()
            if question.lower() == "exit":
                break
            if not question:
                continue

            query_vector = generate_embedding(openai_client, embedding_deployment, question, dimensions)
            results = vector_search(collection, query_vector)

            print("\nRetrieved tickets:")
            for item in results:
                print(f"- {item.get('ticketId')} | {item.get('title')} | Score: {item.get('score')}")

            answer = generate_answer(openai_client, chat_deployment, question, build_context(results))
            print("\nAnswer:")
            print(answer)
            print("\n" + "-" * 80 + "\n")
    finally:
        mongo_client.close()


if __name__ == "__main__":
    main()
