# Requirements: BiQuGe Downloader

**Defined:** 2026-04-23  
**Core Value:** 稳定、可复现地从用户给定的目录页，下载并合并完整、可读的章节正文到本地或 CI Artifact（见 `PROJECT.md`）

## v1 Requirements

### 依赖与可复现性

- [x] **PACK-01**: 仓库根目录提供声明式依赖文件（如 `requirements.txt`），列出版本与 CI/本地文档一致
- [x] **PACK-02**: `manual_download` workflow 的 `pip install` 与该文件对齐（或显式等价的固定集合）

### 质量与验证

- [x] **TEST-01**: 存在可本地与在 CI 中运行的一条命令执行自动化测试（如 `pytest`）
- [x] **TEST-02**: 对 URL/书号归一化或解析辅助逻辑，具备至少不依赖外网的单元测试样例

### 可维护性与可观测

- [ ] **MAIN-01**: `save_to_file` 死代码被删除、接入 `run()` 路径，或在文档与代码中明确弃用并移除（与 `CONCERNS` 一致）
- [ ] **MAIN-02**: 当未解析到任何章节时，用户可见明确失败原因与下一步建议（非静默空成功）

### 可配置

- [ ] **CFG-01**: 下载并发线程数可通过 CLI 参数或环境变量配置，且文档中说明默认值

## v2 Requirements

（暂缓；进入 roadmap 后若调整再迁移）

- **CFG-02**: 大文件或超大章节时降低内存占用的流式/分批落盘（当前 `CONCERNS` 已记录）
- **SITE-01**: 可插拔的站点配置（选择器/域名分文件），多镜像切换成本更低

## Out of Scope

| Feature | Reason |
|--------|--------|
| 带登录/付费/验证码的站点 | 与 README 与法律风险边界不符 |
| 产品化为 SaaS 或分发商用爬虫 | 超出个人工具维护范围 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PACK-01 | Phase 1 | Complete |
| PACK-02 | Phase 1 | Complete |
| TEST-01 | Phase 2 | Complete |
| TEST-02 | Phase 2 | Complete |
| MAIN-01 | Phase 3 | Pending |
| MAIN-02 | Phase 3 | Pending |
| CFG-01 | Phase 4 | Pending |

**Coverage:**  
- v1 requirements: 7 total  
- Mapped to phases: 7  
- Unmapped: 0 ✓  

---

*Requirements defined: 2026-04-23*  
*Last updated: 2026-04-23 after Phase 2 execution (TEST-01/02 complete)*
