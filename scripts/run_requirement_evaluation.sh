#!/usr/bin/env bash

set -euo pipefail

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Load .env
if [[ ! -f ".env" ]]; then
    echo "Error: .env file not found."
    exit 1
fi

set -a
source .env
set +a

# Validate required configuration
if [[ -z "${LLM_MODEL:-}" ]]; then
    echo "Error: LLM_MODEL is not defined in .env."
    exit 1
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "Error: OPENAI_API_KEY is not defined in .env."
    exit 1
fi

# Create filesystem-safe model name.
# Example:
# gpt-5.4 -> gpt-5.4
# provider/model -> provider_model
MODEL_NAME="${LLM_MODEL//\//_}"

# Current date/time
RUN_DATE="$(date '+%Y-%m-%d_%H-%M-%S')"

# Model + date postfix
POSTFIX="${MODEL_NAME}_${RUN_DATE}"

# Output directory
OUTPUT_DIR="evaluation_results"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/requirement_analysis_${POSTFIX}.txt"

echo "Running requirement analyzer evaluation"
echo "Model:  $LLM_MODEL"
echo "Date:   $RUN_DATE"
echo "Output: $OUTPUT_FILE"
echo

uv run python scripts/inspect_requirement_analysis.py \
    | tee "$OUTPUT_FILE"

echo
echo "Evaluation completed."
echo "Results saved to:"
echo "$OUTPUT_FILE"
