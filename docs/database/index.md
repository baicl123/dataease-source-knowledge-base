# DataEase 数据库分析索引（v2.10.7）

> 分析对象：core-backend 的 Flyway DDL（`core/core-backend/src/main/resources/db/`）与 MyBatis Mapper XML（`core/core-backend/src/main/resources/mybatis/`）。
> 所有表结构均由脚本从 DDL 自动解析，结论可回溯到源码。

## 1. 文件清单

### SQL 文件（38 个）
| 集合 | 数量 | 路径 | 说明 |
|------|------|------|------|
| 迁移脚本（MySQL） | 18 | `db/migration/V2.0__*.sql` … `V2.10.7__*.sql` | **规范 schema**，Flyway 顺序迁移（基线 + 增量） |
| 桌面版（H2 变体） | 18 | `db/desktop/V2.0__*.sql` … `V2.10.7__*.sql` | 与 migration 同构，去掉 `USING BTREE`/`COMMENT`/`LOCK TABLES` 且**不含 QRTZ 表**（桌面用 substitute 调度） |
| 分布式管理库 | 1 | `sdk/distributed/.../db/distributed/manage/V1.1__manage_ddl.sql` | 分布式模式下独立 manage 库 |
| 安装初始化 | 1 | `installer/dataease/bin/mysql/init.sql` | **空文件**（0 行），初始化逻辑在 Flyway 完成 |

> migration 与 desktop 为**部署模式变体**（MySQL vs H2），下表以 migration（MySQL）为规范基线做完整解析；desktop 差异见 §4。
> 去重后唯一 schema = **40（V2.0 基线）+ 38（增量新建）= 78 张业务/系统表**（不含 QRTZ 在 desktop 的缺失）。

### Mapper XML（6 个）
| 文件 | namespace | 语句数 | 职责 |
|------|-----------|--------|------|
| ExtCoreChartMapper.xml | `io.dataease.chart.dao.ext.mapper.ExtChartViewMapper` | 3 | 图表查询/自定义列表/按场景批量删除 |
| ExtDataVisualizationMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtDataVisualizationMapper` | 35 | 仪表板复制、快照、恢复、最近访问 |
| ExtVisualizationLinkJumpMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtVisualizationLinkJumpMapper` | 22 | 跳转配置查询/复制/删除（含 snapshot 变体） |
| ExtVisualizationLinkageMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtVisualizationLinkageMapper` | 13 | 联动配置查询/复制/删除 |
| ExtVisualizationOuterParamsMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtVisualizationOuterParamsMapper` | 13 | 外部参数查询 |
| ExtVisualizationTemplateMapper.xml | `io.dataease.template.dao.ext.ExtVisualizationTemplateMapper` | 21 | 模板列表/分类/导入应用 |

## 2. 表清单（按业务域）

| 域 | 表 | 数量 |
|----|----|------|
| 核心业务 | `core_datasource`, `core_driver`, `core_driver_jar`, `core_dataset_group`, `core_dataset_table`, `core_dataset_table_field`, `core_dataset_table_sql_log`, `core_de_engine`, `core_chart_view`, `core_rsa`, `core_store`, `core_menu`, `core_opt_recent`, `core_sys_setting`, `core_ds_finish_page` | 15 |
| 可视化 | `data_visualization_info`, `visualization_background`, `visualization_background_image`, `visualization_subject`, `visualization_link_jump`, `visualization_link_jump_info`, `visualization_link_jump_target_view_info`, `visualization_linkage`, `visualization_linkage_field`, `visualization_outer_params`, `visualization_outer_params_info`, `visualization_outer_params_target_view_info`, `visualization_template`, `visualization_template_category`, `visualization_template_category_map`, `visualization_template_extend_data`, `visualization_watermark`, `visualization_report_filter` | 18 |
| 快照（发布镜像） | `snapshot_core_chart_view`, `snapshot_data_visualization_info`, `snapshot_visualization_link_jump`, `snapshot_visualization_link_jump_info`, `snapshot_visualization_link_jump_target_view_info`, `snapshot_visualization_linkage`, `snapshot_visualization_linkage_field`, `snapshot_visualization_outer_params`, `snapshot_visualization_outer_params_info`, `snapshot_visualization_outer_params_target_view_info` | 10 |
| 扩展/企业 | `xpack_share`, `xpack_setting_authentication`, `xpack_platform_token`, `xpack_plugin`, `xpack_threshold_info`, `xpack_threshold_instance`, `xpack_webhook`, `core_copilot_config`, `core_copilot_msg`, `core_copilot_token`, `core_export_task`, `core_font`, `core_share_ticket`, `core_sys_startup_job`, `core_api_traffic`, `area`, `core_area_custom`, `core_custom_geo_area`, `core_custom_geo_sub_area`, `de_template_version`, `demo_tea_material`, `demo_tea_order` | 22 |
| Quartz 调度 | `QRTZ_JOB_DETAILS`, `QRTZ_TRIGGERS`, `QRTZ_SIMPLE_TRIGGERS`, `QRTZ_CRON_TRIGGERS`, `QRTZ_SIMPROP_TRIGGERS`, `QRTZ_BLOB_TRIGGERS`, `QRTZ_CALENDARS`, `QRTZ_PAUSED_TRIGGER_GRPS`, `QRTZ_FIRED_TRIGGERS`, `QRTZ_SCHEDULER_STATE`, `QRTZ_LOCKS` | 11 |
| **合计** | | **76** |

