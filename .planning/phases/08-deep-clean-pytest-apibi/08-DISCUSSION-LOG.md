# Phase 8: 深度清洗与单测 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.  
> Decisions are captured in `08-CONTEXT.md`.

**Date:** 2026-04-23  
**Phase:** 8 - 深度清洗与单测  
**Mode:** 与 Phase 5 相同的 **无多轮用户菜单**；灰区由 ROADMAP / REQUIREMENTS / E2E-2026-04-23 / 05-CONTEXT 与代码审查收束。  

**Areas informally covered:** 不可见字符策略、apibi 水印扩展、raw 与 FEFF 关系、单测范围、E2E-01 是否进本 phase。

---

## 不可见字符（U+FEFF）

| Option | Description | Selected |
|--------|-------------|----------|
| A. 仅默认清洗去 FEFF，raw 保留 | 与「raw=原文」字面一致，但 E2E 认为 FEFF 非作者内容 |  |
| B. 默认 + raw 均去 U+FEFF，README 一句说明 | 与「可读、无噪声字节」一致；raw 仍保留广告串 | ✓ |
| C. 仅去章首第一个 FEFF | 实现较省，但 E2E 为「章内仍可出现」需再验 |  |

**收束选择:** **B**（见 CONTEXT **D-01、D-02**）。

---

## apibi 水印（jqxs / gctxt 族）

| Option | Description | Selected |
|--------|-------------|----------|
| A. 仅加 2～3 条行内正则以 E2E 为据 | 小步、可测、可回归 | ✓ |
| B. 外置 YAML 全量运营水印库 | 可维护，但超 Phase 8 小步 |  |
| C. 按站点分子模块文件 | 棕地可接受，本 phase 不强制 |  |

**收束选择:** **A** + 单测必带误伤对攻（**D-04～D-06**）。

---

## 可选 E2E-01（HTML 回退）

| Option | Description | Selected |
|--------|-------------|----------|
| A. 纳入 Phase 8 必验收 | 覆盖面大、阻塞 |  |
| B. 可选/后续验证 | 与 `REQUIREMENTS` 中 E2E-01 定位一致 | ✓ |

**收束选择:** **B**（见 CONTEXT `deferred`）。

---

## Claude's Discretion

- 正则细节、函数拆分命名、全角/半角变体。  

## Deferred Ideas

- HTML 路径全书 E2E、外置水印配置 — 已写入 CONTEXT `deferred`。  
