# Milestones: BiQuGe Downloader

## v1.0 — 工程化基线 (closed)

**时间:** 2026-04-23  
**完成内容（摘要）:**  
- 依赖与 CI 对齐（`requirements.txt`、workflow 一致）  
- 测试基线（`pytest`、`url_input`/`bqg_api` 单测、CI 先 `test` 后 `download`）  
- 新站 `apibi.cc` 下载路径、URL 书号解析与 HTML 回退  
**未在 v1.0 内收尾:** 原 Roadmap 中 Phase 3（MAIN-01/02）与 Phase 4（CFG-01）未实施；UAT 发现正文水印/版式问题未编码 — 已转入 **v1.1**。

---

## v1.1 — 输出质量与可维护性 (active)

**开始:** 2026-04-23  
**目标:** 可读的合并 TXT、明确失败诊断、可配置并发、代码卫生；与 `PROJECT.md`「Current Milestone」一致。  

*关闭本里程碑时在此补充 shipped / metrics。*

---

*GSD: new-milestone 于 2026-04-23 创建本文件；历史 roadmap 大段保留在 git 中。*
