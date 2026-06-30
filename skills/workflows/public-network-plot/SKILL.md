---
name: public-network-plot
description: >-
  This skill should be used as an end-to-end shortcut for importing public network air
  quality data and plotting via openair MCP. Triggers: AURN, import europe, import ukaq,
  MY1, monitoring station, regulatory network, time plot NO2. Not for local CSV/Excel
  files. For import-only, use ingest-network.
---

# Workflow — public network → plot

**Invoke:** `@public-network-plot` (Cursor/VS Code) · Claude Code: `/openair-3-mcp-client-plugin-oss:public-network-plot` · keywords: *AURN, import europe, site code, public network*

Pattern recipe — user supplies site, pollutant, dates, network region.

Read `../../../agents/openair-agent.md` · manuals: [`ingest-network`](../../ingest-network/SKILL.md) → [`prepare-plot`](../../prepare-plot/SKILL.md).

## Steps

1. `import_aurn` / `import_europe` / `import_ukaq` — site, pollutant, date range (ask if missing).
2. `prepare_series_for_openair` — `granularity=hourly`, series from import.
3. One plot tool — usually `time_plot`; use `openair_function_help` if user asks for a different openair plot.

## Example instance (AURN)

[examples/aurn-time-plot.md](../../../examples/aurn-time-plot.md)

## Prompt template

> Import [AURN / Europe / UK] data for site `[code]` pollutant `[name]` from `[start]` to `[end]`, prepare hourly, and show a time_plot.

Cite data source and licence in the reply.

## Errors

On failure: `health_r` → report error → stop. Do not invent data or skip prepare.
