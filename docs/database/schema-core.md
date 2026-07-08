# 核心业务域表结构（v2.10.7）

> 15 张表，覆盖数据源、数据集、图表、引擎、驱动、系统设置、菜单、收藏与最近访问。
> 全部源自 `db/migration/V2.0__core_ddl.sql` 基线（少数列在增量脚本中扩展）。

## 域职责

核心业务域是 DataEase 的“数据资产”层：从外部数据源接入（`core_datasource`）→ 构建数据集（`core_dataset_group`/`core_dataset_table`/`core_dataset_table_field`）→ 在图表（`core_chart_view`）中消费。系统级支撑表（`core_sys_setting`/`core_menu`/`core_rsa`/`core_store`/`core_opt_recent`）提供配置、鉴权底座、收藏与最近使用。


## 数据源与驱动
### core_datasource  （13 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `name` | `varchar(255)` | NOT NULL |  | 名称 |
| `description` | `varchar(255)` | NULL | NULL | 描述 |
| `type` | `varchar(50)` | NOT NULL |  | 类型 |
| `pid` | `bigint` | NULL | NULL | 父级ID |
| `edit_type` | `varchar(50)` | NULL |  | 更新方式：0：替换；1：追加 |
| `configuration` | `longtext` | NOT NULL |  | 详细信息 |
| `create_time` | `bigint` | NOT NULL |  | 创建时间 |
| `update_time` | `bigint` | NOT NULL |  | 更新时间 |
| `create_by` | `varchar(50)` | NULL | NULL | 创建人ID |
| `status` | `longtext` | NULL |  | 状态 |
| `qrtz_instance` | `longtext` | NULL |  | 状态 |
| `task_status` | `varchar(50)` | NULL | NULL | 任务状态 |

### core_driver  （6 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `name` | `varchar(50)` | NOT NULL |  | 名称 |
| `create_time` | `bigint(13)` | NOT NULL |  | 创建时间 |
| `type` | `varchar(255)` | NULL | NULL | 数据源类型 |
| `driver_class` | `varchar(255)` | NULL | NULL | 驱动类 |
| `description` | `varchar(255)` | NULL | NULL | 描述 |

### core_driver_jar  （7 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `de_driver_id` | `varchar(50)` | NOT NULL |  | 驱动主键 |
| `file_name` | `varchar(255)` | NULL | NULL | 名称 |
| `version` | `varchar(255)` | NULL | NULL | 版本 |
| `driver_class` | `longtext` | NULL |  | 驱动类 |
| `trans_name` | `varchar(255)` | NULL | NULL |  |
| `is_trans_name` | `tinyint(1)` | NULL | NULL |  |

### core_de_engine  （9 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `name` | `varchar(50)` | NULL | NULL | 名称 |
| `description` | `varchar(50)` | NULL | NULL | 描述 |
| `type` | `varchar(50)` | NOT NULL |  | 类型 |
| `configuration` | `longtext` | NOT NULL |  | 详细信息 |
| `create_time` | `bigint(13)` | NULL | NULL | Create timestamp |
| `update_time` | `bigint(13)` | NULL | NULL | Update timestamp |
| `create_by` | `varchar(50)` | NULL | NULL | 创建人ID |
| `status` | `varchar(45)` | NULL | NULL | 状态 |



## 数据集
### core_dataset_group  （15 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `name` | `varchar(128)` | NULL | NULL | 名称 |
| `pid` | `bigint` | NULL | NULL | 父级ID |
| `level` | `int(10)` | NULL | '0' | 当前分组处于第几级 |
| `node_type` | `varchar(50)` | NOT NULL |  | node类型：folder or dataset |
| `type` | `varchar(50)` | NULL | NULL |  |
| `mode` | `int` | NULL | '0' | 连接模式：0-直连，1-同步(包括excel、api等数据存在de中的表) |
| `info` | `longtext` | NULL |  | 关联关系树 |
| `create_by` | `varchar(50)` | NULL | NULL | 创建人ID |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `qrtz_instance` | `varchar(1024)` | NULL | NULL |  |
| `sync_status` | `varchar(45)` | NULL | NULL | 同步状态 |
| `update_by` | `varchar(50)` | NULL | NULL | 更新人ID |
| `last_update_time` | `bigint` | NULL | '0' | 最后同步时间 |
| `union_sql` | `longtext` | NULL |  | 关联sql |

