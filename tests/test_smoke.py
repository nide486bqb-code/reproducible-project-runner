import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CREATE = ROOT / "scripts" / "create_workflow.py"
AUDIT = ROOT / "scripts" / "audit_workflow.py"


class WorkflowToolSmokeTest(unittest.TestCase):
    def test_create_and_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "demo"
            project.mkdir()
            script = project / "run.py"
            script.write_text("print('ok')\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(CREATE),
                    "--project-dir",
                    str(project),
                    "--purpose",
                    "smoke test",
                    "--language",
                    "Python",
                    "--runtime",
                    sys.executable,
                    "--script",
                    str(script),
                    "--command",
                    f"{sys.executable} {script}",
                    "--input",
                    str(script),
                    "--output",
                    str(project / "out.txt"),
                    "--date",
                    "20261018",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            workflow = Path(result.stdout.strip())
            self.assertTrue(workflow.is_file())
            text = workflow.read_text(encoding="utf-8")
            replacements = {
                "[replace with observed final output/status]": "out.txt created",
                "[input path/source + required structure/prerequisite]": "run.py exists",
                "[output path + format + overwrite rule]": "out.txt; overwrite allowed",
                "[minimal actual sequence; no chat transcript]": "run.py executed",
                "[names and versions required to rerun]": "Python runtime",
                "[scripts and entry points used]": "run.py",
                "[rerun-critical values only]": "none",
                "[exact command with absolute paths where needed]": f"{sys.executable} run.py",
                "[check + observed result + pass/fail]": "audit pass; pass",
                "[only limitations affecting reuse]": "none",
                "[how to recover without chat history]": "rerun command",
                "[exact shortest rerun path]": "rerun command",
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            workflow.write_text(text, encoding="utf-8")
            audited = subprocess.run(
                [sys.executable, str(AUDIT), str(workflow)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(audited.returncode, 0, audited.stdout + audited.stderr)

    def test_config_is_json(self):
        config = ROOT / "config" / "runtime-config.example.json"
        self.assertIsInstance(json.loads(config.read_text(encoding="utf-8")), dict)


if __name__ == "__main__":
    unittest.main()
