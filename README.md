# Piper Morgan plugin

Piper Morgan is a product-management colleague. This plugin connects Claude (and, via OpenAI's
plugin format, ChatGPT) to what Piper knows about you (your organization, projects, stated priorities,
how you like to work, and your open GitHub issues), and adds skills that use it:

| Skill | What it does |
|---|---|
| `what-piper-knows` | Shows what Piper knows about you, empty sections included |
| `morning-standup` | Drafts a 30-second standup from your priorities and open issues |
| `prioritize-my-issues` | Ranks your open issues against your stated priorities |

The connector (`https://mcp.pipermorgan.ai/mcp`) is **read-only**. Signing in happens on a Piper page,
where you approve access.

**Status: alpha, invitation only.** You need a Piper Morgan account at
[pipermorgan.ai](https://pipermorgan.ai).

## Install

- **claude.ai / Claude desktop**: *Customize → Plugins → Add → Upload plugin* with a zip of this
  folder, then connect the **piper-morgan** connector from the plugin's Connectors tab. (Directory
  listing pending.)
- **Claude Code**: `claude --plugin-dir ./piper-morgan-plugin`
- **ChatGPT**: pending (OpenAI plugin submission).

## Evals

`evals/` holds a `claude plugin eval` suite that runs against a **mocked** Piper connector (fixed data, no
sign-in), with and without the plugin. Run `claude plugin eval .` from this folder. As of v0.1.0, all three
skills score 1.00 with the plugin and 0.00 without, and an unrelated request correctly doesn't call Piper.

## Privacy and support

Privacy policy: [pipermorgan.ai/privacy](https://pipermorgan.ai/privacy). Support: see
[pipermorgan.ai](https://pipermorgan.ai).

## License

Apache-2.0. See [LICENSE](LICENSE).
