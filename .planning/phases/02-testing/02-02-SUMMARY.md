---
phase: 02-testing
plan: "02-02"
subsystem: docs
tags: [readme, dev]

requires: [02-01]
provides:
  - README「开发（运行测试）」段落
affects: []

tech-stack:
  added: []
  patterns: [venv + 双 requirements 安装后 pytest]

key-files:
  created: []
  modified: [README.md]

key-decisions:
  - 文档中同时列出 `pip install -r requirements.txt -r requirements-dev.txt`

requirements-completed: [TEST-01]

duration: 5min
completed: 2026-04-23
---

# Phase 2：02-02 Summary

**README 补充本地运行测试说明。**

## Accomplishments

- 新增「开发（运行测试）」：venv、双文件 pip、`pytest` / `pytest -q`

## Deviations from Plan

- pytest 的 `testpaths`/`pythonpath` 已在 02-01 落于 `pyproject.toml`，本计划未再重复新增文件。
