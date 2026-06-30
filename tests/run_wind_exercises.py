#!/usr/bin/env python3
"""Felisa + synthetic wind golden path against a remote openair MCP server."""
from __future__ import annotations

import base64
import sys
from pathlib import Path

from fixture_loader import load_wind_series
from mcp_remote import McpClient

TESTS_DIR = Path(__file__).resolve().parent
OUT_DIR = TESTS_DIR / "output" / "wind"


def save_plot(mcp: McpClient, name: str, data: dict, slug: str) -> bool:
    raw = mcp.call_tool(name, {"data": data})
    png_path = OUT_DIR / f"{slug}.png"
    for block in raw.get("content") or []:
        if block.get("type") == "image" and block.get("data"):
            png_path.write_bytes(base64.b64decode(block["data"]))
            print(f"  OK {name} -> {png_path.name}")
            return True
    print(f"  FAIL {name}: no PNG")
    return False


def main() -> int:
    try:
        wind = load_wind_series()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loaded {len(wind['timestamps'])} rows, pollutants: {[s['name'] for s in wind['series']]}")

    mcp = McpClient()
    results: list[tuple[str, str]] = []

    try:
        mcp.start()
        print("MCP session OK\n")

        for i, (tool, slug, label) in enumerate(
            [
                ("wind_rose", "01_wind_rose", "wind_rose"),
                ("polar_plot", "02_polar_plot_pm10", "polar_plot pm10"),
                ("pollution_rose", "03_pollution_rose", "pollution_rose"),
                ("percentile_rose", "04_percentile_rose", "percentile_rose"),
            ],
            start=1,
        ):
            print(f"{i} {label}")
            ok = save_plot(mcp, tool, wind, slug)
            results.append((f"{i} {label}", "OK" if ok else "FAIL"))

    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1
    finally:
        mcp.close()

    print("\n=== Summary ===")
    for name, status in results:
        print(f"  {status:4}  {name}")
    print(f"\nArtifacts: {OUT_DIR}")
    return 0 if all(s == "OK" for _, s in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
