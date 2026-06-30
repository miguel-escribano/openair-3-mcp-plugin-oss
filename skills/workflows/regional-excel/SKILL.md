---
name: regional-excel
description: >-
  This skill should be used for regional or government Excel air-quality portal exports
  with day-first dates, long headers, or duplicate hours. Triggers: regional excel,
  portal export, Fecha/hora, dedupe timestamps, government download. Not for generic
  CSV on server disk or live public network import.
---

# Workflow — regional Excel export

**Invoke:** `@regional-excel` (Cursor/VS Code) · Claude Code: `/openair-3-mcp-client-plugin-oss:regional-excel` · keywords: *regional excel, Fecha/hora, portal, dedupe, xlsx*

Pattern recipe — adapt column names and timezone to **your** file (analyst supplies domain facts).

Read `../../../agents/openair-agent.md` · manuals: [`ingest-local`](../../ingest-local/SKILL.md) → [`prepare-plot`](../../prepare-plot/SKILL.md).

## When to use

- Excel from a regional/government air-quality portal (any locale).
- Day-first dates, long pollutant headers, possible duplicate hours.

## What you must provide

- `datetime_col` (exact header)
- Pollutant column name(s) — exact portal header(s); server shortens labels on charts (PM10, NO2, O3)
- Optional `site` for plot title
- IANA `timezone` if timestamps are naive local
- Disk path on server **or** attachment for upload
- **Remote MCP + VS Code:** do not invent `data/felisa.xlsx` — use [vscode-chat-felisa.md](../../../examples/vscode-chat-felisa.md) or [`ingest-local-export`](../../ingest-local-export/SKILL.md)

## Steps

1. **Disk** (file on server): `load_series_from_excel` with `path`, `datetime_col`, `columns`, `timezone`, optional `site`, `dedupe_timestamps=true` when needed.
2. **Upload** (remote MCP, ≤ 1 MB): see [`remote-file-upload`](../remote-file-upload/SKILL.md).
3. **Local PC + remote MCP:** prefer [`ingest-local-export`](../../ingest-local-export/SKILL.md).
4. `prepare_series_for_openair` — `series_name`, `granularity=hourly`, `timezone_name` as needed.
5. One plot tool (usually `time_plot` or `calendar_plot`).

## Example instance (Spain)

[examples/local-excel-spain.md](../../../examples/local-excel-spain.md) — `Fecha/hora`, PM10, `Europe/Madrid`, dedupe.

## Prompt template

> I have a regional hourly Excel export. Datetime column is `[col]`, pollutant `[name]`, timezone `[IANA]`. [PC path + export script / Upload: attached file / Dev: tests/fixtures/felisa_munarriz.json]. Dedupe duplicate hours. Prepare hourly and [time_plot / calendar_plot].

**Do not** use “file on server at data/felisa.xlsx” unless the user confirmed that exact path on the MCP host.

## Errors

On failure: `health_r` → report error → stop. Do not invent data or skip prepare.
