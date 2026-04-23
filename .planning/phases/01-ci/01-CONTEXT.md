# Phase 1: 依赖与 CI 对齐 - Context

**Gathered:** 2026-04-23  
**Status:** Ready for planning

<domain>
## Phase Boundary

在**不破坏**现有 `novel_downloader.py` 下载与 GitHub Actions **成功跑通**的前提下，使仓库具备**单一事实来源**的运行时依赖声明：`requirements.txt`（或项目后续选定的等价清单），且 **`.github/workflows/manual_download.yml` 的安装步骤与该清单一致**；README 中安装说明与上述路径对齐。  
本阶段**不**引入 pytest、不强制删除脚本顶部的 `pip` 自举（该选项留给后续阶段或单独决策，避免与 Phase 3 重叠）。

</domain>

<decisions>
## Implementation Decisions

### 依赖清单形式与内容

- **D-01:** 在仓库根新增 `requirements.txt`，列出运行 `novel_downloader.py` 所需的 **三个** 运行时包：`requests`、`beautifulsoup4`、`lxml`（与当前 workflow 中 `pip install` 行一致），**不得**引入未在代码中使用的包。
- **D-02:** 版本策略：使用 **下限约束**（`>=`）以兼顾 README 所述较宽 Python 范围；在注释或 `README` 中注明「与 CI 验证环境一致可得到最可复现行为」。若后续需要逐字可复现，可在以后增加 lock 文件（**非本阶段范围**）。

### 与现有「脚本内自举 pip」的关系

- **D-03:** **本阶段不修改** `novel_downloader.py` 顶部通过 `subprocess` 自动 `pip install` 的逻辑。依赖对齐的第一优先级是：文档 + CI + `requirements.txt` 三者一致。是否在 Phase 3+ 将自举改为「仅检测后退出并提示 `pip install -r`」单独立项，不阻塞 PACK-01/PACK-02。

### GitHub Actions

- **D-04:** `manual_download` workflow 的 **Install dependencies** 步骤改为 `python -m pip install --upgrade pip`（可选但推荐）后 `pip install -r requirements.txt`，**删除**与清单重复的逐包 `pip install requests beautifulsoup4 lxml` 行，除非在注释中说明临时例外（原则上不需要）。
- **D-05:** 保持 `python-version: '3.10'` 与现有一致；不在本阶段增加多版本 matrix。

### 文档

- **D-06:** 更新 `README.md`：增加「使用 `requirements.txt` 安装」的推荐步骤（`venv` + `pip install -r requirements.txt`），并说明与 GitHub Actions 使用同一套依赖；保留「直接运行脚本可自举装包」作为**可选**说明，避免误导「唯一方式仍是自动 pip」。

### Claude's Discretion

- 依赖版本号具体写出来时的次要修订（在仍满足 D-02 策略前提下）。
- `pip` 升级行是否写进 workflow（推荐保留一行以防 Actions 环境过旧）。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 范围与需求

- `.planning/REQUIREMENTS.md` — **PACK-01**, **PACK-02** 验收锚点  
- `.planning/ROADMAP.md` — Phase 1 目标、成功标准与计划 01-01 … 01-03  
- `.planning/PROJECT.md` — 范围、Validated 能力、非目标边界  

### 实现与现状

- `novel_downloader.py` — 当前依赖集合与自举安装逻辑（本阶段 D-03 不强制改）  
- `.github/workflows/manual_download.yml` — 待与 `requirements.txt` 对齐的安装块  
- `README.md` — 待补充 venv + `-r` 说明  

### 工程背景

- `.planning/codebase/STACK.md` — 技术栈与「无锁文件」现状  
- `.planning/codebase/CONCERNS.md` — `subprocess` 自举 pip 风险（供 Phase 3+ 参考，不阻塞本阶段）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- 无多模块包结构；`novel_downloader.py` 为唯一应用入口。本阶段**仅**新增/修改清单与 workflow、文档。

### Established Patterns

- 运行时依赖在脚本内以 `required_packages` 字典 + `import` 检测表达；`requirements.txt` 将成为对外「声明式」补充，与字典三者语义一致（同名三包）。

### Integration Points

- **CI:** `.github/workflows/manual_download.yml` 的 `Install dependencies` 与 `Run Downloader` 步序保持不变，仅改安装子命令。  
- **本地:** 用户可通过 `pip install -r` 预先装包，减少脚本触网 `pip install` 次数。

</code_context>

<specifics>
## Specific Ideas

- 与 `ROADMAP` 中 01-01、01-02、01-03 计划条目一一可追踪即可；无外部产品图或品牌约束。

</specifics>

<deferred>
## Deferred Ideas

- 在 `requirements-dev.txt` / `tox` 中声明 **pytest**（**Phase 2**）。  
- 删除或约束脚本内**自动** `pip install` 的行为（**Phase 3 或**单独变更，见 `CONCERNS.md`）。  
- 多 Python 版本 CI matrix（**非本阶段**）。

### Reviewed Todos (not folded)

- `todo match-phase` 无匹配项。

</deferred>

---

*Phase: 01-ci*  
*Context gathered: 2026-04-23*
