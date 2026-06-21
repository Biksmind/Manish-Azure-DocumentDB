from __future__ import annotations

import argparse

from vector_search_support import main as vector_main


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple workshop hybrid-search note.")
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    print("Text-search step to run in mongosh:")
    print('db.supportInc.find({ $text: { $search: "' + args.query.replace('"', '\\"') + '" } })')
    print("\nVector-search results:")

    import sys

    sys.argv = ["vector_search_support.py", "--query", args.query]
    vector_main()


if __name__ == "__main__":
    main()
