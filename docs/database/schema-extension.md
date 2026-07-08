# 扩展 / 企业域表结构（v2.10.7）

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


## 分享与认证
### xpack_share  （9 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `creator` | `bigint` | NOT NULL |  | 创建人 |
| `time` | `bigint` | NOT NULL |  | 创建时间 |
| `exp` | `bigint` | NULL | NULL | 过期时间 |
| `uuid` | `varchar(16)` | NOT NULL |  | uuid |
| `pwd` | `varchar(255)` | NULL | NULL | 密码 |
| `resource_id` | `bigint` | NOT NULL |  | 资源ID |
| `oid` | `bigint` | NOT NULL |  | 组织ID |
| `type` | `int` | NOT NULL |  | 业务类型 |

### xpack_setting_authentication  （6 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `name` | `varchar(100)` | NOT NULL |  | 名称 |
| `type` | `varchar(10)` | NOT NULL |  | 类型 |
| `enable` | `tinyint(1)` | NOT NULL |  | 是否启用 |
| `sync_time` | `bigint` | NOT NULL |  | 同步时间 |
| `relational_ids` | `varchar(255)` | NULL | NULL | 相关的ID |

### xpack_platform_token  （4 列[from V2.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `int` | NOT NULL |  |  |
| `token` | `varchar(255)` | NOT NULL |  |  |
| `create_time` | `bigint` | NOT NULL |  |  |
| `exp_time` | `bigint` | NOT NULL |  |  |

### core_share_ticket  （6 列[from V2.8__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `uuid` | `varchar(255)` | NOT NULL |  | 分享uuid |
| `ticket` | `varchar(255)` | NOT NULL |  | ticket |
| `exp` | `bigint` | NULL | NULL | ticket有效期 |
| `args` | `longtext` | NULL |  | ticket参数 |
| `access_time` | `bigint` | NULL | NULL | 首次访问时间 |



## AI Copilot
### core_copilot_config  （4 列[from V2.9__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `copilot_url` | `varchar(255)` | NULL | NULL |  |
| `username` | `varchar(255)` | NULL | NULL |  |
| `pwd` | `varchar(255)` | NULL | NULL |  |

### core_copilot_msg  （18 列[from V2.9__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `user_id` | `bigint` | NULL | NULL | 用户ID |
| `dataset_group_id` | `bigint` | NULL | NULL | 数据集ID |
| `msg_type` | `varchar(255)` | NULL | NULL | user or api |
| `engine_type` | `varchar(255)` | NULL | NULL | mysql oracle ... |
| `schema_sql` | `longtext` | NULL |  | create sql |
| `question` | `longtext` | NULL |  | 用户提问 |
| `history` | `longtext` | NULL |  | 历史信息 |
| `copilot_sql` | `longtext` | NULL |  | copilot 返回 sql |
| `api_msg` | `longtext` | NULL |  | copilot 返回信息 |
| `sql_ok` | `int` | NULL | NULL | sql 状态 |
| `chart_ok` | `int` | NULL | NULL | chart 状态 |
| `chart` | `longtext` | NULL |  | chart 内容 |
| `chart_data` | `longtext` | NULL |  | 视图数据 |
| `exec_sql` | `longtext` | NULL |  | 执行请求的SQL |
| `msg_status` | `int` | NULL | NULL | msg状态，0失败 1成功 |
| `err_msg` | `longtext` | NULL |  | de错误信息 |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |

### core_copilot_token  （4 列[from V2.9__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `type` | `varchar(255)` | NULL | NULL | free or license |
| `token` | `longtext` | NULL |  |  |
| `update_time` | `bigint` | NULL | NULL |  |



## 导出 / 插件 / 字体 / 阈值 / Webhook
### core_export_task  （12 列[from V2.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(255)` | NOT NULL |  |  |
| `user_id` | `bigint(20)` | NOT NULL |  |  |
| `file_name` | `varchar(2048)` | NULL | NULL |  |
| `file_size` | `DOUBLE` | NULL | NULL |  |
| `file_size_unit` | `varchar(255)` | NULL | NULL |  |
| `export_from` | `varchar(255)` | NULL | NULL |  |
| `export_status` | `varchar(255)` | NULL | NULL |  |
| `export_from_type` | `varchar(255)` | NULL | NULL |  |
| `export_time` | `bigint(20)` | NULL | NULL |  |
| `export_progress` | `varchar(255)` | NULL | NULL |  |
| `export_machine_name` | `varchar(512)` | NULL | NULL |  |
| `params` | `longtext` | NOT NULL |  | 过滤参数 |

### xpack_plugin  （11 列[from V2.8__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `name` | `varchar(255)` | NOT NULL |  | 插件名称 |
| `icon` | `longtext` | NOT NULL |  | 图标 |
| `version` | `varchar(255)` | NOT NULL |  | 版本 |
| `install_time` | `bigint` | NOT NULL |  | 安装时间 |
| `flag` | `varchar(255)` | NOT NULL |  | 类型 |
| `developer` | `varchar(255)` | NOT NULL |  | 开发者 |
| `config` | `longtext` | NOT NULL |  | 插件配置 |
| `require_version` | `varchar(255)` | NOT NULL |  | DE最低版本 |
| `module_name` | `varchar(255)` | NOT NULL |  | 模块名称 |
| `jar_name` | `varchar(255)` | NOT NULL |  | Jar包名称 |

