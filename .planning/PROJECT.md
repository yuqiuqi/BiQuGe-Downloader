# BiQuGe Downloader（笔趣阁类小说下载器）

## What This Is

基于 Python 的**命令行小说下载工具**：从笔趣阁结构站点拉取章节目录与正文，多线程获取后合并为单份 UTF-8 文本；支持书号/URL 启动、可选 apibi 书库、HTML 回退、**可配置并发**（`--workers` / `BQUGE_MAX_WORKERS`），以及**正文类水印/噪音清洗**（`text_clean`）与 **raw 模式**；支持 GitHub Actions 产出 Artifact。面向自用与学习场景。详见 `README.md`。

## Core Value

**稳定、可复现**地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI。

## Current state（after v1.4）

- **v1.3（SHIPPED）:** CLEAN-03、CFG-01 — 见 `MILESTONES.md`、**`milestones/v1.3-ROADMAP.md`**。  
- **v1.4（SHIPPED 2026-04-24）:** E2E-01/02、Phase 13 — **`milestones/v1.4-ROADMAP.md`**；实证 **`13-e2e-html/E2E-2026-04-24.md`**；Git tag **`v1.4`**。  

## Next milestone goals

- 由 **`/gsd-new-milestone`** 定义（需求与 ROADMAP 将写入新的 `REQUIREMENTS.md` / `ROADMAP.md` 活动段）。  
- 暂缓大项仍见 **`REQUIREMENTS.md`** 的 CFG-02、SITE-01 等。  

## Requirements

### Validated

- v1.0–v1.2 与里程碑摘要 — 见 `MILESTONES.md`  
- ✓ **CLEAN-03, CFG-01** — v1.3（`milestones/v1.3-REQUIREMENTS.md`）  
- ✓ **E2E-01, E2E-02** — v1.4 Phase 13（`milestones/v1.4-REQUIREMENTS.md`，实证见 `13-SUMMARY` / `E2E-2026-04-24`）  

### Active

- 无（待 **`/gsd-new-milestone`**）  

### Out of Scope

- 大规模 GUI、账号登录/Cookie 管理、付费墙或验证码破解 — 非本仓库核心。  
- 将产出用于商业传播 — README 已声明学习交流用途。  

## Context

- **棕地项目:** 见 `.planning/codebase/` 下 `ARCHITECTURE.md`、`CONCERNS.md` 等。  
- **GSD:** 规划产物在 `.planning/`。  

## Constraints

- **Python:** README 为 3.6+，CI 使用 3.10。  
- **合规:** 不扩展明显规避版权或站点条款的能力。  

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|--------|
| v1.4 以 E2E 一书双路径为轴心 | 补全 apibi 与 HTML 可观测差异 | ✓ 见 v1.4 归档与 E2E 文档 |
| 不重置阶段号 | 与历史 11+ 一致 | Phase 14+ 接档 |

## Evolution

在里程碑收束时做了全文件评审。  

**After each milestone** (`/gsd-complete-milestone`): 全节审视、Core Value、Out of Scope、Context。  

---

*Last updated: 2026-04-24 after v1.4 milestone close*  
