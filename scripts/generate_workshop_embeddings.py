from __future__ import annotations

import os

from openai import AzureOpenAI

from common import get_database, load_workshop_env, require_env


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
        total = 0
        for document in db.supportInc.find({}, {"embedding": 0}):
            response = openai_client.embeddings.create(
                model=embedding_deployment,
                input=support_text(document),
                dimensions=dimensions,
            )
            db.supportInc.update_one(
                {"_id": document["_id"]},
                {"$set": {"embedding": response.data[0].embedding}},
            )
            total += 1

        print(f"Generated embeddings for {total} records in {database_name}.supportInc")
    finally:
        client.close()


if __name__ == "__main__":
    main()
