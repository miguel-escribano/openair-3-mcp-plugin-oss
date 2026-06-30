#!/usr/bin/env python3
"""Felisa Munarriz pollutant golden path against a remote openair MCP server."""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

from fixture_loader import load_series_v1
from mcp_remote import McpClient, extract_tool_payload

TESTS_DIR = Path(__file__).resolve().parent
OUT_DIR = TESTS_DIR / "output" / "series"


def prep_to_series_v1(prep: dict, meta: dict | None = None) -> dict:
    out: dict = {"timestamps": prep["timestamps"], "series": prep["series"]}
    if meta:
        out["meta"] = meta
    elif prep.get("meta"):
        out["meta"] = prep["meta"]
    return out


def prepare(
    mcp: McpClient,
    data: dict,
    series_name: str | None = None,
) -> dict:
    args: dict = {
        "data": data,
        "granularity": "hourly",
        "timezone_name": "Europe/Madrid",
    }
    if series_name:
        args["series_name"] = series_name
    prep = extract_tool_payload(mcp.call_tool("prepare_series_for_openair", args))
    if prep.get("error"):
        raise RuntimeError(prep["error"])
    return prep


def tool_json(mcp: McpClient, name: str, data: dict, **extra) -> dict:
    payload = prep_to_series_v1(data) if "coverage_ratio" in data else data
    return extract_tool_payload(mcp.call_tool(name, {"data": payload, **extra}))


def save_plot(mcp: McpClient, name: str, data: dict, slug: str, **extra) -> bool:
    payload = prep_to_series_v1(data) if "coverage_ratio" in data else data
    raw = mcp.call_tool(name, {"data": payload, **extra})
    png_path = OUT_DIR / f"{slug}.png"
    for block in raw.get("content") or []:
        if block.get("type") == "image" and block.get("data"):
            png_path.write_bytes(base64.b64decode(block["data"]))
            print(f"  OK {name} -> {png_path.name}")
            return True
    print(f"  FAIL {name}: no PNG")
    return False


def subset_series(data: dict, names: list[str]) -> dict:
    return {**data, "series": [s for s in data["series"] if s["name"] in names]}


def main() -> int:
    try:
        raw = load_series_v1()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    names = [s["name"] for s in raw["series"]]
    print(f"Loaded {len(raw['timestamps'])} timestamps, series: {names}")

    mcp = McpClient()
    results: list[tuple[str, str]] = []

    try:
        mcp.start()
        print("MCP session OK\n")

        pm10_name = next(n for n in names if "10" in n or "PM" in n.upper())
        no2_name = next(n for n in names if "nitr" in n.lower())

        print("1 time_plot PM10")
        s1 = prep_to_series_v1(prepare(mcp, raw, series_name=pm10_name), raw.get("meta"))
        save_plot(mcp, "time_plot", s1, "01_time_plot_pm10")
        results.append(("1 time_plot PM10", "OK"))

        print("2 time_plot all pollutants")
        s2 = prep_to_series_v1(prepare(mcp, raw), raw.get("meta"))
        save_plot(mcp, "time_plot", s2, "02_time_plot_all")
        results.append(("2 time_plot x3", "OK"))

        print("3 calendar_plot PM10")
        save_plot(mcp, "calendar_plot", s1, "03_calendar_pm10")
        results.append(("3 calendar_plot", "OK"))

        print("4 time_variation")
        save_plot(mcp, "time_variation", s2, "04_time_variation")
        results.append(("4 time_variation", "OK"))

        print("5 trend_level PM10")
        save_plot(mcp, "trend_level", s1, "05_trend_level_pm10")
        results.append(("5 trend_level", "OK"))

        print("6 scatter_plot NO2 vs PM10")
        sp = prep_to_series_v1(prepare(mcp, subset_series(raw, [no2_name, pm10_name])), raw.get("meta"))
        save_plot(mcp, "scatter_plot", sp, "06_scatter_no2_pm10")
        results.append(("6 scatter_plot", "OK"))

        print("7 cor_plot")
        save_plot(mcp, "cor_plot", s2, "07_cor_plot")
        results.append(("7 cor_plot", "OK"))

        print("8 aq_stats PM10")
        stats = tool_json(mcp, "aq_stats", s1)
        (OUT_DIR / "08_aq_stats_pm10.json").write_text(
            json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print("  OK aq_stats -> 08_aq_stats_pm10.json")
        results.append(("8 aq_stats", "OK"))

        print("9 smooth_trend PM10")
        save_plot(mcp, "smooth_trend", s1, "09_smooth_trend_pm10")
        results.append(("9 smooth_trend", "OK"))

        print("10 rolling_mean 8h -> time_plot")
        rolled = tool_json(mcp, "rolling_mean", s1)
        if rolled.get("timestamps") and rolled.get("series"):
            save_plot(mcp, "time_plot", rolled, "10_rolling8h_timeplot")
            results.append(("10 rolling_mean 8h", "OK"))
        else:
            results.append(("10 rolling_mean", "FAIL"))

        print("11 time_average daily -> time_plot")
        daily = tool_json(mcp, "time_average", s1)
        if daily.get("timestamps"):
            save_plot(mcp, "time_plot", daily, "11_daily_timeplot")
            results.append(("11 time_average", "OK"))
        else:
            results.append(("11 time_average", "FAIL"))

        print("12 summary_plot all pollutants")
        save_plot(mcp, "summary_plot", s2, "12_summary_plot_all")
        results.append(("12 summary_plot", "OK"))

    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1
    finally:
        mcp.close()

    print("\n=== Summary ===")
    for name, status in results:
        print(f"  {status:4}  {name}")
    print(f"\nArtifacts: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
