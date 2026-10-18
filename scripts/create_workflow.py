#!/usr/bin/env python3
"""Create or refresh a reproducible project workflow record."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path


DEFAULT_CONFIG = {
    "default_python": None,
    "arcpy_python": None,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--runtime")
    parser.add_argument("--config", help="Optional JSON runtime configuration")
    parser.add_argument("--script", action="append", default=[], help="Script path used to infer runtime when --runtime is omitted")
    parser.add_argument("--command", action="append", default=[])
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--date", help="YYYYMMDD; defaults to local date")
    return parser.parse_args()


def load_config(path: str | None) -> dict[str, str | None]:
    config = dict(DEFAULT_CONFIG)
    if not path:
        return config
    config_path = Path(path).expanduser().resolve()
    if not config_path.is_file():
        raise SystemExit(f"Config file does not exist: {config_path}")
    try:
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON config: {config_path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise SystemExit("Runtime config must be a JSON object")
    for key in DEFAULT_CONFIG:
        value = loaded.get(key)
        if value is not None and not isinstance(value, str):
            raise SystemExit(f"Runtime config value must be a string or null: {key}")
        config[key] = value
    return config


def bullets(values: list[str], fallback: str) -> str:
    return "\n".join(f"- `{value}`" for value in values) if values else f"- {fallback}"


def workflow_path(project_dir: Path, date: str) -> Path:
    existing = sorted(
        project_dir.glob(f"*_{project_dir.name}_WORKFLOW.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return existing[0] if existing else project_dir / f"{date}_{project_dir.name}_WORKFLOW.md"


def infer_runtime(project_dir: Path, scripts: list[str], config: dict[str, str | None]) -> str:
    for script in scripts:
        path = Path(script)
        if not path.is_absolute():
            path = project_dir / path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?m)^\s*(import\s+arcpy\b|from\s+arcpy\b)", text):
            return config["arcpy_python"] or os.environ.get("ARCGIS_PYTHON") or "python"
    return config["default_python"] or sys.executable


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    if not project_dir.is_dir():
        raise SystemExit(f"Project directory does not exist: {project_dir}")
    date = args.date or dt.datetime.now().astimezone().strftime("%Y%m%d")
    try:
        dt.datetime.strptime(date, "%Y%m%d")
    except ValueError as exc:
        raise SystemExit("--date must use a valid YYYYMMDD calendar date") from exc
    config = load_config(args.config)
    runtime = args.runtime or infer_runtime(project_dir, args.script, config)
    workflow = workflow_path(project_dir, date)
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    text = f"""# {project_dir.name} reproducible workflow

Keep this file concise: short sentences, paths, commands, parameters, and QA results only.

## Project purpose and final result

Purpose: {args.purpose}

Final result: [replace with observed final output/status]

## Working directory and run time

- Working directory: `{project_dir}`
- Latest run: `{now}`

## Inputs and prerequisites

{bullets(args.input, "[input path/source + required structure/prerequisite]")}

## Outputs and overwrite behavior

{bullets(args.output, "[output path + format + overwrite rule]")}

## Complete processing sequence

1. [minimal actual sequence; no chat transcript]

## Language, runtime, and dependencies

- Language: `{args.language}`
- Runtime: `{runtime}`
- Dependencies: [names and versions required to rerun]

## Scripts, parameters, and rules

- Scripts/functions: [scripts and entry points used]
- Parameters/thresholds/mappings/CRS/naming rules: [rerun-critical values only]

## Exact commands

{bullets(args.command, "[exact command with absolute paths where needed]")}

## Validation and QA results

- [check + observed result + pass/fail]

## Limitations, recovery, and rerun

- Known limitations: [only limitations affecting reuse]
- Failure recovery: [how to recover without chat history]
- Rerun instructions: [exact shortest rerun path]

## Current workflow state

- Latest complete run: `{now}`
- This file is the current reproducible version. Replace obsolete content instead of appending dated change logs.
"""
    workflow.write_text(text, encoding="utf-8")
    print(workflow)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
