# 可视化域表结构（v2.10.7）

> 18 张主表 + 10 张快照镜像表 = 28 张。覆盖仪表板/大屏资源树、画布样式、主题、背景、水印、模板、跳转/联动/外部参数交互配置，以及发布时的 `snapshot_*` 镜像。

## 域职责

可视化域以 `data_visualization_info` 为根（folder/panel 自引用树），聚合图表组件。交互能力通过三套平行模型实现：
- **跳转（Link Jump）**：`visualization_link_jump` → `visualization_link_jump_info` → `visualization_link_jump_target_view_info`
- **联动（Linkage）**：`visualization_linkage` → `visualization_linkage_field`
- **外部参数（Outer Params）**：`visualization_outer_params` → `visualization_outer_params_info` → `visualization_outer_params_target_view_info`

三套模型均带 `copy_from/copy_id` 复制链；发布（publish）时将当前态写入对应的 `snapshot_*` 表，供只读预览/回滚使用。


## 仪表板资源
### data_visualization_info  （22 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  |  |
| `name` | `varchar(255)` | NULL | NULL | 名称 |
| `pid` | `varchar(50)` | NULL | NULL | 父id |
| `org_id` | `varchar(50)` | NULL | NULL | 所属组织id |
| `level` | `int` | NULL | NULL | 层级 |
| `node_type` | `varchar(255)` | NULL | NULL | 节点类型  folder or panel 目录或者文件夹 |
| `type` | `varchar(50)` | NULL | NULL | 类型 |
| `canvas_style_data` | `longtext` | NULL |  | 样式数据 |
| `component_data` | `longtext` | NULL |  | 组件数据 |
| `mobile_layout` | `varchar(255)` | NULL | NULL | 移动端布局 |
| `status` | `int` | NULL | '1' | 状态 0-未发布 1-已发布 |
| `self_watermark_status` | `int` | NULL | '0' | 是否单独打开水印 0-关闭 1-开启 |
| `sort` | `int` | NULL | '0' | 排序 |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `create_by` | `varchar(255)` | NULL | NULL | 创建人 |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `update_by` | `varchar(255)` | NULL | NULL | 更新人 |
| `remark` | `varchar(255)` | NULL | NULL | 备注 |
| `source` | `varchar(255)` | NULL | NULL | 数据来源 |
| `delete_flag` | `tinyint(1)` | NULL | '0' | 删除标志 |
| `delete_time` | `bigint` | NULL | NULL | 删除时间 |
| `delete_by` | `varchar(255)` | NULL | NULL | 删除人 |

### visualization_subject  （13 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  |  |
| `name` | `varchar(255)` | NULL | NULL | 主题名称 |
| `type` | `varchar(255)` | NULL | NULL | 主题类型 system 系统主题，self 自定义主题 |
| `details` | `longtext` | NULL |  | 主题内容 |
| `delete_flag` | `tinyint(1)` | NULL | '0' | 删除标记 |
| `cover_url` | `longtext` | NULL |  | 封面信息 |
| `create_num` | `int` | NOT NULL | '0' |  |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `create_by` | `varchar(255)` | NULL | NULL | 创建人 |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `update_by` | `varchar(255)` | NULL | NULL | 更新人 |
| `delete_time` | `bigint` | NULL | NULL | 删除时间 |
| `delete_by` | `bigint` | NULL | NULL | 删除人 |

### visualization_background  （9 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(64)` | NOT NULL |  |  |
| `name` | `varchar(255)` | NULL | NULL |  |
| `classification` | `varchar(255)` | NOT NULL |  |  |
| `content` | `longtext` | NULL |  |  |
| `remark` | `varchar(255)` | NULL | NULL |  |
| `sort` | `int` | NULL | NULL |  |
| `upload_time` | `bigint` | NULL | NULL |  |
| `base_url` | `varchar(255)` | NULL | NULL |  |
| `url` | `varchar(255)` | NULL | NULL |  |

### visualization_background_image  （9 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(64)` | NOT NULL |  |  |
| `name` | `varchar(255)` | NULL | NULL |  |
| `classification` | `varchar(255)` | NOT NULL |  |  |
| `content` | `longtext` | NULL |  |  |
| `remark` | `varchar(255)` | NULL | NULL |  |
| `sort` | `int` | NULL | NULL |  |
| `upload_time` | `bigint` | NULL | NULL |  |
| `base_url` | `varchar(255)` | NULL | NULL |  |
| `url` | `varchar(255)` | NULL | NULL |  |

