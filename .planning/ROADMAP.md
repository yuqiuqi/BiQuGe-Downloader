# Roadmap: BiQuGe Downloader

## Overview

在**不破坏现有下载与 Actions 能力**的前提下，先统一依赖声明与 CI，再建立自动化测试与基础可配置、可诊断能力，使笔趣阁类 HTML 变更时的维护成本可控。

## Phases

- [x] **Phase 1: 依赖与 CI 对齐** — 声明式依赖与流水线安装一致   (completed 2026-04-23)
- [x] **Phase 2: 测试基线** — pytest 与 CI 跑通，关键纯逻辑有测   (completed 2026-04-23)
- [ ] **Phase 3: 可维护性与错误信息** — 死代码与空目录体验  
- [ ] **Phase 4: 可配置并发** — 线程数可配并文档化  

## Phase Details

### Phase 1: 依赖与 CI 对齐

**Goal**: 所有环境与文档从同一依赖声明安装，减少脚本内自举与漂移。  
**Depends on**: 无（首阶段）  
**Requirements**: PACK-01, PACK-02  
**Success Criteria** (what must be TRUE):

1. 协作者可仅凭 `pip install -r`（或项目选定的方式）在干净虚拟环境中安装与 README 一致依赖  
2. `manual_download` workflow 使用的包集合与 `requirements.txt` 一致或显式说明等价性  
3. 既有本地与 Actions 运行方式在 README 或 workflow 注释中有对应说明  

**Plans**: 2–3 份（规划阶段再拆）  
**UI hint**: no  

Plans:

- [x] 01-01: 添加/校验 `requirements.txt` 与 Python 版本说明  
- [x] 01-02: 调整 `.github/workflows/manual_download.yml` 使用同一依赖源  
- [x] 01-03: 更新 `README.md` 安装与运行段落（如需要）  

### Phase 2: 测试基线

**Goal**: 合并前可在本地与 PR 中自动跑测试。  
**Depends on**: Phase 1  
**Requirements**: TEST-01, TEST-02  
**Success Criteria** (what must be TRUE):

1. 一条命令（如 `pytest`）在仓库根可运行且退出 0（至少 smoke）  
2. GitHub Actions 在下载 job 前或并行 job 中执行同一测试命令  
3. 至少一个测试不访问外网，覆盖可稳定实现的逻辑（如 URL/ID 规范化）  

**Plans**: 2–3 份  
**UI hint**: no  

Plans:

- [x] 02-01: 引入 pytest 与目录结构（如 `tests/`）  
- [x] 02-02: 实现首批单元测试与可选样例 HTML fixture  
- [x] 02-03: CI 中接入测试步骤  

### Phase 3: 可维护性与错误信息

**Goal**: 消除或解释死代码，失败可诊断。  
**Depends on**: Phase 2  
**Requirements**: MAIN-01, MAIN-02  
**Success Criteria** (what must be TRUE):

1. 不存在未使用的 `save_to_file` 与 `run()` 的重复/歧义，或已删除并统一写入路径  
2. 当目录页零章节时，日志/退出信息明确（例如提示站点结构变更、检查 URL）  
3. 回归测试不破坏 Phase 1–2 成果  

**Plans**: 2 份  
**UI hint**: no  

Plans:

- [ ] 03-01: 处理 `save_to_file` 与写入路径一致性  
- [ ] 03-02: 加强 `get_download_url` 空结果路径的用户可见诊断  

### Phase 4: 可配置并发

**Goal**: 用户可按网络环境调节并发，免改源码。  
**Depends on**: Phase 3  
**Requirements**: CFG-01  
**Success Criteria** (what must be TRUE):

1. 通过 CLI 或环境变量可设置 `max_workers`（或等效名），有默认值与边界说明  
2. README 或 `--help` 中说明该选项  
3. 默认行为与当前体验兼容（不默认破坏现有用户）  

**Plans**: 1–2 份  
**UI hint**: no  

Plans:

- [ ] 04-01: 参数解析 + 传入 `ThreadPoolExecutor`  
- [ ] 04-02: 文档与轻量测试（如参数默认值）  

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|------------|
| 1. 依赖与 CI 对齐 | 3/3 | Complete    | 2026-04-23 |
| 2. 测试基线 | 3/3 | Complete    | 2026-04-23 |
| 3. 可维护性与错误信息 | 0/TBD | Not started | - |
| 4. 可配置并发 | 0/TBD | Not started | - |

---

*Roadmap created: 2026-04-23*  
*Last updated: 2026-04-23 — Phase 2 complete*  
*Granularity: coarse (4 phases)*
