# 版本升级机制 (Version Upgrade Mechanism)

> 本文件定义 DataEase 源码知识库（SKB）在**源码版本升级**时的工作机制。
> 呼应 [`../AGENTS.md`](../AGENTS.md) §2.6（版本感知与增量更新）与 §2.7（结构化元数据）。

---

## 1. 目标与原则

| 原则 | 说明 |
|------|------|
| 版本对应 | 知识库必须标注其对应的源码版本（`TASKS.md` 的 *Current Version*）；每次升级都留下可追溯记录。 |
| 多版本共存 | 各版本的 Source Map 与差异数据长期保留于 `metadata/`，不互相覆盖。 |
| **增量优先** | 升级时**只更新受影响的文档**，绝不重生成整个知识库（见 §5 映射表）。 |
| 证据驱动 | 所有「变更/风险」结论必须来自 `diff_versions.py` 的结构化输出或源码证据，禁止猜测。 |
| 兼容性先行 | 升级报告必须显式评估兼容性风险（数据库 / API / 配置 / 依赖）。 |

---

## 2. 触发条件

满足任一即触发本机制：

1. 上游发布新 tag（如 `v2.10.8`），且需要将 SKB 跟进到该版本；
2. 用户明确告知「升级到 `<version>`」；
3. 源码仓库出现破坏性变更（删除表/API），需评估影响。

> 当前 SKB 版本：**v2.10.7**（见 `TASKS.md`）。源码仓库可用标签：`v2.2.0` ~ `v2.10.25`。

---

## 3. 前置依赖

| 资产 | 路径 | 作用 |
|------|------|------|
| 源码 git 仓库 | `~/workspace/code/references/dataease` | 含完整历史 tag；差异引擎直接读取任意 ref 的 `git ls-tree`。 |
| 源码扫描器 | `scripts/scan_source.py` | 产出每版本的 `source-map-<ver>.json`。 |
| **版本差异引擎** | `scripts/diff_versions.py` | 本机制核心：对比两版本，产出 `diff-<old>..<new>.json`。 |
| 升级报告模板 | `docs/upgrade/template.md` | 升级报告的填空模板。 |
| 元数据目录 | `metadata/` | 存放各版本 Source Map 与 diff 结果。 |

---

## 4. 标准工作流（6 步）

```text
① 确认版本       ② 生成新版地图      ③ 运行差异引擎
   └ 旧/新 ref       └ scan_source.py      └ diff_versions.py
                                              │
                                              ▼
④ 填写升级报告   ⑤ 增量更新文档       ⑥ 更新索引 + 提交
   └ template.md      └ 按 §5 映射表        └ INDEX/TASKS/git
```

### Step 1 — 确认版本号与 ref
记录旧版本（当前 SKB 版本）与新版本（目标 tag），例如 `v2.10.7 → v2.10.8`。

### Step 2 — 生成新版本 Source Map（仅新版本需要）
```bash
python3 scripts/scan_source.py \
  --src ~/workspace/code/references/dataease \
  --version v2.10.8 \
  --out metadata/source-map-v2.10.8.json
```
> 旧版地图若已存在（`metadata/source-map-v2.10.7.json`）则跳过扫描。

### Step 3 — 运行差异引擎
两种模式任选其一：

```bash
# 模式 B（推荐）：直接对两个 git 标签 diff，按 blob-sha 精确判定
python3 scripts/diff_versions.py \
  --src ~/workspace/code/references/dataease \
  --old-ref v2.10.7 --new-ref v2.10.8 \
  --out metadata/diff-v2.10.7..v2.10.8.json

# 模式 A：对比两份预生成的 source-map.json（按 size 判定，较快但精度略低）
python3 scripts/diff_versions.py \
  --old-map metadata/source-map-v2.10.7.json \
  --new-map metadata/source-map-v2.10.8.json \
  --out metadata/diff-v2.10.7..v2.10.8.json
```
输出 `diff-<old>..<new>.json` 含：`added / removed / modified` 明细 + 按 `module / language / category` 的聚合摘要。

### Step 4 — 生成升级报告
复制 `template.md` 为 `docs/upgrade/<old>-to-<new>.md`，据 diff JSON 填写四大部分：
- **变更摘要**（计数）
- **影响范围**（按模块/文件明细）
- **兼容性风险**（DB / API / 配置 / 依赖）
- **知识库更新计划**（受影响文档清单）

### Step 5 — 增量更新受影响文档
**只碰 §5 映射表命中的文档**，其余保持不变。新增文件若落入尚未覆盖的包/组件，按需补写新文档。

