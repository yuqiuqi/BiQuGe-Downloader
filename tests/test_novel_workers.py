"""Phase 12 / CFG-01: 并发线程数解析（CLI 与环境变量）。"""

import os

import pytest

import novel_downloader as nd


def test_resolve_default_no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BQUGE_MAX_WORKERS", raising=False)
    assert nd.resolve_max_workers(None) == nd.DEFAULT_MAX_WORKERS


def test_env_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BQUGE_MAX_WORKERS", "4")
    assert nd.resolve_max_workers(None) == 4


def test_cli_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BQUGE_MAX_WORKERS", "3")
    assert nd.resolve_max_workers(8) == 8


def test_cli_clamp_high() -> None:
    assert nd.resolve_max_workers(500) == nd.MAX_WORKERS_CAP


def test_invalid_env_uses_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BQUGE_MAX_WORKERS", "not-a-number")
    assert nd.resolve_max_workers(None) == nd.DEFAULT_MAX_WORKERS


def test_env_clamp_over_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BQUGE_MAX_WORKERS", "200")
    assert nd.resolve_max_workers(None) == nd.MAX_WORKERS_CAP


def test_cli_rejects_zero() -> None:
    with pytest.raises(ValueError):
        nd.resolve_max_workers(0)


def test_partial_failure_produces_report_and_nonzero(tmp_path, monkeypatch):
    import json
    import zipfile
    from types import SimpleNamespace

    monkeypatch.setattr(nd, "__file__", str(tmp_path / "novel_downloader.py"))

    def content(url):
        if url == "bad":
            raise RuntimeError("simulated network error")
        return "章节正文已经成功下载，长度符合预期。"

    downloader = SimpleNamespace(
        novel_name="下载测试", _opt_max_workers=2,
        get_download_url=lambda: [("第一章", "ok"), ("第二章", "bad")],
        get_chapter_content=content,
    )
    with pytest.raises(RuntimeError, match="1 章下载失败"):
        nd.NovelDownloader.run(downloader)

    with zipfile.ZipFile(tmp_path / "下载测试.zip") as archive:
        report = json.loads(archive.read("下载测试.report.json"))
        text = archive.read("下载测试.txt").decode("utf-8")
    assert report["total"] == 2
    assert report["succeeded"] == 1
    assert report["failed"][0]["title"] == "第二章"
    assert "章节正文已经成功" in text
    assert "[本章下载失败" in text


def test_successful_download_writes_ordered_zip(tmp_path, monkeypatch):
    import json
    import zipfile
    from types import SimpleNamespace
    monkeypatch.setattr(nd, "__file__", str(tmp_path / "novel_downloader.py"))

    downloader = SimpleNamespace(
        novel_name="成功测试", _opt_max_workers=2,
        get_download_url=lambda: [("第一章", "one"), ("第二章", "two")],
        get_chapter_content=lambda url: "正文" + url,
    )
    zip_path = nd.NovelDownloader.run(downloader)
    with zipfile.ZipFile(zip_path) as archive:
        text = archive.read("成功测试.txt").decode("utf-8")
        report = json.loads(archive.read("成功测试.report.json"))
    assert text.index("第一章") < text.index("第二章")
    assert report["succeeded"] == 2
    assert report["failed"] == []
