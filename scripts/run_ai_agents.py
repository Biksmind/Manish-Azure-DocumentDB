from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_URL = "https://github.com/Biksmind/DocumentDB_Workshop_0906.git"
COMPANION_REPO_NAME = "DocumentDB_Workshop_0906"
AGENTS_RELATIVE_PATH = Path("4-AI-Agents") / "mobile-agents"


def ensure_command_exists(cmd: str) -> None:
    if shutil.which(cmd) is None:
        raise RuntimeError(f"Required command not found in PATH: {cmd}")


def run_command(args: list[str], cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=str(cwd) if cwd else None, check=True)


def module_available(python_exe: str, module_name: str) -> bool:
    result = subprocess.run(
        [python_exe, "-c", f"import {module_name}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    python_exe = sys.executable
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    parent_dir = repo_root.parent
    companion_repo = parent_dir / COMPANION_REPO_NAME
    agents_app_dir = companion_repo / AGENTS_RELATIVE_PATH

    try:
        ensure_command_exists("git")

        if not companion_repo.exists():
            print("Companion repo not found. Cloning DocumentDB_Workshop_0906...")
            run_command(["git", "clone", REPO_URL], cwd=parent_dir)

        if not agents_app_dir.exists():
            raise RuntimeError(f"AI agents app path not found: {agents_app_dir}")

        # First run on a new machine may miss required Python deps for the companion app.
        if not module_available(python_exe, "dotenv"):
            requirements_file = companion_repo / "requirements.txt"
            if not requirements_file.exists():
                raise RuntimeError(f"requirements.txt not found: {requirements_file}")

            print("Installing companion repo dependencies...")
            run_command([python_exe, "-m", "pip", "install", "-r", str(requirements_file)], cwd=companion_repo)

        print(f"Starting AI agents app from: {agents_app_dir}")
        run_command([python_exe, "app.py"], cwd=agents_app_dir)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
