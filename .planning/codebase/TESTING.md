# Testing Patterns

**Analysis Date:** 2026-04-23

## Test Framework

**Runner:**
- 未配置。仓库中无 `pytest.ini`、`tox.ini`、`unittest` 主入口

**Assertion Library:**
- 不适用

**Run Commands:**

```bash
# 当前无标准测试命令。若引入 pytest，典型将是：
# pytest
# pytest tests/ -q
```

## Test File Organization

**Location:**
- 无 `tests/`、`test_*.py` 或 `*_test.py`

**Naming:**
- 无约定（尚无测试代码）

**Structure:**
- 单文件 `novel_downloader.py` 占全部业务逻辑，便于后续旁挂 `tests/test_novel_downloader.py` 做纯函数/解析提取测试

## Test Structure

- 无 `describe`/`it` 等结构（非 JS 项目且未引入 pytest 风格示例）

**若添加测试的合理切入点:**
- 对 URL 规范化（纯数字 id → 完整 URL）可抽为纯函数后单元测试
- 对章节 id 提取正则 `get_id` 逻辑可表驱动测试
- 对 `BeautifulSoup` 依赖部分需 `responses` 或 `requests_mock` 夹具，或解耦为「传 HTML 字符串进解析函数」

## Mocking

- 无既有 mock 约定；引入后应对 `requests.Session.get` 或抽取的 fetch 层进行 mock，避免对真实笔趣阁站点发请求

## Fixtures and Factories

- 无共享 fixture；可保存**脱敏的 HTML 样例**于 `tests/fixtures/` 供解析回归

## Coverage

- 无 CI 中覆盖率步骤；`manual_download.yml` 仅跑脚本无测试阶段

**若启用 coverage：**

```bash
# 示例（未在仓库中配置）
# pytest --cov=novel_downloader --cov-report=term-missing
```

## Test Types

**Unit / Integration / E2E:**
- 当前均为**手动**：本地或 Actions 全链路跑通即视为验证

## Common Patterns

- N/A，直至引入测试依赖

---

*Testing analysis: 2026-04-23*  
*Update when adding pytest/unittest and CI test job*