### core_dataset_table  （8 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `name` | `varchar(128)` | NULL | NULL | 名称 |
| `table_name` | `varchar(128)` | NULL | NULL | 物理表名 |
| `datasource_id` | `bigint` | NULL | NULL | 数据源ID |
| `dataset_group_id` | `bigint` | NOT NULL |  | 数据集ID |
| `type` | `varchar(50)` | NULL | NULL |  |
| `info` | `longtext` | NULL |  |  |
| `sql_variable_details` | `longtext` | NULL |  | SQL参数 |

### core_dataset_table_field  （22 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `datasource_id` | `bigint` | NULL | NULL | 数据源ID |
| `dataset_table_id` | `bigint` | NULL | NULL | 数据表ID |
| `dataset_group_id` | `bigint` | NULL | NULL | 数据集ID |
| `chart_id` | `bigint` | NULL | NULL | 图表ID |
| `origin_name` | `longtext` | NOT NULL |  | 原始字段名 |
| `name` | `longtext` | NULL | NULL | 字段名用于展示 |
| `description` | `longtext` | NULL | NULL | 描述 |
| `dataease_name` | `varchar(255)` | NULL | NULL | de字段名用作唯一标识 |
| `field_short_name` | `varchar(255)` | NULL | NULL | de字段别名 |
| `group_type` | `varchar(50)` | NULL | NULL | 维度/指标标识 d:维度，q:指标 |
| `type` | `varchar(255)` | NOT NULL |  | 原始字段类型 |
| `size` | `int` | NULL | NULL |  |
| `de_type` | `int` | NOT NULL |  | dataease字段类型：0-文本，1-时间，2-整型数值，3-浮点数值，4-布尔，5-地理位置，6-二进制，7-URL |
| `de_extract_type` | `int` | NOT NULL |  | de记录的原始类型 |
| `ext_field` | `int` | NULL | NULL | 是否扩展字段 0原始 1复制 2计算字段... |
| `checked` | `tinyint(1)` | NULL | NULL | 是否选中 |
| `column_index` | `int` | NULL | NULL | 列位置 |
| `last_sync_time` | `bigint` | NULL | NULL | 同步时间 |
| `accuracy` | `int` | NULL | '0' | 精度 |
| `date_format` | `varchar(255)` | NULL | NULL |  |
| `date_format_type` | `varchar(255)` | NULL | NULL | 时间格式类型 |

### core_dataset_table_sql_log  （7 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL | '' | ID |
| `table_id` | `varchar(50)` | NOT NULL | '' | 数据集SQL节点ID |
| `start_time` | `bigint(13)` | NULL | NULL | 开始时间 |
| `end_time` | `bigint(13)` | NULL | NULL | 结束时间 |
| `spend` | `bigint(13)` | NULL | NULL | 耗时(毫秒) |
| `sql` | `longtext` | NOT NULL |  | 详细信息 |
| `status` | `varchar(45)` | NULL | NULL | 状态 |



