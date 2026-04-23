# External Integrations

**Analysis Date:** 2026-04-23

## APIs & External Services

**笔趣阁类小说站点（可配置为同类镜像）**

- **用途:** 拉取章节目录 HTML、逐章 HTML；默认示例域名为 `m.bqg92.com`（见 `novel_downloader.py` 中注释与纯数字 ID 补全 URL 逻辑）
- **集成方式:** 服务端无官方 API，全部为匿名 HTTP `GET` + HTML 解析
- **鉴权:** 无；依赖浏览器式请求头（`User-Agent`、`Referer` 等）降低被封概率
- **行为约束:** 代码内对单章分页有最大页数限制（`page_count < 50`），线程数固定为 10，章节间/请求间有随机短延时

**GitHub（CI/CD 仅）**

- **用途:** 通过 Actions 在云端执行同一脚本并上传 `*.txt` 为 artifact
- **工作流:** `.github/workflows/manual_download.yml` — `actions/checkout@v3`, `actions/setup-python@v4`, `actions/upload-artifact@v4`
- **凭据:** 不需要 API token 即可运行下载步骤；`contents: write` 已声明，当前工作流未展示推送到仓库的步骤

## Data Storage

**Databases:**
- 无

**File Storage:**
- 本地/CI 工作目录：单文件 `{安全化小说名}.txt` 与脚本同目录；Artifact 通配 `*.txt`

**Caching:**
- 无；`requests.Session` 仅复用连接，非业务缓存

## Authentication & Identity

- 不集成第三方身份提供方；不处理用户账户

## Monitoring & Observability

- 无 Sentry/日志服务；`print` 与 `sys.stdout` 进度输出
- 失败时以进程退出码 `sys.exit(1)` 让 CI 标红（无章节时）

## CI/CD & Deployment

**CI Pipeline:**
- GitHub Actions — 手动触发，输入 `novel_id` 传给 `python novel_downloader.py "<input>"`

**Hosting:**
- 不适用；产物为可下载的文本 artifact

## Environment Configuration

**Local:**
- 无 `.env`；可选站点 URL 或纯数字 ID

**Actions:**
- `python-version: '3.10'` 在 workflow 中写死

## Webhooks & Callbacks

- 无

---

*Integration audit: 2026-04-23*  
*Update when adding env vars, new hosts, or auth*
