# Changelog

版本号使用 Python/PEP 440 的三段式格式；历史 GitHub Release 的标签可能使用简写形式（如 `1.5`）。

## [1.5.0] — 2026-10-15 ([Release tag: 1.5](https://github.com/yuqiuqi/BiQuGe-Downloader/releases/tag/1.5))

- 适配 `xbiquge.info` 站点目录、分页目录和 `article.font_max` 正文容器。
- 对 HTTP 502/522、超时等异常增加备用域名切换及失败章节补抓处理。
- 改进下载报告与失败记录；维持 TXT/ZIP 产物和 GitHub Actions 搜索/下载入口。
- 增加目录/正文/异常路径的单元测试。

**验证范围：** [2026-10-15 的手动下载工作流](https://github.com/yuqiuqi/BiQuGe-Downloader/actions/runs/38698784987) 已成功完成，不能据此承诺其他小说、关键词搜索或未来站点始终可用。

较早版本及历史说明见 [GitHub Releases](https://github.com/yuqiuqi/BiQuGe-Downloader/releases)。
