#!/usr/bin/env bash
# Generate readme.md for each tool folder from its tool-info.json
# Usage: bash ai-tools/generate-readmes.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for dir in "$SCRIPT_DIR"/*/; do
  json="$dir/tool-info.json"
  [ -f "$json" ] || continue

  name=$(jq -r '.name // empty' "$json")
  [ -z "$name" ] && continue

  type=$(jq -r '.type // "tool"' "$json")
  version=$(jq -r '.version // "n/a"' "$json")
  os=$(jq -r '(.os // []) | join(", ")' "$json")
  description=$(jq -r '.description // empty' "$json")
  tags=$(jq -r '(.tags // []) | join(", ")' "$json")
  overview=$(jq -r '.overview // empty' "$json")
  custom=$(jq -r '.customInstructions // empty' "$json")
  author=$(jq -r '.author // empty' "$json")

  readme="$dir/readme.md"

  {
    echo "# $name"
    echo ""
    echo "**Type:** $type | **Version:** $version | **OS:** $os"
    echo ""
    echo "$description"
    echo ""

    if [ -n "$tags" ]; then
      echo "## Tags"
      echo "$tags"
      echo ""
    fi

    if [ -n "$overview" ]; then
      echo "## Overview"
      echo "$overview"
      echo ""
    fi

    # Prompt Suggestions
    count=$(jq -r '(.promptSuggestions // []) | length' "$json")
    if [ "$count" -gt 0 ]; then
      echo "## Try These Prompts"
      jq -r '.promptSuggestions[] | "- " + .' "$json"
      echo ""
    fi

    # Applications
    count=$(jq -r '(.applications // []) | length' "$json")
    if [ "$count" -gt 0 ]; then
      echo "## Use Cases"
      jq -r '.applications[] | "- " + .' "$json"
      echo ""
    fi

    if [ -n "$custom" ]; then
      echo "## Additional Requirements"
      echo "$custom"
      echo ""
    fi

    echo "---"
    echo "*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*"
  } > "$readme"

  echo "Generated: $readme"
done
