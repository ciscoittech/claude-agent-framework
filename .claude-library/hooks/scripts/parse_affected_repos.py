#!/usr/bin/env python3
"""
Parse Affected Repos
Determines which repos were modified from edit log.
"""

import sys
import json
from pathlib import Path
from typing import Set, Tuple


def parse_edit_log(log_path: str) -> Set[Tuple[str, str]]:
    """Parse edit log and return unique repos."""
    try:
        with open(log_path) as f:
            edits = json.load(f)

        repos = set()
        for edit in edits:
            repo_name = edit.get("repo_name", "unknown")
            repo_root = edit.get("repo_root", ".")
            if repo_name and repo_root:
                repos.add((repo_name, repo_root))

        return repos
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        return

    log_path = sys.argv[1]
    repos = parse_edit_log(log_path)

    # Output in repo_name:repo_path format
    for repo_name, repo_path in repos:
        print(f"{repo_name}:{repo_path}")


if __name__ == "__main__":
    main()
