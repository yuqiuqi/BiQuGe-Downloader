# Phase 9 — Pattern Map

| 主题 | 当前形态 | 目标 |
|------|-----------|------|
| 整本书写入 | 仅 `run()` 内顺序 `write` | 无第二套 `save_to_file` API |
| 失败退出 | `sys.exit(1)` 当无章节 | 保留；增强 stderr/stdout 可读后仍 exit 1 |
| 文档真源 | `CONCERNS` 记死代码 | 删除代码后三处文档对齐 |
