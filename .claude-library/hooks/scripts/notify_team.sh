#!/bin/bash
# Send team notifications via Slack/Discord webhooks
# Usage: notify_team.sh <event_type> <status>

event_type="$1"
status="$2"

# Load environment variables if .env exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Exit silently if no webhook configured
if [ -z "$SLACK_WEBHOOK_URL" ] && [ -z "$DISCORD_WEBHOOK_URL" ]; then
    exit 0
fi

# Prepare message
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
project_name=$(basename "$(pwd)")
user=$(whoami)

# Send to Slack if webhook configured
if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
    curl -X POST "$SLACK_WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{
            \"text\": \"🤖 Claude Agent Framework\",
            \"blocks\": [
                {
                    \"type\": \"section\",
                    \"text\": {
                        \"type\": \"mrkdwn\",
                        \"text\": \"*Event:* ${event_type}\\n*Status:* ${status}\\n*Project:* ${project_name}\\n*User:* ${user}\\n*Time:* ${timestamp}\"
                    }
                }
            ]
        }" \
        --silent --output /dev/null 2>&1 || true
fi

# Send to Discord if webhook configured
if [ ! -z "$DISCORD_WEBHOOK_URL" ]; then
    curl -X POST "$DISCORD_WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{
            \"embeds\": [{
                \"title\": \"🤖 Claude Agent Framework\",
                \"color\": 5814783,
                \"fields\": [
                    {\"name\": \"Event\", \"value\": \"${event_type}\", \"inline\": true},
                    {\"name\": \"Status\", \"value\": \"${status}\", \"inline\": true},
                    {\"name\": \"Project\", \"value\": \"${project_name}\", \"inline\": false},
                    {\"name\": \"User\", \"value\": \"${user}\", \"inline\": true},
                    {\"name\": \"Time\", \"value\": \"${timestamp}\", \"inline\": true}
                ]
            }]
        }" \
        --silent --output /dev/null 2>&1 || true
fi

# Log notification
if [ ! -z "$CLAUDE_HOOKS_LOG" ]; then
    echo "$(date -Iseconds) | notify_team | ${event_type} ${status} | sent" >> "$CLAUDE_HOOKS_LOG"
fi

exit 0