### Step 6 — 收尾
- 更新 `TASKS.md` 的 *Current Version* 与 *Current Phase*；
- 在 `INDEX.md` 的「版本升级」节追加本次报告链接；
- 执行一次 Git 提交（增量、可审查）。

---

## 5. 文件类别 → 知识库文档映射

差异引擎已按 `category` 归类，据此决定要更新哪篇文档：

| 文件特征 | 归类 | 需更新的知识库文档 |
|----------|------|--------------------|
| `core/core-backend/**/*.java` | source | `docs/backend/<package>.md`（按 Java 包映射） |
| `core/core-frontend/**/*.{vue,ts}` | source | `docs/frontend/<area>.md` |
| `sdk/**/*.java` | source | `docs/backend/` 或 `docs/modules/` 对应 SDK 模块文档 |
| `**/db/{migration,desktop}/V*__*.sql` | source(sql) | `docs/database/migrations.md` + `docs/database/schema-*.md`（表结构增量） |
| `**/mapper/**/*.xml` 或 `Ext*Mapper` | source(xml) | `docs/database/mappers.md` |
| `**/resources/i18n/*.properties` | config | `docs/backend/` 国际化说明（或首页注释） |
| `pom.xml` / `package.json` | build | `docs/architecture/overview.md` 依赖栈 / `docs/modules/` |
| `application*.yml` / `*.properties`（配置） | config | `docs/architecture/` 配置相关文档 |
| `README.md` / `docs/**` | doc | 视内容更新对应文档 |
| 其它（脚本、二进制、子模块指针） | other/build | 通常无需更新文档，仅记录 |

> 映射规则与 `scan_source.py` 的 `classify()` 口径一致，保证 diff 聚合与文档归属可对齐。

---

## 6. 多版本共存约定

```
metadata/
  source-map-v2.10.7.json        # 各版本 Source Map 快照（长期保留）
  source-map-v2.10.8.json
  diff-v2.10.7..v2.10.8.json     # 每次升级的差异（长期保留）

docs/upgrade/
  index.md                       # 本机制规范
  template.md                    # 报告模板
  v2.10.7-to-v2.10.8.md          # 历次升级报告（示例）
```

- **主文档始终描述「当前版本」**（即 `TASKS.md` 的 *Current Version*）。
- 历史版本差异沉淀于 `docs/upgrade/<old>-to-<new>.md`，不污染主文档。
- 若需长期并行维护多版本文档，可在 `docs/` 下建 `v<ver>/` 归档（可选，当前不启用）。

---

## 7. 兼容性风险分级

| 等级 | 判定（依据 diff 输出） | 处理要求 |
|------|------------------------|----------|
| 🔴 高 | `removed` 含表/列/API/配置文件；或 DDL 含 `DROP`/`RENAME`；破坏性依赖升级 | 必须写迁移方案 + 回滚预案 |
| 🟡 中 | 新增必填列/参数；API 行为变更；新增权限/表关联 | 注明影响，更新相关文档 |
| 🟢 低 | 新增可选列、新增表、`INSERT` 种子数据、i18n 新增、纯前端样式/文案 | 记录即可，常规更新 |

> 实际风险以 **DDL 语句内容**与**接口签名变更**为准，分级仅作初筛。

---

## 8. 检查清单

- [ ] 旧/新版本号已确认并记录
- [ ] 新版本 `source-map-<ver>.json` 已生成（或复用已有）
- [ ] `diff-<old>..<new>.json` 已生成且概要计数合理
- [ ] 升级报告 `<old>-to-<new>.md` 已填写（摘要/范围/风险/计划）
- [ ] 仅按 §5 映射表增量更新了受影响文档
- [ ] 兼容性风险已分级并处置
- [ ] `TASKS.md` / `INDEX.md` 已更新
- [ ] 覆盖率未回退（对照 `metadata/coverage.json`）
- [ ] 已 Git 提交

---

## 9. 命令速查

```bash
# 列出版本标签
git -C ~/workspace/code/references/dataease tag

# 生成某版本地图
python3 scripts/scan_source.py --src <repo> --version <ver> --out metadata/source-map-<ver>.json

# 版本差异（精确模式，推荐）
python3 scripts/diff_versions.py --src <repo> --old-ref <old> --new-ref <new> \
  --out metadata/diff-<old>..<new>.json

# 版本差异（地图模式，快速）
python3 scripts/diff_versions.py --old-map metadata/source-map-<old>.json \
  --new-map metadata/source-map-<new>.json --out metadata/diff-<old>..<new>.json
```
