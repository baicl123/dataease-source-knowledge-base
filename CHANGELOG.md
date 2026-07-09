# CHANGELOG.md

知识库自身的更新记录（与源码版本区分）。最新变更置顶。

## 2026-07-09

- **Task 8 版本升级机制完成**：
  - 新增 `scripts/diff_versions.py`——版本差异引擎（支持 `git ls-tree` 按 blob-sha 精确 diff 与 source-map 地图对比两种模式）。
  - 新增 `docs/upgrade/index.md`——机制规范（6 步工作流、文件类别→文档映射、多版本共存约定、兼容性风险分级、检查清单）。
  - 新增 `docs/upgrade/template.md`——升级报告模板（变更摘要 / 影响范围 / 兼容性风险 / 知识库更新计划）。
  - 新增 `docs/upgrade/v2.10.7-to-v2.10.8.md`——真实示例报告（对源码仓库 v2.10.7/v2.10.8 两 tag 实跑，综合风险 🟢 低）。
  - 同步更新 `README.md` / `AGENTS.md` §8 / `TASKS.md` / `INDEX.md` 引用；Task 1-9 全部完成，进入 Phase 3。

## 2026-07-08

- **结构对齐**：改写 `README.md` 目录结构以匹配实际产出（删除未使用的 `api/`、`deployment/`、`adr/`、`glossary/`、`plugin/`、`versions/` 规划目录引用，修正 `metadata/` 文件清单）。
- **补建** `TODO.md` 与 `CHANGELOG.md`（README 此前引用但不存在）。
- **清理** 6 个空占位目录。
- **Task 7 数据库分析完成**：`docs/database/` 7 篇（78 张表全解析）+ `scripts/` 5 个解析脚本（parse_ddl / extract_deltas / aggregate_schema / schema_to_md / build_database_docs）。
- 前端分析完成（12 篇，702 个 .vue/.ts 100% 覆盖）已提交。

## 2026-07-07

- 乐享知识库首轮全量同步（30 篇文档）。
- 权限二次开发建议完成（`docs/upgrade/permission-development-guide.md`）。
- 后端分析完成（11 篇，1003 个 Java 100% 覆盖）已提交。
- 架构分析完成（5 篇 + Mermaid 图）已提交。
- 源码扫描与 Source Map 建立（6091 文件）已提交。
