# Phase 8 — Pattern Map

| 区域 | 既有模式 | Phase 8 增量 |
|------|-----------|----------------|
| 正文清洗 | `text_clean.clean_chapter_text` 单入口；`_normalize_newlines` → 行内 `_INLINE_NOISE` → 行滤 → 压空行 | 在 norm 之后插入 **U+FEFF 剥离**；扩展行内表 **jqxs⊙/gctxt点cc** 族 |
| 测试 | `tests/test_text_clean.py` 仅 `import text_clean` | 追加 FEFF、raw+FEFF、新水印、防误伤 |
| 文档 | `README` 清洗 + raw 段 | 补 **一句**：raw 仍去 FEFF/换行统一 |

**集成点:** `novel_downloader.NovelDownloader._finalize_chapter_text` 不变更职责，仅消费新 `clean_chapter_text` 行为。
