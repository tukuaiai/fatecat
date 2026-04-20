# Debug Record

## Bug

- 标题：`weakStrong` 强弱口径退化为二档，导致历史样本被误判为“全部偏强”
- 症状：安装后的排盘结果里，身强弱不再输出五档（`身弱 / 中和偏弱 / 中和 / 中和偏强 / 身强`），而是只剩 `身强 / 身弱`；用户反馈实际结果明显偏向“全部身强”
- 首次发现位置 / 时间：线上安装包反馈，2026-04-20

## Environment

- 仓库 / 模块：`fatecat/project/modules/telegram`
- 关键文件：`src/bazi_calculator.py`
- 上游参照：`project/assets/vendor/github/bazi-1-master/bazi.py`

## Reproduction

1. 用 `BaziCalculator(...)._calc_wuxing_scores()` 直接计算四柱五行分数
2. 观察 `weakStrong`
3. 对 2013-01-01 09:19（北京）样本，旧实现输出 `身强`

## Observations

- O1: 当前 `_calc_wuxing_scores()` 只返回 `\"身强\" if not weak else \"身弱\"`，实现上已经不可能产出五档
- O2: `models.py` 的 `DayMaster.strength` 历史上设计为五档口径，说明展示层原本就期待细粒度强弱
- O3: 上游 `bazi-1` 同时给出 `weak` 布尔值和 `strong` 原始分数；README 明确标注“通常 >29 为强，需要参考月份、坐支等”
- O4: 历史故障样本 `2013-01-01 09:19` 的 raw `strongScore` 为 `25`，旧实现却因为存在一个 `帝` 直接落成 `身强`

## Hypotheses

### H1: （ROOT HYPOTHESIS）
- Supports: 现实现把上游原始强弱信息压扁成二档，展示层因此失去五档能力
- Conflicts: 无
- Test: 恢复上游 `strong` 原始分数，并基于上游经验线做五档归一

### H2:
- Supports: 只看 `weak` 布尔值会把边界样本误推到“身强”
- Conflicts: 无
- Test: 用 `strongScore=25` 的历史样本回归验证，修复后应落到 `中和偏弱`

## Experiments

### E1
- Hypothesis: 当前实现已经退化成二档输出
- Change: 直接检查 `project/modules/telegram/src/bazi_calculator.py`
- Expected: `weakStrong` 只会返回 `身强/身弱`
- Result: 确认存在
- Verdict: confirmed
- Revert: 无

### E2
- Hypothesis: 历史故障样本的 raw score 不支持“身强”
- Change: 用内部方法直算 2013-01-01 09:19（北京）样本
- Expected: `strongScore` 落在 29 以下
- Result: `strongScore = 25`，旧实现仍输出 `身强`
- Verdict: confirmed
- Revert: 无

### E3
- Hypothesis: 只按 `strongScore` 做五档映射，会与上游 `weak` 布尔值冲突
- Change: 抽查 2001-01-01 12:00（北京）样本
- Expected: 若 `weak=True`，标签不应落入偏强侧
- Result: 样本出现 `weak=True` 且 `strongScore = 32` 的组合，说明“只看分数”会导致标签与上游原始判定打架
- Verdict: confirmed
- Revert: 无

## Root Cause

- 根因不是用户安装问题，也不是上游 `bazi-1` 自身故障，而是 FateCat 本地胶水层把上游强弱结果退化成了二档展示：
  - 保留了 `weak` 布尔判定
  - 丢失了上游 `strong` 原始分数
  - 于是所有边界样本都会被粗暴压到 `身强/身弱`

## Fix

- 在 `_calc_wuxing_scores()` 中补回上游 `strongScore`
- 保留上游 `weak` 原始布尔值，作为原始诊断字段输出
- 五档映射改为“先尊重 `weak`，再用 `strongScore` 细分”：
  - `weak=True`: `<=20 -> 身弱`，`21-28 -> 中和偏弱`，`>=29 -> 中和`
  - `weak=False`: `<=25 -> 中和偏弱`，`26-33 -> 中和`，`34-37 -> 中和偏强`，`>=38 -> 身强`

## Regression Evidence

- 新增测试：`project/tests/test_strength_mapping.py`
- 验证点：
  - 五档阈值边界可用
  - 历史故障样本 `2013-01-01 09:19` 回归到 `中和偏弱`
  - `weak=True` 的边界样本不会被错误落到偏强侧

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
