# Architecture

**Analysis Date:** 2026-04-23

## Pattern Overview

**Overall:** 单文件、面向脚本的**命令行批处理工具**，通过 HTTP 爬取 + 内存中汇总结果、最后顺序写盘。

**Key Characteristics:**
- 无分层后端；核心为单一类 `NovelDownloader`（`novel_downloader.py`）
- 目录抓取与正文章节抓取均同步函数，用线程池对章节 URL 并行拉取
- 状态主要为 `requests.Session`、解析出的 `chapters` 列表与每章内容字典 `results`
- 无持久化服务；运行结束即退出

## Layers

**脚本入口 / CLI 层**
- 职责: 解析 `sys.argv[1]` 或交互式输入，将纯数字补全为 `https://m.bqg92.com/book/{id}/`，必要时补全 `https://` 前缀，构造 `NovelDownloader` 并调用 `run()`
- 位置: `if __name__ == "__main__":` 块

**网络与 HTML 层（`NovelDownloader` 方法级）**
- `get_download_url()`: 拉目录页、解析 `book_id`、收集章节链接触 `temp_chapters`，按 URL 中章节 id 排序
- `get_chapter_content(url)`: 单章多页循环保底（「下一页」链），去广告片段，重试与 `time.sleep` 防爬

**协调与 I/O 层**
- `run()`: 调用目录解析 → 线程池 `submit(get_chapter_content)` → `as_completed` 收集到 `results` → 按索引顺序 `open(..., 'a', encoding='utf-8')` 写入整本 TXT；无章节时打印 `_empty_catalog_diagnostics()` 并以退出码 1 结束

## Data Flow

**用户执行 → 成书 TXT:**

1. 用户或 CI 传入目录 URL 或 book id（`novel_downloader.py` 末尾）
2. `get_download_url()` HTTP GET 目录，BeautifulSoup 提取章节 `(title, url)` 列表
3. `ThreadPoolExecutor` 为每章 `submit` `get_chapter_content(url)`，结果写入 `results[index]`
4. 按 `0..N-1` 顺序将标题与正文写入 `safe_novel_name.txt`

**单章多页内循环 (`get_chapter_content`):**
- 多次 GET 同一章的分页，直到无「下一页」或达页数上限

**State Management:**
- 无跨运行持久状态；同一次运行内以内存字典 `results` 保证乱序完成线程仍能顺序落盘

## Key Abstractions

**`NovelDownloader`**
- 代表一次「从目录 URL 到单文件」的下载任务
- 封装 `Session` 头、小说名、目标 URL

**章节列表**
- `List[Tuple[title, href]]`，排序键为 URL 中的数字 id（`get_id`）

## Entry Points

**CLI 主入口**
- 位置: `novel_downloader.py` 模块级 `if __name__ == "__main__"`
- 触发: `python novel_downloader.py [url_or_id]` 或无参交互
- 职责: 参数规范化并调用 `NovelDownloader(target_url).run()`

**CI 入口**
- `.github/workflows/manual_download.yml` 中 `python novel_downloader.py "${{ github.event.inputs.novel_id }}"`

## Error Handling

**策略:** 以打印消息与 `return []` / 占位字符串（如「无法解析此章节内容」）为主；致命失败（无章节）时 `sys.exit(1)`。

**模式:**
- `get_download_url` 外层 `try/except` 返回空列表
- `get_chapter_content` 在解析失败时可能返回错误描述字符串，仍参与写入
- 文件写入有 `try/except` 打印错误

## Cross-Cutting Concerns

**防爬 / 礼仪:**
- 随机 `User-Agent`、常见浏览器头、章节间 `random.uniform(0.1, 0.3)` 延时、Referer
- 站点结构变更时目录或正文选择器失效会导致整体失败，需人工修 HTML 逻辑

**编码:** 使用 `response.apparent_encoding` 与 UTF-8 写文件，减轻乱码问题

---

*Architecture analysis: 2026-04-23*  
*Update when splitting modules or adding library-style APIs*
