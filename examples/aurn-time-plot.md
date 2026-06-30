# Example: AURN NO2 time series

**Goal:** Plot hourly NO2 from a UK AURN site for one month.

## Steps (with openair-3-mcp connected)

Follow [skills/workflows/public-network-plot/SKILL.md](../skills/workflows/public-network-plot/SKILL.md):

1. `import_aurn` — site code, pollutant `no2`, start/end dates.
2. `prepare_series_for_openair` — pass the **full** import result as `data`; `granularity=hourly`; `timezone_name=UTC` unless local diurnal view requested.
3. `time_plot` — one call; summarise PNG (range, timezone).

**MCP chain only** — do not read import JSON from disk, PowerShell, or VS Code chat session files. Use the structured output from step 1 in step 2.

## VS Code tip

For chat, start with **one month or two weeks**. A full quarter (~2,184 hourly rows) often makes Copilot spill the import to `workspaceStorage` and burn time on scripts. For a long range, use the [test harness](../tests/README.md) or ask for a shorter window first.

## Prompt (chat — one month)

```
Import AURN data for MY1 NO2 from 2024-01-01 to 2024-01-31.
MCP tools only — no terminal or scripts.
Chain: import_aurn → prepare_series_for_openair (hourly, UTC) → time_plot.
```

## Prompt (longer range — harness)

Use `tests/mcp_remote.py` after `import_aurn` returns, or keep the chat window to ≤14 days.

## References

- [openair book](https://github.com/openair-project/book/)
- Server tool list: [openair-3-mcp-server-oss README](https://github.com/miguel-escribano/openair-3-mcp-server-oss#available-tools)
