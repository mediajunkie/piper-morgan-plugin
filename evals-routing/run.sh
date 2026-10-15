#!/usr/bin/env bash
# Routing eval: bare connector under each tool description, plus the full plugin on the current one.
# Usage: evals-routing/run.sh <out-dir> [runs-per-case, default 5]
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:?out dir}; RUNS=${2:-5}
mkdir -p "$OUT"
for job in bare:current bare:usefirst full:current; do
  variant=${job%%:*}; suite=${job#*:}
  dir=$ROOT; [ "$variant" = bare ] && dir=$ROOT/variants/bare-mcp
  (cd "$dir" && claude plugin eval . --eval-dir "evals-routing/suite-$suite" --ablation none --runs "$RUNS" \
    --no-publish --trust-plugin -j 4 --max-cost-usd 4 --threshold 0 \
    --output-dir "$OUT/$variant-$suite" --json "$OUT/$variant-$suite.json" >"$OUT/$variant-$suite.log" 2>&1)
  echo "$variant-$suite exit $?"
done
