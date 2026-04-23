# Requirements: BiQuGe Downloader

**Core Value:** 稳定、可复现地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI Artifact（见 `PROJECT.md`）

## v1.0（已完成，摘要）

- PACK-01, PACK-02, TEST-01, TEST-02 — 见 `MILESTONES.md` v1.0

---

## v1.1（已关闭，摘要）

- [x] **TXT-01**: 对 API/解析得到的章节正文，提供**可关闭**的清洗层，去除或弱化源站内嵌的水印/推广片段；默认可配或文档化 — 已实现基线，**apibi 多类串仍见 v1.2 CLEAN-02 与** `E2E-2026-04-23.md`
- [x] **TXT-02**: 落盘时规范章首/文件头多余空行与换行风格 — 已按 Phase 5 实现

**未在 v1.1 内收尾、已转入 v1.2：**

- [ ] **MAIN-01, MAIN-02, CFG-01**（及下列 CLEAN / E2E）

---

## v1.2（本里程碑 — active）

### 正文深度洁净（E2E / 999.1 promote）

- [x] **CLEAN-01**: 对正文（apibi 与 HTML 拉取后统一）剥离行首/段级 **U+FEFF**（BOM/ZWNBSP）及同类「仅噪声」的不可见前缀，不破坏用户可见叙事；`raw=True` 时行为在 README/代码中可预期（至少保留或明确不剥离）
- [x] **CLEAN-02**: 覆盖 apibi 抽测中高频水印形态（如 `jqxs` + `⊙` + `cc`、`gctxt` + `点cc` 等**固定**推广串），**需** 黄金用例/合成单测，并记录「不得误伤」的合法正文边界（可引用 E2E 与人工抽样结论）

### 可维护性与可观测

- [ ] **MAIN-01**: `save_to_file` 死代码被删除、接入 `run()` 路径，或明确弃用并移除（与 `CONCERNS` 一致）
- [ ] **MAIN-02**: 当未解析到任何章节时，用户可见明确失败原因与下一步建议（非静默空成功）

### 可配置

- [ ] **CFG-01**: 下载并发线程数可通过 CLI 参数或环境变量配置，且文档中说明默认值

### 可选增强

- [ ] **E2E-01**: 至少对 **HTML 目录回退** 路径做一书抽样或全本下载，记录与 apibi 路径对照（无乱码、章数、版式；阻塞项进 issue/backlog）— 不阻塞 v1.2 收束，但可提前暴露解析差异

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
| TXT-01, TXT-02 | v1.1（Phase 5 实现） | Complete（基线；残留见 CLEAN-02） |
| CLEAN-01 | 8（`08-01-PLAN.md`） | Complete |
| CLEAN-02 | 8（`08-02-PLAN.md`） | Complete |
| MAIN-01 | 9（`09-01-PLAN.md`） | Pending — execute |
| MAIN-02 | 9（`09-02-PLAN.md`） | Pending — execute |
| CFG-01 | 10 可配置并发 | Pending |
| E2E-01 | 8 或独立验证任务；可选 | Pending |

**Coverage (v1.2):** 6 requirements（含 1 项可选 E2E）— 映射 3 个必做阶段 + 可选 E2E  

---

*Last updated: 2026-04-24 — Phase 9 plans 09-01, 09-02*  