### visualization_watermark  （5 列[from V2.3__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  | 主键 |
| `version` | `varchar(255)` | NULL | NULL | 版本号 |
| `setting_content` | `longtext` | NULL |  | 设置内容 |
| `create_by` | `varchar(255)` | NULL | NULL | 创建人 |
| `create_time` | `bigint(13)` | NULL | NULL | 创建时间 |

### visualization_report_filter  （11 列[from V2.8__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | id |
| `report_id` | `bigint` | NULL | NULL | 定时报告id |
| `task_id` | `bigint` | NULL | NULL | 任务id |
| `resource_id` | `bigint` | NULL | NULL | 资源id |
| `dv_type` | `varchar(255)` | NULL | NULL | 资源类型 |
| `component_id` | `bigint` | NULL | NULL | 组件id |
| `filter_id` | `bigint` | NULL | NULL | 过滤项id |
| `filter_info` | `longtext` | NULL |  | 过滤组件内容 |
| `filter_version` | `int` | NULL | NULL | 过滤组件版本 |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `create_user` | `varchar(255)` | NULL | NULL | 创建人 |



## 模板市场
### visualization_template  （13 列[from V2.1__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  | 主键 |
| `name` | `varchar(255)` | NULL | NULL | 名称 |
| `pid` | `varchar(255)` | NULL | NULL | 父级id |
| `level` | `int` | NULL | NULL | 层级 |
| `dv_type` | `varchar(255)` | NULL | NULL | 模板种类  dataV or dashboard 目录或者文件夹 |
| `node_type` | `varchar(255)` | NULL | NULL | 节点类型  folder or panel 目录或者文件夹 |
| `create_by` | `varchar(255)` | NULL | NULL | 创建人 |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `snapshot` | `longtext` | NULL |  | 缩略图 |
| `template_type` | `varchar(255)` | NULL | NULL | 模板类型 system 系统内置 self 用户自建  |
| `template_style` | `longtext` | NULL |  | template 样式 |
| `template_data` | `longtext` | NULL |  | template 数据 |
| `dynamic_data` | `longtext` | NULL |  | 预存数据 |

### visualization_template_category  （10 列[from V2.1__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  | 主键 |
| `name` | `varchar(255)` | NULL | NULL | 名称 |
| `pid` | `varchar(255)` | NULL | NULL | 父级id |
| `level` | `int` | NULL | NULL | 层级 |
| `dv_type` | `varchar(255)` | NULL | NULL | 模板种类  dataV or dashboard 目录或者文件夹 |
| `node_type` | `varchar(255)` | NULL | NULL | 节点类型  folder or panel 目录或者文件夹 |
| `create_by` | `varchar(255)` | NULL | NULL | 创建人 |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `snapshot` | `longtext` | NULL |  | 缩略图 |
| `template_type` | `varchar(255)` | NULL | NULL |  |

### visualization_template_category_map  （3 列[from V2.1__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  | 主键 |
| `category_id` | `varchar(255)` | NULL | NULL | 名称 |
| `template_id` | `varchar(255)` | NULL | NULL | 父级id |

### visualization_template_extend_data  （6 列[from V2.1__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `dv_id` | `bigint` | NULL | NULL |  |
| `view_id` | `bigint` | NULL | NULL |  |
| `view_details` | `longtext` | NULL |  |  |
| `copy_from` | `varchar(255)` | NULL | NULL |  |
| `copy_id` | `varchar(255)` | NULL | NULL |  |



## 跳转配置
### visualization_link_jump  （7 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `source_dv_id` | `bigint` | NULL | NULL | 源仪表板ID |
| `source_view_id` | `bigint` | NULL | NULL | 源图表ID |
| `link_jump_info` | `varchar(4000)` | NULL | NULL | 跳转信息 |
| `checked` | `tinyint(1)` | NULL | NULL | 是否启用 |
| `copy_from` | `bigint` | NULL | NULL |  |
| `copy_id` | `bigint` | NULL | NULL |  |

