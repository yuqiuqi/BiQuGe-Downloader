# -*- coding: utf-8 -*-
"""
笔趣阁新站：目录与正文由 apibi.cc JSON API 提供（浏览器中对应 *.bqg655.cc 单页应用）。

无浏览器依赖，纯 HTTP；供 NovelDownloader 在解析到书号时优先走此路径。

环境变量 ``BQUGE_API_BASE`` 可覆写 API 根路径（需以 /api 结尾或完整到域名，见 ``api_base``）。
"""
from __future__ import annotations

import os
import re
import time
from typing import Any, List, Optional, Tuple

_DEFAULT_APBI = "https://apibi.cc/api"


def api_base() -> str:
    """
    可通过环境变量 ``BQUGE_API_BASE`` 指定完整 API 根（须含 ``/api`` 路径，例如 ``https://apibi.cc/api``）。
    """
    return (os.environ.get("BQUGE_API_BASE") or _DEFAULT_APBI).strip().rstrip("/")

# 传给 get_chapter_content 的伪 URL 前缀，避免与真实 http(s) 链接混淆
CHAPTER_URL_PREFIX = "apibi://"


def parse_book_id_from_url(url: str) -> Optional[str]:
    """
    从用户或跳转后的地址中提取书号（与 apibi 的 id 一致，与 m.bqg92.com 的 /book/数字 一般一致）。

    尽量兼容：hash 路由、路径、查询串、手抄 API 地址等；多个命中时以前缀路径为准。
    """
    if not url or not str(url).strip():
        return None
    s = str(url).strip()

    if s.isdigit():
        return s

    patterns = (
        r"#/book/(\d+)",
        r"/book/(\d+)",
        r"/kan/(\d+)",
        r"(?:^|[?&])id=(\d+)(?:\D|$)",  # ?id= 或 &id=，避免吞掉后段数字
        r"(?:^|[?&])book_?id=(\d+)(?:\D|$)",
        r"apibi\.cc/api/book\b[^#]*[?&]id=(\d+)",
    )
    for p in patterns:
        m = re.search(p, s, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def apibi_chapter_token(book_id: str, chapter_index: int) -> str:
    """chapter_index 为 1 起始，与 /api/chapter?chapterid= 一致。"""
    return f"{CHAPTER_URL_PREFIX}{book_id}/{chapter_index}"


def parse_apibi_chapter_token(token: str) -> Optional[Tuple[str, int]]:
    m = re.match(
        re.escape(CHAPTER_URL_PREFIX) + r"(\d+)/(\d+)\Z", token, re.UNICODE
    )
    if not m:
        return None
    return m.group(1), int(m.group(2))


def _apibi_headers() -> dict:
    return {
        "Accept": "application/json, text/javascript, */*;q=0.1",
        "Referer": "https://m.bqg92.com/",
        "X-Requested-With": "XMLHttpRequest",
    }


def _get_json(session: Any, path: str, params: dict) -> Optional[dict]:
    import requests  # 延迟，与 novel_downloader 一致

    url = f"{api_base()}/{path.lstrip('/')}"
    for attempt in range(3):
        try:
            r = session.get(
                url,
                params=params,
                timeout=(10, 45),
                headers=_apibi_headers(),
            )
            if r.status_code != 200:
                time.sleep(0.3 * (attempt + 1))
                continue
            data = r.json()
            if isinstance(data, (dict, list)):
                return data
            return None
        except (requests.RequestException, ValueError):
            time.sleep(0.4 * (attempt + 1))
    return None


def try_fetch_book_api(session: Any, book_id: str) -> Optional[dict]:
    data = _get_json(session, "book", {"id": book_id})
    if not isinstance(data, dict) or "title" not in data:
        return None
    return data


def fetch_chapter_titles_api(session: Any, book_id: str) -> Optional[List[str]]:
    data = _get_json(session, "booklist", {"id": book_id})
    if not isinstance(data, dict) or "list" not in data:
        return None
    lst = data.get("list")
    if not isinstance(lst, list):
        return None
    return [str(x).strip() or f"第{i}章" for i, x in enumerate(lst, start=1)]


def fetch_chapter_text_api(session: Any, book_id: str, chapter_index: int) -> Optional[str]:
    """
    返回单章纯文本；chapter_index 为 1..N，与站内核 chapterid 一致。
    """
    data = _get_json(
        session,
        "chapter",
        {"id": book_id, "chapterid": str(chapter_index)},
    )
    if not isinstance(data, dict):
        return None
    txt = data.get("txt")
    if txt is None:
        return None
    if not isinstance(txt, str):
        return str(txt) if txt is not None else None
    return txt


# xbiquge.info HTML adapter. Keep the old API helpers above for compatibility.

from collections import deque
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

BASE = "https://www.xbiquge.info/"
BOOK_RE = re.compile(r"^/(\d+)/(\d+)/$")
INDEX_RE = re.compile(r"^/(\d+)/(\d+)/(?:index(?:_(\d+))?\.html)$")
CHAPTER_RE = re.compile(r"^/(\d+)/(\d+)/(\d+)\.html$")
MAX_CATALOG_PAGES = 200


def _safe_url(href, base=BASE):
    url = urljoin(base, href)
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in (
        "www.xbiquge.info", "xbiquge.info"
    ) or parsed.username or parsed.password or parsed.port not in (None, 80, 443):
        raise ValueError("仅支持 xbiquge.info 站内链接")
    return url


def _soup(session, url, **kwargs):
    response = session.get(url, timeout=(10, 25), **kwargs)
    response.raise_for_status()
    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "lxml")


