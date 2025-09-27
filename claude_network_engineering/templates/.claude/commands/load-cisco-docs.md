# Load Cisco Documentation Command

Intelligently fetch specific sections from Cisco documentation based on your project needs.

## Usage

```bash
claude> load-cisco-docs <url> --project="<description>" [--sections="<list>"] [--interactive]
```

## Examples

```bash
# Interactive mode - system helps you choose sections
claude> load-cisco-docs "https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cucm/upgrade/14_0_1/cucm_b_upgrade-and-migration-guide_14.html" --project="CUCM 14.0.1 upgrade planning" --interactive

# Direct section loading
claude> load-cisco-docs "https://cisco.com/voice/guide" --project="Voice troubleshooting" --sections="call-flow,debugging,common-issues"

# Quick analysis without loading
claude> analyze-cisco-doc "https://cisco.com/config/guide"
```

## How It Works

1. **Analyzes document structure** first (table of contents only)
2. **Asks clarifying questions** about your specific needs
3. **Recommends relevant sections** based on your project
4. **Fetches only selected content** to stay within context limits
5. **Caches content locally** for reuse

## Implementation

When you use this command, Claude will:

1. Use WebFetch to analyze the document structure
2. Present you with section options based on your project description
3. Ask you to confirm which sections to load
4. Fetch only the selected sections
5. Save the content for later reference

## Safety Features

- **Context limit protection** - Stops fetching before hitting limits
- **Size estimation** - Shows estimated size before fetching
- **Incremental loading** - Loads sections one at a time
- **User confirmation** - Always asks before fetching large content

## Project Context Awareness

The system understands common Cisco project phases:

- **Planning**: Loads requirements, prerequisites, overview sections
- **Implementation**: Loads step-by-step procedures, configuration guides
- **Troubleshooting**: Loads debugging, common issues, resolution sections
- **Validation**: Loads verification, testing, post-implementation sections

## Cache Management

Fetched content is automatically cached locally:
- Use `list-cached-docs` to see cached documents
- Use `load-cached-doc <filename>` to reload previous content
- Cache includes project context for better organization