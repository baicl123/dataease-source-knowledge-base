#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建 docs/database/ 下的数据库知识库文档。
复用 /tmp/de_schema_md.txt（由 schema_to_md.py 生成，含全部 78 张表的 Markdown 表）。
用法： python3 build_database_docs.py
"""
import os, re

SRC = '/tmp/de_schema_md.txt'
OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'database')
os.makedirs(OUT, exist_ok=True)

# ---- 1. 解析 markdown 表为 {table_name: md_block} ----
def load_tables(path):
    blocks = {}
    cur_name = None; cur_lines = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^### (\S+)  ', line)
            if m:
                if cur_name: blocks[cur_name] = ''.join(cur_lines)
                cur_name = m.group(1); cur_lines = [line]
            elif cur_name:
                cur_lines.append(line)
    if cur_name: blocks[cur_name] = ''.join(cur_lines)
    return blocks

T = load_tables(SRC)

def tbl(name):
    return T.get(name, f"<!-- 未找到表 {name} 的 schema -->\n")

# ---- 2. 领域分组 ----
CORE = ['core_datasource','core_driver','core_driver_jar','core_dataset_group',
        'core_dataset_table','core_dataset_table_field','core_dataset_table_sql_log',
        'core_de_engine','core_chart_view','core_rsa','core_store','core_menu',
        'core_opt_recent','core_sys_setting','core_ds_finish_page']

VIS = ['data_visualization_info','visualization_background','visualization_background_image',
       'visualization_subject','visualization_link_jump','visualization_link_jump_info',
       'visualization_link_jump_target_view_info','visualization_linkage','visualization_linkage_field',
       'visualization_outer_params','visualization_outer_params_info',
       'visualization_outer_params_target_view_info','visualization_template',
       'visualization_template_category','visualization_template_category_map',
       'visualization_template_extend_data','visualization_watermark','visualization_report_filter']

SNAP = ['snapshot_core_chart_view','snapshot_data_visualization_info','snapshot_visualization_link_jump',
        'snapshot_visualization_link_jump_info','snapshot_visualization_link_jump_target_view_info',
        'snapshot_visualization_linkage','snapshot_visualization_linkage_field',
        'snapshot_visualization_outer_params','snapshot_visualization_outer_params_info',
        'snapshot_visualization_outer_params_target_view_info']

EXT = ['xpack_share','xpack_setting_authentication','xpack_platform_token','xpack_plugin',
       'xpack_threshold_info','xpack_threshold_instance','xpack_webhook','core_copilot_config',
       'core_copilot_msg','core_copilot_token','core_export_task','core_font','core_share_ticket',
       'core_sys_startup_job','core_api_traffic','area','core_area_custom','core_custom_geo_area',
       'core_custom_geo_sub_area','de_template_version','demo_tea_material','demo_tea_order']

QUARTZ = ['QRTZ_JOB_DETAILS','QRTZ_TRIGGERS','QRTZ_SIMPLE_TRIGGERS','QRTZ_CRON_TRIGGERS',
          'QRTZ_SIMPROP_TRIGGERS','QRTZ_BLOB_TRIGGERS','QRTZ_CALENDARS','QRTZ_PAUSED_TRIGGER_GRPS',
          'QRTZ_FIRED_TRIGGERS','QRTZ_SCHEDULER_STATE','QRTZ_LOCKS']

def section(title, names):
    out = [f"\n## {title}\n"]
    for n in names:
        out.append(tbl(n))
    return ''.join(out)

# ---- 3. 各文档 ----
def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('written:', path)

# 3.1 index.md
index = f"""# DataEase 数据库分析索引（v2.10.7）

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
| 核心业务 | {', '.join('`'+n+'`' for n in CORE)} | {len(CORE)} |
| 可视化 | {', '.join('`'+n+'`' for n in VIS)} | {len(VIS)} |
| 快照（发布镜像） | {', '.join('`'+n+'`' for n in SNAP)} | {len(SNAP)} |
| 扩展/企业 | {', '.join('`'+n+'`' for n in EXT)} | {len(EXT)} |
| Quartz 调度 | {', '.join('`'+n+'`' for n in QUARTZ)} | {len(QUARTZ)} |
| **合计** | | **{len(CORE)+len(VIS)+len(SNAP)+len(EXT)+len(QUARTZ)}** |

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
"""
write(os.path.join(OUT,'index.md'), index)

# 3.2 schema-core.md
core_doc = f"""# 核心业务域表结构（v2.10.7）

