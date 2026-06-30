"""Minimal HTTP/SSE client for remote openair MCP harness scripts."""
from __future__ import annotations

import json
import os

import httpx

DEFAULT_URL = "https://mcp.miguel-escribano.com/openair-3-mcp-server-oss/sse"


class McpClient:
    def __init__(self, url: str | None = None, token: str | None = None) -> None:
        self.url = url or os.environ.get("OPENAIR_MCP_URL", DEFAULT_URL)
        self.token = token or os.environ.get("OPENAIR_MCP_TOKEN", "")
        if not self.token:
            raise ValueError("Set OPENAIR_MCP_TOKEN")
        self.session_id: str | None = None
        self.client = httpx.Client(timeout=180.0)
        self._id = 0

    def _headers(self) -> dict[str, str]:
        h = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "X-MCP-Token": self.token,
        }
        if self.session_id:
            h["Mcp-Session-Id"] = self.session_id
        return h

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    @staticmethod
    def _parse_sse(body: str) -> list[dict]:
        out: list[dict] = []
        for block in body.split("\n\n"):
            data_lines = [ln[5:].strip() for ln in block.splitlines() if ln.startswith("data:")]
            if not data_lines:
                continue
            try:
                out.append(json.loads("\n".join(data_lines)))
            except json.JSONDecodeError:
                continue
        return out

    def _post(self, message: dict) -> dict:
        r = self.client.post(self.url, headers=self._headers(), json=message)
        r.raise_for_status()
        if not self.session_id and "mcp-session-id" in r.headers:
            self.session_id = r.headers["mcp-session-id"]
        events = self._parse_sse(r.text)
        for ev in events:
            if ev.get("id") == message.get("id") and "result" in ev:
                return ev["result"]
            if ev.get("id") == message.get("id") and "error" in ev:
                raise RuntimeError(ev["error"])
        if events:
            return events[-1].get("result") or events[-1]
        return {}

    def start(self) -> None:
        self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "openair-plugin-tests", "version": "1.0"},
                },
            }
        )
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            }
        )

    def close(self) -> None:
        self.client.close()


def extract_tool_payload(raw: dict) -> dict:
    if isinstance(raw, dict) and raw.get("structuredContent"):
        return raw["structuredContent"]
    for block in raw.get("content") or []:
        if block.get("type") == "text":
            try:
                return json.loads(block["text"])
            except json.JSONDecodeError:
                return {"text": block["text"]}
    if "timestamps" in raw or "series" in raw or "error" in raw or "ws" in raw:
        return raw
    return {"raw": raw}
