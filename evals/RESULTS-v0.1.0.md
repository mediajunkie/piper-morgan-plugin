# Eval results: v0.1.0 (complete run)

**Run**: 2026-10-06, `claude plugin eval . -j 2` on commit `7af6a4a`, Claude Code 2.1.280, default agent
and judge models. **Complete** (`partial: false`, exit 0). 4 cases × 3 runs × 2 arms (with and without the
plugin). List-price estimate $1.46. Full machine-readable record: `RESULTS-v0.1.0.json`.

**Setup**: the Piper connector is **mocked** with fixed sample data (an organization, two stated priorities,
an empty colleague model, four open issues including one that serves no priority). These results measure the
skills' behaviour on that sample, not live accounts.

| Case | With plugin (3 runs) | Without (3 runs) | Δ |
|---|---|---|---|
| what-piper-knows: names the profile, says the colleague model is empty, invents nothing | 1, 1, 1 | 0, 0, 0 | +1.00 |
| morning-standup: focus items tied to priorities and issue numbers, no invented past progress | 1, 1, 1 | 0, 0, 0 | +1.00 |
| prioritize-my-issues: priority-serving issues ranked above the distractor, with reasons | 1, 1, 1 | 0, 0, 0 | +1.00 |
| unrelated request (a haiku): must not call Piper | 1, 1, 1 | 1, 1, 1 | 0.00 (correct) |

Behaviour cases are judge-graded (3 votes per run, PASS on ≥2). Connector-call checks score only the
with-plugin arm, so the baseline isn't penalized for lacking the plugin.

**Earlier runs the same day showed 0.5–0.67 on the standup case.** Those came from a regex grader (since
removed) that matched the skill's own disclaimer, *"Piper can only see your stated priorities and open
issues, not what you finished yesterday"*, as if it were a claim of past progress. The judge grader, which
checks that by meaning, passed in every run.
