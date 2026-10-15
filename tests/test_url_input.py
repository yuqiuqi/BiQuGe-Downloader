# -*- coding: utf-8 -*-
import pytest

from url_input import normalize_target_url


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("https://www.xbiquge.info/12/345/", "https://www.xbiquge.info/12/345/"),
        ("www.xbiquge.info/12/345/", "https://www.xbiquge.info/12/345/"),
        ("  https://www.xbiquge.info/12/345/  ", "https://www.xbiquge.info/12/345/"),
        ("", ""),
        (" https://example.com/book/1/ ", "https://example.com/book/1/"),
    ],
)
def test_normalize_target_url(raw, expected):
    assert normalize_target_url(raw) == expected


@pytest.mark.parametrize("raw", ["3953", "  3953  ", "0003953"])
def test_numeric_legacy_book_id_is_rejected(raw):
    with pytest.raises(ValueError, match="完整目录 URL"):
        normalize_target_url(raw)
