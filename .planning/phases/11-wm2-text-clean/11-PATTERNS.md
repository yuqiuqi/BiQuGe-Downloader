# Phase 11 — Pattern Map（类水印二期）

| 角色 | 文件 | 类比 |
|------|------|------|
| 清洗主逻辑 | `text_clean.py` | 同 Phase `08-01/08-02` 对 `text_clean` 的改法：扩展元组/小函数，不动下载器主流程 |
| 单测 | `tests/test_text_clean.py` | 与 Phase 8 相同：`pytest`、无 `novel_downloader` import |
| 调用方（只读） | `novel_downloader.py` → `_finalize_chapter_text` | 本阶段**默认不改**；若改签名需单独任务与全仓测 |

**数据流:** 章节 HTML/API 字符串 → `clean_chapter_text` → 换行/FEFF/（非 raw）行内 sub → 行滤 → 空行压缩。
