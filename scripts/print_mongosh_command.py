from __future__ import annotations

from common import require_env, load_workshop_env


def main() -> None:
    load_workshop_env()
    connection_string = require_env("DOCUMENTDB_CONNECTION_STRING")
    print('Copy and run this command:')
    print(f'mongosh "{connection_string}"')


if __name__ == "__main__":
    main()
