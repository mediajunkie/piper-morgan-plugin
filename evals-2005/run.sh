#!/usr/bin/env bash
# Run every #2005 suite against the bare connector and the full plugin.
# Usage: evals-2005/run.sh <out-dir> [suite ...]   (default: all suites)
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:?out dir}; shift
SUITES=${*:-"prefix postfix postfix-desc short short-desc"}
mkdir -p "$OUT"
for suite in $SUITES; do
  for variant in bare full; do
    dir=$ROOT; [ "$variant" = bare ] && dir=$ROOT/variants/bare-mcp
    (cd "$dir" && claude plugin eval . --eval-dir "evals-2005/suite-$suite" --ablation none \
      --no-publish --trust-plugin -j 4 --max-cost-usd 4 --threshold 0 \
      --output-dir "$OUT/$variant-$suite" --report "$OUT/$variant-$suite/report.html" \
      --json "$OUT/$variant-$suite.json" >"$OUT/$variant-$suite.log" 2>&1)
    echo "$variant-$suite exit $?"
  done
done
