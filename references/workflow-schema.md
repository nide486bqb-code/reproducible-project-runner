# Workflow record schema

## Required sections

1. Project purpose and final result
2. Exact working directory and run time
3. Inputs, source paths, expected structure, and prerequisites
4. Outputs, formats, paths, and overwrite behavior
5. Complete processing sequence
6. Programming language, version, exact runtime, and dependencies
7. Scripts, key functions, parameters, thresholds, mappings, CRS, and naming rules
8. Exact commands used
9. Validation and QA checks with observed results
10. Known limitations, recovery, and rerun instructions
11. Current workflow state

## Acceptance criteria

- A new operator can rerun the project without chat history.
- Commands use absolute paths where ambiguity is possible.
- Values are observed, not guessed.
- Inputs and outputs are individually identifiable.
- QA contains results, not only planned checks.
- The record includes working directory, input paths, output paths, runtime/interpreter, commands, parameters or processing rules, QA results, and overwrite behavior.
- The record is a single current version by default, updated in place instead of accumulating dated versions or timestamped change logs.
- No credentials or secrets are present.
- The record is concise: short sentences, paths, commands, parameters, QA results, no chat transcript, no repeated background, and no generic advice unrelated to rerun, validation, recovery, or final outputs.

## Recommended run manifest shape

```json
{
  "schema_version": "1.0",
  "project": {},
  "run": {},
  "runtime": {},
  "inputs": [],
  "outputs": [],
  "parameters": {},
  "validation": [],
  "recovery": {},
  "notes": []
}
```
