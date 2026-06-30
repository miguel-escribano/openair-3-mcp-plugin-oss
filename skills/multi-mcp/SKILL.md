---
name: multi-mcp
description: >-
  This skill should be used when chaining another MCP's time-series JSON into openair
  plots via json_exports. Triggers: another MCP, API, postgres, airtable, json_exports,
  sensor platform, upstream MCP. Not for CSV/Excel on disk or public network import_*.
---

# Multi-MCP bridge

**Invoke:** `@multi-mcp` (Cursor/VS Code) · Claude Code: `/openair-3-mcp-client-plugin-oss:multi-mcp` · keywords: *another MCP, json_exports, API, database, postgres, airtable*

Read `../../agents/openair-agent.md` for guardrails.

## When to use

- User has a **second MCP** configured (REST API, Postgres read, Airtable, custom sensor store, etc.).
- Data does **not** come from CSV/Excel on disk, upload, or `import_*`.

This project does **not** ship Postgres, Airtable, or API connectors — only the bridge into openair.

## Steps

1. Call the **upstream MCP tool** that returns hourly/time-series JSON (user names source and query).
2. `prepare_series_for_openair(json_exports=[export])` — optional `series_name`, `parameter`, `granularity`, `timezone_name`.
3. One plot tool via [`prepare-plot`](../prepare-plot/SKILL.md).

The upstream MCP owns fetch and query; the openair server owns alignment and plots. Never build series arrays in the client (O2).

## Export requirements

Deterministic structured JSON — `series_v1` or compatible export shape. Schema: [SeriesV1](https://github.com/miguel-escribano/openair-3-mcp-server-oss/blob/main/schemas/series.v1.json).

Wire both MCPs in `.mcp.json` — see [CONNECTORS.md](../../CONNECTORS.md).

## Errors

On failure: `health_r` → report upstream or openair MCP error; do not invent data.