def _catalog_root(book_url):
    url = _safe_url(book_url)
    path = urlparse(url).path
    match = BOOK_RE.fullmatch(path) or INDEX_RE.fullmatch(path)
    if not match:
        raise ValueError("小说目录地址格式应为 /数字/数字/ 或 /数字/数字/index_N.html")
    return urljoin(url, "/" + match.group(1) + "/" + match.group(2) + "/")


def search(session, keyword):
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("搜索关键字不能为空")
    soup = _soup(session, urljoin(BASE, "search.php"), params={"p": 1, "q": keyword})
    found, seen = [], set()
    for link in soup.select("a[href]"):
        try:
            url = _safe_url(link.get("href", ""))
        except (ValueError, TypeError):
            continue
        if not BOOK_RE.fullmatch(urlparse(url).path) or url in seen:
            continue
        title = link.get_text(" ", strip=True)
        if not title:
            continue
        parent = link.find_parent(["li", "article", "tr", "div"])
        context = parent.get_text(" ", strip=True) if parent else ""
        author = re.search(r"作者[：:]\s*([^\s]+)", context)
        status = re.search(r"状态[：:]\s*(完本|连载|完结)", context)
        found.append({"title": title, "author": author.group(1) if author else "",
                      "status": status.group(1) if status else "", "url": url})
        seen.add(url)
    return found


def catalog(session, book_url):
    """Read every linked catalog page; accept /book/ and index_N.html input."""
    start = _safe_url(book_url)
    root = _catalog_root(start)
    book_path = urlparse(root).path
    pending = deque([start])
    if start != root:
        pending.append(root)
    visited = set()
    chapters = {}
    page_errors = []
    name = "未知小说"

    while pending:
        if len(visited) >= MAX_CATALOG_PAGES:
            raise ValueError("目录分页超过安全上限，请检查页面分页链接")
        page = pending.popleft()
        if page in visited:
            continue
        visited.add(page)
        try:
            soup = _soup(session, page)
        except Exception as exc:
            page_errors.append(str(exc))
            continue
        if name == "未知小说":
            title = soup.find("h1")
            if title:
                name = title.get_text(" ", strip=True)
            elif soup.title:
                name = soup.title.get_text(" ", strip=True).split("_")[0]
        for link in soup.select("a[href]"):
            try:
                url = _safe_url(link["href"], page)
            except (ValueError, TypeError):
                continue  # External links are ordinary on these pages.
            path = urlparse(url).path
            if path.startswith(book_path) and CHAPTER_RE.fullmatch(path):
                title = link.get_text(" ", strip=True)
                if title and url not in chapters:
                    chapters[url] = title
            elif path.startswith(book_path) and (BOOK_RE.fullmatch(path) or INDEX_RE.fullmatch(path)):
                if url not in visited and url not in pending:
                    pending.append(url)

    if page_errors:
        raise ValueError("部分目录页读取失败，拒绝生成可能缺章的 TXT：" + "; ".join(page_errors[:3]))
    if not chapters:
        raise ValueError("目录中未找到章节，请检查页面结构")
    # Pages may show chapter links in reverse order or repeat the latest 12 chapters.
    # Chapter IDs in these URLs are generally assigned in reading order.
    def chapter_order(item):
        path = urlparse(item[0]).path
        return int(CHAPTER_RE.fullmatch(path).group(3))
    return name, [(title, url) for url, title in sorted(chapters.items(), key=chapter_order)]


def chapter(session, chapter_url):
    url = _safe_url(chapter_url)
    if not CHAPTER_RE.fullmatch(urlparse(url).path):
        raise ValueError("无效的章节地址")
    soup = _soup(session, url)
    node = next((soup.select_one(sel) for sel in (
        "#content", "#chaptercontent", ".read-content", ".content", "#txt"
    ) if soup.select_one(sel)), None)
    if node is None:
        raise ValueError("无法找到章节正文容器")
    for tag in node.select("script,style,ins"):
        tag.decompose()
    text = node.get_text("\n", strip=True)
    if len(text.strip()) < 20:
        raise ValueError("章节正文过短，可能被拦截")
    return text
