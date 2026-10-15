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


def test_multi_page_chapter_includes_all_pages():
    base = "https://www.xbiquge.info/11/11549/"
    pages = {
        base + "301.html": (
            '<div id="content">第一页的小说正文，包含一些用于验证分页处理的文字。</div>'
            '<a href="301_2.html">下一页</a>'
        ),
        base + "301_2.html": (
            '<div id="content">第二页的小说正文，包含另一段用于验证分页处理的文字。</div>'
            '<a href="302.html">下一章</a>'
        ),
    }

    class PageSession:
        def get(self, url, **kwargs):
            assert url in pages, url
            return Response(pages[url])

    text = chapter(PageSession(), base + "301.html")
    assert "第一页" in text and "第二页" in text
    assert text.index("第一页") < text.index("第二页")


@pytest.mark.parametrize("path", [
    "/11/11549/",
    "/11/11549/index.html",
    "/11/11549/index_1.html",
    "/11/11549/index_25.html",
])
def test_supported_download_entry_urls(path):
    from bqg_api import _catalog_root
    assert _catalog_root("https://www.xbiquge.info" + path) == (
        "https://www.xbiquge.info/11/11549/"
    )


@pytest.mark.parametrize("url", [
    "https://www.xbiquge.info/11/11549/301.html",
    "https://www.xbiquge.info/book/11549/",
    "https://www.xbiquge.info/",
    "https://evil.example/11/11549/",
])
def test_unsupported_download_entry_urls(url):
    from bqg_api import _catalog_root
    with pytest.raises(ValueError):
        _catalog_root(url)


def test_live_style_article_font_max_content():
    html = (
        '<html><head><title>第1968章</title></head>'
        '<body><div class="container"><article class="font_max">'
        '这是一段与真实网站正文容器相同结构的章节文本。'
        '保留章节内容，并且不误把外围页面当作小说正文。'
        '</article></div><div id="footer">网站导航信息</div></body></html>'
    )
    result = chapter(Session(html), "https://www.xbiquge.info/11/11549/1163958.html")
    assert "这是一段与真实网站正文容器相同结构" in result
    assert "网站导航信息" not in result


def test_gateway_error_fails_over_to_official_alternate_host():
    url = "https://www.xbiquge.info/11/11549/1163959.html"
    backup = "https://xbiquge.info/11/11549/1163959.html"
    html = "<article class='font_max'>这里是通过备用域名成功获取的一段章节正文内容。</article>"

    class GatewayResponse(Response):
        status_code = 502
        def raise_for_status(self):
            raise RuntimeError("gateway 502")

    class GatewaySession:
        def __init__(self):
            self.urls = []

        def get(self, url, **kwargs):
            self.urls.append(url)
            return GatewayResponse("") if url.startswith("https://www.") else Response(html)

    session = GatewaySession()
    text = chapter(session, url)
    assert "备用域名" in text
    assert session.urls == [url, backup]


def test_522_gateway_falls_back_to_alternate_host():
    from bqg_api import _soup
    import requests
    class Resp:
        encoding = "utf-8"
        apparent_encoding = "utf-8"
        url = None
        def __init__(self, code, html=""):
            self.status_code = code
            self.text = html
        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(f"HTTP {self.status_code}")
    class Fake:
        calls = []
        def get(self, url, **kwargs):
            self.calls.append(url)
            if "www.xbiquge.info" in url:
                return Resp(522)
            return Resp(200, "<article class='font_max'>有效正文所在的章节标签</article>")
    sess = Fake()
    soup = _soup(sess, "http://www.xbiquge.info/11/11549/1163959.html")
    assert soup.select_one("article.font_max")
    assert sess.calls == [
        "https://www.xbiquge.info/11/11549/1163959.html",
        "https://xbiquge.info/11/11549/1163959.html"
    ]


def test_read_timeout_falls_back_to_alternate_host():
    from bqg_api import _soup
    import requests
    class Fake:
        calls = []
        def get(self, url, **kwargs):
            self.calls.append(url)
            if "www.xbiquge.info" in url:
                raise requests.ReadTimeout("simulated")
            return Response("<article class='font_max'>正文</article>")
    sess = Fake()
    soup = _soup(sess, "https://www.xbiquge.info/11/11549/1163959.html")
    assert soup.select_one("article.font_max")
    assert len(sess.calls) == 2
