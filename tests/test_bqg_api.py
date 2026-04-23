# -*- coding: utf-8 -*-
import pytest

from bqg_api import (
    apibi_chapter_token,
    parse_apibi_chapter_token,
    parse_book_id_from_url,
    CHAPTER_URL_PREFIX,
)


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://m.bqg92.com/book/3953/", "3953"),
        ("https://a.b.bqg655.cc/#/book/1155/", "1155"),
        ("https://a.b.bqg655.cc/book/1155/6693.html", "1155"),
        ("https://m.bqg92.com/kan/520/", "520"),
    ],
)
def test_parse_book_id_from_url(url, expected):
    assert parse_book_id_from_url(url) == expected


def test_apibi_chapter_token_roundtrip():
    t = apibi_chapter_token("1155", 1)
    assert t.startswith(CHAPTER_URL_PREFIX)
    assert parse_apibi_chapter_token(t) == ("1155", 1)
    assert parse_apibi_chapter_token("https://x.com/1") is None
