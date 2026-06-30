# VS Code chat — Felisa Munarriz (remote MCP)

**Use this when** VS Code Copilot is wired to a **remote** MCP server (HTTP + `mcp-remote`) and you want a quick plot without hunting for Excel files.

The golden dataset is already in this repo:

`tests/fixtures/felisa_munarriz.json`

649 hourly rows · NO₂, PM₁₀, O₃ · June 2026 · site Felisa Munarriz, Pamplona · real ERA5 wind in `meta`.

## Prompt (copy-paste)

```
Use the committed test fixture tests/fixtures/felisa_munarriz.json in this repo.
Read that file and pass it as data to prepare_series_for_openair
(granularity hourly, timezone_name Europe/Madrid), then time_plot all pollutants.

MCP tools only — do not search for data/felisa.xlsx or other Excel paths on disk or server.
Do not write scripts.
```

## What the agent should do

1. Read `tests/fixtures/felisa_munarriz.json` (read-file tool).
2. `prepare_series_for_openair(data=<fixture JSON>, granularity=hourly, timezone_name=Europe/Madrid)`.
3. `time_plot` with the prepare output.

Same pipeline as `tests/run_series_exercises.py` exercise 2 — without the harness.

## If you have a real Excel on your PC

Do **not** say “on the server” unless you literally uploaded the file to the Linode host.

```
I have the Navarra Excel on my PC at C:\Users\me\Downloads\felisa.xlsx
Datetime column Fecha/hora, timezone Europe/Madrid, dedupe duplicate hours.
Run export_local_series.py from openair-3-mcp-server-oss, then prepare hourly and time_plot via MCP.
```

Or attach the file and ask for base64 upload (≤ 1 MB) — see [local-excel-spain.md](local-excel-spain.md).

## Reliable batch check (no Copilot)

```powershell
$env:OPENAIR_MCP_TOKEN = "…"
$env:OPENAIR_MCP_URL = "https://…/sse"
python tests/run_series_exercises.py
```

See [tests/README.md](../tests/README.md).
