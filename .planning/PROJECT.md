# BiQuGe Downloader（笔趣阁类小说下载器）

## What This Is

基于 Python 的**命令行小说下载工具**：从笔趣阁结构站点拉取章节目录与正文，多线程获取后合并为单份 UTF-8 文本；支持通过小说 ID 或完整 URL 启动，并可用 GitHub Actions 在云端跑同一脚本产出 Artifact。面向自用与学习场景，不替代正版阅读。详见仓库 `README.md`。

## Core Value

**稳定、可复现地**从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地（或 CI Artifact）。

## Current Milestone: v1.3 类水印残留与清洗二期

**Goal:** 在 v1.2 已交付的 `text_clean` 深化（Phase 8）与可维护性（Phase 9）之上，针对**成书全文仍可见的类水印/推广行/源站固定噪音**，做**可测、可回归**的二期规则与单测；并收尾 v1.2 未完成的**可配置并发（CFG-01）**与可选的 **E2E-01**。

**Target features:**

- **类水印/残留行二期（CLEAN-03 等）：** 以复现样例 + 黄金/合成用例为锚，扩展或调整 `text_clean`（及必要时的调用链），减少「像水印的」行**误留**、控制**误伤**合法叙述（边界以单测锁定）  
- **可配置并发（CFG-01）：** CLI/环境变量可设 `max_workers`（或等效名），与 README / `--help` 一致，默认与当前 10 线程行为兼容或显式说明  
- **（可选）E2E-01：** 至少一书 HTML 回退路径抽样/记录，与 apibi/默认路径对照

**前序里程碑 (v1.2) 摘要:** Phase 8（CLEAN-01/02）与 Phase 9（MAIN-01/02）已落地；**Phase 10（CFG-01）** 未在 v1.2 内交付，**并入 v1.3**。详见 `MILESTONES.md`。

**Previous (v1.1 / v1.0):** 见 `MILESTONES.md` 与 v1.1 关闭注记。

## Requirements

### Validated（历史）

- 多线程、URL/书号、清洗与落盘、CI、apibi/HTML 等 — 见上文各里程碑

### Active (v1.3)

- [ ] **CLEAN-03**: 在现有 `text_clean` 与 CLEAN-01/02 之外，**消除或弱化**用户/抽测中仍可见的**类水印、行内/整行推广噪音**；每条规则需有**可运行单测**或黄金字符串，并明确 **raw 模式** 行为  
- [ ] **CFG-01**: 并发线程数可经 CLI/环境变量配置，文档与默认值/边界说明完整  
- [ ] **E2E-01**（可选）: HTML 回退路径一书对照记录  

### Out of Scope

- 大规模 GUI、账号登录/Cookie 管理、付费墙或验证码破解 — 非本仓库核心
- 自动发现「哪个镜像可用」的爬虫服务化运营 — 超出维护型里程碑
- 将产出用于商业传播 — README 已声明学习交流用途

## Context

- **棕地项目：** 代码与意图见 `.planning/codebase/ARCHITECTURE.md`、`STRUCTURE.md`、`CONCERNS.md`；技术栈见 `STACK.md`。
- **GSD 目标:** 在保留现有能力的前提下，提升可测性、可配置性与工程卫生，使后续改版成本可控。

## Constraints

- **Python：** README 为 3.6+，CI 使用 3.10；新变更应避免无故抬高下限。
- **合规与版权:** 仅技术维护；不扩展为明显规避版权或站点条款的功能。
- **单仓库:** 无 monorepo；规划产物在 `.planning/`（见 `config.json` 中 `commit_docs`）。

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|--------|
| 本里程碑以「工程化维护」为主，不重新定义产品为 Web 服务 | 与当前 CLI + Actions 形态一致，降低范围 | — Pending |
| v1.2 未关闭项（CFG-01 等）并入 v1.3，不平行维护两套 State | 用户以「仍见类水印」启新轮，与并发收尾可同程交付 | 2026-04-24 |
| 本轮不跑四代理领域预研 | 与既有 E2E/999.1 与 `text_clean` 上下文足够；需要时在 phase 内补 RESEARCH | 2026-04-24 |

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
2. Core Value check — still the right priority?  
3. Audit Out of Scope — reasons still valid?  
4. Update Context with current state  

---

*Last updated: 2026-04-24 — 新里程碑 v1.3（new-milestone）*  
