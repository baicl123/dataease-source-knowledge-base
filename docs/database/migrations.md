# DataEase 数据库迁移 Lineage（v2.10.7）

> 迁移机制：Flyway。脚本位于 `core/core-backend/src/main/resources/db/migration/`，命名 `V{version}__{desc}.sql`，按版本号升序执行（基线 `V2.0__core_ddl.sql` 一次性建 40 张表，后续为增量）。
> 本文档以 migration（MySQL）集为规范，逐版本记录结构变更。desktop（H2）集为等价变体（见 index.md §4）。
> 所有变更由脚本自动提取，可回溯到源码 DDL 文件。

## 迁移机制要点

- **基线**：`V2.0__core_ddl.sql`（4174 行）一次性建立 40 张表（含 11 张 `QRTZ_*`）+ 20 条种子数据（菜单、RSA 密钥等）。
- **增量**：V2.1 → V2.10.7 仅做 `CREATE TABLE` / `ALTER TABLE ADD` / `CREATE INDEX` / `DROP`（旧表清理）。
- **种子数据**：V2.1(7)、V2.3(2)、V2.6(131 示例数据)、V2.9(4)、V2.10(3)、V2.10.2(3)、V2.10.3(3) 等含 `INSERT`。
- **xpack 引用**：多个增量脚本 `ALTER` 了 `xpack_*`/`core_copilot_*` 等表——这些表的建表 DDL 同样落在社区 migration 脚本中，但其高级逻辑由 de-xpack 企业 submodule 承载。

## 逐版本变更

### V2.0（基线）
- 建立全部 40 张核心/可视化/Quartz 表，含 `QRTZ_*` 11 张。
- 含 20 条种子（菜单树、RSA 密钥、系统设置、主题、背景等）。
- 另含一批 `ALTER TABLE ... ADD COLUMN core_datasource.update_by` 与若干 `DROP TABLE`（升级清理历史表）。

### V2.1
- 新建：`visualization_template`、`visualization_template_category`、`visualization_template_category_map`、`visualization_template_extend_data`、`core_area_custom`。
- `ALTER`：`core_opt_recent` 结构调整。
- 种子：7 条（模板初始数据）。

### V2.2（`update_table_desc_ddl`）
- 纯 `ALTER/MODIFY`：对 19 张表补充/修正列注释与类型（core_dataset_group、core_dataset_table_field、core_datasource_task、core_datasource_task_log、core_driver_jar、core_rsa、data_visualization_info、visualization_*、core_opt_recent 等）。**无结构新增**，仅元数据完善。

### V2.3
- 新建：`visualization_watermark`。
- `visualization_template` 增加 `use_count` 列。
- 种子：2 条。

### V2.4
- **空增量**（0 操作），占位版本。

### V2.5
- 新建：`visualization_outer_params`、`visualization_outer_params_info`、`visualization_outer_params_target_view_info`（外部参数交互模型）。
- `ALTER`：`data_visualization_info` 调整。

### V2.6
- 新建：`demo_tea_material`、`demo_tea_order`（示例数据，中文列名）、`de_template_version`（Flyway 风格版本表）。
- `xpack_share` 增加 `auto_pwd`；`data_visualization_info` 增加 `version`；`visualization_template` 增加 `version`。
- 种子：131 条（奶茶店 demo）。

### V2.7
- 新建：`core_sys_startup_job`、`core_export_task`、`xpack_platform_token`（平台令牌）。
- `core_chart_view` 增加 `aggregate`；`xpack_setting_authentication` 增加 `plugin_json`/`synced`/`valid`。

### V2.8
- 新建：`xpack_plugin`、`core_share_ticket`（访问票据）、`visualization_report_filter`（定时报告过滤）。
- `core_export_task` 增加 `msg`；`xpack_share` 增加 `ticket_require`。

### V2.9
- 新建：`core_copilot_msg`、`core_copilot_token`、`core_copilot_config`、`core_api_traffic`（AI Copilot + API 流量）。
- `ALTER`：`visualization_template` 调整。
- 种子：4 条。

### V2.10
- 新建：`xpack_threshold_info`、`xpack_threshold_instance`（阈值告警）、`core_font`（字体）。
- `core_dataset_table_field` 增加 `params`；`core_datasource` 增加 `enable_data_fill`；`core_chart_view` 增加 `flow_map_start_name`/`flow_map_end_name`/`ext_color`；`core_font` 增加 `size`/`size_type`。
- 种子：3 条。

### V2.10.1
- `visualization_outer_params_info` 增加 `required`；`visualization_link_jump_info` 增加 `window_size`。

### V2.10.2
- `core_chart_view` 增加 `custom_attr_mobile`（移动端样式）。

### V2.10.3
- 新建：`core_custom_geo_area`、`core_custom_geo_sub_area`（自定义地理区域）。
- `data_visualization_info` 增加 `content_id`/`check_version`；`visualization_link_jump_target_view_info` 增加 `target_type` 并调整结构。
- 种子：3 条。

### V2.10.4
- 新建：`xpack_webhook`（Webhook 通知）。
- `core_chart_view` 增加 `sort_priority`。
- `core_datasource_task_log` 增加索引 `idx_dataset_table_task_log_A`。
- `ALTER`：core_copilot_config/token、core_font、de_template_version、visualization_subject、xpack_platform_token、xpack_threshold_info/instance、core_area_custom、core_export_task 等表结构微调。

### V2.10.5
- `xpack_threshold_info` 增加 `reci_larksuite_groups`（飞书群聊接收）。

### V2.10.6
- `core_dataset_table_field` 增加 `group_list`/`other_group`（分组字段扩展）。

### V2.10.7
- 新建 10 张 `snapshot_*` 镜像表：`snapshot_core_chart_view`、`snapshot_data_visualization_info`、`snapshot_visualization_link_jump`/`_info`/`_target_view_info`、`snapshot_visualization_linkage`/`_field`、`snapshot_visualization_outer_params`/`_info`/`_target_view_info`。
- 用途：仪表板**发布（publish）**时把当前态写入 snapshot 表，作为只读镜像与回滚点（配合 `ExtDataVisualizationMapper` 的 snapshot/restore 语句）。

## 演进趋势小结

1. **交互能力持续增强**：外部参数（V2.5）、跳转/联动细化（V2.10.1/10.3）、快照发布（V2.10.7）。
2. **企业/扩展能力下沉到社区 DDL**：Copilot（V2.9）、阈值告警/Webhook（V2.10/10.4/10.5）、字体/插件/平台令牌（V2.8/10）。
3. **移动端支持**：`mobile_layout`（V2.3 起）、`custom_attr_mobile`（V2.10.2）。
4. **地理能力**：内置 `area` + 自定义 `core_area_custom`/`core_custom_geo_*`（V2.1/10.3）。
5. **发布模型成熟**：从单纯 `status` 标志演进到 `snapshot_*` 镜像表（V2.10.7），支持不可变发布态。
