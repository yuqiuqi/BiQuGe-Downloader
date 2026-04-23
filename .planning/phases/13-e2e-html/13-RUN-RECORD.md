# Phase 13 — 采数记录（13-01，机器可复现片段）

**日期:** 2026-04-24  
**书号/URL:** `3953` → 归一化 `https://m.bqg92.com/book/3953/`（`url_input.normalize_target_url`）  
**环境:** 仓库根、`python3`、依赖已装（`requests` 等）  

## 路径 A — apibi（默认 API）

**命令（节选，无额外 env）:**

```bash
cd /path/to/BiQuGe-Downloader
python3 -c "
from url_input import normalize_target_url
from novel_downloader import NovelDownloader
u = normalize_target_url('3953')
d = NovelDownloader(u)
ch = d.get_download_url() or []
print('use_api', d._use_api, 'n', len(ch))
if ch:
    print('first', ch[0][1])
"
```

**复现事实（本机当次）:**

- 终端出现 **`已连接 apibi 书库`**、**`API 目录共 113 章`**
- `d._use_api is True`；首章假链形如 **`apibi://3953/1`**
- apibi 书名（元数据）: 《亲妈被认回豪门后》 (id=3953)  

**判定依据:** `CHAPTER_URL_PREFIX` 前缀 + 上述日志 = **全程 API 章链**（见 `13-CONTEXT` D-00）。

---

## 路径 B — HTML 目录（apibi 书元拉取失败 → 无 API 目录）

**目的:** 使 `try_fetch_book_api` 失败，从而 **`_use_api` 不置真**，`get_download_url` 走 **`_get_chapters_from_page()`**（真实 `https://` 章链）。

**命令:**

```bash
export BQUGE_API_BASE='http://127.0.0.1:1/api'
cd /path/to/BiQuGe-Downloader
python3 -c "
from url_input import normalize_target_url
from novel_downloader import NovelDownloader
u = normalize_target_url('3953')
d = NovelDownloader(u)
ch = d.get_download_url() or []
print('use_api', d._use_api, 'n', len(ch))
if ch:
    print('first', ch[0][1])
"
```

**复现事实（本机当次）:**

- **未**出现「已连接 apibi 书库」；`d._use_api` 为 **False**
- 终端出现 **`HTTP状态码: 200`**、**`正在分析小说:`** 与 HTML 侧解析得到 **13** 个章节链接
- 首章 URL 形如 **`https://m.bqg92.com/kan/3953/1.html`**（真实 http(s)，非 `apibi://`）
- HTML 页内解析到的小说标题与 apibi 元数据**不一致**（见结论文档对照表；可能为站点同 ID 多版本/缓存/区块差异 — **不**在本记录贴长正文）  

**判定依据:** 无 apibi 书库成功日志、章链为网站 HTML 链接 = **HTML 目录路径**（D-00）。

---

## 两路径章数/元数据对比（摘要）

| 项 | 路径 A (apibi) | 路径 B (HTML) |
|----|----------------|-----------------|
| 章数 (N) | 113 | 13 |
| 书名片段（元数据/页） | 亲妈被认回豪门后（apibi） | 页内标题与 A 不同（需见终端） |
| 首章 URL 形态 | `apibi://3953/1` | `https://m.bqg92.com/kan/3953/1.html` |

**说明:** 同书号 **3953** 下，**两路径的目录项数量与标题来源不同**，可视为本 E2E 的**核心可观测差异**；非代码 bug 的自证，但需在结论文档写清**复现步骤与免责（站点/时间）**。

---

## 样章/正文

本 13-01 **未**全本下载；未新增正文摘抄。结论文档可只依赖目录级事实。  

---

*本文件为 `13-01-PLAN` 交付物，供 `13-02` 合并为 `E2E-*.md`。*
