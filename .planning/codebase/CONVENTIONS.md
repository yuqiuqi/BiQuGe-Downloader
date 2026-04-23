# Coding Conventions

**Analysis Date:** 2026-04-23

## Naming Patterns

**Files:**
- 单模块脚本：`novel_downloader.py`（`snake_case`）

**Classes / functions / methods:**
- 类名 `PascalCase`（`NovelDownloader`）
- 方法如 `get_download_url`, `get_chapter_content`, `run`, `save_to_file` 为 `snake_case`
- 局部变量 `camelCase` 与 `snake_case` 混用较少；多为 `soup`, `chapters`, `response` 等描述性小写

**Constants:**
- 无显式模块级常量枚举；`max_workers = 10` 等写死在 `run()` 内

**Private:**
- 无下划线约定私有成员

## Code Style

**Formatting:**
- 无 Black / Ruff / isort 配置文件；缩进为 4 空格
- 存在少量不一致空格（如 `if info_div and info_div.find('h2'):` 下一行多空格）

**Linting / typing:**
- 无 mypy / pyright 配置；仅 `get_download_url` 有返回意图注释，无全面类型标注

**Docstrings:**
- 模块与类有中文说明性注释；`get_download_url` / `get_chapter_content` 有简短 docstring

## Import Organization

**Order（`novel_downloader.py` 实际模式）:**

1. 标准库: `os`, `sys`, `subprocess`（用于自举安装依赖）
2. 动态安装后再 `import` 第三方：`requests`, `bs4`, `lxml` 相关在成功安装后
3. 后续标准库: `time`, `re`, `random`, `concurrent.futures`

**特点:** 因「先装再导」，第三方 import 不能全部置于文件最顶（设计使然）。

## Error Handling

**Patterns:**
- 网络/解析: 多层 `try/except`，常打印错误后返回空或默认字符串
- 安装失败: `subprocess` 失败则 `sys.exit(1)`
- 较少使用自定义异常类

**用户可见失败:**
- 「未找到章节」时退出码 1，便于 CI 显示失败

## Logging

- 无 logging 模块；以 `print` 和 `sys.stdout.write` 进度为主

## Comments

- 中文注释说明站点结构、反爬、历史 bug（如曾用 urllib、写入截断等）
- 部分分支保留「未完全实现的 fallback」注释（如目录未匹配时的 `pass`）

## Function Design

- `get_download_url` 与 `get_chapter_content` 体量大、分支多，承担解析与重试
- `save_to_file` 存在但未被 `run` 使用，易误导读者（见 `CONCERNS.md`）

## Module Design

- 单文件即应用；无 `__all__` 或包级导出
- 未来若拆包，建议将「站点选择器/解析器」与「线程调度 + 落盘」分离便于测试

---

*Convention analysis: 2026-04-23*  
*Update when introducing formatters, tests, or packaging*
