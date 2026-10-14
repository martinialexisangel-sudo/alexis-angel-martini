#!/bin/bash
SP=/tmp/claude-0/-home-user-alexis-angel-martini/fdf41730-a49c-58dc-81a0-9336a7868929/scratchpad
for f in /root/.claude/projects/-home-user-alexis-angel-martini/fdf41730-a49c-58dc-81a0-9336a7868929/tool-results/mcp-Parallel_Search-web_fetch-*.txt; do cp --update=none "$f" $SP/edb/$(basename $f .txt).json; done
python3 $SP/edb_parse.py $SP/edb $SP/edb_rows.csv > $SP/pages.log
grep -c . $SP/pages.log
python3 $SP/edb_plan.py $SP | tail -3
