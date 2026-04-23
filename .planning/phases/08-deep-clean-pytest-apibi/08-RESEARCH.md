# Phase 8 — Research（合并说明）

**状态:** 本仓库为棕地实现；Phase 8 需求已在 `08-CONTEXT.md`、`.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` 与现有 `text_clean.py` 中可验证，**未**单独跑 `gsd-phase-researcher`。

**结论（给 planner/executor）：**

- U+FEFF：源站/apibi 在 `txt` 前附加的噪声字节，**全串 `replace("\ufeff", "")`** 足够，与 Python 3 `str` 模型一致。  
- 水印：`jqxs`/`gctxt` 为固定推广族，适合与现有 `_INLINE_NOISE` 同一数据驱动表，用单测锁回归。  

**无需外网或新依赖。**

---

*Phase 8 — 2026-04-23*  
