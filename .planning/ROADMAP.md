# Roadmap: BiQuGe Downloader

## Overview

**当前里程碑: v1.1 — 输出质量与可维护性**（自 Phase 5 起编号，承接 v1.0 已交付的依赖/CI/测试与 apibi 下载能力）。

v1.0 阶段 1–4 的详细说明已写入 **`.planning/MILESTONES.md`**；本文件仅规划 **v1.1** 待实施阶段。

## Phases (v1.1)

- [ ] **Phase 5: 输出质量与测试** — 正文清洗与版式、无网单测  
- [ ] **Phase 6: 可维护性与诊断** — 死代码与空目录体验  
- [ ] **Phase 7: 可配置并发** — 线程数可配与文档化  

## Phase Details

### Phase 5: 输出质量与测试

**Goal:** 合并后的 TXT 无显著源站噪音，版式稳定；关键清洗逻辑有测试。  
**Depends on:** v1.0 已完成之下载与 apibi 通道  
**Requirements:** TXT-01, TXT-02  
**Success Criteria (what must be TRUE):**

1. 对 API 路径下载的正文，在写入前可应用清洗，且可关闭或文档中说明如何保留原文（避免误伤合法字句，边界用单测与抽样回归说明）  
2. 全本文件与章间分隔清晰，无 UAT 指出的成段多余空行或异常换行问题（目标：优于 UAT 时「章首/文首空行」表现）  
3. 对清洗/版式相关纯函数有 `pytest` 覆盖（不依赖外网、不 `import` 会触发自举安装的全模块顶栏）  
4. 不破坏 v1.0 既有 CI 与无网单测

**Plans (规划阶段再拆):** 5-01 清洗模块与策略；5-02 落盘/trim；5-03 用例与文档  
**UI hint:** no  

### Phase 6: 可维护性与诊断

**Goal:** 消除或解释死代码，零章节时失败可诊断。  
**Depends on:** Phase 5（可并行在 Phase 5 快结束时规划）  
**Requirements:** MAIN-01, MAIN-02  
**Success Criteria (what must be TRUE):**

1. `save_to_file` 与 `run()` 写入路径无重复/歧义，或已删除并统一  
2. `get_download_url` 无章节时，日志与退出信息给出可操作提示（如检查书号/站点变更）  
3. 回归不破坏 Phase 1–2 与 Phase 5 行为  

**Plans:** 6-01, 6-02  
**UI hint:** no  

### Phase 7: 可配置并发

**Goal:** 用户可配置并发度，免改硬编码。  
**Depends on:** Phase 6 推荐（逻辑上可只依赖 v1.0 下载，但与诊断信息叠加更稳妥）  
**Requirements:** CFG-01  
**Success Criteria (what must be TRUE):**

1. 通过 CLI 或环境变量可设置 `max_workers`（或等效名），有默认值与合理边界说明  
2. `README` 或 `--help` 中说明该选项  
3. 默认与当前 10 线程行为兼容（或显式在 CHANGELOG/文档中说明变化）  

**Plans:** 7-01, 7-02  
**UI hint:** no  

## Backlog

### Phase 999.1: apibi 正文水印与 BOM 跟进（E2E 回写）

**来源:** `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md`（《领地》id=6094 全本抽测）  
**Goal:** 扩展 `text_clean` 或 apibi 后处理，覆盖 `jqxs ⊙cc` / `gctxt点cc` 等 apibi 常见水印；正文字段首的 **U+FEFF** 剥离；规则需单测 + 防误伤合法正文。  
**状态:** 待排期；提升后可再 promote 为正式 Phase 子计划。

**Plans:** 0 plans（待 `/gsd-review-backlog` 时拆解）

## Progress (v1.1)

| Phase | Theme | Status | Note |
|-------|--------|--------|------|
| 5 | 输出质量与测试 | Not started | |
| 6 | 可维护性与诊断 | Not started | |
| 7 | 可配置并发 | Not started | |
| 999.1 | apibi 水印与 BOM 跟进 | Backlog | 见上 |

---

*Last updated: 2026-04-23 — v1.1 里程碑 + E2E backlog*  
