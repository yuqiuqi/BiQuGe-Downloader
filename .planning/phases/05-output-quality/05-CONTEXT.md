# Phase 5: 输出质量与测试 - Context

**Gathered:** 2026-04-23  
**Status:** Ready for planning  

**注:** 本次在无多轮交互下依据 `ROADMAP` / `REQUIREMENTS` / UAT 报告与代码结构锁定决策；若需调整可编辑本文件后再 `/gsd-plan-phase 5`。

<domain>
## Phase Boundary

在**不破坏**既有下载、CI、`pytest` 无网用例与 apibi/HTML 双路径的前提下，为合并 TXT 提供**可关闭**的正文清洗与**版式规范化**，并为清洗/版式逻辑补充**可维护的无网单测**。

本阶段**不包含** Phase 6 的死代码/零章节诊断、也不包含 Phase 7 的并发配置（见 `ROADMAP.md`）。

</domain>

<decisions>
## Implementation Decisions

### 清洗职责划分

- **D-01:** 新增独立模块（建议名 `text_clean.py` 或与项目风格一致的短名）存放**纯函数**：入参/出参为 `str`（或明确定义的片段），不发起网络、不依赖 `novel_downloader` 顶层自举安装逻辑。  
- **D-02:** `bqg_api.py` 保持**传输与 JSON 解析**职责；清洗在**拿到 `txt` 之后**、返回给 `NovelDownloader` 之前应用，或在与 `apibi://` 分支汇合的统一出口调用（避免两处分叉逻辑漂移）。  
- **D-03:** **HTML 解析路径**（`get_chapter_content` 非 apibi）：优先对**从 `content`/`showtxt` 等提取的合并字符串**复用同一套 `clean_chapter_text`；若源站广告形态与 apibi 差异大，实现阶段允许「HTML 子集规则」在模块内分函数，但**对外仍单一入口**以便测试。

### 默认行为与开关

- **D-04:** **默认开启**清洗（与 UAT 中「无推广噪声的阅读体验」一致）。  
- **D-05:** 提供**显式关闭**方式（二选一或同时支持，由实现择一并在 README 写清）：环境变量（例 `BQUGE_RAW_TEXT=1`）与/或 CLI 标志（例 `--raw-text`）。关闭时落盘为**与当前 API/解析尽量一致**的原始正文（仍保留 UTF-8 合法换行，不做删广告）。  
- **D-06:** 清洗规则**数据驱动**为一组可维护的「模式」列表（正则或固定子串 + 说明注释），**禁止**在业务路径散落魔法字符串；首版至少覆盖 UAT 已记录项：`bqfun`/`⊕cc` 类水印、「顶点小说」**独立成行的宣传句**、章末**独立成行的** `/read/\d+/` 类路径行（需避免误删对话内合法路径，故以**行级**或保守正则为主）。

### 版式（TXT-02）

- **D-07:** 全本文件**开头**在写入第一节前去掉**前导**空白行（UAT P2）。  
- **D-08:** 章与章之间：保持「空行 + 标题 + 分隔线 + 正文」的可读结构；避免**重复空行**堆叠（连续 `\n` 压成**最多**单段空行，或按现有 20 横线方案微调时保持与 `run()` 现有写入循环兼容）。  
- **D-09:** 不在本阶段改**章节序**、不改章标题来源（仍来自 booklist/目录解析）。

### 测试策略

- **D-10:** 新增 `tests/test_text_clean.py`（或等效名）：以**合成字符串**与 UAT **匿名化**片段为输入，覆盖「默认清洗」「raw 模式等价恒等/跳过规则」「边界：不误删正常引号/对话」。  
- **D-11:** 测试不 `import novel_downloader` 作为模块副作用入口（与 Phase 2 约定一致）；仅测 `text_clean` / 轻量 import。  
- **D-12:** CI 中现有 `pytest` 必须继续全绿；不新增必须联网的测试。

### Claude's Discretion

- 正则的具体写法、是否在首版合并「全角/半角空格变体」、HTML 与 apibi 是否完全同一规则集。  
- CLI 与 env 的命名在实现时与 `README` 保持对称即可。

</decisions>

<canonical_refs>
## Canonical References

**规划与需求**

- `.planning/ROADMAP.md` — Phase 5 成功标准与计划拆分提示（5-01～5-03）  
- `.planning/REQUIREMENTS.md` — **TXT-01**、**TXT-02**  
- `.planning/MILESTONES.md` — v1.0 / v1.1 边界  

**实证**

- `.planning/phases/03-content-quality/03-UAT-DOWNLOAD-REPORT.md` — P1（水印/推广串）、P2（文首空行）、P3（章末链接行）  

**实现锚点**

- `bqg_api.py` — `fetch_chapter_text_api` 返回的 `txt` 字段  
- `novel_downloader.py` — `get_chapter_content`（`apibi://` 分支）、`run()` 中顺序写文件逻辑  
- `.planning/codebase/CONCERNS.md` — 全本内存、站点耦合等约束（不扩大本阶段范围）  

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `bqg_api.fetch_chapter_text_api` / `parse_apibi_chapter_token` — apibi 章节正文入口  
- `url_input` / 既有 `tests/test_url_input.py`、`tests/test_bqg_api.py` — 无网测试范式  

### Established Patterns

- 工具函数放独立模块、关键逻辑 `pytest` 参数化；`novel_downloader` 为编排层  

### Integration Points

- `NovelDownloader.get_chapter_content` 在 `text` 返回前；`run()` 在**首次** `open` 写文件前可对「全书首行」做一次性 trim（若放在 `run()` 而非 per-chapter，仅解决文首，章首见 D-08）  

</code_context>

<specifics>
## Specific Ideas

- UAT 中「`bqfun ⊕cc`」为高频噪声，应作为**首条**回归用例。  
- 用户若需保留证迹，依赖 **D-05** 的 raw 模式而非在默认路径放宽规则。  

</specifics>

<deferred>
## Deferred Ideas

- 流式落盘/超大书内存优化（`CFG-02` / `CONCERNS`）— 非本阶段  
- 可插拔多站点配置（`SITE-01`）— 非本阶段  
- Phase 6/7 事项 — 各归其阶段  

</deferred>

---

*Phase: 05-output-quality*  
*Context gathered: 2026-04-23*  
