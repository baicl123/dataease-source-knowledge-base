# DataEase 整体架构总览

> 版本：**v2.10.7** ｜ 分析依据：`core/`、`sdk/`、`pom.xml`、`package.json`、关键启动/鉴权类（见各文档引用）。
> 配套图：`docs/diagrams/architecture.mmd`

## 1. 产品定位

DataEase 是开源 BI（商业智能）工具，支持：

- 多数据源接入（OLTP/OLAP/数据仓库/文件/API）
- 拖拽式图表与仪表板制作
- 仪表板分享与嵌入
- AI 辅助分析（v2.10 引入 `ai`/`copilot` 包）

源码是 **Java 21 + Spring Boot 3.3** 后端与 **Vue 3** 前端的单体（可分布式部署）应用。

## 2. 分层架构

| 层 | 模块 | 说明 |
|----|------|------|
| 展现层 | `core/core-frontend` | Vue3 SPA，构建产物由 Spring Boot 静态托管 |
| 接入层 | `io.dataease.interceptor`（仅分享链接）、`sdk/common` `CommunityTokenFilter` | 全局 JWT 鉴权、静态资源、分享链接拦截 |
| 业务层 | `core/core-backend` `io.dataease.*` | 数据集、数据源、图表、可视化、首页、分享、系统、AI、导出等 |
| 能力层 | `sdk`（api / common / distributed / extensions） | 权限 API、公共鉴权、分布式 Feign、扩展点 |
| 引擎层 | `io.dataease.engine` + Apache Calcite | 跨数据源 SQL 解析/计划/执行 |
| 存储层 | H2（元数据）+ 外部数据源 | 元数据存 H2；业务数据在外部库 |

## 3. 部署模式

`core/core-backend/src/main/resources/` 提供三套 Profile：

- **standalone**（默认）：单体，权限逻辑由内置/企业包提供
- **distributed**：权限等领域服务以 Feign 微服务形态独立部署（`sdk/distributed`）
- **desktop**：桌面版，使用 `substitute` 兜底服务（离线场景）

安装/部署脚本见 `installer/`（`install.sh`、`dectl`、`quick_start.sh`、Dockerfile）。

## 4. 后端模块地图（core-backend，包 `io.dataease`）

| 包 | 职责（推断/已验证） |
|----|------|
| `commons` | 公共基类、工具、上下文 |
| `config` | Spring 配置（`DeMvcConfig` 注册拦截器） |
| `dataset` / `datasource` | 数据集与数据源管理（核心领域） |
| `engine` | Calcite SQL 引擎 |
| `chart` / `visualization` / `home` | 图表计算、可视化、工作台 |
| `system` | 系统参数、菜单等 |
| `share` | 仪表板分享/嵌入（JWT 链接令牌） |
| `substitute.permissions.*` | 登录/鉴权/组织/用户**兜底服务**（社区版离线用） |
| `interceptor` | `MybatisInterceptor`（MyBatis SQL 拦截，非 Web 拦截） |
| `ai` / `copilot` | AI 辅助分析（v2.10 新增） |
| `exportCenter` / `job` / `msgCenter` / `operation` | 导出、定时任务、消息、操作日志 |
| `websocket` / `defeign` | 实时推送 / Feign 客户端定义 |
| `menu` / `license` / `map` / `template` / `resource` | 菜单、许可证、地图、模板、资源 |

> 详细包职责与调用链见后续 `docs/backend/*` 逐包分析。

## 5. SDK 模块地图

| 模块 | 路径 | 作用 |
|------|------|------|
| `api-base` | `sdk/api/api-base` | 基础 API 契约 |
| `api-permissions` | `sdk/api/api-permissions` | **权限领域 API**（登录/用户/角色/组织/关系/鉴权/数据集行列权限/嵌入/APIKey/设置/变量） |
| `api-sync` | `sdk/api/api-sync` | 同步相关 API |
| `common` | `sdk/common` | `CommunityTokenFilter`、公共工具、鉴权 BO |
| `distributed` | `sdk/distributed` | 分布式 Feign 客户端 |
| `extensions-datasource` / `-view` / `-datafilling` | `sdk/extensions/*` | 数据源/视图/数据填报扩展 |

## 6. 前端概览（core-frontend）

- 技术栈：Vue 3.3 + TypeScript + Vite 4 + Pinia + Vue Router 4 + Vue I18n 9 + Element Plus（secondary）+ ECharts/AntV
- 源码目录（`src/`）：`views`（页面，含 `dashboard`/`panel`/`visualized`/`data-visualization`/`system`/`share`/`login`/`copilot` 等）、`components`、`api`（按后端领域拆分，`auth.ts`/`login.ts`/`user.ts`/`org.ts`/`dataset.ts`…）、`router`、`store`（Pinia）、`permission.ts`（前端路由守卫）、`locales`、`websocket`
- 构建模式：`build:base`、`build:distributed`、`build:lib`

## 7. 与后续集成目标的关系

`README.md` 规划本知识库服务于后续集成 **RuoYi-Vue-Plus**、**Casbin**。当前 v2.10.7 权限模型为**自研可插拔架构**（见 `security-model.md`）：社区版用 `CommunityTokenFilter` + 权限领域 API；企业版由 `de-xpack` 扩展。接入 Casbin 做 ABAC/RBAC 统一策略引擎的切入点，建议放在 `sdk/api/api-permissions` 的 `AuthApi` 实现层与数据集行列权限（`RowPermissionsApi`/`ColumnPermissionsApi`）处。

## 8. 待验证项

- [Need Verification] 社区版登录签发 JWT 的具体实现位置（`SubstituleLoginServer` 为兜底占位，正式实现疑似在 `de-xpack` 或 `loginServer` Bean）。
- [Need Verification] 正式 DDL/建表 SQL 位置（资源 `sql/` 仅含 `sqlTemplate.stg` 模板，`db/` 目录与安装器需进一步确认）。
- [Inference] `substitute` 包命名疑似历史遗留（"替补/兜底"之意），不代表"用户替换"语义。
