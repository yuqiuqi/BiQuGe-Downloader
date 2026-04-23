# BiQuGe Downloader（笔趣阁类小说下载器）

## What This Is

基于 Python 的**命令行小说下载工具**：从笔趣阁结构站点拉取章节目录与正文，多线程获取后合并为单份 UTF-8 文本；支持书号/URL 启动、可选 apibi 书库、HTML 回退、**可配置并发**（`--workers` / `BQUGE_MAX_WORKERS`），以及**正文类水印/噪音清洗**（`text_clean`）与 **raw 模式**；支持 GitHub Actions 产出 Artifact。面向自用与学习场景。详见 `README.md`。

## Core Value

**稳定、可复现**地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI。

## Current state (after v1.3)

- **已发布里程碑:** **v1.3**（2026-04-24）— *类水印清洗二期*（CLEAN-03）+ *可配置并发*（CFG-01）。详见 `MILESTONES.md`、**`milestones/v1.3-ROADMAP.md`**。  
- **技术要点:** 默认 10 线程与旧版一致；`text_clean` 在 Phase 8/11 规则与单测上可回归；根目录 `pytest` 为工程门禁。  
- **未纳入 v1.3 必做项:** 原 **E2E-01**（HTML 回退一书对照）仍为候选，见 **`REQUIREMENTS.md`** 与 `ROADMAP` Phase 13。  

## Next milestone goals（待 /gsd-new-milestone 正式命名）

- 选择是否以 **Phase 13 / E2E-01** 为下一版核心，或转向维护/新主题。  
- 视需要补跑或关闭 **`11-UAT.md`** 等半成品流程文档。  

## Requirements

### Validated

- v1.0–v1.2 基线、清洗与可维护性主线的历史需求 — 见 `MILESTONES.md` 与各阶段 `*-SUMMARY.md`  
- ✓ **CLEAN-03** — v1.3 Phase 11（`11-SUMMARY.md`）  
- ✓ **CFG-01** — v1.3 Phase 12（`12-SUMMARY.md`）  

### Active (post–v1.3; 待新里程碑定稿)

- 见 **`.planning/REQUIREMENTS.md`** 当前候选项（如 E2E-01）  

### Out of Scope

- 大规模 GUI、账号登录/Cookie 管理、付费墙或验证码破解 — 非本仓库核心  
- 自动发现「哪个镜像可用」的服务化运营 — 超出维护型工具  
- 将产出用于商业传播 — README 已声明学习交流用途  

## Context

- **棕地项目:** 架构与关注见 `.planning/codebase/` 下 `ARCHITECTURE.md`、`CONCERNS.md` 等。  
- **GSD:** 规划产物在 `.planning/`；`commit_docs` 以仓库策略为准。  

## Constraints

- **Python:** README 为 3.6+，CI 使用 3.10；新变更避免无故抬高下限。  
- **合规:** 仅技术维护；不扩展明显规避版权或站点条款的能力。  

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|--------|
| 清洗二期以盘点 + 单测加固为主、无新子串不硬加规则 | 降低误伤与维护成本 | ✓ v1.3 收束见 `11-INVENTORY` |
| 并发可配时保持默认 10 线程 | 与既有行为/CI 一致，便于 bisect | ✓ v1.3 收束见 `12-SUMMARY` |
| 可选 E2E 不阻塞 v1.3 打 tag | 必做/可选分轨 | ✓ 见 `MILESTONES` |

## Evolution

在里程碑收束时做了全文件评审（`PROJECT.md` 与 `MILESTONES` / `REQUIREMENTS` 归档对齐）。

---

*Last updated: 2026-04-24 after v1.3 milestone close*  
