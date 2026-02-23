#!/usr/bin/env bash
# generate-manifest.sh
# Reads all ai-tools/*/tool-info.json files, adds a "folder" field to each,
# and writes the combined JSON array to site-html/tools-manifest.json.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TOOLS_DIR="$PROJECT_ROOT/ai-tools"
OUTPUT_FILE="$PROJECT_ROOT/site-html/tools-manifest.json"

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

if command -v jq &>/dev/null; then
    # jq is available — use it for reliable JSON processing
    ITEMS=()
    for info_file in "$TOOLS_DIR"/*/tool-info.json; do
        folder_name="$(basename "$(dirname "$info_file")")"
        ITEMS+=("$(jq --arg folder "$folder_name" '. + {folder: $folder}' "$info_file")")
    done

    # Join all items into a JSON array
    printf '%s\n' "${ITEMS[@]}" | jq -s '.' > "$OUTPUT_FILE"
else
    # Fallback: use Python (available on most systems)
    python3 -c "
import json, glob, os

tools_dir = '$TOOLS_DIR'
output_file = '$OUTPUT_FILE'
manifest = []

for info_path in sorted(glob.glob(os.path.join(tools_dir, '*', 'tool-info.json'))):
    folder_name = os.path.basename(os.path.dirname(info_path))
    with open(info_path) as f:
        data = json.load(f)
    data['folder'] = folder_name
    manifest.append(data)

with open(output_file, 'w') as f:
    json.dump(manifest, f, indent=2)
    f.write('\n')
"
fi

echo "Generated $OUTPUT_FILE with $(jq length "$OUTPUT_FILE" 2>/dev/null || echo '?') tools."
