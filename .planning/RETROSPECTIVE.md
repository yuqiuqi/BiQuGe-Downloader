# Retrospective: BiQuGe Downloader

## Milestone: v1.3 — 类水印残留与清洗·二期

**Shipped:** 2026-04-24  
**Phases:** 11–12（必做）| **Plans:** 11-01+11-02 + 12 单次落实  

### What was built

- Phase 11: 盘点 + 变体单测 + 文档/注释，无无据扩大 `text_clean` 正则。  
- Phase 12: 可配置并发，默认 10 与历史一致；CLI 与 `BQUGE_MAX_WORKERS`。  

### What worked

- 先 INVENTORY 再实现的顺序降低了「拍脑袋新规则」风险。  
- 单元测试为 CLI 与 env 提供快速回归。  

### What was inefficient / gaps

- `gsd-tools` 本机 `audit-open` / `milestone complete` 与仓库内版本不同步，里程碑收尾部分步骤改手工完成。  
- 完整对话式 UAT 未跑完，依赖 SUMMARY + pytest。  

### Key lessons

- 对棕地工具，**保持默认行为不变**是并发类改动的可合并前提。  
- 可选 Phase（E2E-01）与必做分轨，避免阻塞发布。  

---

## Cross-Milestone Trends

| Milestone | Focus | Phases in scope (high level) |
|-----------|--------|------------------------------|
| v1.3 | 清洗二期 + 并发可配 | 11, 12 |

*Append new rows when additional milestones close.*  
