from __future__ import annotations

from pathlib import Path

from common import ROOT_DIR, get_database, load_json_array, replace_collection, support_inc_documents


def main() -> None:
    client, db, database_name = get_database()
    try:
        sample_dir = ROOT_DIR / "sample-docs"
        data_files: list[tuple[str, Path]] = [
            ("mobiles", sample_dir / "mobiles_sample.json"),
            ("support_articles", sample_dir / "support_articles_sample.json"),
            ("retail_offers", sample_dir / "retail_offers_sample.json"),
        ]

        print(f"Connected to database: {database_name}")
        for collection_name, path in data_files:
            count = replace_collection(db, collection_name, load_json_array(path))
            print(f"Loaded {count} documents into {collection_name}")

        support_count = replace_collection(db, "supportInc", support_inc_documents())
        print(f"Loaded {support_count} documents into supportInc")

        print("\nVerification:")
        for collection_name in ["mobiles", "support_articles", "retail_offers", "supportInc"]:
            print(f"  {collection_name}: {db[collection_name].count_documents({})}")

        print("\nBase data load complete. No indexes were created by this script.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
