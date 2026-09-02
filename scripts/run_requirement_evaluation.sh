#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if [[ ! -f ".env" ]]; then
    echo "Error: .env file not found."
    exit 1
fi

set -a
source .env
set +a

if [[ -z "${LLM_MODEL:-}" ]]; then
    echo "Error: LLM_MODEL is not defined."
    exit 1
fi

MODEL_NAME="${LLM_MODEL//\//_}"
RUN_DATE="$(date '+%Y-%m-%d_%H-%M-%S')"

POSTFIX="${MODEL_NAME}_${RUN_DATE}"

OUTPUT_DIR="evaluation_results"
mkdir -p "$OUTPUT_DIR"

TEXT_OUTPUT="$OUTPUT_DIR/requirement_analysis_${POSTFIX}.txt"
JSON_OUTPUT="$OUTPUT_DIR/requirement_analysis_${POSTFIX}.json"

uv run python scripts/evaluate_requirement_analyzer.py \
    | tee "$TEXT_OUTPUT"

if [[ -f "$OUTPUT_DIR/latest.json" ]]; then
    mv \
        "$OUTPUT_DIR/latest.json" \
        "$JSON_OUTPUT"
fi

echo
echo "Evaluation saved:"
echo "  $TEXT_OUTPUT"
echo "  $JSON_OUTPUT"