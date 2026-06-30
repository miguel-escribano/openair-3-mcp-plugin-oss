# Connectors

## openair MCP (required)

This plugin expects **openair-3-mcp-server-oss** in your MCP client config (see `.mcp.json.example`).

### Local (default)

Install R + openair 3.x and the server on the **same machine** as your IDE:

| Transport | When to use |
|-----------|-------------|
| **stdio** | Simplest — IDE spawns Python; no Node, no HTTP port |
| **HTTP + `mcp-remote`** | Server on `127.0.0.1:8001`; client uses `npx mcp-remote` |

### Remote (optional)

Run the server on another host (your VM, cloud, or a maintainer pilot). Point `mcp-remote` at that HTTPS URL; use `X-MCP-Token` when auth is enabled.

Same server code — only the URL in `.mcp.json` changes.

### Remote + attachments

When the user's Excel/CSV is **not** on the server disk (typical **VS Code + remote MCP**):

1. **Preferred** — [`ingest-local-export`](skills/ingest-local-export/SKILL.md): `export_local_series.py` on the user's PC → `prepare(data=…)` on MCP.
2. **Dev / smoke (no Excel)** — [examples/vscode-chat-felisa.md](examples/vscode-chat-felisa.md): read `tests/fixtures/felisa_munarriz.json` → prepare → plot. **Do not** hunt for `data/felisa.xlsx` or other example server paths.
3. **Upload (last resort)** — `load_series_from_upload` base64 via `_b64_tmp.txt` (max 1 MB raw); see [remote-file-upload](skills/workflows/remote-file-upload/SKILL.md).
4. **Fallback** — user copies file to server disk and uses `load_series_from_csv` / `load_series_from_excel` with a **confirmed absolute path on the host**.

Never parse files with pandas in the IDE.

**Acceptance after deploy:** plugin [tests/README.md](tests/README.md) (15-plot harness) — not example doc paths on the server.

### File imports (server disk)

When ADMS or AURN CSV files are on the server host: `import_adms`, `import_aurn_csv` → prepare → plot. See `skills/ingest-local/SKILL.md` and `examples/adms-or-aurn-csv.md`.

## Multi-MCP (API, database, spreadsheet, …)

Add a **second MCP server** in `.mcp.json` for data that does not live in CSV, Excel, or public AURN/EU networks.

1. Upstream MCP runs the fetch/query (REST API, Postgres, Airtable, custom store, …).
2. Pass the export to openair: `prepare_series_for_openair(json_exports=[…])`.
3. Plot via openair tools.

Export must be structured JSON — see [SeriesV1 schema](https://github.com/miguel-escribano/openair-3-mcp-server-oss/blob/main/schemas/series.v1.json). Calculation stays on upstream MCP + openair server; the LLM only orchestrates.

Standalone CSV / `import_*` users do not need a second MCP. openair does not ship Postgres, Airtable, or API connectors itself.

## Setup

1. [Run the server](https://github.com/miguel-escribano/openair-3-mcp-server-oss#choose-your-setup) — local or remote.
2. Copy `.mcp.json.example` → `.mcp.json` (gitignored) — stdio, localhost, or remote URL.
3. Install this plugin in Claude Code / Cursor / Codex / VS Code.
