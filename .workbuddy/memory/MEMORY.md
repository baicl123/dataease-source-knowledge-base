# DataEase 源码知识库项目 Memory

## 项目定位
- DataEase v2.10.7 源码知识库（SKB），遵循 AGENTS.md 规范
- 目标：构建与源码同步演进的结构化知识库

## 当前状态
- 架构分析：✅ 5篇 + Mermaid 图（docs/diagrams/architecture.md，4 图各独立 mermaid 块 + 中文说明）
- 后端 Java：✅ 100%（1003 文件，11 篇文档）
- 前端：✅ 100%（463 .vue + 239 .ts，12 篇文档）
- 权限二次开发建议：✅ 完成（4 套方案 + 安全加固）→ docs/customization/permission-development-guide.md
- 数据库分析：✅ 完成（38 SQL + 6 Mapper，78 张表全解析，7 篇文档）
- 版本升级机制：✅ 完成（Task 8：scripts/diff_versions.py 差异引擎 + docs/upgrade/index.md 机制 + template.md + v2.10.7→v2.10.8 真实示例）

## 目录约定
- docs/customization/：二次开发相关（建议方案 + 未来实际改造记录）
- docs/upgrade/：版本升级机制 + 历次差异报告（index.md 机制 / template.md 模板 / <old>-to-<new>.md 示例）
- 文档交叉引用一律用相对路径（如 ../backend/dataset.md）

## 数据库分析关键事实（v2.10.7）
- DDL 位置：core/core-backend/src/main/resources/db/{migration,desktop}/V2.0..V2.10.7__*.sql
- migration=MySQL 规范 schema（含 11 张 QRTZ_*）；desktop=H2 等价变体（去 USING BTREE/COMMENT/LOCK TABLES，且不含 QRTZ）
- 去重后 78 张表：核心业务 15 + 可视化 19 + 快照 10 + 扩展/企业 22 + Quartz 11
- 发布模型：V2.10.7 引入 snapshot_* 镜像表（仪表板发布不可变态）；Mapper 用 resourceTable='snapshot' 切换
- 6 个 Ext* Mapper 共 107 条自定义 SQL，承载复制(copy_from/copy_id)/快照/恢复/模板导入
- 脚本可复用：scripts/parse_ddl.py、extract_deltas.py、aggregate_schema.py、schema_to_md.py、build_database_docs.py

## 版本升级机制关键事实（Task 8）
- 差异引擎：scripts/diff_versions.py（复用 scan_source 的 MODULE_MAP/classify/map_module）
  - 模式 B（推荐）：--src + --old-ref/--new-ref，用 `git ls-tree -r -l <ref>` 取 blob-sha+size，精确判定 added/removed/modified，不 checkout
  - 模式 A：--old-map/--new-map 两份 source-map.json，按 size 判定（快但精度低）
  - 输出 metadata/diff-<old>..<new>.json（summary 聚合 + added/removed/modified 明细）
- 机制规范：docs/upgrade/index.md（6 步工作流、文件类别→文档映射、多版本共存、兼容性风险分级🔴🟡🟢、检查清单）
- 报告模板：docs/upgrade/template.md
- 示例：v2.10.7→v2.10.8 真实 diff（6 新增/0 删除/139 修改）；风险🟢低——core_dataset_group 新增 is_cross 列 + 注册 datasetCrossListener 启动任务
- 源码仓库可用 tag：v2.2.0 ~ v2.10.25（当前 SKB 对应 v2.10.7）

## 乐享知识库同步
- 2026-07-07 首次同步；2026-07-08 增量同步（数据库 7 篇 + customization 重组）
- space_id: 89fa5a14a9334e4cbe48c9dfc9d97ed0
- 顶层文件夹 "DataEase 源码知识库 v2.10.7"（id: 806febae0e0943708718bb5a820f1eb3）
  - 架构(5) / 后端(11) / 前端(12) / 模块(1) / 数据库(7) / 二次开发(1) / 版本升级(待 Task 8 同步) / INDEX
- 关键文件夹 ID：数据库=29789593a346412bb816ec3ca14887b1，二次开发=b7d9b5d583474cb9a2a7c3c370db2d99
- company_domain: https://lexiangla.com（需 company_from 参数）

## 技术栈关键事实
- 后端：Java 21 + Spring Boot 3.3.0 + MyBatis-Plus 3.5.6 + Calcite 1.35.18
- 前端：Vue 3.3 + TypeScript + Vite 4 + Pinia + Element Plus
- 权限模型：6 层架构（L1 JWT → L2/L3 空转 → L4 桩 → L5 null → L6 分享）

## Git 提交记录
- 04a0073: Foundation (scan + 5 architecture docs)
- 39e1f0f: Backend analysis (11 docs, 100% Java)
- e2ad7f2: Task 9 permission guide
- 59f7b85: Frontend analysis (12 docs)
- d4dde68: Task 7 database analysis (78 tables, 7 docs + scripts)
- 83b7e9f: Architecture diagram .mmd→.md rewrite
- 1085d57: Customization restructure + README/AGENTS alignment
- 5357262: Task 8 版本升级机制（diff_versions.py + docs/upgrade/* 3 篇 + 示例报告）
- Remote: git@github.com:baicl123/dataease-source-knowledge-base.git