### core_font  （7 列[from V2.10__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `name` | `varchar(255)` | NOT NULL |  | 字体名称 |
| `file_name` | `varchar(255)` | NULL | NULL | 文件名称 |
| `file_trans_name` | `varchar(255)` | NULL | NULL | 文件转换名称 |
| `is_default` | `tinyint(1)` | NULL | 0 | 是否默认 |
| `update_time` | `bigint` | NOT NULL |  | 更新时间 |
| `is_BuiltIn` | `tinyint(1)` | NULL | 0 | 是否内置 |

### xpack_threshold_info  （25 列[from V2.10__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `name` | `varchar(255)` | NOT NULL |  | 告警名称 |
| `enable` | `tinyint(1)` | NOT NULL |  | 是否启用 |
| `rate_type` | `int` | NOT NULL |  | 频率类型 |
| `rate_value` | `varchar(255)` | NOT NULL |  | 频率值 |
| `resource_type` | `varchar(50)` | NOT NULL |  | 资源类型 |
| `resource_id` | `bigint` | NOT NULL |  | 资源ID |
| `chart_type` | `varchar(255)` | NOT NULL |  | 图表类型 |
| `chart_id` | `bigint` | NOT NULL |  | 图表ID |
| `threshold_rules` | `longtext` | NULL |  | 告警规则 |
| `recisetting` | `varchar(50)` | NOT NULL | '0' | 消息渠道 |
| `reci_users` | `longtext` | NULL |  | 接收人 |
| `reci_roles` | `longtext` | NULL |  | 接收角色 |
| `reci_emails` | `longtext` | NULL |  | 接收邮箱 |
| `reci_lark_groups` | `longtext` | NULL |  | 飞书群聊 |
| `reci_webhooks` | `longtext` | NULL |  | Web hooks |
| `msg_title` | `varchar(255)` | NOT NULL |  | 消息标题 |
| `msg_type` | `int` | NOT NULL | '0' | 消息类型 |
| `msg_content` | `longtext` | NULL |  | 消息内容 |
| `repeat_send` | `tinyint(1)` | NOT NULL | '1' | 是否重复发送 |
| `status` | `tinyint(1)` | NOT NULL | '0' | 数据状态 |
| `creator` | `bigint` | NOT NULL |  | 创建者ID |
| `creator_name` | `varchar(255)` | NOT NULL |  | 创建人名称 |
| `create_time` | `bigint` | NOT NULL |  | 创建时间 |
| `oid` | `bigint` | NOT NULL |  | 所属组织 |

### xpack_threshold_instance  （6 列[from V2.10__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `task_id` | `bigint` | NOT NULL |  | 阈值信息ID |
| `exec_time` | `bigint` | NOT NULL |  | 检测时间 |
| `status` | `tinyint(1)` | NOT NULL | '0' | 数据状态 |
| `content` | `longtext` | NULL |  | 通知内容 |
| `msg` | `longtext` | NULL |  | 报错信息 |

### xpack_webhook  （8 列[from V2.10.4__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `name` | `varchar(255)` | NOT NULL |  | 名称 |
| `url` | `varchar(255)` | NOT NULL |  | url |
| `content_type` | `varchar(255)` | NOT NULL |  | content_type |
| `secret` | `varchar(255)` | NULL | NULL | 密钥 |
| `ssl` | `tinyint(1)` | NOT NULL | '0' | 开启ssl |
| `oid` | `bigint` | NOT NULL |  | 组织ID |
| `create_time` | `bigint` | NOT NULL |  | 创建时间 |


## 地理与运维
### area  （4 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(255)` | NOT NULL |  |  |
| `level` | `varchar(255)` | NULL | NULL |  |
| `name` | `varchar(255)` | NULL | NULL | 区域名称 |
| `pid` | `varchar(255)` | NOT NULL |  | 父级区域id |

### core_area_custom  （3 列[from V2.1__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(255)` | NOT NULL |  |  |
| `name` | `varchar(255)` | NOT NULL |  |  |
| `pid` | `varchar(255)` | NOT NULL |  |  |

### core_custom_geo_area  （2 列[from V2.10.3__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  | id |
| `name` | `varchar(50)` | NULL |  | 区域名称 |

### core_custom_geo_sub_area  （4 列[from V2.10.3__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | id |
| `name` | `varchar(50)` | NOT NULL |  | 名称 |
| `scope` | `varchar(1024)` | NULL |  | 区域范围 |
| `geo_area_id` | `varchar(50)` | NOT NULL |  | 自定义地理区域id |

### core_sys_startup_job  （3 列[from V2.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(64)` | NOT NULL |  | ID |
| `name` | `varchar(255)` | NULL | NULL | 任务名称 |
| `status` | `varchar(255)` | NULL | NULL | 任务状态 |

### core_api_traffic  （4 列[from V2.9__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `api` | `varchar(255)` | NOT NULL |  | api |
| `threshold` | `int` | NOT NULL | '2' | 阈值 |
| `alive` | `int` | NOT NULL | '0' | 活动并发 |

### de_template_version  （10 列[from V2.6__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `installed_rank` | `int` | NOT NULL |  |  |
| `version` | `varchar(50)` | NULL | NULL |  |
| `description` | `varchar(200)` | NULL | NULL |  |
| `type` | `varchar(20)` | NULL | NULL |  |
| `script` | `varchar(1000)` | NOT NULL |  |  |
| `checksum` | `int` | NULL | NULL |  |
| `installed_by` | `varchar(100)` | NULL | NULL |  |
| `installed_on` | `timestamp` | NOT NULL | CURRENT_TIMESTAMP |  |
| `execution_time` | `int` | NULL | NULL |  |
| `success` | `tinyint(1)` | NOT NULL |  |  |



## 示例数据
### demo_tea_material  （0 列[from V2.6__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|

### demo_tea_order  （0 列[from V2.6__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|


