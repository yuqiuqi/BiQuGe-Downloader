# Phase 8 — Execution Summary

**Date:** 2026-04-23  
**Plans:** 08-01（U+FEFF）, 08-02（jqxs/gctxt + README + 全量 pytest）

## Shipped

- `text_clean._strip_feff`：换行规范化后、全路径去除 `\ufeff`；`raw=True` 仍去 FEFF，不跑营销行内/行滤。  
- `_INLINE_NOISE` 增加 `jqxs⊙cc`、`gctxt点cc`、`gctxt.cc` 族（`re.IGNORECASE`）。  
- `tests/test_text_clean.py`：FEFF、raw+FEFF、jqxs/gctxt、ASCII 点变体。  
- `README`：raw 与 U+FEFF 一句说明。  

## Verify

- `pytest`（根目录，无参）24 passed。

## Follow-up

- **E2E-01**（HTML 回退）仍为可选，未本 phase 必跑。  
