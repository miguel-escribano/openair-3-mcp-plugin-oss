# Example: CSV → calendar plot

**Goal:** Plot daily PM2.5 from a CSV file on the MCP server host.

## Prerequisites

- openair-3-mcp-server-oss running (HTTP or stdio).
- CSV on the **MCP server host** with columns `date`, `PM25` (copy server `fixtures/sample_hourly.csv` there, or use an absolute path on the host).

**Remote MCP (VS Code):** paths in the IDE workspace are invisible to the server. For smoke without uploading CSV, use [vscode-chat-felisa.md](vscode-chat-felisa.md) instead.

## Steps

Manual: [skills/ingest-local/SKILL.md](../skills/ingest-local/SKILL.md) → [skills/prepare-plot/SKILL.md](../skills/prepare-plot/SKILL.md).

1. `load_series_from_csv` — `path` to file, `columns`: `["PM25"]`, `datetime_col`: `"date"`.
2. `prepare_series_for_openair` — `data` from step 1, `granularity`: `"hourly"`, `series_name`: `"PM25"`.
3. `calendar_plot` — one call; summarise PNG.

## Prompt

**Local stdio or file copied to server host:**

```
Load /path/on/server/sample_hourly.csv, prepare hourly UTC,
and show a calendar_plot for PM25.
```

**Remote MCP:** use [vscode-chat-felisa.md](vscode-chat-felisa.md) or [ingest-local-export](../skills/ingest-local-export/SKILL.md) — not a repo-relative `fixtures/` path unless that file exists on the server.

## Notes

- Path is on the server filesystem, not the IDE machine (unless they are the same).
- IoT exports with extra numeric columns — always pass `columns` to select pollutants.
