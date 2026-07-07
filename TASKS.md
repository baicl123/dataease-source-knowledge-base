# TASKS.md


## Current Project

DataEase

源码路径：`~/workspace/code/references/dataease`


## Current Version

v2.10.7


## Current Goal

建立 DataEase Source Knowledge Base。


## Current Phase

Phase 1 —— 模块/类级分析（已完成：源码扫描、Source Map、整体架构、后端逐包分析、权限二次开发建议）


## Task Status

- [x] 1. 扫描源码（6091 受控文件，git ls-files）
- [x] 2. 建立 Source Map（metadata/source-map.json；源码文件目标 1791）
- [x] 3. 分析整体架构（docs/architecture/* 5 篇 + docs/diagrams/architecture.mmd）
- [x] 3.1 鉴权与权限安全模型（docs/architecture/security-model.md，Task 9 基石）
- [x] 4. 分析模块（docs/modules/index.md）
- [x] 5. 分析 Backend（docs/backend/ 11 篇，1003 个 Java 文件 100% 覆盖）
- [ ] 6. 分析 Frontend（docs/frontend/，463 .vue / 257 .ts）
- [ ] 7. 分析 Database（docs/database/，38 个 SQL）
- [ ] 8. 建立版本升级机制（scripts/scan_source.py 已可复用做版本差异）
- [x] 9. 二次开发建议——权限检查（RBAC/ACL/ABAC，docs/upgrade/permission-development-guide.md）


## Task（编号映射）

1. 扫描源码 2. 建立 Source Map 3. 分析整体架构 4. 分析模块 5. 分析 Backend
6. 分析 Frontend 7. 分析 Database 8. 建立版本升级机制
9. 二次开发建议（重点围绕权限检查，包括 RBAC、ACL、ABAC 等）
