---
type: llm
---

The connector returned 4 issues with count 4, total 4, truncated false. This IS the complete list.
PASS if the reply treats these 4 as the user's open issues (if it gives a number, 4) without suggesting more probably exist beyond what was returned.
FAIL if it gives a different count, or adds an unfounded caveat that the list is likely partial, capped or truncated.
