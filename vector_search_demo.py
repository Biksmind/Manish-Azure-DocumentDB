from pymongo import MongoClient
from openai import AzureOpenAI

AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
AZURE_OPENAI_KEY = "<your-azure-openai-key>"
AZURE_OPENAI_API_VERSION = "2024-02-01"
EMBEDDING_DEPLOYMENT = "text-embedding-3-small"

MONGO_URI = "<your-documentdb-connection-string>"

DB_NAME = "Workshop_DB"
COLLECTION_NAME = "supportInc"

openai_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]

query = "what is score for ind vs afg test match"

response = openai_client.embeddings.create(
    model=EMBEDDING_DEPLOYMENT,
    input=query
)

query_vector = response.data[0].embedding

pipeline = [
    {
        "$search": {
            "cosmosSearch": {
                "vector": query_vector,
                "path": "embedding",
                "k": 5
            },
            "returnStoredSource": True
        }
    },
    {
        "$project": {
            "_id": 0,
            "ticketId": 1,
            "title": 1,
            "description": 1,
            "category": 1,
            "score": {"$meta": "searchScore"}
        }
    }
]

results = collection.aggregate(pipeline)

print("\nVector Search Results:\n")

for doc in results:
    print(f"{doc['ticketId']} | {doc['title']} | Score: {doc.get('score')}")
    print(doc["description"])
    print("-" * 80)