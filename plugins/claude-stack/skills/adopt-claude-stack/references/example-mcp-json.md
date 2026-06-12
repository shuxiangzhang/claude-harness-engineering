# Example: `.mcp.json` (Layer 7)

The article's full five-server config for the citation-rag service. **Adoption installs three of these, not all five.** This file documents the mature target.

## Why five, not fifteen

From the article:

> The Model Context Protocol connects the agent to external tools. Many developers install fifteen servers and wonder why the agent gets confused.
>
> Every server you install provides tool schemas. Those schemas consume context tokens on every single turn. Anthropic's Tool Search documentation notes that without lazy loading, 50 tools can consume 10,000 to 20,000 tokens per turn. Tool search lazy loading reduces that by roughly 85%, but fewer servers is still the better strategy.

The article's five-server pick:

> You need a code graph server with persistent session memory, a GitHub server for branch and commit management, a filesystem server for cross-directory access, a live web search server for current documentation and a dedicated context server for version-specific library pulls.

## The full mature config

```json
{
  "mcpServers": {
    "vexp": {
      "command": "npx",
      "args": ["-y", "@vexp/mcp-server@latest"],
      "env": {
        "VEXP_PROJECT": "citation-rag",
        "VEXP_MEMORY_DIR": ".vexp"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${HOME}/code/citation-rag",
        "${HOME}/code/shared-prompts"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

From the article on the code-graph payoff:

> The `vexp` server alone drives a 65–70% token reduction on long-running agent setups according to vexp's own published benchmarks.

On the April 2026 server-side feature:

> The April 2026 release also added a subtle server-side feature you should look for in documentation tools. Servers can now set an `anthropic/maxResultSizeChars` annotation in their tool's `_meta` field. This keeps large library documentation pulls inline instead of forcing the agent to read them from disk, entirely bypassing the old file-write workarounds.

## What adoption installs

Three servers, not five:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

…and the `github` block is dropped entirely if `git remote get-url origin` doesn't return a `github.com` URL.

## When to graduate to the full five

- **Add `vexp` (or equivalent code-graph server)** once the repo is large enough that long-running agent sessions start filling up with redundant code exploration. The vexp benefit (65–70% token reduction) only materialises on long sessions — adding it on day one pays the schema cost without earning the saving.
- **Add `brave-search` (or equivalent live web search)** the first time the user notices the agent quoting outdated framework docs.

Stay below five total. Tool schemas are not free.

## Security note

Never put a token directly in `.mcp.json`. The example uses `${GITHUB_TOKEN}` so the value is read from the user's environment at server start. Tell the user to `export GITHUB_TOKEN=...` (or set it as a user env var on Windows) — don't commit secrets.
