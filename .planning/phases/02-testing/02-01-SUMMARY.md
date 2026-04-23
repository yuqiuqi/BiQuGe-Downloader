---
phase: 02-testing
plan: "02-01"
subsystem: testing
tags: [pytest, url_input, TDD]

requires: [Phase 1]
provides:
  - `requirements-dev.txt`（pytest）
  - `url_input.py` 与 `normalize_target_url` 纯函数
  - `tests/test_url_input.py` 无网用例
  - 根 `pyproject.toml` 中 `[tool.pytest.ini_options]`（`testpaths`、`pythonpath`）
affects: [02-02-PLAN, 02-03-PLAN]

tech-stack:
  added: [requirements-dev.txt, url_input.py, tests/test_url_input.py, pyproject.toml]
  patterns: [入口归一化逻辑与 CLI 可测分离]

key-files:
  created:
    - requirements-dev.txt
    - url_input.py
    - tests/test_url_input.py
    - pyproject.toml
  modified:
    - novel_downloader.py

key-decisions:
  - 测试不 `import novel_downloader`，避免自举/顶置 pip
  - 用 `pythonpath = ["."]` 使根目录模块可被 pytest 发现

patterns-established:
  - `normalize_target_url` 为 strip 后非空字符串的归一化

requirements-completed: [TEST-02]

duration: 15min
completed: 2026-04-23
---

# Phase 2：02-01 Summary

**pytest 基线、`url_input` 单测与入口接入。**

## Performance

- **Duration:** ~15 min
- **Files:** 4 created, 1 modified

## Accomplishments

- `requirements-dev.txt` 声明 pytest
- `url_input.normalize_target_url` 与 `NovelDownloader` 入口行为对齐
- `tests/test_url_input.py` 四组 parametrize 用例；`pytest` 在仓库根退出 0
- `pyproject.toml` 配置 `testpaths` 与 `pythonpath`

## Deviations from Plan

- 在根目录增加最简 `pyproject.toml`（仅 `[project]` 元数据 + `tool.pytest`），非「可选样例 HTML fixture」路线；fixture 未引入。
