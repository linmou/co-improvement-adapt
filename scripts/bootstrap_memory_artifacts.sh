#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -gt 1 ]; then
  echo "Usage: $0 [target_dir]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${1:-./co-improvement/skill/memory-persistent}"

mkdir -p "$TARGET_DIR"

cp "$SKILL_DIR/references/memory-protocol.md" "$TARGET_DIR/memory-protocol.md"
cp "$SKILL_DIR/references/context-persistence-rubric.md" "$TARGET_DIR/context-persistence-rubric.md"
cp "$SKILL_DIR/references/rubric-persistence-rubric.md" "$TARGET_DIR/rubric-persistence-rubric.md"
cp "$SKILL_DIR/references/rubric-entry-template.md" "$TARGET_DIR/rubric-entry-template.md"
cp "$SKILL_DIR/scripts/validate_rubric_memory.py" "$TARGET_DIR/validate_rubric_memory.py"

echo "Copied memory artifacts to: $TARGET_DIR"
