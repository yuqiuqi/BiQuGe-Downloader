# -*- coding: utf-8 -*-
"""
笔趣阁新站：目录与正文由 apibi.cc JSON API 提供（浏览器中对应 *.bqg655.cc 单页应用）。

无浏览器依赖，纯 HTTP；供 NovelDownloader 在解析到书号时优先走此路径。
"""
from __future__ import annotations

import re
from typing import Any, List, Optional, Tuple

APBI_BASE = "https://apibi.cc/api"

# 传给 get_chapter_content 的伪 URL 前缀，避免与真实 http(s) 链接混淆
CHAPTER_URL_PREFIX = "apibi://"


def parse_book_id_from_url(url: str) -> Optional[str]:
    """
    从用户或跳转后的地址中提取书号（与 apibi 的 id 一致，与 m.bqg92.com 的 /book/数字 一般一致）。

    支持示例：
    - https://m.bqg92.com/book/3953/
    - https://xxxxx.bqg655.cc/#/book/1155/
    - https://xxxxx.bqg655.cc/book/1155/6693.html
    """
    if not url:
        return None
    m = re.search(r"#/book/(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/book/(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/kan/(\d+)", url)
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


def _get_json(session: Any, path: str, params: dict) -> Optional[dict]:
    import requests  # 延迟，与 novel_downloader 一致

    try:
        r = session.get(f"{APBI_BASE}/{path}", params=params, timeout=20)
        if r.status_code != 200:
            return None
        return r.json()
    except (requests.RequestException, ValueError):
        return None


def try_fetch_book_api(session: Any, book_id: str) -> Optional[dict]:
    data = _get_json(session, "book", {"id": book_id})
    if not data or "title" not in data:
        return None
    return data


def fetch_chapter_titles_api(session: Any, book_id: str) -> Optional[List[str]]:
    data = _get_json(session, "booklist", {"id": book_id})
    if not data or "list" not in data:
        return None
    lst = data.get("list")
    if not isinstance(lst, list):
        return None
    return [str(x) for x in lst]


def fetch_chapter_text_api(session: Any, book_id: str, chapter_index: int) -> Optional[str]:
    """
    返回单章纯文本；chapter_index 为 1..N，与站内核 chapterid 一致。
    """
    data = _get_json(
        session,
        "chapter",
        {"id": book_id, "chapterid": str(chapter_index)},
    )
    if not data:
        return None
    txt = data.get("txt")
    if not isinstance(txt, str):
        return None
    return txt
