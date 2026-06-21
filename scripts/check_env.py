from __future__ import annotations

import os

from common import load_workshop_env, require_env


def main() -> None:
    load_workshop_env()
    required = [
        "DOCUMENTDB_CONNECTION_STRING",
        "DOCUMENTDB_DATABASE",
    ]
    optional_for_ai = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_CHAT_DEPLOYMENT",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
        "EMBEDDING_DIMENSIONS",
    ]

    for name in required:
        require_env(name)

    print("Environment check passed.")
    print(f"DOCUMENTDB_DATABASE={os.getenv('DOCUMENTDB_DATABASE', 'Workshop_DB')}")

    missing_ai = [
        name
        for name in optional_for_ai
        if not os.getenv(name) or "<" in os.getenv(name, "") or ">" in os.getenv(name, "")
    ]
    if missing_ai:
        print("Azure OpenAI values are not fully configured. Search/RAG/agent AI steps will need them.")
        for name in missing_ai:
            print(f"  Missing or placeholder: {name}")
    else:
        print("Azure OpenAI configuration found.")


if __name__ == "__main__":
    main()
