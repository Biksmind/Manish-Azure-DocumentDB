"""Generate embeddings for workshop collections and store them in Azure DocumentDB.

This script updates:
  - Workshop_DB.mobiles.contentVector
  - Workshop_DB.supportInc.contentVector

Requirements:
  - DOCUMENTDB_CONNECTION_STRING
  - AZURE_OPENAI_ENDPOINT
  - AZURE_OPENAI_API_KEY
  - AZURE_OPENAI_API_VERSION
  - AZURE_OPENAI_EMBEDDING_DEPLOYMENT
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AzureOpenAI
from pymongo import MongoClient


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


def build_mobile_text(document: dict) -> str:
    return "\n".join(
        [
            f"Title: {document.get('title', '')}",
            f"Brand: {document.get('brand', '')}",
            f"Segment: {document.get('segment', '')}",
            f"Description: {document.get('description', '')}",
            f"Features: {'; '.join(document.get('features', []))}",
            f"Use Cases: {'; '.join(document.get('useCases', []))}",
        ]
    ).strip()


def build_support_text(document: dict) -> str:
    return "\n".join(
        [
            f"Article ID: {document.get('articleId', '')}",
            f"Title: {document.get('title', '')}",
            f"Product: {document.get('product', '')}",
            f"Category: {document.get('category', '')}",
            f"Severity: {document.get('severity', '')}",
            f"Content: {document.get('content', '')}",
            f"Tags: {'; '.join(document.get('tags', []))}",
        ]
    ).strip()


def create_embedding(client: AzureOpenAI, model: str, text: str, dimensions: int | None) -> list[float]:
    kwargs: dict = {"model": model, "input": text}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions
    response = client.embeddings.create(**kwargs)
    return response.data[0].embedding


def main() -> None:
    connection_string = require_env("DOCUMENTDB_CONNECTION_STRING")
    database_name = os.getenv("DOCUMENTDB_DATABASE", "Workshop_DB")

    endpoint = require_env("AZURE_OPENAI_ENDPOINT")
    api_key = require_env("AZURE_OPENAI_API_KEY")
    api_version = require_env("AZURE_OPENAI_API_VERSION")
    embedding_deployment = require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

    dimensions = os.getenv("EMBEDDING_DIMENSIONS")
    embedding_dimensions = int(dimensions) if dimensions else None

    openai_client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    mongo_client = MongoClient(connection_string)
    db = mongo_client[database_name]

    print("Generating embeddings for mobiles...")
    mobile_total = 0
    for document in db.mobiles.find({}, {"_id": 1, "title": 1, "brand": 1, "segment": 1, "description": 1, "features": 1, "useCases": 1}):
        text = build_mobile_text(document)
        vector = create_embedding(openai_client, embedding_deployment, text, embedding_dimensions)
        db.mobiles.update_one({"_id": document["_id"]}, {"$set": {"contentVector": vector}})
        mobile_total += 1

    print("Generating embeddings for supportInc...")
    support_total = 0
    for document in db.supportInc.find({}, {"_id": 1, "articleId": 1, "title": 1, "product": 1, "category": 1, "severity": 1, "content": 1, "tags": 1}):
        text = build_support_text(document)
        vector = create_embedding(openai_client, embedding_deployment, text, embedding_dimensions)
        db.supportInc.update_one({"_id": document["_id"]}, {"$set": {"contentVector": vector}})
        support_total += 1

    mongo_client.close()

    print(f"Updated mobiles embeddings: {mobile_total}")
    print(f"Updated supportInc embeddings: {support_total}")
    print("Embedding generation complete.")


if __name__ == "__main__":
    main()

