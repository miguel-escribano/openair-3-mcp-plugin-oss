---
name: ingest-local-export
description: >-
  This skill should be used when a CSV or Excel file is on the user's machine and
  the agent can run export_local_series.py before calling the remote openair MCP.
  Triggers: export script, local file remote MCP, SeriesV1 json, Windows excel path.
  Not for server disk paths, base64 upload, or live public network import.
---

# Ingest local — agent-run export script

**Invoke:** `@ingest-local-export` (Cursor/VS Code) · Claude Code: `/openair-3-mcp-client-plugin-oss:ingest-local-export` · keywords: *export script, local file, remote MCP, _series_v1.json*

For **agent-capable harnesses** (Cursor, VS Code Copilot, Claude Code, Codex) when:

- File is on the **user's machine** (Windows path, attachment, workspace)
- openair MCP is **remote** (or you prefer not to use base64 upload)
- User has Python with the server package installed (`pip install -e` from [openair-3-mcp-server-oss](https://github.com/miguel-escribano/openair-3-mcp-server-oss) — **R not required for export**)

Read `../../agents/openair-agent.md` for guardrails.

## What this is (and is not)

| Yes | No |
|-----|-----|
| Agent runs the **fixed** `export_local_series.py` from the server repo | LLM parses cells or writes SeriesV1 by hand |
| Same date/dedupe logic as `load_series_from_*` on the server | Ad-hoc pandas/openpyxl snippets in chat |
| Output → `prepare_series_for_openair(data=…)` → plot | `_pm10_data.json` invented in the repo |

Deterministic export script pattern: fixed code produces JSON; the model only orchestrates.

## Prerequisites

One-time on the user's machine (export only — no R):

```bash
git clone https://github.com/miguel-escribano/openair-3-mcp-server-oss
cd openair-3-mcp-server-oss
pip install -e .
```

Excel requires `openpyxl` (installed with the server package).

## Steps

1. Analyst supplies: file path, `datetime_col`, `columns`, `timezone`, optional `site`, optional `lat`/`lon` (WGS84), `dedupe`.
2. Agent runs **only** this script (adjust path to server clone):

   ```bash
   python path/to/openair-3-mcp-server-oss/scripts/export_local_series.py \
     --input "C:/Users/you/FELISA-MUNARRIZ.xlsx" \
     --datetime-col "Fecha/hora" \
     --columns "Partículas en suspensión < 10 µm (µg/m³)" \
     --timezone Europe/Madrid \
     --site "Felisa Munarriz, Pamplona" \
     --lat 42.80686 --lon -1.64405 \
     --output _series_v1.json
   ```

3. Agent reads `_series_v1.json` with the read-file tool.
4. `prepare_series_for_openair(data=<json>, series_name=…, granularity=hourly, timezone_name=…)` — output includes **`meta`** (site, timezone) for plot titles when present in the export.
5. One plot tool — see [`prepare-plot`](../prepare-plot/SKILL.md). Chart legends use short ids (PM10, NO2, O3) when headers match common regional patterns.
6. Delete `_series_v1.json` after success.

## When to use another path

| Situation | Use |
|-----------|-----|
| openair + R on same machine as IDE | `load_series_from_*` via [`ingest-local`](../ingest-local/SKILL.md) Disk path |
| Tiny file, no Python export setup | [`remote-file-upload`](../workflows/remote-file-upload/SKILL.md) (base64 — last resort) |
| Sensor API / upstream MCP | [`multi-mcp`](../multi-mcp/SKILL.md) `json_exports` |
| Public network | [`ingest-network`](../ingest-network/SKILL.md) |

## Errors

Script stderr → report to user. Do not fall back to hand-built JSON. On prepare/plot failure: `health_r`.
