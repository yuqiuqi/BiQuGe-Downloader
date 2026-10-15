"""xbiquge.info search, catalog and chapter parser."""
from __future__ import annotations
import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

BASE = "https://www.xbiquge.info/"
BOOK_RE = re.compile(r"^/\d+/\d+/$")
CHAPTER_RE = re.compile(r"^/\d+/\d+/\d+\.html$")

def _safe_url(href, base=BASE):
    url = urljoin(base, href)
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in ("www.xbiquge.info", "xbiquge.info"):
        raise ValueError("仅支持 xbiquge.info 站内链接")
    return url

def _soup(session, url, **kwargs):
    response = session.get(url, timeout=(10, 25), **kwargs)
    response.raise_for_status()
    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "lxml")

def search(session, keyword):
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("搜索关键字不能为空")
    soup = _soup(session, urljoin(BASE, "search.php"), params={"p": 1, "q": keyword})
    found, seen = [], set()
    for link in soup.select("a[href]"):
        href = link.get("href", "")
        if not BOOK_RE.fullmatch(urlparse(urljoin(BASE, href)).path):
            continue
        url = _safe_url(href)
        if url in seen:
            continue
        title = link.get_text(" ", strip=True)
        if not title:
            continue
        parent = link.find_parent(["li", "article", "tr", "div"])
        context = parent.get_text(" ", strip=True) if parent else ""
        author = re.search(r"作者[：:]\s*([^\s]+)", context)
        status = re.search(r"状态[：:]\s*(完本|连载|完结)", context)
        found.append({"title": title, "author": author.group(1) if author else "", "status": status.group(1) if status else "", "url": url})
        seen.add(url)
    return found

def catalog(session, book_url):
    book_url = _safe_url(book_url)
    path = urlparse(book_url).path
    if not BOOK_RE.fullmatch(path):
        raise ValueError("小说目录地址格式应为 /数字/数字/")
    soup = _soup(session, book_url)
    title = soup.find("h1")
    name = title.get_text(" ", strip=True) if title else (soup.title.get_text(" ", strip=True).split("_")[0] if soup.title else "未知小说")
    chapters, seen = [], set()
    for link in soup.select("a[href]"):
        url = _safe_url(link.get("href", ""), book_url)
        if not CHAPTER_RE.fullmatch(urlparse(url).path) or not urlparse(url).path.startswith(path) or url in seen:
            continue
        chapter_title = link.get_text(" ", strip=True)
        if chapter_title:
            seen.add(url)
            chapters.append((chapter_title, url))
    if not chapters:
        raise ValueError("目录中未找到章节，请检查页面结构")
    return name, chapters

def chapter(session, chapter_url):
    url = _safe_url(chapter_url)
    if not CHAPTER_RE.fullmatch(urlparse(url).path):
        raise ValueError("无效的章节地址")
    soup = _soup(session, url)
    node = next((soup.select_one(sel) for sel in ("#content", "#chaptercontent", ".read-content", ".content", "#txt") if soup.select_one(sel)), None)
    if node is None:
        raise ValueError("无法找到章节正文容器")
    for tag in node.select("script,style,ins"):
        tag.decompose()
    text = node.get_text("\n", strip=True)
    if len(text.strip()) < 20:
        raise ValueError("章节正文过短，可能被拦截")
    return text
