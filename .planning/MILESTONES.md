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

## v1.2 — 源站正文洁净与工程收尾 (active)

**开始:** 2026-04-23  
**目标:** 在 v1.1 已交付的清洗/版式基线上，**消灭 apibi 抽测中记录的 BOM 与多类水印**（`999.1` 已 promote 为 Phase 8），并完成 **可维护性诊断**（MAIN）与 **可配置并发**（CFG）。可选：一次 HTML 回退路径的抽样 E2E 记录。  

*关闭本里程碑时在此补充 shipped / metrics。*

---

*GSD: new-milestone 于 2026-04-23 创建本文件；历史 roadmap 大段保留在 git 中。*
