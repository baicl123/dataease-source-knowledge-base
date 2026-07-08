# CHANGELOG.md

知识库自身的更新记录（与源码版本区分）。最新变更置顶。

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
