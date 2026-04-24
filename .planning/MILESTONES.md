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

## v1.3 — 类水印残留与清洗·二期 (closed)

**开始:** 2026-04-24  
**关闭:** 2026-04-24  
**已交付 (SHIPPED `v1.3`):**  
- **CLEAN-03 / Phase 11** — `11-INVENTORY.md`、变体单测与 `text_clean`/`README` 锚点；不扩大无据正则，以可回归单测收束。  
- **CFG-01 / Phase 12** — `novel_downloader` 中 `resolve_max_workers`；CLI `-j`/`--workers`；`BQUGE_MAX_WORKERS`；默认 10 线程、上限 64；`tests/test_novel_workers.py`；README「并发」与 `pytest` 全绿。  
**归档:** `.planning/milestones/v1.3-ROADMAP.md`、`.planning/milestones/v1.3-REQUIREMENTS.md`  
**本版未做（留待后续）:** —（原 v1.3 时推迟的 E2E-01 已由 **v1.4** 收束。）  
**Known 流程注记 at close:** `11-UAT.md` 未完整对话式验收闭环；以各 `*-SUMMARY.md` 与 `pytest` 为交付主证据。  
**Known deferred items at v1.3 close（历史）:** 原「可选 E2E-01」— 后由 v1.4 关闭。  

---

## v1.4 — HTML 回退路径 E2E 与可复现记录 (closed)

**开始:** 2026-04-24  
**关闭:** 2026-04-24  
**已交付 (SHIPPED `v1.4`):** **E2E-01 / E2E-02 / Phase 13** — `13-RUN-RECORD.md`、`E2E-2026-04-24.md`（书号 **3953**：apibi **113** 章 vs HTML 目录 **13** 章及元数据差异）、`README`「路径对照（E2E，v1.4）」；`13-SUMMARY.md`。不强制联网 CI。  
**归档:** `.planning/milestones/v1.4-ROADMAP.md`、`.planning/milestones/v1.4-REQUIREMENTS.md`  

---

*GSD: new-milestone 于 2026-04-23 创建本文件；v1.3 于 2026-04-24 关闭并归档。*  
