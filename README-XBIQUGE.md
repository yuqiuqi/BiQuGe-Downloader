# 新站工作流使用说明（试验版）

1. GitHub Actions 运行 `XBiQuGe Search and Download`，mode=search，keyword 填书名、作者或拼音。
2. 在 Actions 日志或 candidates.json 中查看候选书籍，选择目标的目录 URL。
3. 再次运行同一工作流，mode=download，book_url 填选中的 URL，workers 默认 5。
4. 在 Artifacts 下载 xbiquge-results，其中包含书籍 ZIP（TXT + report.json）。

注意：站点的公开搜索 URL 格式为 `/search.php?p=1&q=...`，目录路径为 `/数字/数字/`；由于执行环境无法直连该站，正文 CSS 选择器、分页目录及站点限制尚未完成线上端到端验证。只下载有权保存的内容。
