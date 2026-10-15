# BiQuGe Downloader · 小说下载器

基于 Python 的小说搜索与多线程下载工具，支持在本地运行，也支持通过 GitHub Actions 搜索、选择并下载小说。

> **当前主要适配站点：** https://www.xbiquge.info/  
> **使用前请注意：** 新站搜索、目录及章节解析尚未完成真实网站的端到端验证。网站页面结构变化、访问限制或网络问题都可能导致失败。本项目仅供合法、授权的个人使用，请尊重作品版权。

## 功能

- **关键词搜索**：通过书名、作者或拼音作为关键词查询候选书籍，结果包含可供选择的目录链接；具体匹配效果取决于目标站点的搜索能力。
- **先选书，再下载**：避免同名作品直接下载错误版本。
- **多线程下载**：默认 5 个线程，可通过命令行或 Actions 参数调整。
- **TXT 与 ZIP**：本地保存小说 TXT，同时生成包含 TXT 的 ZIP 压缩包。
- **GitHub Actions**：无需在电脑上配置 Python 环境，手动运行工作流并下载结果。

## GitHub Actions 使用教程（推荐）

进入 [仓库 Actions 页面](https://github.com/yuqiuqi/BiQuGe-Downloader/actions)，在左侧选择 **Novel Downloader**，点击 **Run workflow**，分支选择 **main**。

当前工作流需要运行 **两次**：第一次搜索，第二次下载。搜索结果不会自动变成下拉菜单，需要手动复制目标小说的目录 URL。

### 第一步：搜索小说

| 参数 | 填写内容 |
| --- | --- |
| `mode` | `search` |
| `keyword` | 小说名称、作者或拼音，例如 `三体` |
| `novel_id` | 留空 |
| `workers` | `5`（搜索时不使用） |

点击 **Run workflow**。任务结束后：

1. 打开该次运行记录，在 **Search or download** 步骤日志中查看候选列表。
2. 或在页面底部 **Artifacts** 中下载 **novel-results**，解压后查看 `candidates.json`。
3. 从候选列表中确认书名、作者，复制所选作品的完整 `url`。

### 第二步：下载所选小说

再次点击 **Run workflow**：

| 参数 | 填写内容 |
| --- | --- |
| `mode` | `download` |
| `keyword` | 留空 |
| `novel_id` | 第一步复制的**完整小说目录 URL** |
| `workers` | `5`（默认，可修改） |

**URL 格式示例**：`https://www.xbiquge.info/12/345/`（仅演示格式，不代表真实书籍）。

运行成功后，在 **Artifacts → novel-results** 下载 GitHub 打包的工作流附件。附件内部会包含程序生成的 `小说名.zip`；再解压一次即可获取小说 TXT。

**注意：** 参数名 `novel_id` 是原工作流沿用的名称，**目前应填写完整目录 URL，而不是纯数字 ID**。旧站书号与新站目录路径不一定对应。

### 为什么没有开始下载？

当前工作流包含两个任务：

1. `test`：安装依赖并运行 `pytest -q`。
2. `download`：只有 `test` 通过后才执行搜索或下载，并上传产物。

如果任务停在 `test`，请先打开失败步骤查看测试日志；如果 `Search or download` 失败，检查关键词、目录 URL、网站是否可访问及页面结构。工作流会在搜索/下载任务结束后尝试上传已经生成的文件，但失败时不保证有完整 ZIP。

## 本地运行

### 环境准备

建议使用 **Python 3.11**（与 GitHub Actions 一致）。

```bash
git clone https://github.com/yuqiuqi/BiQuGe-Downloader.git
cd BiQuGe-Downloader

python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

### 搜索

```bash
python novel_downloader.py --search "三体"
```

程序会打印候选书籍 JSON，并在当前目录保存 `candidates.json`。从中选择对应的 `url`。

### 下载

```bash
python novel_downloader.py "https://www.xbiquge.info/12/345/" --workers 5
```

示例 URL 仅表示目录路径格式，使用时请替换成搜索结果中的真实 URL。

并发数可以用 `-j 5`、`--workers 5` 或环境变量 `BQUGE_MAX_WORKERS=5` 配置。命令行参数优先，代码限制并发数最多为 64；为减少站点压力，建议使用默认值 5 或更低。

可选参数：

- `--raw-text`：跳过营销水印等文本清洗规则（仍会进行基础换行处理）。
- `--help`：查看完整命令行选项。

下载完成后，项目目录中会生成 `小说名.txt` 和 `小说名.zip`。

## 开发与测试

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

主要文件：

| 文件 | 作用 |
| --- | --- |
| `novel_downloader.py` | 命令行入口、下载调度、正文清洗与 ZIP 输出 |
| `bqg_api.py` | 站点搜索、目录和章节获取，以及保留的历史 API 兼容逻辑 |
| `url_input.py` | 输入 URL 归一化 |
| `text_clean.py` | 章节文本清理 |
| `.github/workflows/manual_download.yml` | GitHub Actions 工作流 |

## 已知限制

- **新站尚未完成线上端到端验证**，搜索结果结构、章节内容选择器或站点限制可能变化。
- 目前使用的是**两次手动触发**的搜索与下载流程，并非网页内实时选择候选书籍。
- 下载线程执行失败、正文解析失败等异常的处理仍有改进空间；不要把生成 ZIP 直接视为所有章节均完整下载的证明。
- 旧站相关兼容代码可能仍保留在项目中，但不代表旧站仍然可用。
- 网站内容和访问规则可能发生变化，遇到问题请附上 Actions 日志反馈。

## 免责声明

本项目仅用于学习和技术交流，以及对有权访问和保存的内容进行处理。请遵守适用法律、网站条款并尊重著作权。
