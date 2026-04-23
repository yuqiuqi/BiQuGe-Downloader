# -*- coding: utf-8 -*-
"""
章节正文清洗：去源站常见水印/行内噪音（apibi/HTML 拉取后统一使用）。

仅标准库；可测、无网络。规则见 UAT 与 Phase 5 CONTEXT。
"""
from __future__ import annotations

import re
from typing import Callable, List, Tuple, Union

# ---------------------------------------------------------------------------
# 行级过滤：返回 True 表示整行删除
# ---------------------------------------------------------------------------


def _line_is_read_path(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return bool(re.fullmatch(r"/read/\d+/?", s))


def _line_is_spam_line(line: str) -> bool:
    s = line.strip()
    if not s or len(s) > 120:
        return False
    if "新顶点小说" in s or "手机版阅读网址" in s:
        return True
    if re.search(r"顶点小说.*(网址|阅读|手机版)|阅读网址", s) and "章节" not in s:
        return True
    return False


# ---------------------------------------------------------------------------
# 文本级替换（非 raw）
# ---------------------------------------------------------------------------

_INLINE_NOISE: List[Tuple[str, str]] = [
    (r"bqfun\s*⊕\s*cc", ""),
    (r"bqfun\s*⊕\s*c\s*c", ""),
    (r"\s*⊕\s*cc", ""),
]

_compiled_inline: List[Tuple[re.Pattern, str]] = [
    (re.compile(p, re.IGNORECASE), r) for p, r in _INLINE_NOISE
]


def _apply_inline_replacements(text: str) -> str:
    s = text
    for pat, repl in _compiled_inline:
        s = pat.sub(repl, s)
    return s


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _collapse_excessive_newlines(text: str) -> str:
    s = re.sub(r"\n{4,}", "\n\n\n", text)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.rstrip() + "\n" if s.strip() else s


def _filter_lines(text: str, raw: bool) -> str:
    if raw:
        return text
    out: List[str] = []
    for line in text.split("\n"):
        if _line_is_read_path(line):
            continue
        if _line_is_spam_line(line):
            continue
        out.append(line)
    return "\n".join(out)


def clean_chapter_text(text: str, raw: bool = False) -> str:
    """
    对单章正文做清洗。``raw=True`` 时不移除营销内容，仅统一换行符（及 harmless 规范化）。

    失败提示类短句应由调用方避免传入；如传入，仍做换行统一，不做行删以免误伤。
    """
    if not isinstance(text, str):
        text = str(text)
    t = _normalize_newlines(text)
    if raw:
        return t.rstrip() + "\n" if t.strip() else t

    # 过短且像错误信息：不做行过滤与重度替换
    if len(t) < 32 and any(x in t for x in ("无法解析", "下载失败")):
        return t.rstrip() + ("\n" if t.endswith("\n") else "")

    t = _apply_inline_replacements(t)
    t = _filter_lines(t, raw=False)
    t = _collapse_excessive_newlines(t)
    return t.rstrip() + "\n"
