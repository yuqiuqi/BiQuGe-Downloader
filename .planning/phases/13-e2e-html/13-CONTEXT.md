# Phase 13: HTML 回退 E2E 与可复现记录 - Context

**Gathered:** 2026-04-24  
**Status:** Ready for plan（无多轮用户交互，依据 v1.4 `ROADMAP` / `REQUIREMENTS`（E2E-01/02）、`novel_downloader.py` 行为与 `999.1` 既有 E2E 体例收束灰区。若需改边界可编辑本文件后再 `/gsd-plan-phase 13`。  

<domain>
## Phase Boundary

在**不强制联网 CI**、**默认不为了本 E2E 大改 `novel_downloader` 主逻辑**、且**不粘贴整章版权正文**的前提下，完成 **E2E-01/02**：

- 对**至少一本书**给出**可复现**的两种观察：**apibi/默认可用路径** 与 **HTML 目录页解析/回退路径** 下的**章数或目录事实差异**、以及至少一项**样章/摘要级**质量观察（版式、乱码、残留行类型、终端关键日志行等）。  
- 结论文档落在 **`.planning/phases/13-e2e-html/E2E-*.md`**（日期或 slug），并可**引用/对照** `999.1-apibi-watermark-bom/E2E-2026-04-23.md` **不重复**其长篇摘段。  
- **E2E-02:** 在 `README` 增加**一句话入口**，或在报告中声明「已满足，见 `README` §…」并说明 N/A 理由。  

**本阶段不在范围内：** 新清洗规则、并发默认值变更、可插拔站点、自动爬取多镜像、在 CI 中每 push 拉全书。出现则记入 **`<deferred>`**。

</domain>

<decisions>
## Implementation Decisions

### 代码路径：何谓「apibi 路径」与「HTML/回退路径」

- **D-00（术语，与实现一致）:**  
  - **apibi 路径（本书全程 API 章链）:** `__init__` 中 `parse_book_id_from_url` 得书号且 `try_fetch_book_api` 返回带 `title` 的 `meta` → `self._use_api=True`；`get_download_url` 中 `fetch_chapter_titles_api` **非空** → 章链为 `apibi_chapter_token` 假 URL（`CHAPTER_URL_PREFIX` 前缀），`get_chapter_content` 走 `fetch_chapter_text_api`。**典型终端提示:** `已连接 apibi 书库` + `API 目录共 N 章`。  
  - **HTML 目录路径:** `self._use_api` 为 **False**（无书号、或 API 书信息拉不到、或从未置真），**或** apibi 置真但 `fetch_chapter_titles_api` 空，打印 `API 未返回章节目录，回退到网页解析…` 后 `self._use_api=False` 并 **`_get_chapters_from_page()`** → 章链为真实 `https?://.../book/{id}/*.html` 等。`get_chapter_content` 对非 apibi 假链走 **HTTP 拉章页 HTML** 并解析 `content` 等选择器。  
- **D-01（对照公平性）:** 两次运行宜**同一书号**、同一归一化目录根（如 `https://m.bqg92.com/book/{id}/`），以便章数/链接规则可比。若某路径 0 章，在报告记**失败原因**（网络、反爬、结构变更），不强行凑数。  
- **D-02（如何「只走 HTML」而不改代码 — 可写入 E2E 步骤）:** 任选在文档中写清且可复现的触发方式，例如：  
  - 启动前将 **`BQUGE_API_BASE`** 指向**本机不可达**地址，使 apibi 无法建立「书库 + 目录」成功路径，从逻辑上更易落到 HTML（**仅文档描述环境**，不把秘密写入仓库）；**或**  
  - 利用 **API 未返回章节目录** 时既有的**自动回退**（观察日志 `API 未返回章节目录，回退到网页解析…`），与另一次**完全成功**的 apibi 跑同一书作对比。  
  具体用哪一种，由 **13-01** 在复现时选**最稳、最少副作用**的一种，并在 E2E 文写**逐步命令**。  