### visualization_link_jump_info  （11 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `link_jump_id` | `bigint` | NULL | NULL | link jump ID |
| `link_type` | `varchar(255)` | NULL | NULL | 关联类型 inner 内部仪表板，outer 外部链接 |
| `jump_type` | `varchar(255)` | NULL | NULL | 跳转类型 _blank 新开页面 _self 当前窗口 |
| `target_dv_id` | `bigint` | NULL | NULL | 关联仪表板ID |
| `source_field_id` | `bigint` | NULL | NULL | 字段ID |
| `content` | `varchar(4000)` | NULL | NULL | 内容 linkType = outer时使用 |
| `checked` | `tinyint(1)` | NULL | NULL | 是否可用 |
| `attach_params` | `tinyint(1)` | NULL | NULL | 是否附加点击参数 |
| `copy_from` | `bigint` | NULL | NULL |  |
| `copy_id` | `bigint` | NULL | NULL |  |

### visualization_link_jump_target_view_info  （7 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `target_id` | `bigint` | NOT NULL |  |  |
| `link_jump_info_id` | `bigint` | NULL | NULL |  |
| `source_field_active_id` | `bigint` | NULL | NULL | 勾选字段设置的匹配字段，也可以不是勾选字段本身 |
| `target_view_id` | `bigint` | NULL | NULL |  |
| `target_field_id` | `bigint` | NULL | NULL |  |
| `copy_from` | `bigint` | NULL | NULL |  |
| `copy_id` | `bigint` | NULL | NULL |  |



## 联动配置
### visualization_linkage  （11 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `dv_id` | `bigint` | NULL | NULL |  |
| `source_view_id` | `bigint` | NULL | NULL | 源图表id |
| `target_view_id` | `bigint` | NULL | NULL | 联动图表id |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `update_people` | `varchar(255)` | NULL | NULL | 更新人 |
| `linkage_active` | `tinyint(1)` | NULL | '0' | 是否启用关联 |
| `ext1` | `varchar(2000)` | NULL | NULL |  |
| `ext2` | `varchar(2000)` | NULL | NULL |  |
| `copy_from` | `bigint` | NULL | NULL |  |
| `copy_id` | `bigint` | NULL | NULL |  |

### visualization_linkage_field  （7 列[from V2.0__core_ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  |  |
| `linkage_id` | `bigint` | NULL | NULL | 联动ID |
| `source_field` | `bigint` | NULL | NULL | 源图表字段 |
| `target_field` | `bigint` | NULL | NULL | 目标图表字段 |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `copy_from` | `bigint` | NULL | NULL |  |
| `copy_id` | `bigint` | NULL | NULL |  |



## 外部参数
### visualization_outer_params  （6 列[from V2.5__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `params_id` | `varchar(50)` | NOT NULL |  | 主键 |
| `visualization_id` | `varchar(50)` | NULL | NULL | 可视化资源ID |
| `checked` | `tinyint(1)` | NULL | NULL | 是否启用外部参数标识（1-是，0-否） |
| `remark` | `varchar(255)` | NULL | NULL | 备注 |
| `copy_from` | `varchar(50)` | NULL | NULL | 复制来源 |
| `copy_id` | `varchar(50)` | NULL | NULL | 复制来源ID |

### visualization_outer_params_info  （6 列[from V2.5__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `params_info_id` | `varchar(50)` | NOT NULL |  | 主键 |
| `params_id` | `varchar(50)` | NULL | NULL | visualization_outer_params 表的 ID |
| `param_name` | `varchar(255)` | NULL | NULL | 参数名 |
| `checked` | `tinyint(1)` | NULL | NULL | 是否启用 |
| `copy_from` | `varchar(255)` | NULL | NULL | 复制来源 |
| `copy_id` | `varchar(50)` | NULL | NULL | 复制来源ID |

### visualization_outer_params_target_view_info  （6 列[from V2.5__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `target_id` | `varchar(50)` | NOT NULL |  | 主键 |
| `params_info_id` | `varchar(50)` | NULL | NULL | visualization_outer_params_info 表的 ID |
| `target_view_id` | `varchar(50)` | NULL | NULL | 联动视图ID |
| `target_field_id` | `varchar(50)` | NULL | NULL | 联动字段ID |
| `copy_from` | `varchar(255)` | NULL | NULL | 复制来源 |
| `copy_id` | `varchar(50)` | NULL | NULL | 复制来源ID |



