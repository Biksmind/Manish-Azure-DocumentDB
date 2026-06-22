from __future__ import annotations

import os
from pathlib import Path

from agent_framework.devui import serve
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

from mobile_tools import (
    find_mobile_offers,
    get_mobile_details,
    recommend_mobiles,
    search_mobiles_by_budget,
    search_offers_by_retailer,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value or "<" in value or ">" in value:
        raise RuntimeError(f"Update {name} in {ROOT_DIR / '.env'} before running agents.")
    return value.strip()


def normalize_azure_endpoint(value: str) -> str:
    value = value.rstrip("/")
    if value.endswith("/openai/v1"):
        value = value[: -len("/openai/v1")]
    return value


def azure_openai_base_url(value: str) -> str:
    return normalize_azure_endpoint(value) + "/openai/v1"


def build_agents():
    chat_client = OpenAIChatClient(
        model=require_env("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        base_url=azure_openai_base_url(require_env("AZURE_OPENAI_ENDPOINT")),
        api_key=require_env("AZURE_OPENAI_API_KEY"),
    )

    mobile_advisor_agent = chat_client.as_agent(
        name="MobileAdvisor",
        instructions="""You are a mobile phone advisor powered by Azure DocumentDB.
You help users choose mobiles based on needs, budget, camera, battery, gaming,
productivity, software experience, and brand preferences.

Use recommend_mobiles when the user describes needs in natural language.
Use search_mobiles_by_budget when the user gives a budget.
Use get_mobile_details when the user asks about a specific model.

Always explain why each recommendation fits the customer's requirement.""",
        tools=[recommend_mobiles, search_mobiles_by_budget, get_mobile_details],
    )

    retail_offer_agent = chat_client.as_agent(
        name="RetailOfferFinder",
        instructions="""You help users find retail offers and availability for mobiles.

Use find_mobile_offers when the user asks where to buy a specific mobile.
Use search_offers_by_retailer when the user asks what is available from a retailer.

Clearly show retailer, price, availability, and notes such as exchange or EMI offers.""",
        tools=[find_mobile_offers, search_offers_by_retailer],
    )

    return [mobile_advisor_agent, retail_offer_agent]


def main() -> None:
    print("=" * 70)
    print("  Azure DocumentDB Workshop: Mobile Shopping AI Agents")
    print("  This runs from the current repository only. No companion repo is used.")
    print("=" * 70)
    print("  Agents:")
    print("    1. MobileAdvisor      - Semantic mobile recommendations")
    print("    2. RetailOfferFinder  - Retailer offers and availability")
    print()
    print("  Open http://localhost:8080 in your browser")
    print("  Press Ctrl+C to stop")
    print("=" * 70)

    serve(
        entities=build_agents(),
        auto_open=True,
        port=8080,
        auth_enabled=False,
    )


if __name__ == "__main__":
    main()