## 3. 关键关系（ER 摘要）

- **数据源 → 数据集**：`core_datasource.id` 1:N `core_dataset_table.datasource_id`；`core_dataset_group` 是数据集分组树（pid 自引用），其下挂 `core_dataset_table`（mode=0 直连 / 1 同步）。
- **数据集 → 字段**：`core_dataset_table.id` 1:N `core_dataset_table_field.dataset_table_id`；字段含原始/复制/计算字段（`ext_field`）。
- **数据集 → 图表**：`core_dataset_table.id` 1:N `core_chart_view.table_id`；图表轴/样式全部以 longtext JSON 存储。
- **仪表板**：`data_visualization_info`（node_type=folder/panel，pid 自引用树）聚合 `core_chart_view`（scene_id=仪表板 id，chart_type=private）。
- **交互配置**：`visualization_link_jump`/`visualization_linkage`/`visualization_outer_params` 均以 `*_info` 子表 + `copy_from/copy_id` 复制链建模；发布时写入对应的 `snapshot_*` 镜像表。
- **调度**：业务表通过 `qrtz_instance`/`sync_status` 字段关联 Quartz（`QRTZ_*`）；同步任务 `core_datasource_task` 经 `ScheduleManager` 注册 Quartz CronJob。
- **鉴权/分享**：`xpack_share`（uuid+密码+资源）配合 `core_share_ticket`（访问票据）；`xpack_setting_authentication` 记录 LDAP/CAS/OIDC 等认证源。

## 4. desktop vs migration 差异（H2 变体）

| 差异点 | migration（MySQL） | desktop（H2） |
|--------|--------------------|---------------|
| 主键/索引 | `PRIMARY KEY (id) USING BTREE` | `PRIMARY KEY (id)` |
| 表注释 | `COMMENT='驱动'` | 无 |
| 锁表语句 | `LOCK TABLES ... WRITE` / `UNLOCK TABLES` | 无 |
| Quartz 表 | **包含** 11 张 `QRTZ_*` | **不含**（桌面用 substitute 本地调度） |
| 其余表与列 | 完全一致 | 完全一致 |

> desktop 集是离线/桌面版部署使用的 H2 兼容 DDL，表结构与列定义与 migration 等价（除 MySQL 专有语法与 Quartz 外）。

## 5. 子文档导航

- [schema-core.md](schema-core.md) — 核心业务域（15 表）
- [schema-visualization.md](schema-visualization.md) — 可视化域 + 快照（29 表）
- [schema-extension.md](schema-extension.md) — 扩展/企业域（22 表）
- [schema-quartz.md](schema-quartz.md) — Quartz 调度（11 表）
- [migrations.md](migrations.md) — Flyway 迁移 lineage（V2.0 → V2.10.7）
- [mappers.md](mappers.md) — 6 个 MyBatis Mapper XML 详解
