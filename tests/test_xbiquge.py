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
