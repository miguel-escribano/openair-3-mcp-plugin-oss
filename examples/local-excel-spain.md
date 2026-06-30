# Local Excel — Spain regional export → time_plot

Example for government / regional air-quality Excel downloads (e.g. hourly PM10).

## Pick your path first

| Your setup | Use | Do not use |
|------------|-----|------------|
| **VS Code + remote MCP** (typical) | [vscode-chat-felisa.md](vscode-chat-felisa.md) for dev · [ingest-local-export](../skills/ingest-local-export/SKILL.md) for real Excel on your PC | `load_series_from_excel` with `data/felisa.xlsx` — that path is **not** in the repo and is **not** on Linode unless you uploaded it yourself |
| **Local stdio** (IDE and server on same machine) | Disk path below | — |
| **Quick proof without Excel** | `tests/fixtures/felisa_munarriz.json` + harness or [vscode-chat-felisa.md](vscode-chat-felisa.md) | — |

## Sample shape

| Fecha/hora | Partículas en suspensión < 10 µm (µg/m³) |
|------------|------------------------------------------|
| 23/06/2026 00:00h | 58 |
| 23/06/2026 01:00h | 55 |

- Day-first dates with optional trailing **`h`**
- Long pollutant header — pass exact name in `columns=` (server maps to **PM10 / NO2 / O3** on chart legends). Renaming the Excel column to `PM10` is optional, not required.
- May contain **duplicate hours** — set `dedupe_timestamps=true`

## PC file + remote MCP (most VS Code users)

See [`ingest-local-export`](../skills/ingest-local-export/SKILL.md).

### Prompt

```
I have the Navarra hourly Excel on my PC at [full path to file].
Station Felisa Munarriz, Pamplona. Datetime column Fecha/hora, timezone Europe/Madrid.
Plot NO2, PM10 and ozone. Dedupe duplicate hours.
Run export_local_series.py, then prepare hourly and time_plot via MCP. No ad-hoc scripts.
```

Attach the file if the path is awkward.

## Upload — small file on your PC (≤ 1 MB, last resort)

1. Encode to **`_b64_tmp.txt`** (do not print base64 to terminal — truncated on Windows):

   ```bash
   python -c "import base64,sys; open('_b64_tmp.txt','w',encoding='utf-8').write(base64.b64encode(open(sys.argv[1],'rb').read()).decode())" "path/to/felisa.xlsx"
   ```

2. Read `_b64_tmp.txt` → `load_series_from_upload(content_base64=..., file_type="xlsx", datetime_col="Fecha/hora", columns=[...], timezone="Europe/Madrid", dedupe_timestamps=true)`
3. Delete `_b64_tmp.txt` → `prepare_series_for_openair` → `time_plot`.

Do **not** use `load_series_from_excel` with a local Windows path on a remote server.

## Disk — file on MCP server host only

**Only when** MCP runs on the **same machine** as the file, or you have **confirmed** the file exists on the remote host at an absolute path.

There is **no** bundled `data/felisa.xlsx`. Example paths are placeholders.

```
load_series_from_excel(
  path="/absolute/path/on/server/felisa.xlsx",
  datetime_col="Fecha/hora",
  timezone="Europe/Madrid",
  site="Felisa Munarriz, Pamplona",
  dedupe_timestamps=true
)
-> prepare_series_for_openair(granularity=hourly, timezone_name=Europe/Madrid)
-> time_plot
```

If `load_series_from_excel` returns file not found: stop — do not search the IDE workspace for server paths.

See [skills/workflows/regional-excel/SKILL.md](../skills/workflows/regional-excel/SKILL.md) and [skills/ingest-local/SKILL.md](../skills/ingest-local/SKILL.md).

## Golden test data (no Excel needed)

| File | Purpose |
|------|---------|
| `tests/fixtures/felisa_munarriz.json` | Plugin harness + VS Code chat ([vscode-chat-felisa.md](vscode-chat-felisa.md)) |
| `tests/run_series_exercises.py` | 11-plot acceptance against deployed MCP |

Server repo [`fixtures/sample_spain_hourly.csv`](https://github.com/miguel-escribano/openair-3-mcp-server-oss/blob/main/fixtures/sample_spain_hourly.csv) is for **pytest ingest only**, not Copilot chat.
