# BiQuGe Downloader（笔趣阁类小说下载器）

## What This Is

基于 Python 的**命令行小说下载工具**：从笔趣阁结构站点拉取章节目录与正文，多线程获取后合并为单份 UTF-8 文本；支持通过小说 ID 或完整目录 URL 启动，并可用 GitHub Actions 在云端跑同一脚本产出 Artifact。面向自用与学习场景，不替代正版阅读。详见仓库 `README.md`。

## Core Value

**稳定、可复现地**从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地（或 CI Artifact）。

## Current Milestone: v1.1 输出质量与可维护性

**Goal:** 在保持现有下载与 CI 的前提下，让合并 TXT **少噪音、好排版**（源站广告/水印清洗），并补齐 **可维护性**（死代码/空目录诊断）与 **可配置并发**。

**Target features:**

- 正文与落盘前清洗/版式（含 UAT 记录的推广串与节首空行类问题，见 `.planning/phases/03-content-quality/03-UAT-DOWNLOAD-REPORT.md`）
- 清理或统一 `save_to_file` 与主写入路径；无章节时明确失败原因
- 并发线程数可通过参数或环境变量配置并文档化

**Previous milestone (v1.0) 摘要:** 见 `.planning/MILESTONES.md`（依赖/CI、pytest、apibi 等已交付）。

## Requirements

### Validated

- ✓ 多线程拉取章正文并按章节序写入单个 TXT（`novel_downloader.py`）— 已存在
- ✓ 支持纯数字书号补全为默认笔趣 URL、或完整 URL/补全 `https`（`novel_downloader.py` 入口）— 已存在
- ✓ 单章多页时跟随「下一页」合并（`get_chapter_content`）— 已存在
- ✓ 随机 User-Agent、Referer 与短随机延时等基础防爬头（`NovelDownloader.__init__` / `get_chapter_content`）— 已存在
- ✓ GitHub Actions 手动输入 ID/URL 并上传 `*.txt`（`.github/workflows/manual_download.yml`）— 已存在
- ✓ 根目录 `requirements.txt` 与 `manual_download` workflow、`README` 推荐安装路径一致（Phase 1）— 已验证
- ✓ 本地与 CI 可 `pytest`；`url_input.normalize_target_url` 有无网单测；workflow 中先 `test` 后 `download`（Phase 2）— 已验证

### Active (v1.1)

- [ ] **TXT/排版:** 可开关的正文去水印/尾注清洗与章首/文件头空白处理（UAT 结论）
- [ ] **MAIN-01/02:** 同 `REQUIREMENTS`/`ROADMAP` Phase 6
- [ ] **CFG-01:** 可配置 `max_workers` 与文档
- [ ] 在不大改产品形态的前提下，为清洗与解析层保留可测边界（pytest）

### Out of Scope

- 大规模 GUI、账号登录/Cookie 管理、付费墙或验证码破解 — 非本仓库核心
- 自动发现「哪个镜像可用」的爬虫服务化运营 — 超出维护型里程碑
- 将产出用于商业传播 — README 已声明学习交流用途

## Context

- **棕地项目：** 代码与意图见 `.planning/codebase/ARCHITECTURE.md`、`STRUCTURE.md`、`CONCERNS.md`；技术栈见 `STACK.md`。
- **GSD 目标：** 在保留现有能力的前提下，提升可测性、可配置性与工程卫生，使后续改版成本可控。
- 站点 HTML 与域名强耦合，改版时需改 `novel_downloader.py` 内选择器与正则 — 属已知风险，非本里程碑一次性消除项。

## Constraints

- **Python：** README 为 3.6+，CI 使用 3.10；新变更应避免无故抬高下限。
- **合规与版权：** 仅技术维护；不扩展为明显规避版权或站点条款的功能。
- **单仓库：** 无 monorepo；规划产物在 `.planning/`（见 `config.json` 中 `commit_docs`）。

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|--------|
| 本里程碑以「工程化维护」为主，不重新定义产品为 Web 服务 | 与当前 CLI + Actions 形态一致，降低范围 | — Pending |
| 初始化 GSD 时跳过「全库领域预研」四代理流程 | 加速拿到 ROADMAP；后续可按阶段用 research 工作流补 | — Pending |

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

*Last updated: 2026-04-23 — 新里程碑 v1.1 初始化*  

