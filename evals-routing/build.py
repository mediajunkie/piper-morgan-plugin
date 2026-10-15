#!/usr/bin/env python3
"""Generate the routing eval: does the bare connector reach Piper for questions that don't name Piper?

Why: in the #2005 eval (evals-2005/RESULTS-2026-10-14.md), "How many open GitHub issues do I have?" reached
Piper 7 of 15 times through the bare connector and 15 of 15 through the full plugin. xian's direction (10-14):
smart server first, then connector, then skills. So this measures one server-side lever, the tool description,
before anyone writes a routing skill.

Suites (the mock is suite-wide, so one suite per description):
  suite-current    the tool description as on the server (MCP v14)
  suite-usefirst   the same facts, reordered to lead with the questions it answers
Payload: the post-#2005 shape (50 issues, total 278, truncated true), same as evals-2005 suite-postfix.
Grader: called-piper only (free; no judge). Run with evals-routing/run.sh.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
# Reuse evals-2005/build.py's fixtures and helpers: run everything above its write loop.
src = (HERE.parent / "evals-2005/build.py").read_text().split("\nfor fx, (payload")[0]
ns = {"__file__": str(HERE.parent / "evals-2005/build.py")}
exec(src, ns)

CURRENT = ns["TOOL_DESC"]
# Lever under test: same facts, use-first. Server copy if it ships (CXO, then Comms, own the words).
USEFIRST = (
    "Read-only. Use this for questions about the signed-in user's own work: their open GitHub issues (how many, "
    "which ones, what to work on next), their projects and their priorities. Returns, in one call: their "
    "profile (organization, active projects, stated priorities), their colleague model (what Piper has "
    "confirmed with them about how they work), and their open GitHub issues via their own connected GitHub "
    "account. Each section reports available=false or an explicit empty note rather than guessing; report "
    "empty sections as empty, never fill them in."
)
SUITES = {"current": CURRENT, "usefirst": USEFIRST}
CASES = {
    "count-my-issues": "How many open GitHub issues do I have?",
    "assigned-to-me": "What's assigned to me on GitHub right now?",
    "work-on-today": "What should I work on today?",
}

payload = ns["POST"]
for name, desc in SUITES.items():
    suite = HERE / f"suite-{name}"
    ns["write"](suite / "mocks/piper-morgan/_tools.json", ns["tools_json"](desc))
    result = {"profile": ns["PROFILE"], "colleague_model": ns["COLLEAGUE"], "github_issues": payload}
    ns["write"](suite / "mocks/piper-morgan/what_piper_knows_about_me.md",
                "---\ntype: fixed\n---\n\n" + json.dumps(result) + "\n")
    for case, prompt in CASES.items():
        ns["write"](suite / case / "prompt.md",
                    f"---\nmax_turns: 8\nallowed_tools: [Skill]\ntags: [routing, {name}]\n---\n\n{prompt}\n")
        ns["write"](suite / case / "graders/called-piper.md",
                    "---\ntype: tool_used\ntool: mcp__plugin_piper-morgan_piper-morgan__what_piper_knows_about_me\n"
                    "arm: with-only\n---\n")
print("generated", [f"suite-{s}" for s in SUITES])
