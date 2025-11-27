# Novel Downloader (小说下载器)

这是一个基于 Python 的多线程小说下载工具，专为下载笔趣阁（及同类结构站点）小说而设计。支持 GitHub Actions 自动化运行。

## ✨ 功能特点

- **🚀 多线程并发**：使用线程池实现高速下载。
- **🆔 智能 ID 识别**：直接输入小说 ID（如 `3953`）或完整 URL 即可下载。
- **🛠 自动环境配置**：脚本启动时自动检测并安装缺失的依赖库 (`requests`, `bs4`, `lxml`)。
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

- Python 3.6+
- 脚本会自动安装以下库：
  - `requests`
  - `beautifulsoup4`
  - `lxml`

## 🚀 使用方法

### 方式一：本地运行

1. 克隆仓库或下载 `novel_downloader.py` 文件。
2. 运行脚本：
   ```bash
   python novel_downloader.py
   ```
3. 根据提示输入 **小说 ID**（例如 `3953`）或 **完整目录地址**。
   - 示例输入 1：`3953`
   - 示例输入 2：`https://k.biqu68.com/book/3953/`
4. 等待下载完成，文件将保存在当前目录下。

### 方式二：命令行传参

直接在命令中附带 ID 或 URL：

```bash
# 使用 ID 下载
python novel_downloader.py 3953

# 使用 URL 下载
python novel_downloader.py https://k.biqu68.com/book/3953/
```

### 方式三：GitHub Actions (云端运行)

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

