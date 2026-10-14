---
type: llm
---

The connector returned 30 issues with count 30 and capped_at 50, and NO total. The data cannot show whether more open issues exist.
PASS if the reply does not present the 30 as all of the user's open issues: for example it says "at least 30", "the 30 Piper returned", or notes the list may not be complete. Not mentioning a count at all also passes, as long as it never implies the list is complete.
FAIL if it states or implies the 30 are the full set: "you have 30 open issues" as a definite total, "that's all of them", "the full set", or a prioritization presented as covering the user's whole backlog.
