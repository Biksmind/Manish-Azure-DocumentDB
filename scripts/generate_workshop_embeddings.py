from __future__ import annotations

import os

from openai import AzureOpenAI

from common import get_database, load_workshop_env, require_env


def mobile_text(document: dict) -> str:
    return "\n".join(
        [
            f"Title: {document.get('title', '')}",
            f"Brand: {document.get('brand', '')}",
            f"Segment: {document.get('segment', '')}",
            f"Description: {document.get('description', '')}",
            f"Features: {'; '.join(document.get('features', []))}",
            f"Use cases: {'; '.join(document.get('useCases', []))}",
            f"Price INR: {document.get('priceInr', '')}",
            f"Camera MP: {document.get('cameraMp', '')}",
            f"Battery mAh: {document.get('batteryMah', '')}",
        ]
    )


def support_text(document: dict) -> str:
    return "\n".join(
        [
            f"Ticket ID: {document.get('ticketId', '')}",
            f"Title: {document.get('title', '')}",
            f"Description: {document.get('description', '')}",
            f"Category: {document.get('category', '')}",
            f"Priority: {document.get('priority', '')}",
        ]
    )


def create_embedding(openai_client: AzureOpenAI, deployment: str, text: str, dimensions: int) -> list[float]:
    response = openai_client.embeddings.create(
        model=deployment,
        input=text,
        dimensions=dimensions,
    )
    return response.data[0].embedding


def main() -> None:
    load_workshop_env()
    endpoint = require_env("AZURE_OPENAI_ENDPOINT")
    api_key = require_env("AZURE_OPENAI_API_KEY")
    api_version = require_env("AZURE_OPENAI_API_VERSION")
    embedding_deployment = require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))

    openai_client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    client, db, database_name = get_database()
    try:
        mobile_total = 0
        for document in db.mobiles.find({}, {"contentVector": 0}):
            vector = create_embedding(openai_client, embedding_deployment, mobile_text(document), dimensions)
            db.mobiles.update_one(
                {"_id": document["_id"]},
                {"$set": {"contentVector": vector}},
            )
            mobile_total += 1

        support_total = 0
        for document in db.supportInc.find({}, {"embedding": 0}):
            vector = create_embedding(openai_client, embedding_deployment, support_text(document), dimensions)
            db.supportInc.update_one(
                {"_id": document["_id"]},
                {"$set": {"embedding": vector}},
            )
            support_total += 1

        print(f"Generated embeddings for {mobile_total} records in {database_name}.mobiles.contentVector")
        print(f"Generated embeddings for {support_total} records in {database_name}.supportInc.embedding")
    finally:
        client.close()


if __name__ == "__main__":
    main()
