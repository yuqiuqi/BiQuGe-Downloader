# Phase 11: 类水印/噪音二期 - Context

**Gathered:** 2026-04-24  
**Status:** Executed（Phase 11 已执行，见 `11-SUMMARY.md`）  

**注:** 与 Phase 8 同型，本文件在**无多轮用户交互**下依据 v1.3 `ROADMAP` / `REQUIREMENTS`（CLEAN-03）、**`.planning/phases/05-output-quality/05-CONTEXT.md`** 与 **`.planning/phases/08-deep-clean-pytest-apibi/08-CONTEXT.md`** 已锁定决策、及当前 `text_clean` 实现收束灰区。若需调整可编辑本文件后再 `/gsd-plan-phase 11`。

<domain>
## Phase Boundary

在**不破坏** v1.0+ 已交付的下载管线、**全仓 `pytest` 无网**、**apibi 与 HTML 拉取后统一经 `clean_chapter_text`**、且 **`raw` 语义与 Phase 5/8 一致**的前提下，对 **CLEAN-03** 落地：针对**仍成段/成行/行内**出现的**类水印、源站推广或固定短行噪音**，在 `text_clean.py` 中**追加或收紧**规则，并以 **`tests/test_text_clean.py`（+ 必要时合成/黄金字符串）** 锁定回归与**误伤边界**。

**本阶段不在范围内：** 可配置并发（Phase 12）、HTML-only E2E 全书（Phase 13）、可插拔「规则引擎/外部配置文件」、以及任何需联网的 CI 用例。若讨论中出现，记入 `deferred` / backlog。

</domain>

<decisions>
## Implementation Decisions

### 与 Phase 5 / 8 的继承

- **D-00:** 继承 **05-CONTEXT 的 D-01～D-12** 与 **08-CONTEXT 的 D-00～D-09** 中仍适用的部分：单模块主入口、默认开清洗、**`raw` 不删营销行内/行级规则**但 **U+FEFF 仍去**、测试**禁止** `import novel_downloader` 作入口、行级删除须防误伤「叙事里提到顶点/网址」的句子。Phase 11 **只增**规则与用例，不重新定义里程碑边界。

### 残留形态与输入来源（CLEAN-03）

- **D-01:** 新规则**须**有**可复现依据**：优先使用 `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` 及用户/维护者在 issue 中提供的**摘段、合成复现串**；**无依据的泛化猜测**不单独合入，除非在 PLAN 中记为「实验分支」并经单测对攻。若当前仓库缺少**具体新形态**摘段，**先**在计划中排 **11-01「盘点/固样」**：列出仍见残留类别 + 最小合成样例，再 **11-02「实现+单测」**。
- **D-02:** 规则落点**仅限** `text_clean.py`（及同模块内小函数）；清洗调用链仍以 `NovelDownloader._finalize_chapter_text` → `clean_chapter_text` 为**唯一**章节正文出口（与 Phase 8 一致，不在 Phase 11 改并发/目录解析）。

### 行内 / 行级策略

- **D-03:** 与 Phase 8 **D-05** 同序：**优先**行内 `sub` 去除固定推广片段；仅当用例证明存在**可描述的整行**纯垃圾行时，再扩展 `_line_is_spam_line` 或同类行滤，且每条行规则须配 **防误伤** 单测。
- **D-04（误伤防护）：** 任意新增强删除/替换，须在 `test_text_clean.py` 增加**对攻**用例；至少覆盖一条「与营销词表相似但为合法叙事/对话」的合成句（可沿用/扩展 `test_vertex_in_sentence_not_removed` 思路）。禁止引入整章版权原文。

### raw 与短错误句

- **D-05:** **`raw=True`**：仍只做换行统一 + 去 U+FEFF，**不**应用 `_apply_inline_replacements` 与行级营销过滤（与现有 docstring/Phase 8 一致）。若 Phase 11 动到 `clean_chapter_text` 分支条件，**须**在 README 有对应句且单测 `test_raw_*` 不降级。
- **D-06:** 对「过短且像错误信息」分支（`无法解析` / `下载失败` 且长度阈值）**不**在 Phase 11 扩大替换范围，避免与短句正交；若需调整阈值，单测单独覆盖。

