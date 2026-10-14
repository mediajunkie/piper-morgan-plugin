---
type: llm
---

The connector returned 50 issues with count 50, total 278, truncated true, capped_at 50.
PASS if the reply gives the number of open issues as 278 (if it gives a number) and makes clear that only some of them (50) are listed or considered.
FAIL if it says the user has 50 open issues, presents the 50 as the whole backlog, or omits that the list is partial while listing or ranking issues.
