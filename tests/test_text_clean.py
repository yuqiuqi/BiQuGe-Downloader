# -*- coding: utf-8 -*-
import pytest

from text_clean import clean_chapter_text


def test_cleans_bqfun_inline_spam():
    s = "正文一行 bqfun ⊕cc 后文继续。\n第二段。"
    out = clean_chapter_text(s, raw=False)
    assert "bqfun" not in out
    assert "⊕" not in out
    assert "正文一行" in out
    assert "后文继续" in out


def test_raw_mode_normalizes_crlf_only():
    inp = "第一行\r\n第二行\rbqfun ⊕cc 应保留"
    out = clean_chapter_text(inp, raw=True)
    assert "bqfun" in out
    assert "\r" not in out
    assert out == "第一行\n第二行\nbqfun ⊕cc 应保留\n"


@pytest.mark.parametrize(
    "spam_line",
    [
        "新顶点小说 手机阅读",
        "手机版阅读网址: https://example.com",
    ],
)
def test_spam_line_removed_when_whole_line(spam_line):
    body = f"章节开始。\n{spam_line}\n继续正文。"
    out = clean_chapter_text(body, raw=False)
    assert spam_line not in out
    assert "章节开始" in out
    assert "继续正文" in out


def test_read_path_line_removed():
    body = "段落一。\n/read/12345/\n段落二。"
    out = clean_chapter_text(body, raw=False)
    assert "/read/" not in out
    assert "段落一" in out
    assert "段落二" in out


def test_vertex_in_sentence_not_removed():
    s = "他说顶点小说网这篇写得不错，继续看。"
    out = clean_chapter_text(s, raw=False)
    assert s.strip() in out.replace("\n", "")


def test_error_short_phrase_not_heavily_scrubbed():
    s = "无法解析此章节内容"
    out = clean_chapter_text(s, raw=False)
    assert "无法解析" in out
