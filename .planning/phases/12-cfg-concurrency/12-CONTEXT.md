# Phase 12 — 可配置并发（CFG-01）

**Status:** 已执行（见 `12-SUMMARY.md`）  
**ROADMAP:** v1.3 Phase 12  

## 目标

用户可通过 **CLI**（`-j` / `--workers`）或环境变量 **`BQUGE_MAX_WORKERS`** 设置下载并发线程数，**默认 10** 与历史硬编码行为一致；README / `--help` 说明边界（1~64 上限与提示）。

**Depends on:** v1.0+ 下载能力；与 Phase 11 无代码耦合。  
