# -*- coding: utf-8 -*-
import pytest

from url_input import normalize_target_url


@pytest.mark.parametrize(
    "raw,expected",
    [
        (
            "3953",
            "https://m.bqg92.com/book/3953/",
        ),
        (
            "https://m.bqg92.com/book/3953/",
            "https://m.bqg92.com/book/3953/",
        ),
        (
            "m.bqg92.com/path",
            "https://m.bqg92.com/path",
        ),
        (
            "https://example.com/book/1/",
            "https://example.com/book/1/",
        ),
    ],
)
def test_normalize_target_url(raw, expected):
    assert normalize_target_url(raw) == expected
