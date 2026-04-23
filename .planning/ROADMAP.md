# Roadmap: BiQuGe Downloader

## Milestones

- ✅ **v1.3 — 类水印残留与清洗·二期** — Phases **11–12**（**2026-04-24**） — 见 **`.planning/milestones/v1.3-ROADMAP.md`**
- ✅ **v1.4 — HTML 回退路径 E2E 与可复现记录** — **Phase 13**（E2E-01 / E2E-02，**2026-04-24**）见 `13-SUMMARY.md`  

**编号约定:** 阶段目录延续 **11+**；**Phase 13** 对应当前里程碑。  

## Phases (v1.4 — 当前)

- [x] **Phase 13: HTML 回退 E2E 与可复现记录** — E2E-01, E2E-02（`13-SUMMARY.md`）  

### Phase 13: HTML 回退 E2E 与可复现记录

**Goal:** 一书双路径（apibi 可用时 vs 明确走 **HTML 目录/回退**）**可复现对照**，落盘结论文档；补一句用户可见入口（README 或报告）。  
**Depends on:** 下载与目录解析基线已存在（v1.0+）；不依赖新并发/清洗大改。  
**Requirements:** E2E-01, E2E-02  

**Success Criteria (what must be TRUE):**

1. 存在**可执行**的复现步骤（命令行/环境变量/书号，写清「如何触发 HTML 回退或对照」）。  
2. 对照结果含**可核对事实**（至少：章数或目录项数量是否一致、及一项正文/版式/残留类观察）。  
3. 结论文档路径在 **`.planning/`** 内可追溯；`REQUIREMENTS` 追溯表可标为 In progress / Complete。  
4. 若 README 已有等价说明，E2E-02 可在报告中**显式**说明「由 README §… 满足」并勾选。  

**Plans（建议，执行时以 `discuss`/`plan` 落盘）:**

| Plan | 内容 |
|------|------|
| **13-01** | 选书、环境、跑通两路径、采集数据（可含截图/摘抄路径说明） |
| **13-02** | 撰写 `E2E-*.md`、E2E-02 入口、更新追溯与 `SUMMARY` |

**UI hint:** no  

## Progress (rolling)

| Phase | Theme | Milestone | Status | Note |
|-------|--------|-----------|--------|------|
| 11 | 类水印/噪音二期 | v1.3 | Complete | `11-SUMMARY.md` |
| 12 | 可配置并发 | v1.3 | Complete | `12-SUMMARY.md` |
| 13 | HTML 回退 E2E | **v1.4** | Complete | `13-SUMMARY.md` |

## Shipped: v1.3（摘要）

<details>
<summary>v1.3 — Phases 11–12（2026-04-24）</summary>

- [x] **Phase 11** — CLEAN-03。  
- [x] **Phase 12** — CFG-01。  

</details>

## Shipped: v1.4（摘要）

<details>
<summary>v1.4 — Phase 13（2026-04-24）</summary>

- [x] **Phase 13** — E2E-01/02；`E2E-2026-04-24.md` + `13-RUN-RECORD`；README 入口。  

</details>

## Backlog

### Phase 999.1: apibi 正文水印与 BOM 跟进

**状态:** **已 promote 为 v1.2 Phase 8**；溯源见 `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md`；v1.3 **CLEAN-03 / Phase 11** 对残留族做二期收束。  

**Plans:** 0 plans（关闭）

## Historical

- 更早阶段与 v1.3 全量见 `MILESTONES.md`、`milestones/v1.3-ROADMAP.md`。  

---

*Last updated: 2026-04-24 — v1.4 Phase 13 Complete*  
