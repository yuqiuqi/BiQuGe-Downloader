<!-- gsd-project-start source:PROJECT.md -->
## Project

**BiQuGe Downloader（笔趣阁类小说下载器）**

基于 Python 的**命令行小说下载工具**：从笔趣阁结构站点拉取章节目录与正文，多线程获取后合并为单份 UTF-8 文本；支持通过小说 ID 或完整目录 URL 启动，并可用 GitHub Actions 在云端跑同一脚本产出 Artifact。面向自用与学习场景，不替代正版阅读。详见仓库 `README.md`。

**Core Value:** **稳定、可复现地**从用户给定的目录页，下载并合并**完整、可读**的章节正文到本地（或 CI Artifact）。

### Constraints

- **Python：** README 为 3.6+，CI 使用 3.10；新变更应避免无故抬高下限。
- **合规与版权：** 仅技术维护；不扩展为明显规避版权或站点条款的功能。
- **单仓库：** 无 monorepo；规划产物在 `.planning/`（见 `config.json` 中 `commit_docs`）。
<!-- gsd-project-end -->

<!-- gsd-stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.6+（README 声明；CI 使用 3.10）— 全部应用逻辑在 `novel_downloader.py`
- YAML — `/.github/workflows/manual_download.yml` 的 GitHub Actions 定义
## Runtime
- CPython 解释器；无 Web 服务进程，为一次性 CLI/脚本执行模式
- 无 `requirements.txt` / `pyproject.toml` 锁文件
- 依赖在运行时由脚本顶部逻辑通过 `pip install` 拉取，或在 CI 中 `pip install requests beautifulsoup4 lxml`（见 `.github/workflows/manual_download.yml`）
## Frameworks
- 无全栈 Web 框架；`requests` 提供 HTTP 客户端与 `Session`
- `beautifulsoup4` + `html.parser`（目录页）与 `lxml`（部分章节页解析在 `get_chapter_content` 中）
- 标准库 `concurrent.futures.ThreadPoolExecutor`（默认 `max_workers=10`）
- 当前仓库中无单元测试或测试运行器配置
- 无构建步骤；可编辑运行 `python novel_downloader.py`
## Key Dependencies
- `requests` — 会话、GET 章节与目录、URL 解析
- `beautifulsoup4` — 解析小说标题、目录链接、章节正文容器（`#content` / `.showtxt`）
- `lxml` — `BeautifulSoup(..., 'lxml')` 用于部分页面解析路径
- `re`, `random`, `time`, `os`, `sys`, `subprocess`（启动时补装依赖）, `concurrent.futures`
## Configuration
- 无强制环境变量；目标站点 URL 或小说 ID 通过 CLI 参数或交互式 `input` 传入
- 无 `setup.py` / `pyproject.toml`；部署依赖 README 与 workflow 中的 `pip install` 行
## Platform Requirements
- 任意支持 Python 3 的系统；需网络访问目标小说站点
- GitHub Actions `ubuntu-latest`，`actions/setup-python` 安装 3.10，手动触发 `workflow_dispatch`
<!-- gsd-stack-end -->