## 发布快照镜像（snapshot_*）
### snapshot_core_chart_view  （44 列[from V2.10.7__ddl.sql]）

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
| `custom_attr_mobile` | `longtext` | NULL |  | 图形属性_移动端 |
| `custom_style` | `longtext` | NULL |  | 组件样式 |
| `custom_style_mobile` | `longtext` | NULL |  | 组件样式_移动端 |
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
| `refresh_view_enable` | `tinyint(1)` | NULL | '0' | 是否开启刷新 |
| `refresh_unit` | `varchar(255)` | NULL | 'minute' | 刷新时间单位 |
| `refresh_time` | `int` | NULL | '5' | 刷新时间 |
| `linkage_active` | `tinyint(1)` | NULL | '0' | 是否开启联动 |
| `jump_active` | `tinyint(1)` | NULL | '0' | 是否开启跳转 |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制ID |
| `aggregate` | `bit(1)` | NULL | NULL | 区间条形图开启时间纬度开启聚合 |
| `flow_map_start_name` | `longtext` | NULL |  | 流向地图起点名称field |
| `flow_map_end_name` | `longtext` | NULL |  | 流向地图终点名称field |
| `ext_color` | `longtext` | NULL |  | 颜色维度field |
| `sort_priority` | `longtext` | NULL |  | 字段排序优先级 |

### snapshot_data_visualization_info  （25 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `varchar(50)` | NOT NULL |  | 主键 |
| `name` | `varchar(255)` | NULL | NULL | 名称 |
| `pid` | `varchar(50)` | NULL | NULL | 父id |
| `org_id` | `varchar(50)` | NULL | NULL | 所属组织id |
| `level` | `int` | NULL | NULL | 层级 |
| `node_type` | `varchar(255)` | NULL | NULL | 节点类型  folder or panel 目录或者文件夹 |
| `type` | `varchar(50)` | NULL | NULL | 类型 |
| `canvas_style_data` | `longtext` | NULL |  | 样式数据 |
| `component_data` | `longtext` | NULL |  | 组件数据 |
| `mobile_layout` | `tinyint` | NULL | '0' | 移动端布局0-关闭 1-开启 |
| `status` | `int` | NULL | '1' | 状态 0-未发布 1-已发布 |
| `self_watermark_status` | `int` | NULL | '0' | 是否单独打开水印 0-关闭 1-开启 |
| `sort` | `int` | NULL | '0' | 排序 |
| `create_time` | `bigint` | NULL | NULL | 创建时间 |
| `create_by` | `varchar(255)` | NULL | NULL | 创建人 |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `update_by` | `varchar(255)` | NULL | NULL | 更新人 |
| `remark` | `varchar(255)` | NULL | NULL | 备注 |
| `source` | `varchar(255)` | NULL | NULL | 数据来源 |
| `delete_flag` | `tinyint(1)` | NULL | '0' | 删除标志 |
| `delete_time` | `bigint` | NULL | NULL | 删除时间 |
| `delete_by` | `varchar(255)` | NULL | NULL | 删除人 |
| `version` | `int` | NULL | '3' | 可视化资源版本 |
| `content_id` | `varchar(50)` | NULL | '0' | 内容标识 |
| `check_version` | `varchar(50)` | NULL | '1' | 内容检查标识 |

### snapshot_visualization_link_jump  （7 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `source_dv_id` | `bigint` | NULL | NULL | 源仪表板ID |
| `source_view_id` | `bigint` | NULL | NULL | 源图表ID |
| `link_jump_info` | `varchar(4000)` | NULL | NULL | 跳转信息 |
| `checked` | `tinyint(1)` | NULL | NULL | 是否启用 |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制来源ID |

### snapshot_visualization_link_jump_info  （12 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `link_jump_id` | `bigint` | NULL | NULL | link jump ID |
| `link_type` | `varchar(255)` | NULL | NULL | 关联类型 inner 内部仪表板，outer 外部链接 |
| `jump_type` | `varchar(255)` | NULL | NULL | 跳转类型 _blank 新开页面 _self 当前窗口 |
| `target_dv_id` | `bigint` | NULL | NULL | 关联仪表板ID |
| `source_field_id` | `bigint` | NULL | NULL | 字段ID |
| `content` | `varchar(4000)` | NULL | NULL | 内容 linkType = outer时使用 |
| `checked` | `tinyint(1)` | NULL | NULL | 是否可用 |
| `attach_params` | `tinyint(1)` | NULL | NULL | 是否附加点击参数 |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制来源ID |
| `window_size` | `varchar(255)` | NULL | 'middle' | 窗口大小large middle small |

