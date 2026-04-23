# Phase 1: 依赖与 CI 对齐 - Discussion Log

> **Audit trail only.** 规划/执行智能体以 `01-CONTEXT.md` 为准。  
> 本会话**未**进行多轮交互式逐题确认；下表记录「灰区 + 所采纳的推荐默认」。

**Date:** 2026-04-23  
**Phase:** 1 - 依赖与 CI 对齐  
**Areas discussed:** 依赖清单、版本策略、脚本自举、GitHub Actions、README  

---

## 依赖文件与版本策略

| Option | Description | Selected |
|--------|-------------|----------|
| 根目录 `requirements.txt` 仅含三包 | 与代码/import 及 workflow 当前显式包一致 | ✓ |
| 附带 optional extras 或第 4 个运行时包 | 本阶段不扩展范围 |  |
| 使用 pip-tools / poetry | 本阶段不引入，降低变更面 |  |

**User's choice:** 采纳「仅三包 + `requirements.txt`」（对应 CONTEXT **D-01、D-02**）。  
**Notes:** 版本用 `>=` 下限；可复现 lock 非本阶段。

---

## 是否在本阶段动「脚本内 pip 自举」

| Option | Description | Selected |
|--------|-------------|----------|
| 本阶段只对齐文档+CI+清单，不改脚本 | 与 PACK 范围、Phase 3 可维护性工作区分 | ✓ |
| 本阶段删除/警告自举 | 会扩大争议面，留待后续 |  |

**User's choice:** 不改（**D-03**）。

---

## CI 安装方式

| Option | Description | Selected |
|--------|-------------|----------|
| `pip install -r requirements.txt` | 与仓库单一事实来源一致 | ✓ |
| 保留逐包与 `-r` 双写 | 易漂移，不采用 |  |

**User's choice:** **D-04**（单一 `-r`）。可选保留 `pip install --upgrade pip` 首行由实现裁量（CONTEXT Claude's Discretion）。

---

## Python 版本与 matrix

| Option | Description | Selected |
|--------|-------------|----------|
| 单 job，Python 3.10 | 与现 workflow 一致 | ✓ |
| 多版本 matrix | 超出 Phase 1 边界 |  |

**User's choice:** **D-05**。

---

## README 侧重

| Option | Description | Selected |
|--------|-------------|----------|
| 推荐 venv + `pip install -r` 为主路径 | 专业协作默认 | ✓ |
| 仍以「脚本自举」为唯一说明 | 与工程化目标冲突 |  |

**User's choice:** **D-06**（主路径 venv+`-r`，自举为可选说明）。

---

## Claude's Discretion

- `requirements.txt` 中具体下界数字的微调。  
- workflow 内是否 `pip install --upgrade pip`。

## Deferred Ideas

- pytest、多版本 CI、移除自举：见 `01-CONTEXT.md` `<deferred>`。
