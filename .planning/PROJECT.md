# BiQuGe Downloader（笔趣阁类小说下载器）

## What This Is

基于 Python 的**命令行小说下载工具**：从笔趣阁结构站点拉取章节目录与正文，多线程获取后合并为单份 UTF-8 文本；支持书号/URL 启动、可选 apibi 书库、HTML 回退、**可配置并发**（`--workers` / `BQUGE_MAX_WORKERS`），以及**正文类水印/噪音清洗**（`text_clean`）与 **raw 模式**；支持 GitHub Actions 产出 Artifact。面向自用与学习场景。详见 `README.md`。

## Core Value

**稳定、可复现**地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI。

## Shipped: v1.3（摘要）

- **CLEAN-03、CFG-01** 已随 v1.3 发布；计划追溯见 `MILESTONES.md` 与 `.planning/milestones/v1.3-ROADMAP.md`。

## Current Milestone: v1.4 — HTML 回退路径 E2E 与可复现记录

**Status:** **Phase 13 已执行**（`13-SUMMARY.md`；结论文档 `E2E-2026-04-24.md`）。**一书（书号 3953）**在 **apibi** 与 **仅 HTML 目录** 下的章数/元数据**差异**已记录；README 已加「路径对照（E2E，v1.4）」入口。  

**Target features / 结果:**

- **E2E-01/02** — 见 `REQUIREMENTS.md`（已勾选）与 `13-e2e-html/` 下 E2E、RUN-RECORD。  
- 可选：对结论文档做 **tag/Release** 或 **complete-milestone** 归档。  

## Requirements

### Validated

- v1.0–v1.3 中已标 Complete 的条目 — 见 `MILESTONES.md` 与各 `*-SUMMARY.md` 及 `milestones/v1.3-REQUIREMENTS.md`。  
- ✓ **E2E-01 / E2E-02** — v1.4 Phase 13（`13-SUMMARY.md` / `E2E-2026-04-24.md`）  

### Active (下一里程碑)

- 由 **`/gsd-new-milestone`** 或 **`REQUIREMENTS.md` 重置后** 定义。  

### Out of Scope

- 大规模 GUI、账号登录/Cookie 管理、付费墙或验证码破解 — 非本仓库核心。  
- 将产出用于商业传播 — README 已声明学习交流用途。  
- 全自动、无人工值守的**联网 E2E CI** — 本里程碑不强制。  

## Context

- **棕地项目:** 架构与关注见 `.planning/codebase/` 下 `ARCHITECTURE.md`、`CONCERNS.md` 等。  
- **GSD:** 规划产物在 `.planning/`。  

## Constraints

- **Python:** README 为 3.6+，CI 使用 3.10。  
- **合规:** 不扩展明显规避版权或站点条款的能力。  
- **网络/站点:** 对照实验在用户可控网络下执行；不假设站点 24/7 可用。  

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|--------|
| v1.4 以 E2E-01 为轴心 | v1.3 已刻意推迟可选 E2E | ✓ Phase 13 已收束 |
| 不重置阶段编号，接续 Phase 13 | 与 ROADMAP 已公布编号一致 | 本里程碑使用 **13-01 / 13-02** 计划名 |

## Evolution

本文件在阶段转换与里程碑边界会更新。

**After each phase transition** (via `/gsd-transition`):

1. Requirements invalidated? → Move to Out of Scope with reason  
2. Requirements validated? → Move to Validated with phase reference  
3. New requirements emerged? → Add to Active  
4. Decisions to log? → Add to Key Decisions  
5. "What This Is" still accurate? → Update if drifted  

**After each milestone** (via `/gsd-complete-milestone`):

1. Full review of all sections  
2. Core Value check  
3. Audit Out of Scope  
4. Update Context with current state  

---

*Last updated: 2026-04-24 — Phase 13 execute 完成*  
