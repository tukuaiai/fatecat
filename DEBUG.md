# Debug Record

## Bug

- 标题：iztro 原生算法模块入口缺失
- 症状：Bot 排盘时报错 `ziwei failed: iztro原生算法执行失败`
- 首次发现位置 / 时间：`/paipan` 链路，2026-04-15

## Environment

- 仓库 / 模块：`fatecat/modules/telegram`
- 运行环境：Linux + Python `.venv` + Node `v22.12.0`
- 依赖 / 版本：`assets/vendor/github/iztro-main`
- 配置差异：Python 依赖已安装，Node vendor 依赖未安装

## Reproduction

1. 启动 Bot
2. 发送 `/paipan`
3. 进入紫微斗数分支时抛出 `Cannot find module .../iztro-main/lib/index.js`

## Observations

- O1: `assets/vendor/github/iztro-main/package.json` 存在，且 `main` 指向 `lib/index.js`
- O2: 仓库中只有 `src/index.ts`，没有 `lib/index.js`
- O3: `assets/vendor/github/iztro-main/node_modules` 不存在

## Hypotheses

### H1: （ROOT HYPOTHESIS）
- Supports: vendor 仓库只有源码快照，未执行 `npm install` / `npm run build`
- Conflicts: 无
- Test: 在 Python 集成层先检测 `node_modules` 与入口文件，不满足则自动 install/build

### H2:
- Supports: 代码把入口路径写死为 `lib/index.js`
- Conflicts: `package.json.main` 本身也是 `lib/index.js`，说明单纯改字符串不是根因
- Test: 改为统一从 `package.json.main` 解析入口

### H3:
- Supports: 即使后续有构建产物，没有 `node_modules` 仍可能在 require 时失败
- Conflicts: 无
- Test: 把“入口存在”和“依赖已安装”一起作为 ready 条件

## Experiments

### E1
- Hypothesis: 缺少 Node 依赖与构建产物是直接根因
- Change: 扫描 `iztro-main` 文件结构与 `package.json`
- Expected: 只有 `src/`，没有 `lib/`，且没有 `node_modules`
- Result: 观测符合预期
- Verdict: confirmed
- Revert: 无

## Root Cause

- FateCat 在调用 `iztro` 时默认假设 vendor 仓库已经完成 Node 依赖安装和 TypeScript 构建，但当前环境只有源码快照，缺少 `node_modules` 和 `lib/index.js`，导致运行时 `MODULE_NOT_FOUND`

## Fix

- 按 `package.json.main` 解析 `iztro` 入口，去掉硬编码字符串假设
- 在调用前自动检查 `node_modules` 与入口文件
- 缺依赖时执行 `npm install --no-fund --no-audit`
- 缺入口且存在 `build` 脚本时执行 `npm run build`
- 临时 JS 文件改用 `NamedTemporaryFile`，避免固定 `/tmp/native_iztro.js`

## Regression Evidence

- 测试：新增 `modules/telegram/tests/test_fortel_ziwei_integration.py`
- 结果：覆盖入口解析与 install/build 准备逻辑
- 备注：后续再跑一次真实 `FortelZiweiCalculator` 调用确认 Node 侧可执行
