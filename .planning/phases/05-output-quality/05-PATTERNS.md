# Phase 5 — Pattern Map (output quality)

**Generated:** 2026-04-23 — 轻量对照，供执行期对齐风格。

| 新/改文件 | 角色 | 最近类比 |
|-----------|------|----------|
| `text_clean.py` | 纯函数、无 I/O | `url_input.py`、`bqg_api.py` 中的纯逻辑 |
| `novel_downloader.py` | 编排、调用清洗 | 现有 `get_chapter_content` 分支、`run()` 写盘 |
| `tests/test_text_clean.py` | 无网单测 | `tests/test_bqg_api.py` |

**集成点:** `NovelDownloader.get_chapter_content` 在返回字符串前；`run()` 控制首章前是否多 `\n`（见 PLAN 任务）。
