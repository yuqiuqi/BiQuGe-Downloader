# Phase 9: 可维护性与诊断 - Context

**Gathered:** 2026-04-24  
**Status:** Plans ready（`09-01-PLAN` / `09-02-PLAN`）  

<domain>
## Phase Boundary

在**不改造**产品形态（仍为 CLI + `run()` 集中写整书 TXT）、**不破坏** Phase 8 清洗行为与全仓 `pytest` 的前提下：

1. **MAIN-01**：消除 `save_to_file` 与主写入路径的**重复/死代码**（见 `.planning/codebase/CONCERNS.md`）。  
2. **MAIN-02**：`get_download_url()` 得到**空目录**时，用户可见**可操作的**失败说明与建议（非仅一句「可能改版」），并保持 **exit 1** 以便 CI 失败可辨。

**本阶段不包含** Phase 10 的 `max_workers` 可配（见 `ROADMAP`）。

</domain>

<decisions>
## Implementation Decisions

### MAIN-01 / `save_to_file`

- **D-01:** 经全仓库检索，**无**对 `NovelDownloader.save_to_file` 的调用。采用 **删除** `save_to_file` 方法整段，避免与 `run()` 内 `with open(..., 'a')` 的写入策略并存两套格式（`run()` 使用 20 个 `-` 分隔行，`save_to_file` 为 30 个 `-`）。  
- **D-02:** 同步更新**规划/代码库说明**中与 `save_to_file` 相关的句段：`.planning/codebase/CONCERNS.md`、**`ARCHITECTURE.md`**、**`CONVENTIONS.md`**、`.cursor/rules/gsd.md` 若与仓库事实一致则改为「已移除」或删除该条。**不**为兼容而保留空壳方法。  
- **D-03:** 若未来需要「流式每章落盘」API，应新 Issue / Phase 再设计，**不在**本 phase 以 `save_to_file` 名义恢复。

### MAIN-02 / 空章节诊断

- **D-04:** 保持 **`run()`** 在 `not chapters` 时 **`sys.exit(1)`**（GitHub Actions 依赖失败退出码）。  
- **D-05:** 在退出前 `print` **结构化短段落**（3～8 行内），建议包含：  
  - 当前使用的路径摘要（**apibi** 书号 / **HTML 目录页 URL**）；  
  - 可能原因条列：**书号错误**、**站点目录改版**、**apibi 无 list 且 HTML 解析不到链接**、**网络/反爬**；  
  - **可操作项**：检查 URL/书号、换可解析的 `m.bqg92.com/book/<id>/` 形式、检查 `BQUGE_API_BASE`（若用自架 API）、重试/代理（简要）。  
- **D-06:** 实现上可仅在 `run()` 增强消息；**可选** 在 `NovelDownloader` 上设 `self._empty_catalog_hint: str | None`（在 `get_download_url` 内赋值）以便 `run()` 拼接——由实现/计划择一，不强制 API 面。  
- **D-07:** **不**新增必须联网的 `pytest`；若需单测，对「消息拼接」用**可注入的桩**或轻量**纯函数**测字符串（见计划阶段再拆）。

### 测试与回归

- **D-08:** 根目录 `pytest` 全绿；既有 `bqg_api` / `url_input` / `test_text_clean` 不受影响。  
- **D-09:** 可新增 `tests/` 下**小测** 仅当不 import `novel_downloader` 顶层自举，或**仅**测抽出的无侧效函数；否则以**手工+CI download job 红绿**为验收补注。

</decisions>

<canonical_refs>
## Canonical References

- `.planning/ROADMAP.md` — Phase 9 成功标准  
- `.planning/REQUIREMENTS.md` — **MAIN-01**、**MAIN-02**  
- `.planning/codebase/CONCERNS.md` — `save_to_file` 问题陈述  
- `novel_downloader.py` — `get_download_url`、`_get_chapters_from_page`、`run`  
- `bqg_api.py` — 目录/正文 API 行为（诊断文案勿与实现矛盾）  

</canonical_refs>

<code_context>
## Existing Code Insights

- **写入唯一事实来源：** `run()` 末段 `open(file_path, 'a')` 循环；`save_to_file` 为死代码。  
- **空目录：** `get_download_url` 在 apibi 无 list 时会打印并回退 HTML；双方皆空时 `run()` 仅一句通用提示。  
- **退出：** `if not chapters: print(...); sys.exit(1)` 已存在。  

</code_context>

<deferred>
## Deferred Ideas

- 可插拔「站点配置」、自动镜像探测 — 非本 phase。  
- 结构化日志/JSON 输出 — 非本 phase。  

</deferred>

---

*Phase: 09-maintainability-diagnostics*  
