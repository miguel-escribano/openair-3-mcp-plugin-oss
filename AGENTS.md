# openair-3-mcp-client-plugin-oss

**Agent:** `agents/openair-agent.md` (client orchestrator — not the R server)

**Router:** `skills/openair/SKILL.md` (auto-routes to specialist skills)

## Testing (acceptance)

Golden path: `tests/` + `tests/fixtures/felisa_munarriz.json` — see [tests/README.md](tests/README.md). VS Code chat smoke: [examples/vscode-chat-felisa.md](examples/vscode-chat-felisa.md). Server `pytest` is pre-deploy only.

## MCP

Copy `.mcp.json.example` → `.mcp.json` (gitignored). See [CONNECTORS.md](CONNECTORS.md).

## Skills

| Manual | Use |
|--------|-----|
| *(dev smoke)* | `tests/fixtures/felisa_munarriz.json` → prepare → plot — [vscode-chat-felisa.md](examples/vscode-chat-felisa.md) |
| `ingest-local` | CSV / Excel on **server host** (local stdio or confirmed remote path) |
| `ingest-network` | AURN, Europe, UK public data |
| `prepare-plot` | prepare → one plot tool |
| `ingest-local-export` | Local file → export script → prepare (remote MCP) |
| `multi-mcp` | json_exports from another MCP |

| Workflow | Use |
|----------|-----|
| `regional-excel` | Gov / regional Excel portal pattern |
| `public-network-plot` | Import network → plot |
| `remote-file-upload` | Attachment on PC, remote MCP |

See README → **Using skills** for routing.

## Server

[openair-3-mcp-server-oss](https://github.com/miguel-escribano/openair-3-mcp-server-oss) — self-host with R + openair 3.x.