## 图表
### core_chart_view  （37 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `title` | `varchar(1024)` | NULL | NULL | 标题 |
| `scene_id` | `bigint` | NOT NULL |  | 场景ID chart_type为private的时候 是仪表板id |
| `table_id` | `bigint` | NULL | NULL | 数据集表ID |
| `type` | `varchar(50)` | NULL | NULL | 图表类型 |
| `render` | `varchar(50)` | NULL | NULL | 图表渲染方式 |
| `result_count` | `int` | NULL | NULL | 展示结果 |
| `result_mode` | `varchar(50)` | NULL | NULL | 展示模式 |
| `x_axis` | `longtext` | NULL |  | 横轴field |
| `x_axis_ext` | `longtext` | NULL |  | table-row |
| `y_axis` | `longtext` | NULL |  | 纵轴field |
| `y_axis_ext` | `longtext` | NULL |  | 副轴 |
| `ext_stack` | `longtext` | NULL |  | 堆叠项 |
| `ext_bubble` | `longtext` | NULL |  | 气泡大小 |
| `ext_label` | `longtext` | NULL |  | 动态标签 |
| `ext_tooltip` | `longtext` | NULL |  | 动态提示 |
| `custom_attr` | `longtext` | NULL |  | 图形属性 |
| `custom_style` | `longtext` | NULL |  | 组件样式 |
| `custom_filter` | `longtext` | NULL |  | 结果过滤 |
| `drill_fields` | `longtext` | NULL |  | 钻取字段 |
| `senior` | `longtext` | NULL |  | 高级 |
| `create_by` | `varchar(50)` | NULL | NULL | 创建人ID |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `snapshot` | `longtext` | NULL |  | 缩略图  |
| `style_priority` | `varchar(255)` | NULL | 'panel' | 样式优先级 panel 仪表板 view 图表 |
| `chart_type` | `varchar(255)` | NULL | 'private' | 图表类型 public 公共 历史可复用的图表，private 私有 专属某个仪表板 |
| `is_plugin` | `bit(1)` | NULL | NULL | 是否插件 |
| `data_from` | `varchar(255)` | NULL | 'dataset' | 数据来源 template 模板数据 dataset 数据集数据 |
| `view_fields` | `longtext` | NULL |  | 图表字段集合 |
| `refresh_view_enable` | `tinyint(1)` | NULL | 0 | 是否开启刷新 |
| `refresh_unit` | `varchar(255)` | NULL | 'minute' | 刷新时间单位 |
| `refresh_time` | `int` | NULL | 5 | 刷新时间 |
| `linkage_active` | `tinyint(1)` | NULL | 0 | 是否开启联动 |
| `jump_active` | `tinyint(1)` | NULL | 0 | 是否开启跳转 |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制ID |



## 系统支撑
### core_sys_setting  （5 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `pkey` | `varchar(255)` | NOT NULL |  | 键 |
| `pval` | `varchar(255)` | NOT NULL |  | 值 |
| `type` | `varchar(255)` | NOT NULL |  | 类型 |
| `sort` | `int` | NOT NULL | '0' | 顺序 |

### core_menu  （11 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `pid` | `bigint` | NOT NULL |  | 父ID |
| `type` | `int` | NULL | NULL | 类型 |
| `name` | `varchar(45)` | NULL | NULL | 名称 |
| `component` | `varchar(45)` | NULL | NULL | 组件 |
| `menu_sort` | `int` | NULL | NULL | 排序 |
| `icon` | `varchar(45)` | NULL | NULL | 图标 |
| `path` | `varchar(45)` | NULL | NULL | 路径 |
| `hidden` | `tinyint(1)` | NOT NULL | '0' | 隐藏 |
| `in_layout` | `tinyint(1)` | NOT NULL | '1' | 是否内部 |
| `auth` | `tinyint(1)` | NOT NULL | '0' | 参与授权 |

### core_rsa  （5 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `int` | NOT NULL |  | 主键 |
| `private_key` | `text` | NOT NULL |  | 私钥 |
| `public_key` | `text` | NOT NULL |  | 公钥 |
| `create_time` | `bigint` | NOT NULL |  | 生成时间 |
| `aes_key` | `text` | NOT NULL |  |  |

### core_store  （5 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `resource_id` | `bigint` | NOT NULL |  | 资源ID |
| `uid` | `bigint` | NOT NULL |  | 用户ID |
| `resource_type` | `int` | NOT NULL |  | 资源类型 |
| `time` | `bigint` | NOT NULL |  | 收藏时间 |

### core_opt_recent  （6 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | ID |
| `resource_id` | `bigint` | NOT NULL |  | 资源ID |
| `uid` | `bigint` | NOT NULL |  | 用户ID |
| `resource_type` | `int` | NOT NULL |  | 资源类型 |
| `opt_type` | `int` | NULL | NULL | 1 新建 2 修改 |
| `time` | `bigint` | NOT NULL |  | 收藏时间 |

### core_ds_finish_page  （1 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |


