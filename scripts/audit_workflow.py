#!/usr/bin/env python3
"""Audit a workflow Markdown file for reproducibility facts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = {
    "purpose/result": r"(?im)^## .*?(purpose|目的|result|结果)",
    "working directory/time": r"(?im)^## .*?(working directory|工作目录|run time|运行时间)",
    "inputs": r"(?im)^## .*?(inputs?|输入)",
    "outputs": r"(?im)^## .*?(outputs?|输出)",
    "processing sequence": r"(?im)^## .*?(processing|sequence|流程|处理)",
    "runtime/dependencies": r"(?im)^## .*?(runtime|dependencies|环境|依赖|语言|解释器)",
    "commands": r"(?im)^## .*?(commands?|命令)",
    "validation/QA": r"(?im)^## .*?(validation|QA|质检|验证|检查)",
    "recovery/rerun": r"(?im)^## .*?(recovery|rerun|恢复|复跑|重跑)",
    "current state": r"(?im)^## .*?(current workflow state|current state|当前状态|运行记录)",
}

REQUIRED_FACTS = {
    "working directory path": r"(?is)(工作目录|working directory).{0,160}(?:[A-Z]:[\\/]|/|\\\\|\.\.?[\\/])",
    "input path/list": r"(?is)(输入|input).{0,200}(?:[A-Z]:[\\/]|/|\\\\|\.\.?[\\/]|\bnone\b|无输入)",
    "output path/list": r"(?is)(输出|output).{0,200}(?:[A-Z]:[\\/]|/|\\\\|\.\.?[\\/]|\bnone\b|无输出)",
    "runtime/interpreter": r"(?i)(解释器|runtime|python|Rscript|node|ArcGIS|ArcPy)",
    "command": r"(?i)(& .+|\bpython(?:\.exe|3)?\s|Rscript\.exe|node\s|powershell|命令)",
    "parameters or processing": r"(?i)(参数|parameter|threshold|CRS|分辨率|年份|处理|流程)",
    "QA result": r"(?is)(QA|质检|验证|检查).{0,160}(通过|pass|存在|可打开|一致|完成|exit code 0|0)",
    "overwrite behavior": r"(?i)(覆盖|overwrite|未覆盖|not overwrite|refresh|刷新)",
}

PLACEHOLDERS = (
    "[record",
    "[replace",
    "TODO",
    "待补充",
    "待填写",
    "<project",
    "<input",
    "<output",
    "<command",
)

TOO_MUCH_BACKGROUND = (
    "聊天记录",
    "根据对话",
    "用户要求我",
    "本次对话",
)


def missing_items(patterns: dict[str, str], text: str) -> list[str]:
    return [name for name, pattern in patterns.items() if not re.search(pattern, text)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow", help="Path to *_WORKFLOW.md")
    parser.add_argument("--facts-only", action="store_true", help="Skip section heading checks")
    args = parser.parse_args()

    path = Path(args.workflow)
    if not path.is_file():
        print(f"Workflow not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    missing_sections = [] if args.facts_only else missing_items(REQUIRED_SECTIONS, text)
    missing_facts = missing_items(REQUIRED_FACTS, text)
    placeholders = [item for item in PLACEHOLDERS if item.lower() in text.lower()]
    background = [item for item in TOO_MUCH_BACKGROUND if item in text]

    if missing_sections:
        print("Missing sections: " + ", ".join(missing_sections))
    if missing_facts:
        print("Missing facts: " + ", ".join(missing_facts))
    if placeholders:
        print("Unresolved placeholders: " + ", ".join(placeholders))
    if background:
        print("Likely background/chat text: " + ", ".join(background))

    if missing_sections or missing_facts or placeholders or background:
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
