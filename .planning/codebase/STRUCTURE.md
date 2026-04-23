# Codebase Structure

**Analysis Date:** 2026-04-23

## Directory Layout

```
BiQuGe-Downloader/
├── .github/
│   └── workflows/
│       └── manual_download.yml   # 手动触发的下载 workflow
├── novel_downloader.py           # 主程序：下载器类 + CLI
├── README.md                     # 使用说明与免责声明
├── LICENSE
└── .gitignore                    # 标准 Python / 工具忽略项
```

## Directory Purposes

**`.github/workflows/`**
- 存放 GitHub Actions；当前仅 `manual_download.yml`，负责安装依赖、运行 `novel_downloader.py`、上传 `*.txt` artifact

**项目根**
- 单文件应用：所有 Python 业务逻辑在 `novel_downloader.py`

## Key File Locations

**Entry Points:**
- `novel_downloader.py` — CLI 与 `NovelDownloader.run()`

**Configuration:**
- 无独立配置文件；工作流在 `manual_download.yml` 中固定 Python 3.10 与 pip 依赖

**Core Logic:**
- `novel_downloader.py` 内 `NovelDownloader` 类及启动时的 `install_package` 辅助逻辑

**Testing:**
- 无 `tests/` 或 `test_*.py`

**Documentation:**
- `README.md` — 功能、安装、本地与 Actions 使用步骤

## Naming Conventions

**Files:**
- 主脚本使用 `snake_case.py`（`novel_downloader.py`）

**Classes / functions:**
- 类名 `PascalCase`（`NovelDownloader`），方法名 `snake_case`

**Generated outputs:**
- 运行时生成 `{安全化小说标题}.txt`，与脚本同目录

## Where to Add New Code

**新功能（例如 GUI、配置、多站点）:**
- 若仍保持小体量：继续在 `novel_downloader.py` 拆函数或新类
- 若变复杂：可引入 `package/` 子目录（如 `downloader/`, `sites/`）并把 CLI 保留为薄入口

**新自动化:**
- 其他 CI job：在 `.github/workflows/` 下新增 `.yml`

**测试（若引入）:**
- 建议 `tests/test_novel_downloader.py` 与 `pytest` 配置；当前未建立

## Special Directories

- **无** 生成物目录提交到仓库；下载的 `.txt` 为运行时产物，通常应留在 `.gitignore` 的考虑范围内（若希望忽略本地小说文件可扩展 ignore 规则）

---

*Structure analysis: 2026-04-23*  
*Update when directory layout or packaging changes*
