---
name: openair
description: >-
  This skill should be used to route openair MCP ingest and plot requests to the
  correct specialist skill. Triggers: plot, chart, csv, excel, AURN, import europe,
  upload, json_exports, wind rose, calendar plot. Not for methodology questions
  (use openair_docs on the server).
user-invocable: false
---

# OpenAir — Router

Read `../../agents/openair-agent.md` for guardrails and the analyst contract.

Route the user's request to the matching skill:

| Your data / intent | Skill |
|--------------------|-------|
| **Dev / smoke** in plugin repo (remote MCP, no Excel) | Read [`tests/fixtures/felisa_munarriz.json`](../../tests/fixtures/felisa_munarriz.json) → [`prepare-plot`](../prepare-plot/SKILL.md) — [vscode-chat-felisa.md](../../examples/vscode-chat-felisa.md) |
| CSV or Excel on **server disk** | [`ingest-local`](../ingest-local/SKILL.md) |
| File on **your machine**, remote MCP, agent can run Python | [`ingest-local-export`](../ingest-local-export/SKILL.md) |
| File on **your machine**, remote MCP, upload last resort (≤ 1 MB) | [`remote-file-upload`](../workflows/remote-file-upload/SKILL.md) |
| Regional / government Excel portal | [`regional-excel`](../workflows/regional-excel/SKILL.md) |
| UK / EU **public network** import | [`ingest-network`](../ingest-network/SKILL.md) |
| End-to-end public network → plot shortcut | [`public-network-plot`](../workflows/public-network-plot/SKILL.md) |
| **Another MCP** returns time-series JSON | [`multi-mcp`](../multi-mcp/SKILL.md) |
| SeriesV1 already loaded — plot only | [`prepare-plot`](../prepare-plot/SKILL.md) |

If openair MCP tools are not connected: copy `.mcp.json.example` → `.mcp.json` and restart the IDE session.
