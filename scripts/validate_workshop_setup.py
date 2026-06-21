from __future__ import annotations

from common import get_database


def main() -> None:
    client, db, database_name = get_database()
    try:
        print(f"Connected to database: {database_name}")
        print(f"Ping: {db.command({'ping': 1})}")
        for collection_name in ["mobiles", "support_articles", "retail_offers", "supportInc"]:
            print(f"{collection_name}: {db[collection_name].count_documents({})}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
