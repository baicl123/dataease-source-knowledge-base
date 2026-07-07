# DataEase 源码知识库 · 导航中枢

> 当前分析版本：**v2.10.7** ｜ 覆盖率见 [`../metadata/coverage.json`](../metadata/coverage.json)
> 全量文件清单：[`../metadata/source-map.json`](../metadata/source-map.json) ｜ 统计：[`../metadata/statistics.json`](../metadata/statistics.json)
> 工作规范：[`../AGENTS.md`](../AGENTS.md) ｜ 任务：[`../TASKS.md`](../TASKS.md)

## 阅读顺序建议

1. **架构层**（本项目已完成）→ 先看本文，再读 `architecture/`
2. **模块/类层**（进行中）→ `modules/`、`backend/`、`frontend/`
3. **数据库层** → `database/`
4. **升级与二次开发** → `upgrade/`、`adr/`（含权限二次开发建议）

## 架构（Architecture）✅

| 文档 | 内容 |
|------|------|
| [overview.md](architecture/overview.md) | 产品定位、分层架构、部署模式、后端/SDK/前端模块地图 |
| [tech-stack.md](architecture/tech-stack.md) | 后端/前端依赖与版本表 |
| [directory-structure.md](architecture/directory-structure.md) | 仓库/后端包/前端 src/SDK 目录结构 |
| [build-deploy.md](architecture/build-deploy.md) | Maven 多模块、构建、部署模式、安装脚本 |
| [security-model.md](architecture/security-model.md) | **鉴权与权限模型**（CommunityTokenFilter + 权限领域 API + RBAC/ACL/ABAC 映射）— Task 9 基石 |
| [../diagrams/architecture.mmd](../diagrams/architecture.mmd) | Mermaid 架构图（系统上下文/分层/认证流/权限域） |

## 模块（Modules）✅

- [modules/index.md](modules/index.md)：后端业务域模块地图（领域 → 文档 → 关键类 → 暴露 API → DB 表）

## 后端（Backend）✅

> 1003 个 Java 文件已 100% 覆盖（逐包 `io.dataease.*` + SDK + 包根 2 文件）。

| 文档 | 覆盖包 / 范围 | 关键结论 |
|------|---------------|----------|
| [foundation.md](backend/foundation.md) | commons/config/startup/listener/interceptor/system/menu | 启动编排、MybatisInterceptor 字段加密、Ehcache、菜单 |
| [auth-core.md](backend/auth-core.md) | substitute(permissions)/share | 兜底鉴权实现 + 分享链接 JWT 校验（含硬编码密钥风险） |
| [api-permissions.md](backend/api-permissions.md) | sdk/api/api-permissions | 权限领域契约：RBAC+ACL+ABAC 雏形（行/列权限表达式树） |
| [dataset.md](backend/dataset.md) | dataset | 数据集建模→SQL、行列权限注入点 |
| [datasource.md](backend/datasource.md) | datasource + sdk/extensions/extensions-datasource | 18 类数据源、驱动隔离、连接池、Provider 扩展 |
| [engine.md](backend/engine.md) | engine | ST4 SQL 构建层（Calcite 集成在 datasource/provider） |
| [visualization.md](backend/visualization.md) | chart/visualization/home/template | 图表取数链路、42 Handler、发布镜像、模板市场 |
| [ai-copilot.md](backend/ai-copilot.md) | ai/copilot | 外部 LLM 调用、令牌管理、HTTPS 校验关闭风险 |
| [job-msg-resource.md](backend/job-msg-resource.md) | job/exportCenter/msgCenter/operation/resource/map/font | 双轨调度、导出线程池、操作日志、地图字体 |
| [integration-sdk.md](backend/integration-sdk.md) | defeign/websocket/license + sdk(distributed/api-base/api-sync/common/ext-*) | CommunityTokenFilter、LicenseUtil、Feign 客户端 |
| [application-entry.md](backend/application-entry.md) | 包根 CoreApplication / MybatisPlusGenerator | 启动类注解、代码生成器 |

## 前端（Frontend）🔲

- `frontend/`：Vue 组件/路由/状态/API 分析 — *待分析*（463 个 .vue / 257 个 .ts）

## 数据库（Database）🔲

- `database/`：SQL 脚本、Mapper、表结构 — *待分析*（38 个 SQL）

## 插件机制（Plugin）🔲

- `plugin/`：扩展点（sdk/extensions）机制 — *待分析*

## API 说明（API）🔲

- `api/`：对外 REST API 汇总（基于 Knife4j/OpenAPI）— *待分析*

## 升级差异（Upgrade）🔲

- `upgrade/`：版本间差异分析（支持 v2.10.7 → 后续版本增量更新）— *待分析*

## 架构决策记录（ADR）🔲

- `adr/`：关键架构决策（如自研鉴权、Calcite 引擎选型、可插拔权限）— *待补充*

## 术语表（Glossary）🔲

- `glossary/`：术语对照（Dataset / Datasource / Visualization / Panel / BusiResource ...）— *待补充*

## 进度速览

| 维度 | 状态 |
|------|------|
| 源码扫描 / Source Map | ✅ 完成（6091 文件，1791 源码文件） |
| 架构分析 | ✅ 完成（5 篇 + 图） |
| 模块/类分析（后端 Java） | ✅ 100%（1003 个 Java，11 篇文档） |
| 模块/类分析（前端/数据库） | 🔲 待分析 |
| 前端分析 | 🔲 0% |
| 数据库分析 | 🔲 0% |
| 权限二次开发建议 | 🔲 依赖 `security-model.md` + `backend/api-permissions.md`（基石已完成） |
