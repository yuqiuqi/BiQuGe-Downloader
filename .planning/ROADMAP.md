# Roadmap: BiQuGe Downloader

## Overview

**当前里程碑: v1.2 — 源站正文洁净与工程收尾**（接 v1.1 于 5–7 的**编号**之后：Phase 8 起，不含重置旧目录）。

- **v1.0** 阶段说明见 **`.planning/MILESTONES.md`**。  
- **v1.1** 已关闭；未编码的 **Phase 6/7** 目标平移至本里程碑 **9/10**。  
- **Backlog 999.1**（E2E 回写）**已 promote** 为 **Phase 8**。

## Phases (v1.2)

- [ ] **Phase 8: 深度清洗与单测** — U+FEFF、apibi 多类水印、黄金用例；可选 E2E-01 在此或并行记录  
- [ ] **Phase 9: 可维护性与诊断** — MAIN-01, MAIN-02  
- [ ] **Phase 10: 可配置并发** — CFG-01  

## Phase Details

### Phase 8: 深度清洗与单测

**Goal:** 消除 E2E（《领地》id=6094 等）中记录的**每章 U+FEFF** 与 **jqxs / gctxt 等**残留水印，并保持 `pytest` 无网、raw 可预期。  
**Depends on:** v1.1 已交付的 `text_clean` / 落盘 / 基线单测  
**Requirements:** CLEAN-01, CLEAN-02，可选 E2E-01  
**Success Criteria (what must be TRUE):**

1. 默认清洗路径下，对合成与黄金字符串验证：`jqxs`/`gctxt` 等目标串按约定被移除或削弱，**且** 至少一条「合法含顶点/符号」的句子不被误杀（单测锁定）  
2. U+FEFF 不在典型章首污染可视排版（以合成 + 如适用之抽样为准）  
3. `raw=True` 与 `README` 描述一致，单测或注释说明与默认路径差异  
4. 根目录 `pytest` 通过，不破坏现有用例

**Plans:** 待 `/gsd-plan-phase 8` 拆 8-01、8-02 等  
**UI hint:** no  

### Phase 9: 可维护性与诊断

**Goal:** 消除或解释死代码，零章节时失败可诊断。  
**Depends on:** Phase 8 推荐先合入，以免清洗与写入路径同时大改；逻辑上可只依赖 v1.0 下载能力  
**Requirements:** MAIN-01, MAIN-02  
**Success Criteria (what must be TRUE):**

1. `save_to_file` 与 `run()` 写入路径无重复/歧义，或已删除并统一  
2. `get_download_url` 无章节时，日志与退出信息给出可操作提示（如检查书号/站点变更）  
3. 回归不破坏既有测试与 Phase 8 行为  

**Plans:** 9-01, 9-02  
**UI hint:** no  

### Phase 10: 可配置并发

**Goal:** 用户可配置并发度，免改硬编码。  
**Depends on:** Phase 9 推荐（与诊断信息叠加更稳妥）  
**Requirements:** CFG-01  
**Success Criteria (what must be TRUE):**

1. 通过 CLI 或环境变量可设置 `max_workers`（或等效名），有默认值与合理边界说明  
2. `README` 或 `--help` 中说明该选项  
3. 默认与当前 10 线程行为兼容（或显式在文档中说明变化）  

**Plans:** 10-01, 10-02  
**UI hint:** no  

## Backlog

### Phase 999.1: apibi 正文水印与 BOM 跟进

**状态:** **已 promote 为 v1.2 Phase 8**（`CLEAN-01` / `CLEAN-02`）。本条目保留为溯源指针；技术细节以 `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` 为准。

**Plans:** 0 plans（关闭）

## Progress (v1.2)

| Phase | Theme | Status | Note |
|-------|--------|--------|------|
| 8 | 深度清洗与单测 | Not started | 承接 999.1 |
| 9 | 可维护性与诊断 | Not started | 原 v1.1 P6 |
| 10 | 可配置并发 | Not started | 原 v1.1 P7 |
| 999.1 |（溯源） | Promoted → 8 | 见上 |

## Historical — v1.1（已关闭，只读参考）

- Phase 5–7 的原始目标已部分由代码与本文件承继；`MILESTONES.md` 载明关闭注记。  

---

*Last updated: 2026-04-23 — 里程碑 v1.2*  
