# Phase 11 — 执行摘要

**日期:** 2026-04-24  
**计划:** `11-01`（盘点）→ `11-02`（加固 + 文档）  

## 交付

- **`11-INVENTORY.md`：** 对照 `E2E-2026-04-23.md` 与 `text_clean` / 单测 的映射表；结论为 Phase 8 已覆盖 E2E 所列族，CLEAN-03 以**单测变体 + 注释/README 锚点**收束。  
- **`text_clean.py`：** 模块与 `clean_chapter_text` docstring 增加 Phase 11 / CLEAN-03 / `11-INVENTORY` 引用。  
- **`tests/test_text_clean.py`：** 新增 `test_jqxs_circle_cc_variants_removed`（parametrize）、`test_gctxt_with_ideographic_spaces`、`test_narrative_jqxs_token_in_dialogue_not_a_typical_watermark`。  
- **`README.md`：** 正文清洗节增加 v1.3 CLEAN-03 与 INVENTORY 链接一句。  

## 验证

- `python3 -m py_compile text_clean.py`  
- `pytest` 根目录：**29 passed**（本阶段 +5 用例）  

## 未做（按边界）

- 无新**行内/行级**正则（盘点显示无新必改子串）。  
- 未改 `novel_downloader` 清洗调用链。  
