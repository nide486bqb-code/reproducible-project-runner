---
name: reproducible-project-runner
description: Run, rerun, validate, and document local projects reproducibly across Python, ArcPy, R, JavaScript, PowerShell, Google Earth Engine, GIS, figures, and mixed-language workflows. Use when an agent works in a user-supplied project directory, executes or overwrites outputs, records commands and environments, creates a run manifest, or must leave a current WORKFLOW.md file that can be reused without chat history.
license: MIT
compatibility: Requires Python 3.9 or newer for the bundled scripts; ArcPy is optional and must be supplied by the host environment.
metadata:
  version: "0.1.2"
---

# Project Runner Workflow

Run from the exact project directory supplied by the user. Keep the project's top-level directory unchanged.

## Portable defaults

- Do not infer or switch the project directory. Ask for it when it is required and missing.
- Use the host's native shell and quote paths containing spaces.
- Record the exact runtime used. Pass `--runtime` when the runtime is not the current interpreter.
- For ArcPy, configure `--runtime` or `ARCGIS_PYTHON`; do not assume a fixed ArcGIS Pro installation path.
- Use the smallest project-local helper or run script. Avoid new dependencies unless required.
- If a referenced optional skill is unavailable, continue with this workflow and state the limitation.

## Required sequence

1. Confirm the exact working directory and intended outputs.
2. Inspect inputs, scripts, dependencies, existing outputs, and prior workflow records.
3. Select and record the runtime from actual dependencies.
4. Perform a lightweight syntax, import, or input check before expensive execution.
5. Run with explicit commands and capture exit status, timestamps, parameters, and logs.
6. Validate outputs in proportion to risk: existence, dimensions or row counts, formats, metadata, value ranges, and visual layout when applicable.
7. Create or update the project's single current workflow record after a successful run, overwrite, export, or rerun-relevant script change.
8. Audit the record with `scripts/audit_workflow.py` before reporting completion.

## Workflow record

Use one current workflow per project. If a matching `*_<project-folder>_WORKFLOW.md` exists, update it in place. Otherwise create `YYYYMMDD_<project-folder>_WORKFLOW.md`.

Use `scripts/create_workflow.py` as a deterministic starting point. It accepts `--config` for local runtime defaults and `--runtime` for an explicit runtime. Read `references/workflow-schema.md` for required content.

Keep the record concise: paths, commands, parameters, observed QA results, overwrite behavior, recovery, and rerun instructions. Do not store chat history or secrets.

## Run manifest

For substantial runs, create `run_manifest.json` beside the workflow record with project identity, timestamps, exit status, exact runtime and command, input/output metadata, dependency versions, validation results, overwrite behavior, and recovery instructions. Never store passwords, tokens, cookies, or private credentials.

## Optional capabilities

Use a map, document, spreadsheet, modeling, or visualization skill only when it is installed and materially needed. The core workflow remains usable without those optional skills.

