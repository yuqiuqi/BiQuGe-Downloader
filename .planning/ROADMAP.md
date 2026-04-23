# Roadmap: BiQuGe Downloader

## Milestones

- ✅ **v1.3 — 类水印残留与清洗·二期** — Phases **11–12**（必做 CLEAN-03、CFG-01 已 SHIPPED **2026-04-24**） — 全量见 **`.planning/milestones/v1.3-ROADMAP.md`**
- 📋 **下一段** — 未命名下一里程碑；候选 **`/gsd-new-milestone`** 承接，或从下方 **Phase 13（可选 E2E-01）** 继续

**编号约定:** 阶段目录仍按 **11+** 延续（与 v1.2 的 1–10 不重置）；历史阶段见 `.planning/phases/` 与 `MILESTONES.md`。

## Phases (当前焦点)

- [ ] **Phase 13:（可选）HTML 回退 E2E 记录** — E2E-01  

## Phase 13:（可选）HTML 回退 E2E 记录

**Goal:** 一书走 HTML 目录解析，记录与 apibi 路径在章数/版式/残留上的差异，阻塞项进 issue/backlog。  
**Requirements:** E2E-01（见 `REQUIREMENTS.md` 候选项）  
**Success Criteria (what must be TRUE):** 有**可复现的**书记录与结论段落（可放在 `.planning/phases/999.*` 或 `codebase` 注记），不强制自动化联网 CI。  
**UI hint:** no  

## Progress (rolling)

| Phase | Theme | Milestone | Status | Note |
|-------|--------|-----------|--------|------|
| 11 | 类水印/噪音二期 | v1.3 | Complete | `11-SUMMARY.md` |
| 12 | 可配置并发 | v1.3 | Complete | `12-SUMMARY.md` |
| 13 | E2E HTML | TBD | Not started | 可选，待下一里程碑定 |

## Shipped: v1.3（摘要）

<details>
<summary>v1.3 — Phases 11–12（2026-04-24）</summary>

- [x] **Phase 11** — CLEAN-03；盘点 `11-INVENTORY`、变体单测、`text_clean` / `README` 注记。  
- [x] **Phase 12** — CFG-01；`novel_downloader` `-j`/`--workers`、`BQUGE_MAX_WORKERS`、默认 10 线程兼容。  

</details>

## Backlog

### Phase 999.1: apibi 正文水印与 BOM 跟进

**状态:** **已 promote 为 v1.2 Phase 8**；技术细节以 `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` 为溯源。新残留形态在 v1.3 中由 **CLEAN-03 / Phase 11** 以单测与文档收束。  

**Plans:** 0 plans（关闭）

## Historical

- v1.2 及更早阶段说明见 **`MILESTONES.md`** 与 `milestones/v1.3-ROADMAP.md` 内「Historical — v1.2 及更早」或 git 历史。  

---

*Last updated: 2026-04-24 — v1.3 milestone archived; current roadmap slim*  