### 测试与 CI

- **D-07:** 根目录 `pytest` 全绿；**不新增必须联网**的测试。新用例以合成短串与 E2E **匿名化** 片段为主。
- **D-08:** 现有 Phase 8 黄金/参数化用例**默认不删**；若因规则收紧需改期待值，在 PLAN/提交说明中记 **「刻意变更 + 原因」**。

### Claude's Discretion

- 新水印的具体正则（空白变体、全半角、Unicode 点号）在实现中迭代，以单测为锚。  
- 若维护者后续提供 **1～2 条**真实摘段，是否拆独立 `*_PATTERNS` 元组，由实现者决定。  
- 是否在注释中给出来源日期（E2E / issue #）便于审计。

</decisions>

<specifics>
## Specific Ideas

- 用户/里程碑动机：**成书仍可见「类水印」行或片段**（v1.3 PROJECT），故本阶段强调 **「有样例再落规则」**，避免与 CLEAN-01/02 已收束的边界冲突。

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 路标与需求

- `.planning/ROADMAP.md` — **Phase 11** 成功标准、与 Phase 12/13 的边界  
- `.planning/REQUIREMENTS.md` — **CLEAN-03**  
- `.planning/PROJECT.md` — v1.3 目标（类水印二期 + CFG 在后续阶段）  
- `.planning/STATE.md` — 当前聚焦  

### 前序已锁定决策（清洗）

- `.planning/phases/05-output-quality/05-CONTEXT.md` — 清洗职责、raw、测试约束  
- `.planning/phases/08-deep-clean-pytest-apibi/08-CONTEXT.md` — FEFF、jqxs/gctxt、误伤、单测策略  

### 实证与 E2E

- `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` — 书号 6094 等抽测、残留形态溯源  

### 实现与测试锚点

- `text_clean.py` — `clean_chapter_text`、`_INLINE_NOISE`、`_line_is_spam_line` 等  
- `novel_downloader.py` — `_finalize_chapter_text` 调用点（**规划定位**，本阶段原则上只改 `text_clean` + 测）  
- `tests/test_text_clean.py` — 扩展用例主位置  
- `README.md` — `--raw-text` / `BQUGE_RAW_TEXT` 与清洗语义  

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `clean_chapter_text` 已串联：换行 → FEFF →（非 raw）行内替换 → 行滤 → 多余空行压缩。  
- `_INLINE_NOISE` 元组与 `_line_is_spam_line` 可追加条目；`test_text_clean.py` 已覆盖 bqfun / jqxs / gctxt / 行删 / raw+FEFF。

### Established Patterns

- 行内用编译正则 `sub`；行级用 `split("\n")` 过滤；短错误句**不做重度清洗**。  
- 防误伤：对话里含「顶点」等不删整段。

### Integration Points

- 章节正文在 `NovelDownloader._finalize_chapter_text` 中调用 `clean_chapter_text`；Phase 11 **原则上不修改** 该调用签名，除非 PLAN 将「签名为兼容」列为显式子任务并单测全仓。

</code_context>

<deferred>
## Deferred Ideas

- **可配置规则列表 / 环境变量驱动一整包水印模式** — 新能力，非 CLEAN-03 最小解；可 backlog。  
- **NLP/相似度** 判营销 — 超出本 CLI 工具范围。  
- **Phase 12（CFG-01）** 与 **Phase 13（E2E-01）** — 分属后续阶段，不并入 Phase 11 实现批次。

### Reviewed Todos (not folded)

- 无待折叠 todo（`todo match-phase` 未提供匹配或跳过）。

**讨论范围** 未超出 Phase 11（`text_clean` 二期）；未将 Phase 12/13 拉入本阶段。

</deferred>

---

*Phase: 11-wm2-text-clean*  
*Context gathered: 2026-04-24*  
