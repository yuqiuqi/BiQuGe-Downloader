# Novel Downloader (小说下载器)

这是一个基于 Python 的多线程小说下载工具，专为下载笔趣阁（及同类结构站点）小说而设计。支持 GitHub Actions 自动化运行。

## ✨ 功能特点

- **🚀 多线程并发**：使用线程池实现高速下载。
- **🆔 智能 ID 识别**：直接输入小说 ID（如 `3953`）或完整 URL 即可下载。
- **🛠 环境配置**：推荐用虚拟环境 + `requirements.txt` 预装依赖；**可选**地，直接运行脚本时仍会尝试自动 `pip` 安装缺失包（见 `novel_downloader.py`）。
- **🛡 智能防爬虫**：
  - 随机 User-Agent 伪装。
  - 请求头模拟（Referer, Accept 等）。
  - 随机延时机制，模拟真实用户行为。
- **📖 智能解析**：
  - 自动处理章节内分页（检测“下一页”并合并内容）。
  - 自动识别网页编码，防止乱码。
  - 自动去除广告内容。
- **📂 便捷保存**：自动在脚本同级目录下生成小说 TXT 文件。
- **🤖 GitHub Actions**：支持在云端自动运行并下载文件。

## 📦 依赖要求

- Python 3.6+（与 GitHub Actions 一致时**建议**使用 Python 3.10）
- 运行时需要 **requests**、**beautifulsoup4**、**lxml**（在 `requirements.txt` 中声明）

### 推荐安装（与 CI 一致）

在仓库根目录使用虚拟环境安装，与 **GitHub Actions** 使用同一份 `requirements.txt`：

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows（PowerShell）可使用: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**可选**：若不预先安装，脚本仍会尝试自动 `pip` 安装缺失依赖（见 `novel_downloader.py`）。

## 🧪 开发（运行测试）

在仓库根目录创建虚拟环境并同时安装运行依赖与开发依赖，然后执行 `pytest`：

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows（PowerShell）可使用: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pytest
# 安静模式：pytest -q
```

## 🚀 使用方法

### 方式一：本地运行

1. 克隆仓库或下载 `novel_downloader.py` 文件（完整克隆时推荐先按上文「推荐安装」创建 venv 并执行 `pip install -r requirements.txt`）。
2. 若已安装依赖，运行脚本：
   ```bash
   python novel_downloader.py
   ```
3. 根据提示输入 **小说 ID**（例如 `3953`）或 **完整目录地址**。
   - 示例输入 1：`3953`
   - 示例输入 2：`https://xxxxxxxxx/book/3953/`
4. 等待下载完成，文件将保存在当前目录下。

### 方式二：命令行传参

直接在命令中附带 ID 或 URL：

```bash
# 使用 ID 下载
python novel_downloader.py 3953

# 使用 URL 下载
python novel_downloader.py https://xxxxxxx.com/book/3953/
```

### 方式三：GitHub Actions (云端运行)

工作流在运行前会从仓库根目录的 `requirements.txt` 安装依赖，与本地推荐方式一致。

1. Fork 本仓库到你的 GitHub。
2. 点击仓库上方的 **Actions** 标签。
3. 选择左侧的 **Novel Downloader**。
4. 点击右侧的 **Run workflow**。
5. 在输入框中输入 **小说 ID** (如 `3953`) 或完整链接。
6. 等待任务运行显示 ✅ 成功。
7. 点击该次运行记录，滑动到底部找到 **Artifacts** 区域。
8. 点击 **novel-text-file**，浏览器会自动下载一个 ZIP 压缩包。
9. 解压该 ZIP 文件，即可获得小说的 TXT 文本文件。

## ⚠️ 免责声明

本项目仅供学习和技术交流使用。请勿用于商业用途，请尊重版权，支持正版小说。