> 15 张表，覆盖数据源、数据集、图表、引擎、驱动、系统设置、菜单、收藏与最近访问。
> 全部源自 `db/migration/V2.0__core_ddl.sql` 基线（少数列在增量脚本中扩展）。

## 域职责

核心业务域是 DataEase 的“数据资产”层：从外部数据源接入（`core_datasource`）→ 构建数据集（`core_dataset_group`/`core_dataset_table`/`core_dataset_table_field`）→ 在图表（`core_chart_view`）中消费。系统级支撑表（`core_sys_setting`/`core_menu`/`core_rsa`/`core_store`/`core_opt_recent`）提供配置、鉴权底座、收藏与最近使用。

{section('数据源与驱动', ['core_datasource','core_driver','core_driver_jar','core_de_engine'])}
{section('数据集', ['core_dataset_group','core_dataset_table','core_dataset_table_field','core_dataset_table_sql_log'])}
{section('图表', ['core_chart_view'])}
{section('系统支撑', ['core_sys_setting','core_menu','core_rsa','core_store','core_opt_recent','core_ds_finish_page'])}
"""
write(os.path.join(OUT,'schema-core.md'), core_doc)

# 3.3 schema-visualization.md
vis_doc = f"""# 可视化域表结构（v2.10.7）

> 19 张主表 + 10 张快照镜像表 = 29 张。覆盖仪表板/大屏资源树、画布样式、主题、背景、水印、模板、跳转/联动/外部参数交互配置，以及发布时的 `snapshot_*` 镜像。

## 域职责

可视化域以 `data_visualization_info` 为根（folder/panel 自引用树），聚合图表组件。交互能力通过三套平行模型实现：
- **跳转（Link Jump）**：`visualization_link_jump` → `visualization_link_jump_info` → `visualization_link_jump_target_view_info`
- **联动（Linkage）**：`visualization_linkage` → `visualization_linkage_field`
- **外部参数（Outer Params）**：`visualization_outer_params` → `visualization_outer_params_info` → `visualization_outer_params_target_view_info`

三套模型均带 `copy_from/copy_id` 复制链；发布（publish）时将当前态写入对应的 `snapshot_*` 表，供只读预览/回滚使用。

{section('仪表板资源', ['data_visualization_info','visualization_subject','visualization_background','visualization_background_image','visualization_watermark','visualization_report_filter'])}
{section('模板市场', ['visualization_template','visualization_template_category','visualization_template_category_map','visualization_template_extend_data'])}
{section('跳转配置', ['visualization_link_jump','visualization_link_jump_info','visualization_link_jump_target_view_info'])}
{section('联动配置', ['visualization_linkage','visualization_linkage_field'])}
{section('外部参数', ['visualization_outer_params','visualization_outer_params_info','visualization_outer_params_target_view_info'])}
{section('发布快照镜像（snapshot_*）', SNAP)}
"""
write(os.path.join(OUT,'schema-visualization.md'), vis_doc)

# 3.4 schema-extension.md
ext_doc = f"""# 扩展 / 企业域表结构（v2.10.7）

> 22 张表，覆盖分享/认证、AI Copilot、导出任务、字体、插件、阈值告警、Webhook、自定义地理、API 流量、系统启动任务、模板版本，以及示例数据。

## 域职责

