# 升级报告：<OLD> → <NEW>

> 复制本模板为 `docs/upgrade/<OLD>-to-<NEW>.md` 后填写。
> 所有数据来源于 `metadata/diff-<OLD>..<NEW>.json`（由 `scripts/diff_versions.py` 生成）。

---

## 0. 元数据

| 项 | 值 |
|----|----|
| 项目 | DataEase |
| 旧版本 | `<OLD>` |
| 新版本 | `<NEW>` |
| diff 方法 | `git-ls-tree+sha256` / `source-map-size` |
| 生成时间 | `<generatedAt>` |
| diff 文件 | `metadata/diff-<OLD>..<NEW>.json` |
| 执行人 | `<who>` |

---

## 1. 变更摘要

| 指标 | 值 |
|------|----|
| 文件总数 | `<totalOld>` → `<totalNew>` |
| 新增 (added) | `<added>` |
| 删除 (removed) | `<removed>` |
| 修改 (modified) | `<modified>` |
| 未变 (unchanged) | `<unchanged>` |

**按类别计数（modified）**

| 类别 | 文件数 |
|------|--------|
| source | `<n>` |
| config | `<n>` |
| build | `<n>` |
| doc | `<n>` |
| other | `<n>` |

---

## 2. 影响范围

### 2.1 新增文件（明细）

| 类别 | 模块 | 路径 |
|------|------|------|
| `<category>` | `<module>` | `<path>` |

### 2.2 删除文件

> 无 / 列表如下：

| 类别 | 模块 | 路径 |
|------|------|------|
| `<category>` | `<module>` | `<path>` |

### 2.3 修改文件（按模块）

| 模块 | 修改数 | 其中源码 | 关键文件（示例） |
|------|--------|----------|------------------|
| `<module>` | `<n>` | `<n>` | `<path>` |

### 2.4 按语言分布（modified）

| 语言 | 修改数 |
|------|--------|
| java | `<n>` |
| vue | `<n>` |
| typescript | `<n>` |
| xml | `<n>` |
| properties | `<n>` |
| 其它 | `<n>` |

---

## 3. 兼容性风险

> 分级标准见 `index.md` §7。逐个风险点给出证据（文件路径/SQL 语句/接口签名）。

### 3.1 数据库 schema
- [ ] 无 DDL 变更
- [ ] 有 DDL 变更（详述下表）

| 文件 | 语句类型 | 内容摘要 | 风险 |
|------|----------|----------|------|
| `db/migration/V<NEW>__ddl.sql` | `ALTER/CREATE/INSERT` | `<摘要>` | 🟢/🟡/🔴 |

### 3.2 API / 接口
- [ ] 无接口签名变更
- [ ] 有变更：`<Controller#method 前后对比>`

### 3.3 配置 / 国际化
- [ ] 无
- [ ] 有：`i18n/*.properties` 新增键 `<key>`；`application*.yml` 变更 `<key>`

### 3.4 依赖 (pom / package)
- [ ] 无
- [ ] 有：`pom.xml` `<groupId:artifactId>` `<old>→<new>`；`package.json` `<pkg> <old>→<new>`

### 3.5 风险等级评定

**综合风险：🟢 低 / 🟡 中 / 🔴 高**

理由：`<一句话结论，须可被 diff/源码证据支撑>`

---

## 4. 知识库更新计划

> 依据 `index.md` §5 映射表，列出需要增量更新的文档。

| 受影响文件/模块 | 需更新的 KB 文档 | 更新内容 | 状态 |
|-----------------|------------------|----------|------|
| `core_dataset_group` (DDL) | `docs/database/schema-core.md` | 新增 `is_cross` 列说明 | ⬜ |
| `DatasetCrossListener.java` | `docs/backend/<pkg>.md` | 新增监听器文档 | ⬜ |
| `<module>` 前端改动 | `docs/frontend/<area>.md` | `<说明>` | ⬜ |

---

## 5. 验证

- [ ] `diff-<OLD>..<NEW>.json` 已生成
- [ ] 本报告四大部分已填写
- [ ] 受影响文档已按 §4 增量更新
- [ ] 覆盖率未回退（对比 `metadata/coverage.json`）
- [ ] `TASKS.md` *Current Version* 已更新为 `<NEW>`
- [ ] 已 Git 提交（message：`feat(upgrade) <OLD>→<NEW>`）
