from __future__ import annotations

import os
import re
from typing import Annotated

from agent_framework import tool
from openai import AzureOpenAI
from pydantic import Field
from pymongo.errors import OperationFailure

from common import get_database, load_workshop_env, require_env


SEMANTIC_INTENT_EXPANSIONS = {
    "budget": [
        "affordable 5G smartphone",
        "budget friendly 5G phone",
        "student budget smartphone",
        "value for money 5G",
    ],
    "camera": [
        "camera performance smartphone",
        "photography phone",
        "best camera battery phone",
        "travel photography phone",
    ],
    "battery": [
        "long battery life smartphone",
        "all day battery phone",
        "battery backup mobile",
        "battery monster smartphone",
    ],
    "gaming": [
        "gaming smartphone",
        "high performance gaming phone",
        "smooth gaming fast charging",
        "lag free gaming smartphone",
    ],
    "premium": [
        "flagship camera smartphone",
        "premium photography phone",
        "high end mobile",
        "premium performance smartphone",
    ],
    "office": [
        "business productivity smartphone",
        "phone for office work",
        "clean software productivity phone",
        "multitasking phone",
    ],
}


def _normalize_azure_endpoint(value: str) -> str:
    value = value.rstrip("/")
    if value.endswith("/openai/v1"):
        value = value[: -len("/openai/v1")]
    return value


