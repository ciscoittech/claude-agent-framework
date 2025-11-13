#!/usr/bin/env python3
"""
Skill Auto-Activation System
Analyzes user prompts and file context to suggest relevant skills.
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple


def load_skill_rules(rules_path: str = ".claude-library/skills/skill-rules.json") -> Dict:
    """Load skill rules configuration."""
    try:
        with open(rules_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Skill rules not found at {rules_path}", file=sys.stderr)
        return {"skills": {}, "meta": {}}


def analyze_prompt(prompt: str, skill_rules: Dict) -> Set[str]:
    """Analyze prompt for keyword and pattern matches."""
    matches = set()
    prompt_lower = prompt.lower()

    for skill_name, skill_config in skill_rules.get("skills", {}).items():
        triggers = skill_config.get("promptTriggers", {})
        score = 0

        # Check keywords
        keywords = triggers.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in prompt_lower:
                score += 1

        # Check intent patterns
        patterns = triggers.get("intentPatterns", [])
        for pattern in patterns:
            try:
                if re.search(pattern, prompt, re.IGNORECASE):
                    score += 2  # Patterns are stronger signal
            except re.error:
                continue

        # Add to matches if confidence threshold met
        threshold = skill_rules.get("meta", {}).get("confidenceThreshold", 0.6)
        max_score = len(keywords) + len(patterns) * 2
        if max_score > 0 and (score / max_score) >= threshold:
            matches.add(skill_name)

    return matches


def analyze_file_context(cwd: str, skill_rules: Dict) -> Set[str]:
    """Analyze recently modified files for skill relevance."""
    matches = set()

    # Check for git status to find modified files
    try:
        import subprocess
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=2
        )

        if result.returncode == 0:
            modified_files = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Parse git status format
                    parts = line.strip().split(maxsplit=1)
                    if len(parts) == 2:
                        modified_files.append(parts[1])

            # Check files against skill triggers
            for skill_name, skill_config in skill_rules.get("skills", {}).items():
                file_triggers = skill_config.get("fileTriggers", {})

                # Check path patterns
                path_patterns = file_triggers.get("pathPatterns", [])
                for file_path in modified_files:
                    for pattern in path_patterns:
                        # Convert glob pattern to regex
                        regex_pattern = pattern.replace("**", ".*").replace("*", "[^/]*")
                        regex_pattern = regex_pattern.replace("{", "(").replace("}", ")").replace(",", "|")
                        try:
                            if re.match(regex_pattern, file_path):
                                matches.add(skill_name)
                                break
                        except re.error:
                            continue

    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return matches


def format_activation_message(matched_skills: List[Tuple[str, str]], skill_rules: Dict) -> str:
    """Format skill activation message."""
    if not matched_skills:
        return ""

    message = "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += "🎯 SKILL ACTIVATION CHECK\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    for skill_name, reason in matched_skills:
        skill_config = skill_rules["skills"].get(skill_name, {})
        activation_msg = skill_config.get("activationMessage", f"Consider using {skill_name} skill")
        message += f"{activation_msg}\n"
        message += f"   Reason: {reason}\n"
        message += f"   Location: .claude-library/skills/{skill_name}/\n\n"

    message += "💡 Skills provide context-specific best practices and patterns.\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    return message


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        return

    prompt = sys.argv[1]
    cwd = sys.argv[2] if len(sys.argv) > 2 else "."

    # Load skill rules
    skill_rules = load_skill_rules()
    if not skill_rules.get("skills"):
        return

    # Check if auto-activation is enabled
    if not skill_rules.get("meta", {}).get("autoActivationEnabled", True):
        return

    # Analyze prompt and context
    prompt_matches = analyze_prompt(prompt, skill_rules)
    context_matches = analyze_file_context(cwd, skill_rules)

    # Combine matches
    all_matches = prompt_matches | context_matches

    # Limit to max simultaneous skills
    max_skills = skill_rules.get("meta", {}).get("maxSimultaneousSkills", 3)

    # Prioritize by skill priority
    prioritized = []
    for skill_name in all_matches:
        priority = skill_rules["skills"][skill_name].get("priority", "medium")
        priority_order = {"high": 0, "medium": 1, "low": 2}
        prioritized.append((skill_name, priority_order.get(priority, 1)))

    prioritized.sort(key=lambda x: x[1])
    top_matches = prioritized[:max_skills]

    # Determine reason for each match
    matched_with_reason = []
    for skill_name, _ in top_matches:
        reasons = []
        if skill_name in prompt_matches:
            reasons.append("Prompt keywords/patterns matched")
        if skill_name in context_matches:
            reasons.append("Modified files matched")

        matched_with_reason.append((skill_name, " + ".join(reasons)))

    # Output activation message
    if matched_with_reason:
        message = format_activation_message(matched_with_reason, skill_rules)
        print(message)

        # Log activation
        log_config = skill_rules.get("config", {})
        if log_config.get("log_activations", False):
            log_path = log_config.get("log_path", ".claude-metrics/skill-activations.log")
            try:
                Path(log_path).parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, "a") as f:
                    import datetime
                    timestamp = datetime.datetime.now().isoformat()
                    f.write(f"{timestamp} | Skills: {[s for s, _ in matched_with_reason]} | Prompt: {prompt[:100]}\n")
            except Exception:
                pass


if __name__ == "__main__":
    main()
