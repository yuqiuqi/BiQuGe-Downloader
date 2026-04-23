# Requirements: BiQuGe Downloader

**Core Value:** 稳定、可复现地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI Artifact（见 `PROJECT.md`）  
**Milestone (active):** **v1.4** — HTML 回退路径 E2E 与可复现记录  

## v1.4 Requirements

### 对照与记录（E2E）

- [ ] **E2E-01**: 至少对**一本书**，在**可复现**前提下完成 **apibi/默认可用路径** 与 **HTML 目录解析/回退** 路径的**对照**：记录书号/URL、运行方式、**章数或目录差异**、至少一处**样章**或摘要级观察（版式/乱码/残留行类型等）；**结论与步骤**写入仓库内 Markdown（`.planning/phases/13-e2e-html/` 下 `E2E-*.md` 或经讨论的等价路径；可引用/衔接已有 `999.*` 文档）。不强制在 CI 中做联网自动化。  
- [ ] **E2E-02**（从属、可与 E2E-01 同一 PR 收束）: 在 `README` **或** 上述 E2E 报告显著位置，给出一句话**入口**，说明如何按本仓库约定复现「HTML 回退 vs 默认 apibi」对照（若执行时发现 README 已足够，可勾选并在报告中写「N/A 理由」）。  

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
| E2E-01 | 13 | Pending |
| E2E-02 | 13 | Pending |

**Coverage (v1.4):** 2 项，均映射 **Phase 13**；以 `13-01` / `13-02` 计划承载（见 `ROADMAP.md`）。  

---

*Last updated: 2026-04-24 — /gsd-new-milestone v1.4*  
