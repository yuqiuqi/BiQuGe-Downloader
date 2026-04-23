# Phase 11 — 类水印/噪音二期（CLEAN-03）盘点

**日期:** 2026-04-24  
**来源:**

- `.planning/phases/999.1-apibi-watermark-bom/E2E-2026-04-23.md`（《领地》id=6094 apibi 抽测）  
- `.planning/phases/11-wm2-text-clean/11-CONTEXT.md`（阶段决策 D-00～D-08）  
- 实现：`text_clean.py`  
- 单测：`tests/test_text_clean.py`  

## 1. E2E 已列残留族 → 代码与单测映射

| E2E §4 描述（摘要） | `text_clean` 落点 | 单测（示例） |
|---------------------|-------------------|--------------|
| U+FEFF 每章行首（§2） | `_strip_feff` → `clean_chapter_text` 早段 | `test_strips_feff_default_and_raw` 等（Phase 8） |
| `bqfun ⊕cc` 类 | `_INLINE_NOISE` 前 3 条 | `test_cleans_bqfun_inline_spam` |
| `jqxs ⊙ cc` 及变体 | `_INLINE_NOISE` `jqxs\s*⊙\s*cc` 等 | `test_jqxs_and_gctxt_spam_removed_when_not_raw`、`test_raw_keeps_marketing_but_strips_feff` |
| `gctxt点cc` / `gctxt.cc` | `_INLINE_NOISE` `gctxt\s*点\s*cc`、`gctxt\s*\.\s*cc` | 同上 + `test_gctxt_dot_ascii_variant` |
| 独立营销短行（「新顶点小说」等） | `_line_is_spam_line` | `test_spam_line_removed_when_whole_line`（parametrize） |
| 仅 `/read/<id>/` 行 | `_line_is_read_path` | `test_read_path_line_removed` |
| 叙事中含「顶点小说」不误删 | 行滤条件 + 无整行删 | `test_vertex_in_sentence_not_removed` |

以上与 **E2E-2026-04-23.md** 中「§4 与输出质量差距」所列族 **一致由 Phase 8（CLEAN-01/02）与当前 `text_clean` 覆盖**；仓库内 **无** 未映射的、带具体子串的新增 E2E 附件（全书 TXT 未入库，见 E2E 末注）。

## 2. 分类结论

### 已覆盖

- E2E 粗测列举的 **jqxs / gctxt / bqfun / ⊙ / ⊕ / 点cc** 族，已在 `_INLINE_NOISE` 与相关单测中体现；**FEFF**、**行级营销**、**read 路径行** 亦有专门用例。

### 本阶段可合入（无新子串时的「加固」）

- **不增加**无依据的新行内词根；在 **默认清洗**路径下为已有正则增加 **合成变体单测**（多余 ASCII/全角空白、行内间距），确保 **Unicode 空白** 与 **多空格** 仍被同一模式覆盖或显式断言。  
- 在 `text_clean.py` 增加 **Phase 11 / CLEAN-03** 与本文路径的**注释或 docstring 交叉引用**，便于维护者从代码跳回盘点。

### 需更多摘段 / 不宜本阶段自动化

- 若用户在未来提供 **未出现在 E2E 统计中的新推广串**（新站改版、新 apibi 字段），应 **先** 附 1～2 行合成复现，再开规则与单测。  
- **全章** 再跑 E2E 或联网 CI：**不在** Phase 11 必做项（见 `11-CONTEXT` 与 `ROADMAP` Phase 13 可选 E2E）。

## 3. 与 CLEAN-03 的明确结论

**结论:** 在**仅**依赖仓库内 E2E 文档与当前代码的情形下，**无**与 Phase 8 已收束族相矛盾的「必改新形态」子串可写；**CLEAN-03** 本轮回以 **单测回归加固 + 文档/注释交叉引用** 收束，满足「可测、可复现、不扩大无依据删除」的里程碑表述。若后续有用户摘段，可在 **下一会话** 增 `_INLINE_NOISE` 或行滤条目并复用本 INVENTORY 结构更新。

## 4. 可选后续（非阻塞）

1. 对 `jqxs`/`gctxt` 行内模式增加 **parametrize** 空白变体（见 `11-02` 单测提交）。  
2. 对 **HTML-only** 书籍做一次抽样，与 apibi 对照残留行类（`ROADMAP` Phase 13 / E2E-01）。  

---

*CLEAN-03 · Phase 8 基线 + Phase 11 盘点*  
*关联：`E2E-2026-04-23.md`、`11-CONTEXT.md`*  
