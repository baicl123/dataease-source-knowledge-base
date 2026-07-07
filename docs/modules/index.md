# 后端模块索引（Module Map）

> 版本：**v2.10.7**。本页是后端各业务领域的**模块级导航**，逐包的深度分析见 `docs/backend/*.md`。
> 数据库表（对应 `docs/database/`）将在 Task 7 中补全，此处先标注"待补"。

| 领域 | 后端文档 | 关键类（入口） | 暴露 API（Controller/Feign） | DB 表 |
|------|----------|----------------|------------------------------|--------|
| 基础架构/配置 | [foundation](backend/foundation.md) | CorePermissionManage, MybatisInterceptor, Ehcache 配置 | — | sys_*（待补） |
| 鉴权与分享 | [auth-core](backend/auth-core.md) | Substitule*Server（兜底）, LinkInterceptor, LinkTokenUtil | /link/**（分享） | — |
| 权限领域契约 | [api-permissions](backend/api-permissions.md) | AuthApi/RoleApi/UserApi/OrgApi/RowPermissionsApi… | /api/permissions/**（Feign 远端） | — |
| 数据集 | [dataset](backend/dataset.md) | DatasetSQLManage, DatasetDataManage, PermissionManage | /dataset/**, /chart/** | dataset_table, dataset_group, dataset_field（待补） |
| 数据源 | [datasource](backend/datasource.md) | DatasourceType, DatasourceSyncManage, Provider/ProviderFactory | /datasource/** | datasource（待补） |
| SQL 引擎 | [engine](backend/engine.md) | ST4 SQL 构建层（Calcite 集成在 datasource/provider） | — | — |
| 可视化/图表 | [visualization](backend/visualization.md) | ChartDataManage, ChartViewManege, DataVisualizationInfo | /chartView/**, /visualization/** | core_chart_view, core_data_visualization（待补） |
| AI/Copilot | [ai-copilot](backend/ai-copilot.md) | CopilotService, CopilotAPI, CopilotManage | /copilot/** | core_copilot_token（待补） |
| 任务/导出/消息/资源 | [job-msg-resource](backend/job-msg-resource.md) | 调度/导出线程池/操作日志/地图字体 | /exportCenter/**, /map/**, /font/** | — |
| 集成/SDK 能力层 | [integration-sdk](backend/integration-sdk.md) | CommunityTokenFilter, LicenseUtil, PermissionFeignService | — | — |
| 应用入口 | [application-entry](backend/application-entry.md) | CoreApplication, MybatisPlusGenerator | — | — |

## 模块依赖概要（语言无关）

```
前端(Vue) ──HTTP──> core-backend(Controller)
                         │
        ┌────────────────┼───────────────────────────────┐
        ▼                ▼                               ▼
   dataset ──> engine ──> datasource ──> (外部数据源/JDBC驱动)
        │                │
        ▼                ▼
   api-permissions(API契约) ──Feign──> 权限微服务(de-xpack/分布式)
        │
   CommunityTokenFilter(sdk/common) ──JWT 校验──> 全链路
```

## 说明

- 后端 Java 文件（1003）已 100% 覆盖于上述 11 篇文档（含包根 2 文件）。
- 企业版实现（`de-xpack`、正式 loginServer 等）不在本 OSS 仓，相关处已标注 `[Need Verification]`。
- 下一步：前端分析（Task 6）、数据库分析（Task 7）、版本升级机制（Task 8）、权限二次开发建议（Task 9）。
