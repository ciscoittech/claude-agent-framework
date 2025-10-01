#!/bin/bash
# Auto-format code based on file type
# Usage: format_code.sh <file_path>

file_path="$1"

if [ -z "$file_path" ] || [ ! -f "$file_path" ]; then
    exit 0
fi

# Determine file type and format accordingly
case "$file_path" in
  *.py)
    # Python formatting
    if command -v black &> /dev/null; then
        black "$file_path" 2>/dev/null || true
    fi
    if command -v isort &> /dev/null; then
        isort "$file_path" 2>/dev/null || true
    fi
    ;;

  *.js|*.jsx|*.ts|*.tsx|*.json|*.css|*.scss|*.html)
    # JavaScript/TypeScript/Web formatting
    if command -v npx &> /dev/null; then
        npx prettier --write "$file_path" 2>/dev/null || true
    fi
    if [[ "$file_path" =~ \.(js|jsx|ts|tsx)$ ]]; then
        if command -v npx &> /dev/null; then
            npx eslint --fix "$file_path" 2>/dev/null || true
        fi
    fi
    ;;

  *.rs)
    # Rust formatting
    if command -v rustfmt &> /dev/null; then
        rustfmt "$file_path" 2>/dev/null || true
    fi
    ;;

  *.go)
    # Go formatting
    if command -v gofmt &> /dev/null; then
        gofmt -w "$file_path" 2>/dev/null || true
    fi
    if command -v goimports &> /dev/null; then
        goimports -w "$file_path" 2>/dev/null || true
    fi
    ;;

  *.rb)
    # Ruby formatting
    if command -v rubocop &> /dev/null; then
        rubocop -a "$file_path" 2>/dev/null || true
    fi
    ;;

  *.java)
    # Java formatting
    if command -v google-java-format &> /dev/null; then
        google-java-format -i "$file_path" 2>/dev/null || true
    fi
    ;;

  *.md)
    # Markdown formatting
    if command -v npx &> /dev/null; then
        npx prettier --write "$file_path" 2>/dev/null || true
    fi
    ;;
esac

# Log formatting action
if [ ! -z "$CLAUDE_HOOKS_LOG" ]; then
    echo "$(date -Iseconds) | format_code | $file_path | success" >> "$CLAUDE_HOOKS_LOG"
fi

exit 0  # Never block on formatting errors
