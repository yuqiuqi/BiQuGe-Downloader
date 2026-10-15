import pytest
from bqg_api import search, catalog, chapter, _safe_url

class Response:
    encoding = "utf-8"
    apparent_encoding = "utf-8"
    def __init__(self, text):
        self.text = text
    def raise_for_status(self):
        pass

class Session:
    def __init__(self, text):
        self.text = text
    def get(self, url, **kwargs):
        return Response(self.text)

def test_search():
    html = '<li><a href="/12/345/">测试小说</a> 作者：某作者 状态：连载</li>'
    assert search(Session(html), "测试")[0]["author"] == "某作者"

def test_catalog():
    html = '<h1>测试小说</h1><a href="/12/345/123.html">第一章</a>'
    name, chapters = catalog(Session(html), "https://www.xbiquge.info/12/345/")
    assert name == "测试小说"
    assert len(chapters) == 1

def test_chapter():
    html = '<div id="content">这是一段用于单元测试的章节正文，至少需要二十个字符。</div>'
    assert "章节正文" in chapter(Session(html), "https://www.xbiquge.info/12/345/123.html")

def test_external_url_rejected():
    with pytest.raises(ValueError):
        _safe_url("https://example.org/12/345/")


def test_paginated_catalog_collects_all_chapters_and_ignores_external_links():
    root = "https://www.xbiquge.info/11/11549/"
    pages = {
        root: '<h1>测试长篇</h1><a href="/11/11549/302.html">第二章</a>'
              '<a href="/11/11549/index_1.html">1</a>'
              '<a href="https://external.example/11/11549/404.html">外部广告</a>',
        root + "index_1.html": '<a href="/11/11549/301.html">第一章</a>'
                                '<a href="/11/11549/index_2.html">2</a>',
        root + "index_2.html": '<a href="/11/11549/303.html">第三章</a>',
    }

    class PageSession:
        def get(self, url, **kwargs):
            assert url in pages, url
            return Response(pages[url])

    title, chapters = catalog(PageSession(), root + "index_1.html")
    assert title == "测试长篇"
    assert [chapter_title for chapter_title, _ in chapters] == [
        "第一章", "第二章", "第三章"
    ]


def test_paginated_catalog_fails_on_missing_pages():
    root = "https://www.xbiquge.info/11/11549/"

    class BrokenSession:
        def get(self, url, **kwargs):
            if url.endswith("index_2.html"):
                raise ConnectionError("simulated missing page")
            return Response('<h1>书名</h1><a href="/11/11549/301.html">第一章</a>'
                            '<a href="/11/11549/index_2.html">2</a>')

    with pytest.raises(ValueError, match="部分目录页读取失败"):
        catalog(BrokenSession(), root)


def test_catalog_rejects_non_catalog_chapter_url():
    with pytest.raises(ValueError, match="目录地址格式"):
        catalog(Session(""), "https://www.xbiquge.info/11/11549/301.html")


def test_search_skips_external_book_link():
    html = ('<li><a href="https://external.example/12/345/">欺骗链接</a></li>'
            '<li><a href="/12/345/">正确小说</a> 作者：作者A</li>')
    found = search(Session(html), "正确")
    assert len(found) == 1
    assert found[0]["title"] == "正确小说"
