# -*- coding: utf-8 -*-
"""
小说入口 URL/书号归一化（纯标准库、无网络、无子进程）。

与 `novel_downloader` 的 `if __name__` 中历史逻辑一致，供测试直接导入。
"""
DEFAULT_HOST_BOOK = "https://m.bqg92.com"


def normalize_target_url(s: str) -> str:
    """
    将用户输入的目录 ID 或 URL 归一化为可请求的起始地址。

    前置：调用方已对入参做 strip 且非空。行为对齐原脚本：
    - 全数字则补全为 ``{DEFAULT_HOST_BOOK}/book/{id}/``
    - 否则若无 http 前缀则补全 ``https://``
    - 否则原样返回
    """
    if s.isdigit():
        return f"{DEFAULT_HOST_BOOK}/book/{s}/"
    if not s.startswith("http"):
        return "https://" + s
    return s
