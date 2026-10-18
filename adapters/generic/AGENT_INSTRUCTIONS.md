# Generic Agent Adapter

This bundle does not require a particular agent product. When the user asks to run, rerun, overwrite, validate, or document a local project:

1. Read `SKILL.md`.
2. Confirm the exact project directory and intended outputs.
3. Follow the required sequence in that file.
4. Use `scripts/create_workflow.py` and `scripts/audit_workflow.py`.
5. Treat unavailable optional skills as unavailable capabilities, not as blockers.
6. Do not claim completion until the workflow record contains observed QA results and the audit passes.

This file can be placed in the target agent's project instruction file or included in its prompt. It is not an automatic plugin manifest.

