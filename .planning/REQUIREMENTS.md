# Requirements: BiQuGe Downloader

**Core Value:** 稳定、可复现地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI Artifact（见 `PROJECT.md`）  
**Milestone (active):** **v1.4** — HTML 回退路径 E2E 与可复现记录  

## v1.4 Requirements

### 对照与记录（E2E）

- [x] **E2E-01**: 至少对**一本书**，在**可复现**前提下完成 **apibi/默认可用路径** 与 **HTML 目录解析/回退** 路径的**对照** — 已落实：`E2E-2026-04-24.md` + `13-RUN-RECORD.md`（书号 3953）。不强制在 CI 中做联网自动化。  
- [x] **E2E-02**（从属、可与 E2E-01 同一 PR 收束）: 在 `README` **或** 上述 E2E 报告显著位置，给出一句话**入口** — `README`「路径对照（E2E，v1.4）」+ E2E 文「E2E-02」节（README 主语义已覆盖，见 E2E 说明）。  

## 历史需求追溯

- **v1.3 及此前** 已勾选项 — 见 `.planning/milestones/v1.3-REQUIREMENTS.md` 与更早日志。  

## v2+（暂缓）

- **CFG-02**: 大文件/超大章时的流式或分批落盘（`CONCERNS`）  
- **SITE-01**: 可插拔站点配置  

## Out of Scope

| Feature | Reason |
|--------|--------|
| 带登录/付费/验证码的站点 | 与 README 与法律风险边界不符 |
| 产品化为 SaaS 或分发商用爬虫 | 超出个人工具维护范围 |
| 长驻联网爬虫服务 / 多站点调度平台 | 与本 CLI 工具范围不符 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| E2E-01 | 13 | Complete（`13-SUMMARY.md` / `E2E-2026-04-24.md`） |
| E2E-02 | 13 | Complete（`README` + E2E 文） |

**Coverage (v1.4):** 2 项，**均 Complete**；计划 `13-01` + `13-02` 已执行。  

---

*Last updated: 2026-04-24 — Phase 13 executed*  
