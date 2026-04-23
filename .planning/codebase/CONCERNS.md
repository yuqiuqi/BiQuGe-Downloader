# Codebase Concerns

**Analysis Date:** 2026-04-23

## Tech Debt

**`save_to_file` 未使用**
- 问题: `NovelDownloader.save_to_file`（`novel_downloader.py`）定义后，`run()` 未调用；实际写入在 `run()` 末尾集中完成
- 影响: 读者误以为双路径写入；删除或接入前应统一策略
- 修复: 删除死代码，或让 `run()` 复用该方法以减少重复

**单文件超长、职责集中**
- 问题: 目录解析、正文分页、并发、落盘、CLI、自举装包均在同一文件
- 影响: 难以单测、难以多站点扩展
- 修复: 拆模块（例如 `parsing.py`, `http_client.py`）+ 保留薄 CLI

**目录 fallback 未实现**
- 问题: `get_download_url` 在「未找到符合规则章节」时 `pass`，直接返回空目录（见 `pass` 分支附近注释）
- 影响: 站点小改版即可导致** silently 空结果** 或需人工修选择器
- 修复: 第二套解析策略或更清晰的错误提示/诊断输出

## Known Bugs

**对站点强耦合**
- 症状: 域名、路径正则、`#content` / `.showtxt` 等选择器与笔趣阁类页面绑定
- 触发: 目标站改版或换源
- 缓解: 用户更新 URL/换同类站；无自动适配

**内存中存放全书章节**
- 症状: 极大章节数或超长单章时内存占用高
- 位置: `run()` 中 `results` 字典 + 最终字符串拼接（`novel_downloader.py`）
- 缓解: 分批写盘或流式；当前为「小中篇」假设

## Security Considerations

**无加密与无鉴权外爬**
- 风险: 仅适合用户自担合规与版权责任的场景；README 已声明仅供学习
- 建议: 不在仓库或日志中硬编码账号 cookie；不扩展为绕过付费墙

**`subprocess` 调 pip 安装**
- 风险: 在不可信环境自动执行 `pip install` 可能被投毒包名利用（低概率，但启动即联网装包扩大攻击面）
- 建议: 生产/CI 用固定 `requirements.txt` + `pip install -r`；脚本内自举可改为「检测缺失后退出并提示命令」

**GitHub Actions `contents: write`**
- 当前工作流未显示 git push，但若未来加自动提交，需审查 token 与最小权限

## Performance Bottlenecks

**固定 10 线程 + 对目标站压测感**
- 问题: 高并发易触发限流；低并发则大书耗时长
- 改进: 可配置 `max_workers`、全局限速或指数退避

**同步 HTML 解析在 worker 中**
- CPU 上解析可成为瓶颈；若书极多，可考虑减少线程数 + 或进程池（通常不必要）

## Fragile Areas

**章节链接与排序逻辑**
- 文件: `novel_downloader.py` 中 `pattern` 与 `all_links` 循环、`get_id` 排序
- 易碎原因: 目录页若混入「倒序/推荐」块，需依赖 URL id 排序纠正；仍可能混入无关 `.html` 链

**分页「下一页」解析**
- 文件: `get_chapter_content` 内对 `soup.find('a', string=re.compile('下一页'))` 及 `next_href` 规则
- 易碎原因: 若站点改用 JS 或不同文案，分页合并失败

## Scaling Limits

- 单进程 CLI；无水平扩展
- 目标站点可单方面封 IP 或要求验证码（本工具不处理 CAPTCHA）

## Dependencies at Risk

- `requests` / `bs4` / `lxml` 为常规依赖，风险低
- 无 lockfile 时，长期可能因次版本行为差异需钉版本

## Missing Critical Features

- 无自动化测试、无 `requirements.txt` 锁定
- 无多站点可插拔配置（域名与选择器写死在代码中）

## Test Coverage Gaps

- 全本下载与正文质量（水印/广告串、章首空行）尚无自动化断言；见 UAT 报告

## UAT：全本下载质量（2026-04-23）

随机书号 `3953`、apibi 全本 113 章：**编码与章数完整通过**；问题为源站正文内嵌推广/水印（如 `bqfun ⊕cc`、`顶点小说` 等），影响**可读性与「干净排版」**，非 UTF-8 乱码。

- **详细复现、证据与下一期修改建议:** `.planning/phases/03-content-quality/03-UAT-DOWNLOAD-REPORT.md`

---

*Concerns audit: 2026-04-23*  
*Update as issues are fixed or new ones discovered*
