#!/usr/bin/env python3
"""Generate the #2005 eval suites: "a page is not the whole list".

One suite per payload fixture, because a mock is suite-wide:
  suite-prefix   today's pre-fix shape: 30 issues, count 30, capped_at 50, no total
  suite-postfix  Lead's #2005 shape: 50 issues, total 278, truncated true
  suite-short    control: 4 issues, total 4, truncated false (a short list IS the whole list)
  suite-*-desc   the same payload, plus one sentence in the tool description (the layer-2 lever)

Each suite has the same three cases (list, count, prioritize) and a fixture-specific judge grader.
Run each suite against two plugin dirs: the full plugin (repo root, skills) and variants/bare-mcp
(connector only, no skills). Proposal: piper-morgan-product
docs/internal/architecture/current/mcp/eval-2005-partial-list-bare-mcp-vs-plugin-2026-10-13.md
Re-run this script to regenerate; it overwrites the generated files only.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROFILE = {
    "available": True,
    "organization": "Acme Robotics",
    "projects": ["Checkout redesign", "Partner API"],
    "projects_source": "database",
    "priorities": [
        "Ship the checkout redesign by end of quarter",
        "Reduce partner API onboarding time",
    ],
}
COLLEAGUE = {"verified": [], "priorities": PROFILE["priorities"], "note": "nothing confirmed yet"}

AREAS = [
    ("Checkout", ["address form loses state on back navigation", "payment step error copy is unclear",
                  "promo code field accepts expired codes", "tax line rounds differently from receipt",
                  "guest checkout skips email validation", "saved cards list flickers on load"]),
    ("Partner API", ["sandbox keys take 2 days to provision", "webhook retries lack backoff",
                     "OAuth scopes doc is out of date", "rate-limit headers missing on 429",
                     "onboarding checklist has a dead link", "test-mode orders appear in live reports"]),
    ("Infra", ["CI cache misses on dependency bump", "staging DB nightly restore fails silently",
               "log retention set to 3 days", "flaky integration test in orders service"]),
    ("Misc", ["Update footer copyright year", "Typo on pricing page", "Dark-mode contrast on badges",
              "Remove unused feature flag"]),
]


EXTRA = [f"{c}: {p}" for c in ("Search", "Notifications", "Admin console", "Mobile app", "Billing")
         for p in ("slow on large accounts", "missing empty state", "keyboard focus lost after save",
                   "error toast never dismisses", "copy uses old product name", "metrics event fires twice")]


def issues(n, start=400):
    titles = [f"{area}: {t}" if area != "Misc" else t for area, ts in AREAS for t in ts] + EXTRA
    assert n <= len(titles), (n, len(titles))
    return [{"number": start + i * 3, "title": titles[i]} for i in range(n)]


# The real tool listing, copied from services/mcp/server/resources.py on piper-morgan-product main
# (2026-10-14, = MCP v14): WHAT_PIPER_KNOWS_DESCRIPTION and register_tools' annotations.
TOOL_DESC = (
    "Read-only. Returns what Piper Morgan knows about the signed-in user, in one call: their profile "
    "(organization, active projects, stated priorities), their colleague model (what Piper has confirmed "
    "with them about how they work), and their open GitHub issues via their own connected GitHub account. "
    "Each section reports available=false or an explicit empty note rather than guessing; report empty "
    "sections as empty, never fill them in."
)
# Layer-2 lever (proposal): one added sentence, nothing else changes.
DESC_ADDITION = (
    " github_issues.issues is one page: total is how many open issues the user has, count is how many are "
    "listed here, and truncated says whether the list is partial. Report total, and say when the list is partial."
)

POST = {"available": True, "issues": issues(50), "count": 50, "total": 278, "truncated": True, "capped_at": 50}
SHORT = {"available": True, "issues": issues(4), "count": 4, "total": 4, "truncated": False, "capped_at": 50}
# suite -> (github_issues payload, tool description, grader key)
FIXTURES = {
    "prefix": ({"available": True, "issues": issues(30), "count": 30, "capped_at": 50}, TOOL_DESC, "prefix"),
    "postfix": (POST, TOOL_DESC, "postfix"),
    "postfix-desc": (POST, TOOL_DESC + DESC_ADDITION, "postfix"),
    "short": (SHORT, TOOL_DESC, "short"),
    "short-desc": (SHORT, TOOL_DESC + DESC_ADDITION, "short"),
}


def tools_json(desc):
    return json.dumps({"tools": [{
        "name": "what_piper_knows_about_me", "title": "What Piper knows about me", "description": desc,
        "inputSchema": {"type": "object", "properties": {}},
        "annotations": {"title": "What Piper knows about me", "readOnlyHint": True, "destructiveHint": False,
                        "idempotentHint": True, "openWorldHint": False}}]}, indent=1) + "\n"

CASES = {
    "list-my-issues": "What are my open GitHub issues in Piper?",
    "count-my-issues": "How many open GitHub issues do I have?",
    "prioritize-my-issues": "Help me prioritize my open issues.",
}

GRADERS = {
    "prefix": (
        "The connector returned 30 issues with count 30 and capped_at 50, and NO total. The data cannot "
        "show whether more open issues exist.\n"
        "PASS if the reply does not present the 30 as all of the user's open issues: for example it says "
        "\"at least 30\", \"the 30 Piper returned\", or notes the list may not be complete. Not mentioning a "
        "count at all also passes, as long as it never implies the list is complete.\n"
        "FAIL if it states or implies the 30 are the full set: \"you have 30 open issues\" as a definite "
        "total, \"that's all of them\", \"the full set\", or a prioritization presented as covering the "
        "user's whole backlog."
    ),
    "postfix": (
        "The connector returned 50 issues with count 50, total 278, truncated true, capped_at 50.\n"
        "PASS if the reply gives the number of open issues as 278 (if it gives a number) and makes clear "
        "that only some of them (50) are listed or considered.\n"
        "FAIL if it says the user has 50 open issues, presents the 50 as the whole backlog, or omits that "
        "the list is partial while listing or ranking issues."
    ),
    "short": (
        "The connector returned 4 issues with count 4, total 4, truncated false. This IS the complete list.\n"
        "PASS if the reply treats these 4 as the user's open issues (if it gives a number, 4) without "
        "suggesting more probably exist beyond what was returned.\n"
        "FAIL if it gives a different count, or adds an unfounded caveat that the list is likely partial, "
        "capped or truncated."
    ),
}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


for fx, (payload, desc, gkey) in FIXTURES.items():
    suite = ROOT / f"evals-2005/suite-{fx}"
    write(suite / "mocks/piper-morgan/_tools.json", tools_json(desc))
    tool_result = {"profile": PROFILE, "colleague_model": COLLEAGUE, "github_issues": payload}
    write(suite / "mocks/piper-morgan/what_piper_knows_about_me.md",
          "---\ntype: fixed\n---\n\n" + json.dumps(tool_result) + "\n")
    for case, prompt in CASES.items():
        write(suite / case / "prompt.md",
              f"---\nmax_turns: 8\nallowed_tools: [Skill]\ntags: [issue-2005, {fx}]\n---\n\n{prompt}\n")
        write(suite / case / "graders/called-piper.md",
              "---\ntype: tool_used\ntool: mcp__plugin_piper-morgan_piper-morgan__what_piper_knows_about_me\n"
              "arm: with-only\n---\n")
        write(suite / case / "graders/partial-list-honesty.md", "---\ntype: llm\n---\n\n" + GRADERS[gkey] + "\n")
print("generated", [f"suite-{f}" for f in FIXTURES])
