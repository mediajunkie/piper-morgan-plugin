# MCP Registry entry (prepared, NOT published)

`server.json` for the official MCP Registry (`registry.modelcontextprotocol.io`). Remote-only, so no
`packages` (per modelcontextprotocol.io/registry/remote-servers).

**Not published.** Publishing needs PM's go (part of the R7 demand probe). It also needs domain proof for
the `ai.pipermorgan/*` namespace: either a DNS TXT record on pipermorgan.ai (PM's DNS) or an HTTP proof at
`https://pipermorgan.ai/.well-known/mcp-registry-auth`, then `mcp-publisher login dns|http` and
`mcp-publisher publish` from this folder.
