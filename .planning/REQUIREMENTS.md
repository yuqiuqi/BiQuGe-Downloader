# Requirements: BiQuGe Downloader

**Core Value:** 稳定、可复现地从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地或 CI Artifact（见 `PROJECT.md`）

## 范围说明

本文件在 **v1.3 里程碑于 2026-04-24 收束** 后已重置。上一版完整追溯与 v1.3 勾选项见 **`.planning/milestones/v1.3-REQUIREMENTS.md`**。下一里程碑的需求与编号由 **`/gsd-new-milestone`** 正式落盘后再在此补全。

## 从 v1.3 承继的候选项（尚未经新里程碑采纳）

- [ ] **E2E-01**: 至少对 **HTML 目录回退** 路径做一书抽样或全本下载，记录与 apibi/默认路径对照（原 ROADMAP **Phase 13** 描述；不强制联网 CI）。  

## v2+（暂缓）

- **CFG-02**: 大文件/超大章时的流式或分批落盘（`CONCERNS`）  
- **SITE-01**: 可插拔站点配置  

## Out of Scope

| Feature | Reason |
|--------|--------|
| 带登录/付费/验证码的站点 | 与 README 与法律风险边界不符 |
| 产品化为 SaaS 或分发商用爬虫 | 超出个人工具维护范围 |

## Traceability

| Requirement | Status | 备注 |
|-------------|--------|------|
| 上一里程碑 (v1.3) 必做项 | Complete | 见 `milestones/v1.3-REQUIREMENTS.md` |
| E2E-01 | **Pending** | 是否纳入下一里程碑，由 `gsd-new-milestone` 定 |

---

*Last updated: 2026-04-24 — after v1.3 milestone close (requirements reset)*  
