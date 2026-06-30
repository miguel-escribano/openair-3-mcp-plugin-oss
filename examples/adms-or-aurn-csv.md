# ADMS or AURN CSV on server disk

Use when the file is already on the **MCP server host** (not on the user's laptop unless using local stdio).

## ADMS

```
import_adms(
  path="/data/site/model.bgd",
  format="adms",
  adms_file_type="bgd",
  site="My stack",
  simplify_names=true
)
→ prepare_series_for_openair → time_plot
```

## UK AURN CSV export

```
import_aurn_csv(
  path="/data/aurn/MY1_hourly.csv",
  format="aurn_csv",
  site="Marylebone Road"
)
→ prepare_series_for_openair → calendar_plot
```

Paths must exist on the server filesystem.
