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
