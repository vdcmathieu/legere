#!/bin/zsh
# Usage: run_codex.sh <job>   (job = e.g. lepen_A ; schema chosen by suffix)
cd "${0:A:h}"
job=$1
case $job in *_R) schema=schemas/record.json;; *) schema=schemas/positions.json;; esac
[[ -s raw/$job.json ]] && { echo "skip $job"; exit 0; }
codex --search exec -s read-only --skip-git-repo-check \
  -c model_reasoning_effort=high \
  --output-schema $schema -o raw/$job.json \
  "$(cat prompts/$job.txt)" </dev/null > raw/$job.log 2>&1
echo "$job exit $?"
