# reproducible-project-runner

[![Tests](https://github.com/nide486bqb-code/reproducible-project-runner/actions/workflows/test.yml/badge.svg)](https://github.com/nide486bqb-code/reproducible-project-runner/actions/workflows/test.yml)
[![Release](https://img.shields.io/github/v/release/nide486bqb-code/reproducible-project-runner)](https://github.com/nide486bqb-code/reproducible-project-runner/releases)

Agent-neutral instructions and standard-library tools for running, rerunning, validating, and documenting local projects without relying on chat history.

## When to use

Use this skill when an agent must:

- run or rerun a user-supplied project directory;
- overwrite or export project outputs with explicit behavior;
- select and record the actual runtime;
- create or refresh one current `WORKFLOW.md` record;
- audit a workflow before claiming completion.

It covers Python, ArcPy, R, JavaScript, PowerShell, Google Earth Engine, GIS, figures, and mixed-language projects. Optional domain skills are not required.

## Quick start

Clone the repository into a skill directory supported by your Agent:

```powershell
git clone https://github.com/nide486bqb-code/reproducible-project-runner.git `
  "$env:USERPROFILE\.codex\skills\reproducible-project-runner"
```

Run the generator directly from the repository:

```powershell
python scripts/create_workflow.py `
  --project-dir "C:\path\to\project" `
  --purpose "Describe the run" `
  --language Python `
  --runtime "C:\path\to\python.exe" `
  --script "C:\path\to\project\run.py" `
  --command "python C:\path\to\project\run.py" `
  --input "C:\path\to\input" `
  --output "C:\path\to\output"
```

Complete the observed result and QA fields, then audit:

```powershell
python scripts/audit_workflow.py `
  "C:\path\to\project\20261018_project_WORKFLOW.md"
```

## Runtime configuration

The release does not contain maintainer-specific paths.

- `--runtime` is authoritative for a single run.
- `--config` accepts `default_python` and `arcpy_python`.
- `ARCGIS_PYTHON` can provide an ArcPy interpreter.
- Ordinary Python defaults to the interpreter running the generator.
- ArcPy without configuration falls back to `python`; use an explicit ArcGIS Pro interpreter for a reproducible record.

Example configuration:

```json
{
  "default_python": null,
  "arcpy_python": null
}
```

## What it verifies

`audit_workflow.py` checks required sections, working/input/output paths, runtime, commands, processing parameters, QA results, overwrite behavior, unresolved placeholders, and chat-background leakage. It supports Windows, Unix, UNC, relative, and legacy workflow records.

## Common gotchas

- The generator creates placeholders intentionally; replace them with observed values before auditing.
- An ArcPy workflow is not executed by this skill unless ArcGIS Pro is installed and selected through `--runtime`, `--config`, or `ARCGIS_PYTHON`.
- The skill records workflow facts; it does not infer missing input/output paths or invent QA results.
- Keep project-specific `WORKFLOW.md` files in the project. Do not commit generated records to this repository.

## Repository layout

```text
SKILL.md
README.md
scripts/
  create_workflow.py
  audit_workflow.py
references/
  workflow-schema.md
adapters/
  codex/agents/openai.yaml
  generic/AGENT_INSTRUCTIONS.md
config/runtime-config.example.json
tests/test_smoke.py
```

## Related conventions

This repository follows the common Agent Skills pattern of a frontmatter-based `SKILL.md` plus a human-facing `README.md`. See [Vercel Agent Skills](https://github.com/vercel-labs/skills), [Skill Anatomy](https://github.com/ravidsrk/agent-skills/blob/main/docs/skill-anatomy.md), and [the Agent Skills specification](https://agentskills.io/specification).

## License

MIT. See [LICENSE](LICENSE).
