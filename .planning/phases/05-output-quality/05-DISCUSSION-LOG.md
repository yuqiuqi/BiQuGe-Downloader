# Phase 5: 输出质量与测试 - Discussion Log

> **审计用。** 规划/执行以 `05-CONTEXT.md` 为准；本会话为无交互**一次性锁定**的决策说明。

**Date:** 2026-04-23  
**Phase:** 5 — 输出质量与测试  
**Mode:** 非 TUI 会话，未使用 conversational prompting；依据 ROADMAP / REQUIREMENTS / UAT 与代码扫描。  

---

## 清洗模块与集成点

| 方向 | 说明 | 采用 |
|------|------|------|
| A. 新模块纯函数 + 在 apibi 返回后统一调用 | 可测、低耦合 | ✓ |
| B. 仅在 `bqg_api` 内清洗 | 传输层混杂 | 否 |
| C. 仅在 `run()` 写盘时字符串替换 | 难测、HTML 路径易漏 | 否 |

**User's choice (proxy):** A  

## 默认是否清洗

| 选项 | 说明 | 采用 |
|------|------|------|
| 默认开 | 符合 UAT「可读、少噪音」 | ✓ |
| 默认关 | 保留与旧行为完全一致 | 否 |

**补充:** env/CLI 关闭（见 CONTEXT D-05）。

## 版式

| 项 | 采用 |
|----|------|
| 去文首前导空行 | ✓（UAT P2） |
| 章间不堆叠多余空行 | ✓（见 CONTEXT D-08） |

## Tests

| 项 | 采用 |
|----|------|
| 无网、不顶栏 import `novel_downloader` | ✓（延续 Phase 2 约定） |

## Deferred

- Phase 6/7 范围未纳入讨论（scope guardrail）。  

---

*Log generated: 2026-04-23*  
