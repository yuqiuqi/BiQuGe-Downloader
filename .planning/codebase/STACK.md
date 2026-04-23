# Technology Stack

**Analysis Date:** 2026-04-23

## Languages

**Primary:**
- Python 3.6+（README 声明；CI 使用 3.10）— 全部应用逻辑在 `novel_downloader.py`

**Secondary:**
- YAML — `/.github/workflows/manual_download.yml` 的 GitHub Actions 定义

## Runtime

**Environment:**
- CPython 解释器；无 Web 服务进程，为一次性 CLI/脚本执行模式

**Package Manager:**
- 无 `requirements.txt` / `pyproject.toml` 锁文件
- 依赖在运行时由脚本顶部逻辑通过 `pip install` 拉取，或在 CI 中 `pip install requests beautifulsoup4 lxml`（见 `.github/workflows/manual_download.yml`）

## Frameworks

**Core:**
- 无全栈 Web 框架；`requests` 提供 HTTP 客户端与 `Session`

**HTML 解析:**
- `beautifulsoup4` + `html.parser`（目录页）与 `lxml`（部分章节页解析在 `get_chapter_content` 中）

**并发:**
- 标准库 `concurrent.futures.ThreadPoolExecutor`（默认 `max_workers=10`）

**Testing:**
- 当前仓库中无单元测试或测试运行器配置

**Build / Dev:**
- 无构建步骤；可编辑运行 `python novel_downloader.py`

## Key Dependencies

**Critical:**
- `requests` — 会话、GET 章节与目录、URL 解析
- `beautifulsoup4` — 解析小说标题、目录链接、章节正文容器（`#content` / `.showtxt`）
- `lxml` — `BeautifulSoup(..., 'lxml')` 用于部分页面解析路径

**Standard library（核心用途）:**
- `re`, `random`, `time`, `os`, `sys`, `subprocess`（启动时补装依赖）, `concurrent.futures`

## Configuration

**Environment:**
- 无强制环境变量；目标站点 URL 或小说 ID 通过 CLI 参数或交互式 `input` 传入

**Build:**
- 无 `setup.py` / `pyproject.toml`；部署依赖 README 与 workflow 中的 `pip install` 行

## Platform Requirements

**Development:**
- 任意支持 Python 3 的系统；需网络访问目标小说站点

**Production / automation:**
- GitHub Actions `ubuntu-latest`，`actions/setup-python` 安装 3.10，手动触发 `workflow_dispatch`

---

*Stack analysis: 2026-04-23*  
*Update after major dependency or Python version changes*
