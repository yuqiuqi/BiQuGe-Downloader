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
