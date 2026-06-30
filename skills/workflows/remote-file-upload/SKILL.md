---
name: remote-file-upload
description: >-
  This skill should be used when uploading Excel or CSV from the user's PC to a remote
  openair MCP via base64 as a last resort (≤ 1 MB). Triggers: attachment, upload,
  base64, remote MCP, Downloads, file on my computer. Not for export script path or
  files already on the server disk.
---

# Workflow — remote file upload → plot

**Invoke:** `@remote-file-upload` (Cursor/VS Code) · Claude Code: `/openair-3-mcp-client-plugin-oss:remote-file-upload` · keywords: *attachment, upload, base64, remote MCP, Downloads*

Use when the MCP server is **remote** and the file is **only on the user's PC** (≤ 1 MB raw).

Read `../../../agents/openair-agent.md` · manuals: [`ingest-local`](../../ingest-local/SKILL.md) → [`prepare-plot`](../../prepare-plot/SKILL.md).

## What you must provide

- Attached file or workspace path on user machine
- `datetime_col`, `columns`, `timezone` if not obvious from context
- Desired plot type

## Steps

1. Copy attachment to workspace if the IDE requires it.
2. **Encode to `_b64_tmp.txt`** — never print base64 to terminal (truncated on Windows; agent loops):

   ```bash
   python -c "import base64,sys; open('_b64_tmp.txt','w',encoding='utf-8').write(base64.b64encode(open(sys.argv[1],'rb').read()).decode())" "path/to/file.xlsx"
   ```

3. Read `_b64_tmp.txt` with the read-file tool.
4. `load_series_from_upload` — pass full `content_base64`, `file_type` (`csv` or `xlsx`), parsing params.
5. Delete `_b64_tmp.txt`.
6. `prepare_series_for_openair` → one plot tool.

**Dead ends:** `| clip`, clipboard, terminal stdout capture for large strings, `_pm10_data.json` / hand-built SeriesV1.

If upload fails or file > 1 MB: ask user to copy file to server disk or switch to local stdio — never pandas.

## Related patterns

- Regional Excel quirks → [`regional-excel`](../regional-excel/SKILL.md)
- File on PC, agent can run Python → [`ingest-local-export`](../../ingest-local-export/SKILL.md) (**preferred**)
- File already on server → [`ingest-local`](../../ingest-local/SKILL.md) (Disk path)

## Prompt template

> I attached `[file.csv/xlsx]` at `[path]`. Upload via remote-file-upload workflow (temp base64 file). Datetime `[col]`, pollutant `[name]`, timezone `[IANA]`. Prepare and [calendar_plot / time_plot]. MCP tools only.

## Errors

On failure: `health_r` → report error → stop. Do not invent data or skip prepare.
