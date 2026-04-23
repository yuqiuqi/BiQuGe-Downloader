# Phase 12 — 执行摘要

**日期:** 2026-04-24  
**要求:** CFG-01  

## 交付

- **`novel_downloader.py`：** 抽取 `resolve_max_workers` / 环境 `BQUGE_MAX_WORKERS` / 上限 64 与提示；`NovelDownloader(..., max_workers=...)`；`run()` 使用解析结果。入口改为 `argparse`：`--raw-text`、`-j`/`--workers`、可省略 URL 时仍交互。  
- **`tests/test_novel_workers.py`：** 默认/环境/CLI 优先级、越界上限制、非法环境回退。  
- **`README.md`：** 新增「并发」段（默认 10、`-j`、环境变量、与旧版兼容说明）。  

## 验证

- `python3 -m py_compile novel_downloader.py`  
- `pytest`：36 passed  

## 未改

- GHA `manual_download.yml` 仍用默认 10 线程（不显式传参即与旧版一致）。  
