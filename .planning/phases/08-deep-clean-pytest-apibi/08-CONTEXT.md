# Phase 8: 深度清洗与单测 - Context

**Gathered:** 2026-04-23  
**Status:** Ready for planning  

**注:** 与 Phase 5 CONTEXT 相同，本文件在**无多轮用户交互**下依据 `ROADMAP` / `REQUIREMENTS`、**Phase 5** 已锁定决策、`999.1` E2E 详报与当前 `text_clean` 实现收束灰区。若需调整可编辑本文件后再 `/gsd-plan-phase 8`。

<domain>
## Phase Boundary

在**不破坏** v1.0/v1.1 已交付的下载管线、**全仓 `pytest` 无网**、**apibi 与 HTML 双路径**与 **`raw` 可关清洗** 的前提下，将 **CLEAN-01（不可见字符）** 与 **CLEAN-02（apibi 多类行内/尾缀水印）** 落到 `text_clean`（及统一调用点），并**以合成字符串 + 黄金用例**锁定回归；**不**实施 Phase 9/10（MAIN/CFG）。

**可选** `E2E-01`（仅 HTML 目录回退抽测）若未在本 phase 排期，则留在 `deferred` / 独立验证，不阻塞 Phase 8 收束（见 `REQUIREMENTS.md`）。

</domain>

<decisions>
## Implementation Decisions

### 与 Phase 5 的关系

- **D-00:** 继承 **`.planning/phases/05-output-quality/05-CONTEXT.md` 的 D-01～D-12**（单模块、统一出口、默认开清洗、`raw`、数据驱动模式列表、不 `import novel_downloader` 作测试入口等）。本阶段在其上**只增**规则与单测，不改里程碑边界。

### U+FEFF / CLEAN-01

- **D-01:** 在 `clean_chapter_text` 内、于换行规范化**之后**、其余清洗**之前**，移除全部 **U+FEFF**（BOM / 误用为行首的 ZWNBSP，见 E2E）。实现上可用 `str.replace("\ufeff", "")` 或等价遍历；**不**把其它非 ASCII 当噪声删除。  
- **D-02:** **`raw=True` 时同样移除 U+FEFF**（与换行统一并列，属「传输/源站元字节」而非作者叙事）。`README` 中 **一句** 说明：raw 仍会做「换行统一 + 去 BOM/FEFF」，不删广告营销串。若与旧表述冲突，以本决策为准。  
- **D-03:** 错误提示短句分支（`无法解析` / `下载失败` 且过短）在 **去除 FEFF 与换行统一后** 仍**不**做重度假营销替换，与 Phase 5 一致。  

### apibi 水印 / CLEAN-02

- **D-04:** 在 **非 raw** 路径，向现有「数据驱动」列表 **追加** 针对 E2E 已证形态的行内/尾缀模式，**至少**覆盖：  
  - `jqxs` 与 `⊙`、`cc` 的组合（变体：可选空白、全半角）  
  - `gctxt` 与 `点`/`cc` 的组合（与 E2E「gctxt点cc」同族）  
  具体正则由实现者编写，**必须**有单测对合成串锁定。  
- **D-05:** 优先 **行内 `sub` 去片段**；仅当 E2E 或单测证明存在**整行**纯推广时再增加行级规则，且不得与 **D-06** 冲突。  
- **D-06（误伤防护）:** 保留并强化 Phase 5 的边界：对话/叙事中含「顶点」**但非营销独立行**的句子**不删**；新正则需在 `tests/test_text_clean.py` 中增加 **对攻用例**（可含 E2E **匿名化** 短句，不引入整本版权文本）。  
- **D-07:** **不**在 Phase 8 要求全量重跑 E2E 下载；以 **合成 + 可选本地人工对照** 为满足。HTML 与 apibi 共用**同一** `clean_chapter_text` 入口；若某规则仅 apibi 命中率高，仍放在同一函数内，可用注释/命名分区。

### 测试与 CI

- **D-08:** 扩展 `tests/test_text_clean.py`（或经评审的拆分文件，仍须 **无** `novel_downloader` 顶栏 import）：覆盖 **FEFF**、**新水印**、**raw+FEFF**、**防误伤** 至少各 1 组；可 `parametrize`。  
- **D-09:** 根目录 `pytest` 全绿；不新增**必须**联网的测试。  

### Claude's Discretion

- 各正则的 Unicode 变体（全角点、多余空格）在实现中迭代；  
- 是否在单独模块中拆 `_strip_bom` 命名函数；  
- 若发现 `⊙` 与作者数学/特殊符号极罕见冲突，在 CONTEXT / 注释中记一条「可回退 raw」而不扩大本 phase 到 NLP。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路标

- `.planning/ROADMAP.md` — **Phase 8** 成功标准、与 Phase 9/10 的边界  
- `.planning/REQUIREMENTS.md` — **CLEAN-01**、**CLEAN-02**、可选 **E2E-01**  
- `.planning/STATE.md` — 当前聚焦 Phase 8  

### 前序已锁定决策

- `.planning/phases/05-output-quality/05-CONTEXT.md` — 清洗职责、单入口、`raw`、测试约束（D-01～D-12）  

### 实证与 Backlog 溯源

- `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md` — 书号 6094 抽测、FEFF 计数、jqxs/gctxt 粗测  

### 实现锚点

- `text_clean.py` — `clean_chapter_text` 全链路  
- `novel_downloader.py` — `NovelDownloader._finalize_chapter_text` 调用点（仅规划定位，**本 phase 以 `text_clean` 与测为主**）  
- `tests/test_text_clean.py` — 扩展用例主位置  
- `.planning/codebase/CONCERNS.md` — 不扩大为流式落盘/站点插件  

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `text_clean.clean_chapter_text` — 唯一正文清洗出口；已存在换行、行内 `bqfun ⊕`、行级垃圾行、`raw` 分支。  
- `tests/test_text_clean.py` — 参数化与「不误杀」范式可复用。  

### Established Patterns

- 规则表 `_INLINE_NOISE` + 编译正则可扩展；**禁止**在 `novel_downloader` 内再散落水印字面量。  

### Integration Points

- `get_chapter_content` 在返回用户可见正文前经 `_finalize_chapter_text`；**Phase 8 原则** 为改 `text_clean` + 测即可，除非 FEFF 需更早剥离（经评审再动调用顺序）。当前顺序已为先 `_normalize_newlines` 再他处，**插入 FEFF 步** 放在 normalize 后最自然。  

</code_context>

<specifics>
## Specific Ideas

- E2E 中 **每章一个 U+FEFF** 的场景，用 **单章合成串** 回归即可（`"\\ufeff正文"` → 无 U+FEFF）。  
- **jqxs ⊙cc** 与 **gctxt点cc** 作为**首组**高优先级 apibi 模式；后续若新站新串，再开 Phase 或 backlog，**不**在 Phase 8 无限加规则。  

</specifics>

<deferred>
## Deferred Ideas

- **E2E-01:** 对**仅 HTML 目录**的书做一次全书或长抽样下载，和 apibi 路径对照；发现解析差异时记入 `CONCERNS` 或新 phase，不阻塞本 phase。  
- 将全库水印做成 **YAML/JSON 外置数据文件** — 可维护性佳，但超出「棕地小步」时再放入 backlog。  

### Reviewed Todos (not folded)

- `todo match-phase` 对 Phase 8 **无** 匹配项 — 无。  

**None in scope creep sense** — 讨论未引入新能力，仅细化了 CLEAN-01/02 的可执行性。  

</deferred>

---

*Phase: 08-deep-clean-pytest-apibi*  
*Context gathered: 2026-04-23*  