- **D-03（不新增「隐藏开关」作本阶段前提）:** **不要求**在 Phase 13 为「强制 HTML」新增未文档化的环境变量/flag；若规划阶段认为有必要，单列为**后续 phase/backlog**，本 E2E 以现有可观测行为为限。  

### 结论文档与知识产权

- **D-04:** 正文样例**禁止**大段复制原著；允许 **≤3 行**匿名化/合成说明「残留类型」或版式。  
- **D-05:** 报告必备字段（可表格）：**书号/URL**、**日期/环境（Python/ OS 可简）**、**路径 A/B 的判定依据（日志关键词）**、**章数或 0 章**、**样章观察一行**、**与 999.1 E2E 的差异点一句**。  

### E2E-02 与 README

- **D-06:** 若 `README` 已说明目录页 URL + apibi/回退语义，E2E-02 可在主报告用 **1 节「README 已覆盖，引用 §…」** 收束。否则在 **README 增补一句** 指向本 `E2E-*.md` 或复现总步骤。  
- **D-07:** 不强制改 GitHub Actions；本地复现为主。  

### 测试与代码变更

- **D-08:** 本 phase **不新增**根目录**必须联网**的 `pytest`。若规划增加**纯单元**辅助函数测试，须与 E2E 采数**解耦**或标 `pytest.mark.skip` + 原因。  
- **D-09:** 交付以 **Markdown 证据**为主；**默认不改** `novel_downloader`/`bqg_api`。**仅当** E2E 发现「文档无法解释的确定性 bug」时，在 **13-02** 或 follow-up issue 中讨论是否最小补丁。  

### Claude's Discretion

- E2E 选书可沿用历史常见公开书号（如 **3953**），以你当前网络可重试为准。  
- `E2E-2026-04-24.md` 等文件名可随实际执行日期调整。  
- 与 `11-UAT` 的关系：可一句注明「本 milestone 以本 E2E 报告为 Phase 13 主验收物」。  

</decisions>

<deferred>
## Deferred Ideas（非本 phase）

- 在 CI 中自动跑「一书双路径」的联网集成测试。  
- 为「强制纯 HTML」增加官方 `--html-only` 或等价正式开关。  
- 多站点、多书批量矩阵。  

</deferred>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/ROADMAP.md` — Phase 13 成功标准与 `13-01` / `13-02` 建议切分  
- `.planning/REQUIREMENTS.md` — E2E-01, E2E-02  
- `.planning/PROJECT.md` — v1.4 目标  
- `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` — 历史 apibi 抽测，风格参考，避免正文重复  

### 实现锚点（只读、规划用）

- `novel_downloader.py` — `NovelDownloader.__init__`（`_use_api`）、`get_download_url`、`_get_chapters_from_page`、`get_chapter_content`（`CHAPTER_URL_PREFIX` 分支）  
- `bqg_api.py` — `try_fetch_book_api`、`fetch_chapter_titles_api`、`CHAPTER_URL_PREFIX`  
- `url_input.py` — `normalize_target_url`  
- `README.md` — 现有多线程、API、回退、清洗、并发等说明（供 E2E-02 对照）  

</canonical_refs>

<code_context>
## Existing Code Insights

### 可复用事实

- 数字书号经 `normalize_target_url` 变为 `m.bqg92.com/book/{id}/`，利于 HTML 与 apibi 共用同一**书号维度**。  
- apibi 章 URL 为**伪协议**前缀 + token；HTML 为真实 http(s) 链。对照时「路径」以**终端与日志** + **章链来自 API 或 `_get_chapters_from_page`** 为准。  

### 风险

- 站点/ API 随时间变化，E2E 结论带**时间戳**；0 章应视为**负例结果**写清，不假装成功。  
- 环境变量 `BQUGE_API_BASE` 影响 apibi 根路径；对照实验须记录是否设置。  

</code_context>

**Next steps:** `/gsd-plan-phase 13` 生成 `13-01-PLAN` / `13-02-PLAN` 并执行。  
