# Milestones: BiQuGe Downloader

## v1.0 — 工程化基线 (closed)

**时间:** 2026-04-23  
**完成内容（摘要）:**  
- 依赖与 CI 对齐（`requirements.txt`、workflow 一致）  
- 测试基线（`pytest`、`url_input`/`bqg_api` 单测、CI 先 `test` 后 `download`）  
- 新站 `apibi.cc` 下载路径、URL 书号解析与 HTML 回退  
**未在 v1.0 内收尾:** 原 Roadmap 中 Phase 3（MAIN-01/02）与 Phase 4（CFG-01）未实施；UAT 发现正文水印/版式问题未编码 — 已转入 **v1.1**。

---

## v1.1 — 输出质量与可维护性 (closed)

**开始:** 2026-04-23  
**关闭:** 2026-04-23（转入 v1.2，未实施项由新里程碑承接）  
**已交付（摘要）:** `text_clean` + `NovelDownloader` 集成、章首/章间落盘、无网 `test_text_clean`、`README` 中 `--raw-text` / `BQUGE_RAW_TEXT`；E2E 见 `05` 与 `999.1-apibi-watermark-bom/E2E-2026-04-23.md`（apibi 仍有 `jqxs`/`gctxt` 等水印与每章 U+FEFF 待清）。  
**原 Roadmap 中未在本文件关闭前编码:** Phase 6（MAIN）、Phase 7（CFG）与 E2E 回写项 — **已纳入 v1.2**。

---

## v1.2 — 源站正文洁净与工程收尾 (superseded → v1.3)

**开始:** 2026-04-23  
**收束注记 (2026-04-24):** Phase 8（CLEAN-01/02）与 Phase 9（MAIN-01/02）已交付。用户反馈**成文仍含类水印/类推广行**；**Phase 10 / CFG-01** 未在 v1.2 内实施。**余下目标并入 v1.3**（见下）。

---

## v1.3 — 类水印残留与清洗·二期 (active)

**开始:** 2026-04-24  
**目标:** 在已有 `text_clean` 规则上，针对**仍可见的类水印/源站固定噪音**做**二期可测清洗**；完成 **CFG-01**；可选 **E2E-01**。详见 `.planning/PROJECT.md` 与 `ROADMAP.md` Phase 11+。  

*关闭本里程碑时在此补充 shipped / metrics。*

---

*GSD: new-milestone 于 2026-04-23 创建本文件；历史 roadmap 大段保留在 git 中。*