本域表多由增量迁移脚本（V2.1–V2.10.7）引入，部分为**企业版（xpack）/扩展能力**的数据落地：
- **分享与认证**：`xpack_share`（公共链接）、`core_share_ticket`（访问票据）、`xpack_setting_authentication`（LDAP/CAS/OIDC 认证源，见 security-model.md）。
- **AI Copilot**：`core_copilot_config`/`core_copilot_token`/`core_copilot_msg`（见 ai-copilot.md）。
- **导出/插件/字体**：`core_export_task`、`xpack_plugin`、`core_font`。
- **阈值告警/Webhook**：`xpack_threshold_info`/`xpack_threshold_instance`/`xpack_webhook`（企业版告警）。
- **地理**：`area`（内置行政区划）、`core_area_custom`/`core_custom_geo_area`/`core_custom_geo_sub_area`（自定义地理）。
- **运维**：`core_sys_startup_job`（启动任务）、`core_api_traffic`（API 并发流量）、`de_template_version`（Flyway 风格版本表）。
- **示例数据**：`demo_tea_material`/`demo_tea_order`（中文列名，内置奶茶店示例，131 行种子数据）。

> 注：`xpack_*` 与部分 `core_*` 表（copilot/export/font/threshold/plugin/webhook）的**完整建表 DDL 出现在社区 migration 脚本中**，但其高级逻辑由 de-xpack 企业 submodule 承载（见 security-model.md 与 AGENTS.md 关于 de-xpack 的说明）。

{section('分享与认证', ['xpack_share','xpack_setting_authentication','xpack_platform_token','core_share_ticket'])}
{section('AI Copilot', ['core_copilot_config','core_copilot_msg','core_copilot_token'])}
{section('导出 / 插件 / 字体 / 阈值 / Webhook', ['core_export_task','xpack_plugin','core_font','xpack_threshold_info','xpack_threshold_instance','xpack_webhook'])}
{section('地理与运维', ['area','core_area_custom','core_custom_geo_area','core_custom_geo_sub_area','core_sys_startup_job','core_api_traffic','de_template_version'])}
{section('示例数据', ['demo_tea_material','demo_tea_order'])}
"""
write(os.path.join(OUT,'schema-extension.md'), ext_doc)

# 3.5 schema-quartz.md
qz_doc = f"""# Quartz 调度表结构（v2.10.7）

> 11 张 `QRTZ_*` 表，标准 Quartz 2.x JDBC JobStore  schema（表名前缀 `QRTZ_`）。DataEase 用其承载数据源同步任务（`core_datasource_task`）等定时调度。

## 域职责

Quartz 是 DataEase 的**双轨调度**之一（另一轨为 Spring `@Scheduled`，见 job-msg-resource.md）。所有表以 `SCHED_NAME` 为调度器命名空间首列，形成以下子模型：

- **作业定义**：`QRTZ_JOB_DETAILS`（作业）+ `QRTZ_TRIGGERS`（触发器主表）
- **触发器类型子表**：`QRTZ_CRON_TRIGGERS`（Cron）、`QRTZ_SIMPLE_TRIGGERS`（简单间隔）、`QRTZ_SIMPROP_TRIGGERS`（自定义属性）、`QRTZ_BLOB_TRIGGERS`（序列化触发器）
- **运行时**：`QRTZ_FIRED_TRIGGERS`（已触发实例）、`QRTZ_PAUSED_TRIGGER_GRPS`（暂停组）、`QRTZ_SCHEDULER_STATE`（调度器心跳）、`QRTZ_LOCKS`（行锁）
- **日历**：`QRTZ_CALENDARS`

> ⚠️ 这些表**仅存在于 migration（MySQL）集**；desktop（H2）集不含 QRTZ 表，桌面版改用 substitute 本地调度（见 index.md §4）。

{section('Quartz 表', QUARTZ)}
"""
write(os.path.join(OUT,'schema-quartz.md'), qz_doc)

print("ALL DOCS WRITTEN")
