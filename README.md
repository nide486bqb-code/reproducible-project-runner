# reproducible-project-runner

Agent-neutral workflow instructions and standard-library tools for running, rerunning, validating, and documenting local projects reproducibly.

## Included

- `SKILL.md`: instructions for an agent that supports skills or project rules.
- `references/workflow-schema.md`: required workflow sections and acceptance criteria.
- `scripts/create_workflow.py`: creates a current workflow record.
- `scripts/audit_workflow.py`: checks sections, facts, placeholders, and chat-background leakage.

## Runtime selection

The generator does not assume the maintainer's machine paths.

- `--runtime` is authoritative.
- `--config` can define `default_python` and `arcpy_python`.
- `ARCGIS_PYTHON` is used for ArcPy when no explicit runtime or config value is supplied.
- Ordinary Python defaults to the Python interpreter running the generator.
- ArcPy without configuration falls back to the command name `python`; pass an explicit ArcGIS Pro interpreter for reproducible records.

Example configuration:

```json
{
  "default_python": null,
  "arcpy_python": null
}
```

Create a record:

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

Audit the completed record:

```powershell
python scripts/audit_workflow.py "C:\path\to\project\20261018_project_WORKFLOW.md"
```

The generator intentionally leaves placeholders for observed results. Replace them before running the audit.