def _get_openai_client() -> AzureOpenAI:
    load_workshop_env()
    return AzureOpenAI(
        azure_endpoint=_normalize_azure_endpoint(require_env("AZURE_OPENAI_ENDPOINT")),
        api_key=require_env("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    )


def _generate_embedding(text: str) -> list[float]:
    client = _get_openai_client()
    deployment = require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    response = client.embeddings.create(model=deployment, input=text, dimensions=dimensions)
    return response.data[0].embedding


def _detect_intents(query: str) -> set[str]:
    normalized = query.lower()
    terms = set(re.findall(r"[a-z0-9]+", normalized))
    intents: set[str] = set()

    if terms & {"cheap", "budget", "affordable", "value", "student"}:
        intents.add("budget")
    if re.search(r"\b(under|below|within)\s+\d+", normalized):
        intents.add("budget")
    if terms & {"camera", "photo", "photos", "photography", "portrait", "selfie"}:
        intents.add("camera")
    if terms & {"battery", "backup", "power", "charging"}:
        intents.add("battery")
    if terms & {"gaming", "game", "games", "performance", "lag"}:
        intents.add("gaming")
    if terms & {"premium", "flagship", "business"}:
        intents.add("premium")
    if terms & {"office", "work", "productivity"}:
        intents.add("office")
    if not intents and terms & {"mobile", "mobiles", "phone", "phones", "smartphone"}:
        intents.update({"budget", "camera", "battery"})
    return intents


def _expand_query(query: str) -> str:
    phrases: list[str] = []
    for intent in sorted(_detect_intents(query)):
        phrases.extend(SEMANTIC_INTENT_EXPANSIONS[intent])
    return " | ".join([query, *phrases]) if phrases else query


def _infer_max_price(query: str) -> int | None:
    normalized = query.lower().replace(",", "")
    for pattern in [
        r"\bunder\s+(?:inr|rs\.?|₹)?\s*(\d+)\b",
        r"\bbelow\s+(?:inr|rs\.?|₹)?\s*(\d+)\b",
        r"\bwithin\s+(?:inr|rs\.?|₹)?\s*(\d+)\b",
        r"\bless\s+than\s+(?:inr|rs\.?|₹)?\s*(\d+)\b",
    ]:
        match = re.search(pattern, normalized)
        if match:
            return int(match.group(1))
    return None


def _format_mobile(mobile: dict, include_score: bool = False) -> str:
    price = mobile.get("priceInr", 0)
    score_text = f"\n   Similarity score: {mobile.get('score', 0):.4f}" if include_score else ""
    features = ", ".join(mobile.get("features", [])[:4])
    return (
        f"**{mobile.get('title')}** - {mobile.get('brand')} | {mobile.get('segment')}\n"
        f"   Price: INR {price:,} | Rating: {mobile.get('rating', 'N/A')}/5 | "
        f"Battery: {mobile.get('batteryMah', 'N/A')} mAh | Camera: {mobile.get('cameraMp', 'N/A')} MP\n"
        f"   Features: {features or 'N/A'}\n"
        f"   {mobile.get('description', '')}{score_text}"
    )


@tool
def recommend_mobiles(
    query: Annotated[
        str,
        Field(description="Natural language request, for example 'best camera phone under 50000'."),
    ],
    k: Annotated[int, Field(description="Number of results to return", ge=1, le=10)] = 5,
) -> str:
    """Recommend mobiles using Azure DocumentDB vector search."""
    query_vector = _generate_embedding(_expand_query(query))
    max_price = _infer_max_price(query)
    client, db, _ = get_database()
    try:
        results = list(
            db.mobiles.aggregate(
                [
                    {
                        "$search": {
                            "cosmosSearch": {
                                "vector": query_vector,
                                "path": "contentVector",
                                "k": max(k * 3, 10),
                            }
                        }
                    },
                    {
                        "$project": {
                            "title": 1,
                            "brand": 1,
                            "segment": 1,
                            "description": 1,
                            "priceInr": 1,
                            "rating": 1,
                            "cameraMp": 1,
                            "batteryMah": 1,
                            "features": 1,
                            "score": {"$meta": "searchScore"},
                            "_id": 0,
                        }
                    },
                ]
            )
        )
    except OperationFailure as exc:
        return (
            "Vector recommendation failed. Confirm you ran:\n"
            "python .\\scripts\\generate_workshop_embeddings.py\n"
            "python .\\scripts\\create_workshop_indexes.py\n\n"
            f"Details: {exc}"
        )
    finally:
        client.close()

    if max_price is not None:
        results = [mobile for mobile in results if mobile.get("priceInr", 0) <= max_price]
    results = results[:k]

    if not results:
        return "No matching mobile recommendations found."

    lines = [f"Found {len(results)} recommended mobiles:"]
    for index, mobile in enumerate(results, 1):
        lines.append(f"\n{index}. {_format_mobile(mobile, include_score=True)}")
    return "\n".join(lines)


@tool
def search_mobiles_by_budget(
    max_price_inr: Annotated[int, Field(description="Maximum customer budget in INR")],
    min_rating: Annotated[float, Field(description="Minimum rating from 1 to 5")] = 4.0,
) -> str:
    """Find mobiles within a budget, sorted by rating."""
    client, db, _ = get_database()
    try:
        results = list(
            db.mobiles.find(
                {"priceInr": {"$lte": max_price_inr}, "rating": {"$gte": min_rating}},
                {
                    "title": 1,
                    "brand": 1,
                    "segment": 1,
                    "description": 1,
                    "priceInr": 1,
                    "rating": 1,
                    "cameraMp": 1,
                    "batteryMah": 1,
                    "features": 1,
                    "_id": 0,
                },
            )
            .sort([("rating", -1), ("priceInr", 1)])
            .limit(10)
        )
    finally:
        client.close()

    if not results:
        return f"No mobiles found under INR {max_price_inr:,} with rating >= {min_rating}."

    lines = [f"Mobiles under INR {max_price_inr:,} with rating >= {min_rating}:"]
    for index, mobile in enumerate(results, 1):
        lines.append(f"\n{index}. {_format_mobile(mobile)}")
    return "\n".join(lines)


@tool
def get_mobile_details(
    title: Annotated[str, Field(description="Mobile title to look up")],
) -> str:
    """Get detailed specifications for a specific mobile."""
    client, db, _ = get_database()
    try:
        mobile = db.mobiles.find_one(
            {"title": {"$regex": title, "$options": "i"}},
            {"contentVector": 0, "_id": 0},
        )
    finally:
        client.close()
    if not mobile:
        return f"Mobile '{title}' was not found. Try a different title or ask for recommendations."

    connectivity = ", ".join(mobile.get("connectivity", []))
    features = ", ".join(mobile.get("features", []))
    use_cases = ", ".join(mobile.get("useCases", []))
    return (
        f"**{mobile.get('title')}**\n"
        f"Brand: {mobile.get('brand')}\n"
        f"Segment: {mobile.get('segment')}\n"
        f"Price: INR {mobile.get('priceInr', 0):,}\n"
        f"Rating: {mobile.get('rating', 'N/A')}/5\n"
        f"Camera: {mobile.get('cameraMp', 'N/A')} MP | Battery: {mobile.get('batteryMah', 'N/A')} mAh | "
        f"RAM: {mobile.get('ramGb', 'N/A')} GB | Storage: {mobile.get('storageGb', 'N/A')} GB\n"
        f"Connectivity: {connectivity or 'N/A'}\n"
        f"Features: {features or 'N/A'}\n"
        f"Best for: {use_cases or 'N/A'}\n"
        f"Description: {mobile.get('description', '')}"
    )


@tool
def find_mobile_offers(
    title: Annotated[str, Field(description="Mobile title to find retail offers for")],
) -> str:
    """Find retailers, prices, and availability for a mobile."""
    client, db, _ = get_database()
    try:
        result = db.retail_offers.find_one(
            {"title": {"$regex": title, "$options": "i"}},
            {"_id": 0},
        )
    finally:
        client.close()
    if not result:
        return f"No retail offers found for '{title}'."

    lines = [f"Retail offers for **{result.get('title')}**:"]
    for offer in result.get("offers", []):
        lines.append(
            f"- **{offer.get('retailer')}** ({offer.get('type')}) - "
            f"INR {offer.get('priceInr'):,}, {offer.get('availability')}. {offer.get('notes')}"
        )
    return "\n".join(lines)


@tool
def search_offers_by_retailer(
    retailer: Annotated[str, Field(description="Retailer name, for example Amazon India or Flipkart")],
) -> str:
    """Find mobiles available from a specific retailer."""
    client, db, _ = get_database()
    try:
        results = list(
            db.retail_offers.find(
                {"offers.retailer": {"$regex": retailer, "$options": "i"}},
                {"_id": 0},
            ).sort("title", 1)
        )
    finally:
        client.close()
    if not results:
        return f"No mobiles found for retailer '{retailer}'."

    lines = [f"Mobiles available from **{retailer}**:"]
    for document in results:
        for offer in document.get("offers", []):
            if retailer.lower() in offer.get("retailer", "").lower():
                lines.append(
                    f"- **{document.get('title')}** - INR {offer.get('priceInr'):,}, "
                    f"{offer.get('availability')} ({offer.get('notes')})"
                )
    return "\n".join(lines)
