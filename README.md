# DataEase 源码知识库 (Source Knowledge Base)

本仓库是 **DataEase** 项目的长期、版本化源码知识库。  
它不是一次性学习笔记，而是与源码同步演进的数字孪生，服务于：
- 深度理解 DataEase 架构与实现
- 后续集成 RuoYi-Vue-Plus、Casbin 等项目
- 版本升级影响分析与自定义分支维护
- 作为 AI 辅助开发的第一信息来源

## 当前分析版本

**DataEase v2.10.7**  
（后续版本分析将保存在 `versions/` 中，`versions/latest/` 始终指向最新完成分析的版本）

## 目录结构

- `AGENTS.md`：AI 必须遵守的工作规范（核心，长期稳定）
- `TASKS.md`：当前正在执行的分析任务（频繁更新）
- `TODO.md`：待办事项与未来计划
- `CHANGELOG.md`：知识库本身的更新记录
- `docs/`：人类可读的分析文档（中文）
  - `architecture/`：总体架构
  - `modules/`：模块级分析
  - `backend/`：Java 类级分析
  - `frontend/`：Vue 组件分析
  - `database/`：数据库、SQL、Mapper
  - `api/`：API 说明
  - `plugin/`：插件机制
  - `deployment/`：构建、部署
  - `adr/`：架构决策记录
  - `upgrade/`：版本升级差异分析
  - `glossary/`：术语表
  - `diagrams/`：架构图（Mermaid）
- `metadata/`：结构化数据（JSON），供 AI 和自动化工具消费
  - `source-map.json`：全仓库文件清单
  - `symbol-index.json`：类/方法/组件索引
  - `dependency-graph.json`：模块/类依赖关系
  - `call-graph.json`：调用链
  - `coverage.json`：分析覆盖率统计
  - `statistics.json`：代码统计
- `versions/`：按源码版本归档的知识库快照
- `scripts/`：辅助脚本（可选）

## 使用方式

### 人工阅读
直接浏览 `docs/` 下的 Markdown 文件，从 `docs/INDEX.md` 开始导航。

### 与 AI 协作
1. 让 AI 阅读 `AGENTS.md` 了解工作规范。
2. 从 `TASKS.md` 中指定一个任务（例如：“请根据 AGENTS.md 执行 TASKS.md 中的第一个任务”）。
3. 每完成一个模块或一组文档，提交一次 Git，保持小步提交。
4. 定期检查 `metadata/coverage.json` 确认覆盖率进度，直到 100%。

### 同步到知识库
- 乐享知识库中的`SKB-dataease`
- ima中的`SKB-dataease`

### 版本升级（例如 v2.10.7 → v2.10.25）
1. 更新源码仓库，记录新版本号。
2. 让 AI 执行增量更新：“请根据 AGENTS.md 执行增量更新，从 v2.10.7 到 v2.10.25”。
3. AI 会自动扫描差异，生成 `docs/upgrade/` 文档，并更新受影响的文档和元数据。
4. 更新 `versions/latest/` 指向新版本，并在本 README 中修改“当前分析版本”。

## 维护原则

- 源码是唯一真理（Source of Truth），知识库若与之冲突，以源码为准并立即修正知识库。
- 知识库覆盖率目标始终为 **100%**（每个类、每个组件、每个配置文件都有对应分析）。
- 文档之间保持密集交叉引用，`INDEX.md` 始终保持可导航。
- 所有推断内容必须标注 `[Inference]`，不确定内容标注 `[Need Verification]`。
- 小步提交，每次变更都是可审查的。
