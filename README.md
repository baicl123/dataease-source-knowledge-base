# DataEase 源码知识库 (Source Knowledge Base)

本仓库是 **DataEase** 项目的长期、版本化源码知识库。  
它不是一次性学习笔记，而是与源码同步演进的数字孪生，服务于：
- 深度理解 DataEase 架构与实现
- 后续集成 RuoYi-Vue-Plus、Casbin 等项目
- 版本升级影响分析与自定义分支维护
- 作为 AI 辅助开发的第一信息来源

## 当前分析版本

**DataEase v2.10.7**

## 目录结构

- `AGENTS.md`：AI 必须遵守的工作规范（核心，长期稳定）
- `TASKS.md`：当前正在执行的分析任务（频繁更新）
- `TODO.md`：待办事项与未来计划
- `CHANGELOG.md`：知识库本身的更新记录
- `docs/`：人类可读的分析文档（中文）
  - `architecture/`：总体架构（5 篇 + 安全模型）
  - `modules/`：模块级分析（后端业务域地图）
  - `backend/`：Java 类级分析（11 篇，1003 个 Java 100% 覆盖）
  - `frontend/`：Vue 组件分析（12 篇，702 个 .vue/.ts 100% 覆盖）
  - `database/`：数据库、SQL、Mapper（7 篇，78 张表全解析）
  - `customization/`：二次开发相关（建议方案 + 未来实际改造记录，如权限二次开发建议）
  - `upgrade/`：版本升级差异分析（Task 8 待建）
  - `diagrams/`：架构图（Mermaid）
- `metadata/`：结构化数据（JSON），供 AI 和自动化工具消费
  - `source-map.json`：全仓库文件清单
  - `coverage.json`：分析覆盖率统计
  - `statistics.json`：代码统计
- `scripts/`：辅助脚本（DDL 解析、schema 聚合、版本差异扫描等）

> 注：早期 README 曾规划 `api/`、`deployment/`、`adr/`、`glossary/`、`plugin/`、`versions/` 等目录，但分析工作由 `TASKS.md` 的 9 个任务驱动，内容按主题落入了上述实际目录（如 API 分析在 `frontend/api-layer.md` 与 `backend/api-permissions.md`，部署在 `architecture/build-deploy.md`）。这些规划目录已清理，避免结构错位。

## 使用方式

### 人工阅读
直接浏览 `docs/` 下的 Markdown 文件，从 `docs/INDEX.md` 开始导航。

### 与 AI 协作
1. 让 AI 阅读 `AGENTS.md` 了解工作规范。
2. 从 `TASKS.md` 中指定一个任务（例如：“请根据 AGENTS.md 执行 TASKS.md 中的第一个任务”）。
3. 每完成一个模块或一组文档，提交一次 Git，保持小步提交。
4. 定期检查 `metadata/coverage.json` 确认覆盖率进度，直到 100%。

### 同步到知识库
- 乐享知识库中的 `SKB-dataease`
- ima 中的 `SKB-dataease`

### 版本升级（例如 v2.10.7 → v2.10.25）
1. 更新源码仓库，记录新版本号。
2. 让 AI 执行增量更新：“请根据 AGENTS.md 执行增量更新，从 v2.10.7 到 v2.10.25”。
3. AI 会自动扫描差异，生成 `docs/upgrade/` 版本差异文档，并更新受影响的文档和元数据；二次开发相关内容（建议方案与实际改造记录）统一归入 `docs/customization/`。
4. （版本快照归档目录 `versions/` 将在 Task 8 建立升级机制后引入。）

## 维护原则

- 源码是唯一真理（Source of Truth），知识库若与之冲突，以源码为准并立即修正知识库。
- 知识库覆盖率目标始终为 **100%**（每个类、每个组件、每个配置文件都有对应分析）。
- 文档之间保持密集交叉引用，`INDEX.md` 始终保持可导航。
- 所有推断内容必须标注 `[Inference]`，不确定内容标注 `[Need Verification]`。
- 小步提交，每次变更都是可审查的。
