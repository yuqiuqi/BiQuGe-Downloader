# Requirements: BiQuGe Downloader

**Core Value:** 稳定、可复现地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI Artifact（见 `PROJECT.md`）

## v1.0（已完成，摘要）

- PACK-01, PACK-02, TEST-01, TEST-02 — 见 `MILESTONES.md` v1.0

---

## v1.1 本里程碑

### 输出与排版（来自 UAT `03-UAT-DOWNLOAD-REPORT`）

- [ ] **TXT-01**: 对 API/解析得到的章节正文，提供**可关闭**的清洗层，去除或弱化源站内嵌的水印/推广片段（如 UAT 中记录的重复噪音串与尾行站点宣传），不破坏主叙事句意；默认策略可配或文档化
- [ ] **TXT-02**: 落盘时规范章首/文件头多余空行与换行风格，与现有「章节标题 + 分隔线」结构一致、易于阅读

### 可维护性与可观测

- [ ] **MAIN-01**: `save_to_file` 死代码被删除、接入 `run()` 路径，或明确弃用并移除（与 `CONCERNS` 一致）
- [ ] **MAIN-02**: 当未解析到任何章节时，用户可见明确失败原因与下一步建议（非静默空成功）

### 可配置

- [ ] **CFG-01**: 下载并发线程数可通过 CLI 参数或环境变量配置，且文档中说明默认值

## v2（暂缓）

- **CFG-02**: 大文件/超大章时的流式或分批落盘（`CONCERNS`）
- **SITE-01**: 可插拔站点配置

## Out of Scope

| Feature | Reason |
|--------|--------|
| 带登录/付费/验证码的站点 | 与 README 与法律风险边界不符 |
| 产品化为 SaaS 或分发商用爬虫 | 超出个人工具维护范围 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PACK-01, PACK-02 | v1.0 P1 | Complete |
| TEST-01, TEST-02 | v1.0 P2 | Complete |
| TXT-01, TXT-02 | 5 输出质量与测试 | Pending |
| MAIN-01, MAIN-02 | 6 可维护性与诊断 | Pending |
| CFG-01 | 7 可配置并发 | Pending |

**Coverage (v1.1):** 5 requirements — mapped to 3 phases  

---

*Last updated: 2026-04-23 — milestone v1.1 初始化*  
