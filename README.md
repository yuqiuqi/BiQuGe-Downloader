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

## GitHub Actions 使用教程（推荐，无需安装 Python）

**入口：[点击打开 Novel Downloader 工作流](https://github.com/yuqiuqi/BiQuGe-Downloader/actions/workflows/manual_download.yml)**

整个过程是 **搜索 → 从候选列表选书 → 下载 ZIP**。目前 GitHub Actions 无法在同一次手动运行中动态弹出搜索候选，因此需要**分别点击两次 Run workflow**。

### 0. 打开运行界面

1. 登录 GitHub，进入本仓库顶部的 **Actions** 标签。
2. 在左侧 **All workflows** 下点击 **Novel Downloader**。
3. 点击页面右侧的 **Run workflow** 按钮。
4. 在 **Use workflow from** 中选择 **Branch: main**。
5. 根据下面的搜索或下载步骤填写参数，再点击弹窗底部的绿色 **Run workflow**。

> 如果看不到 **Run workflow**，确认已登录、有权运行该仓库的工作流、工作流存在于默认分支且仓库 Actions 已启用。

### 1. 第一次运行：搜索小说

选择 `mode = search`，填写关键词：

| 界面字段 | 示例值 | 说明 |
| --- | --- | --- |
| **mode** | `search` | 搜索模式 |
| **keyword** | `三体` | 可输入书名、作者或拼音；匹配情况取决于网站 |
| **novel_id** | *留空* | 搜索时不用填 |
| **workers** | `5` | 搜索时不生效，保留默认值 |

提交后，GitHub Actions 列表会出现一条新的运行记录（可能先显示黄色等待图标）。点击该记录，等待任务执行结束。

**查看搜索结果有两种方式：**

1. **直接看日志**：点击 `download` 任务，再展开 **Search or download** 步骤。日志中会打印候选书籍 JSON，包含 `title`、`author`、`status`、`url` 等字段（字段可能为空）。
2. **下载候选列表**：回到该次运行记录的概览页，在底部 **Artifacts** 找到 **novel-results**，下载并解压，打开 `candidates.json`。

候选结果结构示意（**仅示意，不是真实搜索结果**）：

```json
[
  {
    "title": "示例小说",
    "author": "示例作者",
    "status": "连载",
    "url": "https://www.xbiquge.info/12/345/"
  }
]
```

核对书名和作者后，**复制选中作品的完整 `url`**，下一步要用到它。

### 2. 第二次运行：下载小说

回到 [Novel Downloader 工作流页面](https://github.com/yuqiuqi/BiQuGe-Downloader/actions/workflows/manual_download.yml)，再次点击 **Run workflow**，仍选择 **main**，填写：

| 界面字段 | 示例值 | 说明 |
| --- | --- | --- |
| **mode** | `download` | 下载模式 |
| **keyword** | *留空* | 下载时不用填 |
| **novel_id** | `https://www.xbiquge.info/12/345/` | 粘贴第一步选中的**完整目录 URL** |
| **workers** | `5` | 下载并发线程数，建议先用默认值 |

> **重点：`novel_id` 虽然叫“ID”，但现在必须填完整的小说目录 URL（也支持 `index_1.html` 等目录分页地址），不能只填数字书号。** 表格中的 URL 仅演示格式，请换成实际搜索结果里的 URL。

提交后打开新的运行记录，等待 `download` 任务完成。`test` 会独立并行执行，不再阻止手动搜索或下载。

### 3. 下载 TXT / ZIP 文件

1. 打开**第二次运行（download）**的记录。
2. 向下找到 **Artifacts** 区域，点击 **novel-results**。
3. GitHub 会先下载一个用于传输 Artifact 的 ZIP 压缩包。
4. 解压后，找到程序生成的 **`小说名.zip`**；再次解压即可获得 **`小说名.txt`**。

因此看到**两层 ZIP 是正常的**：外层由 GitHub Artifacts 生成，内层由小说下载程序生成。

### 4. 运行失败时怎么排查？

| 现象 | 检查位置 | 可能原因或处理方法 |
| --- | --- | --- |
| 点击 Run workflow 后一直等待 | Actions 运行记录 | 等待 GitHub 分配 runner；检查 Actions 是否启用 |
| `test` 任务显示红叉 | `test` → `pytest -q` | 自动测试未通过，但不影响独立运行的下载任务；仍应修复测试 |
| 搜索没有候选结果 | `download` → `Search or download` | 关键词无结果、网站无法访问或搜索页面结构变化；尝试完整书名或作者 |
| 下载任务失败 | `download` → `Search or download` | 目录 URL 不正确、网站限流、章节页面结构变化或网络错误 |
| 没有 Artifacts | 运行记录底部 | `download` 未执行或没有生成符合上传规则的文件 |
| ZIP 缺少章节 | 任务日志及 TXT 内容 | 失败章节将记录在报告中，并使下载任务返回失败；请检查 ZIP 内的 report.json |

**工作流执行顺序：** 每次运行都会独立执行 `test`（安装依赖、运行 `pytest -q`）和 `download`；测试失败不再阻止搜索或下载。**即使 `mode=search`，执行搜索的任务也叫 `download`，这是工作流的内部任务名，不表示正在下载小说。**

搜索/下载任务中，`upload-artifact` 步骤设置为 `if: always()`，因此即使该任务中的命令失败，也会尝试上传已经生成的 `*.zip` 或 `candidates.json`；失败报告 `*.report.json` 也会单独上传（若已生成）。

> **当前版本说明：** 新站在线搜索和下载尚未完成端到端验证。如果首次运行失败，请在对应运行记录里展开红色步骤，复制错误日志用于排查。不要仅凭任务产生了 ZIP 就认定所有章节都完整。

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