### snapshot_visualization_link_jump_target_view_info  （8 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `target_id` | `bigint` | NOT NULL |  | 主键 |
| `link_jump_info_id` | `bigint` | NULL | NULL | visualization_link_jump_info 表的 ID |
| `source_field_active_id` | `bigint` | NULL | NULL | 勾选字段设置的匹配字段，也可以不是勾选字段本身 |
| `target_view_id` | `varchar(50)` | NULL | NULL | 目标图表ID |
| `target_field_id` | `varchar(50)` | NULL | NULL | 目标字段ID |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制来源ID |
| `target_type` | `varchar(50)` | NULL | 'view' | 联动目标类型 view 图表 filter 过滤组件 outParams 外部参数 |

### snapshot_visualization_linkage  （11 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `dv_id` | `bigint` | NULL | NULL | 联动大屏/仪表板ID |
| `source_view_id` | `bigint` | NULL | NULL | 源图表id |
| `target_view_id` | `bigint` | NULL | NULL | 联动图表id |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `update_people` | `varchar(255)` | NULL | NULL | 更新人 |
| `linkage_active` | `tinyint(1)` | NULL | '0' | 是否启用关联 |
| `ext1` | `varchar(2000)` | NULL | NULL | 扩展字段1 |
| `ext2` | `varchar(2000)` | NULL | NULL | 扩展字段2 |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制来源ID |

### snapshot_visualization_linkage_field  （7 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `id` | `bigint` | NOT NULL |  | 主键 |
| `linkage_id` | `bigint` | NULL | NULL | 联动ID |
| `source_field` | `bigint` | NULL | NULL | 源图表字段 |
| `target_field` | `bigint` | NULL | NULL | 目标图表字段 |
| `update_time` | `bigint` | NULL | NULL | 更新时间 |
| `copy_from` | `bigint` | NULL | NULL | 复制来源 |
| `copy_id` | `bigint` | NULL | NULL | 复制来源ID |

### snapshot_visualization_outer_params  （6 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `params_id` | `varchar(50)` | NOT NULL |  | 主键 |
| `visualization_id` | `varchar(50)` | NULL | NULL | 可视化资源ID |
| `checked` | `tinyint(1)` | NULL | NULL | 是否启用外部参数标识（1-是，0-否） |
| `remark` | `varchar(255)` | NULL | NULL | 备注 |
| `copy_from` | `varchar(50)` | NULL | NULL | 复制来源 |
| `copy_id` | `varchar(50)` | NULL | NULL | 复制来源ID |

### snapshot_visualization_outer_params_info  （9 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `params_info_id` | `varchar(50)` | NOT NULL |  | 主键 |
| `params_id` | `varchar(50)` | NULL | NULL | visualization_outer_params 表的 ID |
| `param_name` | `varchar(255)` | NULL | NULL | 参数名 |
| `checked` | `tinyint(1)` | NULL | NULL | 是否启用 |
| `copy_from` | `varchar(255)` | NULL | NULL | 复制来源 |
| `copy_id` | `varchar(50)` | NULL | NULL | 复制来源ID |
| `required` | `tinyint(1)` | NULL | '0' | 是否必填 |
| `default_value` | `varchar(255)` | NULL | NULL | 默认值 JSON格式 |
| `enabled_default` | `tinyint(1)` | NULL | '0' | 是否启用默认值 |

### snapshot_visualization_outer_params_target_view_info  （7 列[from V2.10.7__ddl.sql]）

| 列 | 类型 | 空 | 默认 | 说明 |
|----|------|----|------|------|
| `target_id` | `varchar(50)` | NOT NULL |  | 主键 |
| `params_info_id` | `varchar(50)` | NULL | NULL | visualization_outer_params_info 表的 ID |
| `target_view_id` | `varchar(50)` | NULL | NULL | 联动视图ID/联动过滤项ID |
| `target_field_id` | `varchar(50)` | NULL | NULL | 联动字段ID |
| `copy_from` | `varchar(255)` | NULL | NULL | 复制来源 |
| `copy_id` | `varchar(50)` | NULL | NULL | 复制来源ID |
| `target_ds_id` | `varchar(50)` | NULL | NULL | 联动数据集id/联动过滤组件id |


