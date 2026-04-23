# Phase 11: 类水印/噪音二期 - Discussion Log

> **审计用。** 下游研究/计划/执行以 `11-CONTEXT.md` 为准。  
> 本会话**未**进行多轮交互式灰区点选，采用与 Phase 8 相同的**无交互收束**策略。

**Date:** 2026-04-24  
**Phase:** 11-类水印/噪音二期（text_clean）  
**方式:** 负责人（agent）据 `ROADMAP`、`REQUIREMENTS` CLEAN-03、Phase 5/8 `*-CONTEXT` 与代码审计直接锁定决策。  

---

## 灰区与结论摘要

| 灰区 | 说明 | 结论 |
|------|------|------|
| 新规则依据 | 无摘段时是否允许猜规则 | **须**有 E2E/摘段/合成可复现串；可分两计划：先固样、后实现。 |
| 行内 vs 行级 | 与 Phase 8 策略是否一致 | **一致**，优先行内 `sub`，整行须配误伤用例。 |
| raw | 是否扩大 raw 下清洗 | **不扩大**；与 Phase 5/8 同，仅换行+FEFF。 |
| 范围 | 是否纳入 CFG/HTML E2E | **否**，记 deferred。 |

## Claude's Discretion

- 各正则的 Unicode/空白变体在实现中迭代，以 `tests/test_text_clean.py` 为真值来源。  

## Deferred Ideas

- 见 `11-CONTEXT.md` \<deferred\> 节。  
