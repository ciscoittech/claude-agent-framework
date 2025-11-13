#!/usr/bin/env python3
"""
Error Handling Reminder
Gentle self-check reminder for risky code patterns.
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Set


def load_quality_config() -> Dict:
    """Load quality control configuration."""
    try:
        with open(".claude-library/hooks/configs/quality-control.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"config": {"risky_patterns": {}}}


def analyze_edited_files(file_paths: str, config: Dict) -> Dict[str, List[str]]:
    """Analyze edited files for risky patterns."""
    if not file_paths:
        return {}

    files = file_paths.split(",") if "," in file_paths else [file_paths]
    risky_patterns = config.get("config", {}).get("risky_patterns", {})

    found_risks = {}

    for file_path in files:
        file_path = file_path.strip()
        if not file_path or not Path(file_path).exists():
            continue

        try:
            content = Path(file_path).read_text()

            for category, patterns in risky_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in content.lower():
                        if category not in found_risks:
                            found_risks[category] = []
                        if file_path not in found_risks[category]:
                            found_risks[category].append(file_path)
                        break
        except Exception:
            continue

    return found_risks


def format_reminder(risks: Dict[str, List[str]]) -> str:
    """Format gentle reminder message."""
    if not risks:
        return ""

    message = "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += "📋 ERROR HANDLING SELF-CHECK\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    total_files = sum(len(files) for files in risks.values())
    message += f"⚠️  Risky Code Detected\n"
    message += f"   {total_files} file(s) with error-prone patterns\n\n"

    if "backend" in risks:
        message += "   ❓ Did you add proper error handling?\n"
        message += "   ❓ Are async operations wrapped in try-catch?\n"
        message += "   ❓ Are database operations error-safe?\n\n"
        message += "   💡 Backend Best Practice:\n"
        message += "      - All errors should be properly caught and logged\n"
        message += "      - Database operations need error handling\n"
        message += "      - API endpoints should handle failure cases\n\n"

    if "frontend" in risks:
        message += "   ❓ Did you add error boundaries (React)?\n"
        message += "   ❓ Are fetch/axios calls wrapped in try-catch?\n"
        message += "   ❓ Do async effects handle cleanup?\n\n"
        message += "   💡 Frontend Best Practice:\n"
        message += "      - Use error boundaries for component errors\n"
        message += "      - Handle loading and error states\n"
        message += "      - Clean up async operations in useEffect\n\n"

    if "database" in risks:
        message += "   ❓ Did you test the migration?\n"
        message += "   ❓ Is there a rollback plan?\n"
        message += "   ❓ Are constraints properly defined?\n\n"
        message += "   💡 Database Best Practice:\n"
        message += "      - Always test migrations locally first\n"
        message += "      - Write rollback scripts\n"
        message += "      - Backup before schema changes\n\n"

    message += "💭 This is a gentle reminder, not a blocker.\n"
    message += "   Take a moment to review error handling.\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    return message


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        return

    file_paths = sys.argv[1]

    # Load configuration
    config = load_quality_config()

    # Analyze files
    risks = analyze_edited_files(file_paths, config)

    # Show reminder if risks found
    if risks:
        message = format_reminder(risks)
        print(message)


if __name__ == "__main__":
    main()
