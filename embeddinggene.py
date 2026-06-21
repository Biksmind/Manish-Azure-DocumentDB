from pathlib import Path
import os

from dotenv import load_dotenv
from openai import AzureOpenAI
from pymongo import MongoClient


ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

COLLECTION_NAME = "supportInc"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Update .env in {ROOT_DIR} and rerun."
        )
    if value.startswith("<") and value.endswith(">"):
        raise RuntimeError(
            f"{name} is still a placeholder in .env. Replace it with a real value and rerun."
        )
    if value.strip() in {'""', "''"}:
        raise RuntimeError(
            f"{name} is empty in .env. Replace it with a real value and rerun."
        )
    return value


def generate_embedding(client: AzureOpenAI, deployment: str, text: str):
    response = client.embeddings.create(
        model=deployment,
        input=text
    )
    return response.data[0].embedding


def main():
    mongo_uri = require_env("DOCUMENTDB_CONNECTION_STRING")
    database_name = os.getenv("DOCUMENTDB_DATABASE", "Workshop_DB")
    endpoint = require_env("AZURE_OPENAI_ENDPOINT")
    api_key = require_env("AZURE_OPENAI_API_KEY")
    api_version = require_env("AZURE_OPENAI_API_VERSION")
    embedding_deployment = require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

    openai_client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    mongo_client = MongoClient(mongo_uri)
    collection = mongo_client[database_name][COLLECTION_NAME]

    tickets = collection.find({})
    updated_count = 0

    for ticket in tickets:
        text_for_embedding = f"""
Title: {ticket.get('title', '')}
Description: {ticket.get('description', '')}
Category: {ticket.get('category', '')}
Priority: {ticket.get('priority', '')}
""".strip()

        embedding = generate_embedding(openai_client, embedding_deployment, text_for_embedding)

        collection.update_one(
            {"_id": ticket["_id"]},
            {
                "$set": {
                    "embedding": embedding,
                    "embeddingText": text_for_embedding,
                }
            },
        )

        print(f"Updated embedding for {ticket['ticketId']}")
        updated_count += 1

    mongo_client.close()
    print(f"All embeddings generated successfully. Updated {updated_count} documents.")


if __name__ == "__main__":
    main()