# Phase 2: 测试基线 - Context

**Gathered:** 2026-04-23  
**Status:** Ready for planning

<domain>
## Phase Boundary

在**不破坏**现有多线程下载、CLI 与 GitHub Actions 成功跑通的前提下，建立 **pytest 可发现的最小测试布局**、**开发依赖声明**，并保证 **CI 在合并/运行下载工作流前能执行同一条 `pytest` 命令**；至少含 **1 个不访问外网**的单元测试，覆盖**可稳定**逻辑（以 URL/书号归一化为主）。  
本阶段**不**追求高覆盖率、不强制 HTML 夹具与解析全分支（可在 02-02 计划中加可选/扩展）。

</domain>

<decisions>
## Implementation Decisions

### 可测性与模块边界

- **D-01:** 禁止在单测中 `import novel_downloader` 作为被测主入口的默认方式：该文件在 import 时执行 `pip` 自举，会导致测试环境不确定、且拖慢/污染 CI。  
- **D-02:** 将 `__main__` 块中的「纯数字 ID 补全 URL」与「无 `http` 时补全协议」抽成 **纯函数**，放入新模块 `url_input.py`（仓库根、与 `novel_downloader.py` 并列）。函数**无网络、无子进程、无 import 时副作用**。默认笔趣基座域名与现逻辑一致：``https://m.bqg92.com/book/{id}/``；补协议规则与当前 `elif not target_url.startswith('http')` 一致。  
- **D-03:** `novel_downloader.py` 的 `if __name__ == "__main__":` 改为调用 `url_input.normalize_target_url`（或同类命名）后再构造 `NovelDownloader`，行为与现用户可见结果一致（回归可用手动/后续集成测验证）。

### 测试运行器与布局

- **D-04:** 使用 **pytest**（`>=7.0` 下界即可），`pytest` 在仓库根执行且退出码 0 即满足 **TEST-01** 最低档「smoke」。  
- **D-05:** 测试根目录为 `tests/`，文件命名 `test_*.py`；**不**采用 `src/` 布局（本阶段不引入包安装模式）。  
- **D-06:** 开发依赖单独文件 **`requirements-dev.txt`**，首行起注释说明「仅开发/CI 测试用」，第一有效行为 `pytest>=7.0.0`（不引入 coverage/tox 除非后续阶段扩展）。

### 首批单测内容（无网）

- **D-07:** 首批必测为 **`url_input` 的表驱动用例**（如：纯数字 `3953`、完整 `https://.../book/3953/`、缺协议的域名等），**不**在默认 CI 中访问公网。  
- **D-08:** 对 `BeautifulSoup`、章节拉取的单测、HTML fixture 为 **Phase 2 内 02-02 计划可选项**；本 CONTEXT 不强制 02-02 必含样例 HTML，但允许规划时加入。

### CI

- **D-09:** 在 **`.github/workflows/manual_download.yml`** 中：增加独立 **`test` job**（`runs-on: ubuntu-latest`，Python **3.10** 与下载 job 一致），步骤：checkout → setup-python → `pip install -r requirements.txt` → `pip install -r requirements-dev.txt` → `pytest`。  
- **D-10:** **`download` job** 与 **`test` job** 的编排：使用 **`needs: [test]`** 使 download 在该 workflow 中仅在测试通过之后运行；若将来拆为多 workflow，以「PR 上可跑同条 pytest」为准。  
- **D-11:** 本地与 CI 的测试命令统一为根目录 `pytest`（可接受 `python -m pytest` 等文档等价写法，**默认文档写 `pytest`**）。

### Claude's Discretion

- 纯函数/模块的**精确**命名、是否增加 `if __name__` 下的薄封装。  
- 是否在 `pyproject.toml` 增加 `[tool.pytest.ini_options]` 最小配置（`testpaths = tests`）— **可选**，不阻塞 TEST-01。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 范围与需求

- `.planning/REQUIREMENTS.md` — **TEST-01**, **TEST-02**  
- `.planning/ROADMAP.md` — Phase 2 目标、成功标准、02-01 … 02-03 草案  
- `.planning/PROJECT.md` — 当前 Validated/Active 与工程目标  

### 实现现状

- `novel_downloader.py` — 入口 URL 处理逻辑位置（`__main__` 块，约 360+ 行）；import 时 pip 自举（**D-01 约束来源**）  
- `requirements.txt` — 运行时依赖（Phase 1）  
- `.github/workflows/manual_download.yml` — 待增 `test` job 与 `needs`（**D-09、D-10**）  

### 上游阶段

- `.planning/phases/01-ci/01-CONTEXT.md` — 与「不在 Phase 1 动主脚本」一致；本阶段在受控下抽 `url_input` 并改主入口为薄调用  

**无**外部 ADR 文件；以本文与 REQUIREMENTS 为准。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- 入口 URL 规则已存在，仅需搬迁到 `url_input` 并供测试导入。

### Established Patterns

- 单文件脚本 + 顶置自举；新模块应 **0 自举、仅标准库**。

### Integration Points

- `novel_downloader.py` 仅 `if __name__` 与类型无关处引用 `url_input`；`NovelDownloader` 类**不改**类签名为 Phase 2 之默认（只改入口字符串来源）。

</code_context>

<specifics>
## Specific Ideas

- 表驱动用例显式覆盖书中 ID `3953`（与 README 一致）。

</specifics>

<deferred>
## Deferred Ideas

- **MAIN-01 / 死代码、零章节诊断** — Phase 3。  
- **全站 HTML fixture / 多页章节解析单测** — 可作为 Phase 2 后续计划加项，**非**本 CONTEXT 必达。  
- **coverage、pre-commit、多 Python 版本 matrix** — 后续阶段或产品化时再议。

### Reviewed Todos (not folded)

- `todo match-phase` 无匹配项。

</deferred>

---

*Phase: 02-testing*  
*Context gathered: 2026-04-23*
