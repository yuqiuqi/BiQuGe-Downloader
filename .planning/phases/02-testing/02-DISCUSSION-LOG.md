# Phase 2: 测试基线 - Discussion Log

> **审计用。** 规划/执行以 `02-CONTEXT.md` 为准。  
> 本会话采用**推荐默认**（与 Phase 1 相同策略），无逐题交互。

**Date:** 2026-04-23  
**Phase:** 2 - 测试基线  
**Areas discussed:** 模块切分、pytest 与目录、无网用例、CI job、dev 依赖文件  

---

## 是否将 URL 归一化抽成独立可导入模块

| Option | Description | Selected |
|--------|-------------|----------|
| 新 `url_input.py`（纯函数、无自举） | 避免 `import novel_downloader` 触发 pip | ✓ |
| 直接测 `novel_downloader` 模块 | 与 D-01 冲突 |  |
| 仅 subprocess 测 CLI | 重、慢，非首批 |  |

**Notes:** 对应 CONTEXT **D-01～D-03**。

---

## 测试工具与依赖文件

| Option | Description | Selected |
|--------|-------------|----------|
| `requirements-dev.txt` + `pytest>=7` | 与运行时分离 | ✓ |
| 把 pytest 写进主 `requirements.txt` | 污染运行镜像 |  |

**Notes:** **D-06**。

## CI 编排

| Option | Description | Selected |
|--------|-------------|----------|
| 独立 `test` job + `download` needs test | 失败即不跑下载，省 Actions 分钟 | ✓ |
| 并行 job 互不依赖 | 未选 |  |

**Notes:** **D-09、D-10**。

## 首批无网用例

| Option | Description | Selected |
|--------|-------------|----------|
| 表驱动 `url_input` | 满足 TEST-02 不访问外网 | ✓ |
| 首批即 HTML 解析大套 | 超出「基线」 | 选作 02-02 可选项（D-08） |

---

## Deferred

见 `02-CONTEXT.md` `<deferred>`。
