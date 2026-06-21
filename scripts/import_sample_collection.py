from __future__ import annotations

import argparse
from pathlib import Path

from common import get_database, load_json_array, replace_collection


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a JSON array file into a workshop collection.")
    parser.add_argument("--file", required=True, help="Path to JSON file containing an array of documents.")
    parser.add_argument("--collection", required=True, help="Target collection name.")
    args = parser.parse_args()

    client, db, database_name = get_database()
    try:
        count = replace_collection(db, args.collection, load_json_array(Path(args.file)))
        print(f"Connected to {database_name}")
        print(f"Imported {count} records into {args.collection}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
