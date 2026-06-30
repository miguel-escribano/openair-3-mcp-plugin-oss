---
name: ingest-local
description: >-
  This skill should be used when loading CSV or Excel from the MCP server disk,
  or ADMS/AURN CSV files already on the server host. Triggers: csv, xlsx, disk path,
  load_series_from_csv, load_series_from_excel, import_adms, import_aurn_csv.
  Not for files on the user's PC, base64 upload, live public network import, or
  regional portal Excel (use ingest-local-export, remote-file-upload, ingest-network,
  or regional-excel).
---

# Ingest local — CSV / Excel

**Invoke:** `@ingest-local` (Cursor/VS Code) · Claude Code: `/openair-3-mcp-client-plugin-oss:ingest-local` · keywords: *csv, xlsx, disk path, server path*

Read `../../agents/openair-agent.md` for guardrails and the analyst contract.

## When to use

- CSV or Excel on the **MCP server host** (local stdio recommended).
- ADMS or UK AURN CSV exports already on the server disk.
- **Not** for remote MCP when the file is only in the IDE workspace — use [`ingest-local-export`](../ingest-local-export/SKILL.md) or [vscode-chat-felisa.md](../../examples/vscode-chat-felisa.md) for smoke.
- Not for public live network import — use [`ingest-network`](../ingest-network/SKILL.md).
- Not for regional/government portal Excel — use [`regional-excel`](../workflows/regional-excel/SKILL.md).

## Paths

| Path | When | Next step |
|------|------|-----------|
| **Disk** | File on the **MCP server host** | `load_series_from_csv` or `load_series_from_excel` → [`prepare-plot`](../prepare-plot/SKILL.md) |
| **Local PC + remote MCP** | File on user's machine | [`ingest-local-export`](../ingest-local-export/SKILL.md) (preferred) or [`remote-file-upload`](../workflows/remote-file-upload/SKILL.md) (last resort) |

Do **not** call `load_series_from_*` with a path on the user's laptop when MCP runs on a **remote** server.

Do **not** use pandas, openpyxl, or manual SeriesV1 in the IDE (O1, O2).

## Parameter glossary (user supplies domain facts)

Ask the user when missing — do not guess column names, timezone, or site.

1. **`datetime_col`** — exact header name (e.g. `date`, `Fecha/hora`).
2. **`columns`** — exact pollutant header(s); use `columns` on load to skip IoT metadata numerics.
3. **`timezone`** — IANA zone for naive local timestamps (e.g. `Europe/Madrid`).
4. **`site`** — optional station label for plot titles (`meta.site`); ask when the file name or user context implies a site name.
5. **`lat` / `lon`** — optional WGS84 coordinates for `meta` (needed before future **worldmet** meteo merge → wind plots).
6. **`dedupe_timestamps`** — `true` when portal exports repeat the same hour.
7. **`path`** (Disk) — path on **server** filesystem.

After load, always `prepare_series_for_openair` before any plot — see [`prepare-plot`](../prepare-plot/SKILL.md).

## openair file formats (server disk)

When ADMS or UK AURN CSV exports already sit on the **MCP server host**, use R import tools (not pandas):

| Tool | Format | Notes |
|------|--------|-------|
| `import_adms` | CERC ADMS (`.bgd`, `.met`, `.mop`, `.pst`) | `path` on server; optional `adms_file_type`, `site` |
| `import_aurn_csv` | UK AURN hourly CSV | `path` on server; optional `site`, `simplify_names` |

Both return SeriesV1 → chain `prepare_series_for_openair` → plot. See [`examples/adms-or-aurn-csv.md`](../../examples/adms-or-aurn-csv.md).

Do **not** list these under public network ingest — they are local/server-disk paths, not live portal fetch.

## Pattern recipes

| Situation | Workflow |
|-----------|----------|
| Regional / gov Excel portal | [`regional-excel`](../workflows/regional-excel/SKILL.md) |
| Attachment on PC, remote MCP | [`ingest-local-export`](../ingest-local-export/SKILL.md) (**preferred**) or [`remote-file-upload`](../workflows/remote-file-upload/SKILL.md) |
| CSV on server disk | [examples/csv-calendar-plot.md](../../examples/csv-calendar-plot.md) |

## Errors

On failure: `health_r` → report error → stop. Do not fabricate plots or skip prepare.
