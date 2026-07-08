# DataEase 源码知识库 · 导航中枢

> 当前分析版本：**v2.10.7** ｜ 覆盖率见 [`../metadata/coverage.json`](../metadata/coverage.json)
> 全量文件清单：[`../metadata/source-map.json`](../metadata/source-map.json) ｜ 统计：[`../metadata/statistics.json`](../metadata/statistics.json)
> 工作规范：[`../AGENTS.md`](../AGENTS.md) ｜ 任务：[`../TASKS.md`](../TASKS.md)

## 阅读顺序建议

1. **架构层**（本项目已完成）→ 先看本文，再读 `architecture/`
2. **模块/类层**（进行中）→ `modules/`、`backend/`、`frontend/`
3. **数据库层** → `database/`
4. **二次开发与版本升级** → `customization/`（二次开发：权限方案 / 未来改造记录）、`upgrade/`（版本升级差异，Task 8 待建）

## 架构（Architecture）✅

| 文档 | 内容 |
|------|------|
| [overview.md](architecture/overview.md) | 产品定位、分层架构、部署模式、后端/SDK/前端模块地图 |
| [tech-stack.md](architecture/tech-stack.md) | 后端/前端依赖与版本表 |
| [directory-structure.md](architecture/directory-structure.md) | 仓库/后端包/前端 src/SDK 目录结构 |
| [build-deploy.md](architecture/build-deploy.md) | Maven 多模块、构建、部署模式、安装脚本 |
| [security-model.md](architecture/security-model.md) | **鉴权与权限模型**（CommunityTokenFilter + 权限领域 API + RBAC/ACL/ABAC 映射）— Task 9 基石 |
| [../diagrams/architecture.md](../diagrams/architecture.md) | 架构图集（系统上下文/分层/认证流/权限域，含中文说明） |

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

## 前端（Frontend）✅

> 463 个 .vue + 239 个 .ts 文件已 100% 覆盖（12 篇文档）。

| 文档 | 覆盖范围 | 关键结论 |
|------|---------|---------|
| [index.md](frontend/index.md) | 前端架构导航索引 | 架构图、覆盖统计、技术栈 |
| [infrastructure.md](frontend/infrastructure.md) | router/store/hooks/permission | 路由守卫（动态角色路由）、Pinia 22 模块、三层白名单 |
| [utils-supplement.md](frontend/utils-supplement.md) | utils/config/directive/plugins/models | AES+RSA 加密、CrossPermission、Vue 指令（v-permission/v-click-outside） |
| [api-layer.md](frontend/api-layer.md) | api/ (31 文件) | 8 大领域 API 契约、axios 拦截链、token 自动刷新 |
| [chart-views.md](frontend/chart-views.md) | views/chart/ (141 文件) | 图表编辑器、40 种图表类型、4 引擎（ECharts/G2Plot/L7/S2） |
| [visualization-views.md](frontend/visualization-views.md) | views/data-visualization/dashboard/ (62 文件) | 画布编辑器拖拽/缩放/对齐、预览/分享链接、数据集管理 |
| [views-visualized.md](frontend/views-visualized.md) | views/visualized/ (48 文件) | 数据集/数据源管理界面、InfoTemplate K/V 通用配置 |
| [views-system.md](frontend/views-system.md) | views/system/ (21 文件) | 系统管理（用户/角色/组织/菜单/嵌入/外观/水印/API Key） |
| [views-share.md](frontend/views-share.md) | views/share/ (14 文件) | 公共链接分享（UUID→密码→Ticket→PreviewCanvas） |
| [misc-views.md](frontend/misc-views.md) | layout/pages/mobile/common/template/copilot/login/about/watermark/… | 应用框架、登录 RSA 加密、移动端 Vant 适配、Copilot |
| [components.md](frontend/components.md) | components/ (133 文件) | 画布核心（CanvasCore+Shape+MarkLine）、矩阵排版、筛选器 |
| [custom-component.md](frontend/custom-component.md) | custom-component/ (112 文件) | 组件注册表（16 项）、v-query 筛选器联动、user-view 图表容器 |

## 数据库（Database）✅

> 38 个 SQL（migration 18 + desktop 18 + distributed 1 + installer 1）+ 6 个 Mapper XML，去重后 **78 张表**全部解析。
> 所有表结构由脚本从 DDL 自动提取，结论可回溯到源码。

| 文档 | 内容 |
|------|------|
| [index.md](database/index.md) | 文件清单（38 SQL + 6 Mapper）、表清单（按域）、ER 关系摘要、desktop vs migration 差异 |
| [schema-core.md](database/schema-core.md) | 核心业务域（15 表）：数据源/驱动/引擎、数据集、图表、系统设置/菜单/RSA/收藏 |
| [schema-visualization.md](database/schema-visualization.md) | 可视化域 + 发布快照（28 表）：仪表板/主题/背景/水印/模板/跳转/联动/外部参数/snapshot_* |
| [schema-extension.md](database/schema-extension.md) | 扩展/企业域（22 表）：分享/认证/Copilot/导出/字体/插件/阈值/Webhook/地理/示例数据 |
| [schema-quartz.md](database/schema-quartz.md) | Quartz 调度（11 张 `QRTZ_*` 表） |
| [migrations.md](database/migrations.md) | Flyway 迁移 lineage（V2.0 基线 → V2.10.7 增量），逐版本变更与演进趋势 |
| [mappers.md](database/mappers.md) | 6 个 `Ext*` Mapper 详解（107 条自定义 SQL：复制/快照/恢复/模板导入） |

## 二次开发（Customization）✅

> 所有二次开发相关内容（建议方案 + 未来实际改造记录）统一存放于 `customization/`。

| 文档 | 内容 |
|------|------|
| [permission-development-guide.md](customization/permission-development-guide.md) | **权限二次开发建议（Task 9）** — 六层权限架构剖析 + RBAC/ACL/ABAC 落地方案（A/B/C/D 四方案）+ Casbin 集成 + 安全加固 + 实施检查清单 |

## 版本升级（Upgrade）🔲

- `upgrade/`：版本升级差异分析（变更摘要 / 影响范围 / 兼容性风险）— *Task 8 待建*

## 待补充（非当前 9 任务范围，未来可选）

- **插件机制**（`plugin/`）：sdk/extensions 扩展点 — 待分析
- **对外 API 汇总**（`api/`）：基于 Knife4j/OpenAPI — 待分析
- **架构决策记录**（`adr/`）：关键架构决策 — 待补充
- **术语表**（`glossary/`）：术语对照（Dataset / Datasource / Visualization / Panel / BusiResource …）— 待补充

## 进度速览

| 维度 | 状态 |
|------|------|
| 源码扫描 / Source Map | ✅ 完成（6091 文件，1791 源码文件） |
| 架构分析 | ✅ 完成（5 篇 + 图） |
| 模块/类分析（后端 Java） | ✅ 100%（1003 个 Java，11 篇文档） |
| 模块/类分析（前端） | ✅ 100%（463 .vue + 239 .ts，12 篇文档） |
| 数据库分析 | ✅ 完成（38 SQL + 6 Mapper，78 张表全解析，7 篇文档） |
| 权限二次开发建议 | ✅ 完成（`customization/permission-development-guide.md`，含 4 套方案 + 安全加固） |