<!-- gsd-conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- 单模块脚本：`novel_downloader.py`（`snake_case`）
- 类名 `PascalCase`（`NovelDownloader`）
- 方法如 `get_download_url`, `get_chapter_content`, `run` 为 `snake_case`
- 局部变量 `camelCase` 与 `snake_case` 混用较少；多为 `soup`, `chapters`, `response` 等描述性小写
- 无显式模块级常量枚举；`max_workers = 10` 等写死在 `run()` 内
- 无下划线约定私有成员
## Code Style
- 无 Black / Ruff / isort 配置文件；缩进为 4 空格
- 存在少量不一致空格（如 `if info_div and info_div.find('h2'):` 下一行多空格）
- 无 mypy / pyright 配置；仅 `get_download_url` 有返回意图注释，无全面类型标注
- 模块与类有中文说明性注释；`get_download_url` / `get_chapter_content` 有简短 docstring
## Import Organization
## Error Handling
- 网络/解析: 多层 `try/except`，常打印错误后返回空或默认字符串
- 安装失败: `subprocess` 失败则 `sys.exit(1)`
- 较少使用自定义异常类
- 「未找到章节」时退出码 1，便于 CI 显示失败
## Logging
- 无 logging 模块；以 `print` 和 `sys.stdout.write` 进度为主
## Comments
- 中文注释说明站点结构、反爬、历史 bug（如曾用 urllib、写入截断等）
- 部分分支保留「未完全实现的 fallback」注释（如目录未匹配时的 `pass`）
## Function Design
- `get_download_url` 与 `get_chapter_content` 体量大、分支多，承担解析与重试
- 章节写入仅在 `run()` 内完成（历史 `save_to_file` 已移除，Phase 9）
## Module Design
- 单文件即应用；无 `__all__` 或包级导出
- 未来若拆包，建议将「站点选择器/解析器」与「线程调度 + 落盘」分离便于测试
<!-- gsd-conventions-end -->

<!-- gsd-architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- 无分层后端；核心为单一类 `NovelDownloader`（`novel_downloader.py`）
- 目录抓取与正文章节抓取均同步函数，用线程池对章节 URL 并行拉取
- 状态主要为 `requests.Session`、解析出的 `chapters` 列表与每章内容字典 `results`
- 无持久化服务；运行结束即退出
## Layers
- 职责: 解析 `sys.argv[1]` 或交互式输入，将纯数字补全为 `https://m.bqg92.com/book/{id}/`，必要时补全 `https://` 前缀，构造 `NovelDownloader` 并调用 `run()`
- 位置: `if __name__ == "__main__":` 块
- `get_download_url()`: 拉目录页、解析 `book_id`、收集章节链接触 `temp_chapters`，按 URL 中章节 id 排序
- `get_chapter_content(url)`: 单章多页循环保底（「下一页」链），去广告片段，重试与 `time.sleep` 防爬
- `run()`: 调用目录解析 → 线程池 `submit(get_chapter_content)` → `as_completed` 收集到 `results` → 按索引顺序 `open(..., 'a', encoding='utf-8')` 写入整本 TXT
- 无章节时 `run()` 打印 `_empty_catalog_diagnostics()` 并以退出码 1 结束（MAIN-02）
## Data Flow
- 多次 GET 同一章的分页，直到无「下一页」或达页数上限
- 无跨运行持久状态；同一次运行内以内存字典 `results` 保证乱序完成线程仍能顺序落盘
## Key Abstractions
- 代表一次「从目录 URL 到单文件」的下载任务
- 封装 `Session` 头、小说名、目标 URL
- `List[Tuple[title, href]]`，排序键为 URL 中的数字 id（`get_id`）
## Entry Points
- 位置: `novel_downloader.py` 模块级 `if __name__ == "__main__"`
- 触发: `python novel_downloader.py [url_or_id]` 或无参交互
- 职责: 参数规范化并调用 `NovelDownloader(target_url).run()`
- `.github/workflows/manual_download.yml` 中 `python novel_downloader.py "${{ github.event.inputs.novel_id }}"`
## Error Handling
- `get_download_url` 外层 `try/except` 返回空列表
- `get_chapter_content` 在解析失败时可能返回错误描述字符串，仍参与写入
- 文件写入有 `try/except` 打印错误
## Cross-Cutting Concerns
- 随机 `User-Agent`、常见浏览器头、章节间 `random.uniform(0.1, 0.3)` 延时、Referer
- 站点结构变更时目录或正文选择器失效会导致整体失败，需人工修 HTML 逻辑
<!-- gsd-architecture-end -->

<!-- gsd-skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.cursor/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- gsd-skills-end -->

<!-- gsd-workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- gsd-workflow-end -->



<!-- gsd-profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- gsd-profile-end -->
