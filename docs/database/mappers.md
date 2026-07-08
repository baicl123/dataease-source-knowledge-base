# MyBatis Mapper XML 分析（v2.10.7）

> 位置：`core/core-backend/src/main/resources/mybatis/`。6 个 `Ext*` Mapper，合计 **107 条自定义 SQL 语句**（其余 CRUD 由 MyBatis-Plus `auto` 包自动生成，不在此列）。
> 这些 `Ext*` Mapper 承载 MyBatis-Plus 无法直接表达的复杂查询、复制、快照/恢复与模板导入等逻辑。

## 总览

| Mapper | namespace（接口） | 语句数 | 核心职责 |
|--------|-------------------|--------|----------|
| ExtCoreChartMapper.xml | `io.dataease.chart.dao.ext.mapper.ExtChartViewMapper` | 3 | 图表查询（含快照态切换）、按场景批量删除 |
| ExtDataVisualizationMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtDataVisualizationMapper` | 35 | 仪表板复制、快照、恢复、最近访问、批量删除、报告过滤 |
| ExtVisualizationLinkJumpMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtVisualizationLinkJumpMapper` | 22 | 跳转配置查询/复制/删除（含 snapshot 变体） |
| ExtVisualizationLinkageMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtVisualizationLinkageMapper` | 13 | 联动配置查询/复制/删除 |
| ExtVisualizationOuterParamsMapper.xml | `io.dataease.visualization.dao.ext.mapper.ExtVisualizationOuterParamsMapper` | 13 | 外部参数查询 |
| ExtVisualizationTemplateMapper.xml | `io.dataease.template.dao.ext.ExtVisualizationTemplateMapper` | 21 | 模板列表/分类/去重校验/导入应用数据收集 |

## 贯穿性设计模式

1. **snapshot / 非 snapshot 切换**：`ExtCoreChartMapper` 与所有 `*Jump`/`*Linkage`/`*OuterParams` Mapper 均通过 `<choose><when test="resourceTable == 'snapshot'">` 在 `core_*` 与 `snapshot_*` 表之间动态切换。读取发布态时查 `snapshot_*` 镜像（见 migrations.md V2.10.7）。
2. **复制链 `copy_from`/`copy_id`**：跳转/联动/外部参数表均带 `copy_from`/`copy_id`，复制/应用时由 `copy*` 语句把源配置写入新记录并回填 `copy_id`。
3. **嵌套 resultMap + `select` 关联**：`ExtVisualizationLinkJumpMapper` 用 `<collection ... select="getLinkJumpInfo">` 把主表与 `*_info`/`*_target_view_info` 子表组装成 DTO 树，snapshot 态用 `...Snapshot` 变体。
4. **模板导入数据收集**：`ExtVisualizationTemplateMapper` 的 `findApp*` 系列按 `dvId`/`dsIds` 聚合图表、数据集、数据源、任务、跳转、联动等全部相关实体，供模板“应用/导入”一次性拉取。

## 各 Mapper 详解

### 1. ExtCoreChartMapper（3 条）
- `queryChart`：按 `id` 联表 `core_chart_view` + `data_visualization_info`（或快照态），返回 `ChartBasePO`（含轴/堆叠/气泡/流向图起止名等全部图表属性列）。
- `selectListCustom`：`select * from core_chart_view where scene_id = #{sceneId}`（snapshot 态切 `snapshot_core_chart_view`）。
- `deleteViewsBySceneId`：按 `scene_id` 删除图表（snapshot 态切 `snapshot_core_chart_view`）。

### 2. ExtDataVisualizationMapper（35 条）
- **复制**：`dvCopy`（复制仪表板）、`viewCopyWithDv`（复制图表+关联）、`findViewInfoByCopyId`、`findDvInfo`。
- **快照（发布）**：`snapshotDataV`/`snapshotViews`/`snapshotLinkJump*`/`snapshotOuterParams*` —— 把当前态写入 `snapshot_*` 镜像。
- **恢复**：`restoreDataV`/`restoreViews`/`restoreLinkJump*`/`restoreOuterParams*` —— 从镜像回写 `core_*`。
- **查询/删除**：`getVisualizationViewDetails`、`findRecent`（最近访问）、`deleteDataVBatch`/`deleteViewsBatch`、`queryReportFilter`、`queryInnerUserInfo`。

### 3. ExtVisualizationLinkJumpMapper（22 条）
- **查询**：`queryWithDvId`/`queryWithViewId`/`getLinkJumpInfo`/`getViewTableDetails`/`getTargetVisualizationJumpInfo`/`findLinkJumpWithDvId`/`findLinkJumpInfoWithDvId`，每个均有 `*Snapshot` 变体。
- **复制/删除**：`copyLinkJump`/`copyLinkJumpInfo`/`copyLinkJumpTarget`，及 `deleteJump*`/`deleteJumpInfo*`/`deleteJumpTargetViewInfo*`（均含 snapshot 变体，按 `visualization` 批量清理）。

### 4. ExtVisualizationLinkageMapper（13 条）
- **查询**：`getViewLinkageGather`/`getPanelAllLinkageInfo`（+`*Snapshot`）、`queryTableField`/`queryTableFieldWithViewId`。
- **复制/删除**：`copyViewLinkage`、`deleteViewLinkage`/`deleteViewLinkageField`（+`*Snapshot`）、`findLinkageWithDvId`/`findLinkageFieldWithDvId`。

### 5. ExtVisualizationOuterParamsMapper（13 条）
- **查询**：`getVisualizationOuterParamsInfo`/`getVisualizationOuterParamsInfoBase`/`getOuterParamsInfoSnapshot`/`queryWithVisualizationIdSnapshot`、`queryDsWithVisualizationId`/`getDsFieldInfo`/`getViewInfo`。
- **删除**：`deleteOuterParams*`/`deleteOuterParamsInfo*`/`deleteOuterParamsTarget*`（`WithVisualizationId` + `*Snapshot` 变体）。

### 6. ExtVisualizationTemplateMapper（21 条）
- **列表/分类**：`findBaseTemplateList`/`findTemplateList`（含 `use_count` 与最近使用）、`findCategories`、`findTemplateCategories`/`findTemplateArrayCategories`。
- **校验**：`checkCategoryMap`/`checkRepeatTemplateId`/`checkCategoryTemplateName`/`checkCategoryTemplateBatchNames`（名称/分类去重，防重复导入）。
- **维护**：`deleteCategoryMapByTemplate`、`Base_Column_List`/`Blob_Column_List`（基础列 + 大字段列复用片段）。
- **导入应用数据收集**：`findAppViewInfo`/`findAppDatasetGroupInfo`/`findAppDatasetTableInfo`/`findAppDatasetTableFieldInfo`/`findAppDatasourceInfo`/`findAppDatasourceTaskInfo`/`findAppLinkageInfo`/`findAppLinkageFieldInfo`/`findAppLinkJumpInfo`/`findAppLinkJumpInfoInfo`/`findAppLinkJumpTargetViewInfoInfo` —— 按 `dvId`/`dsIds` 聚合模板所依赖的全部实体。

## 与表结构的关系

- Mapper 中的 `snapshot_*` 读写直接对应 migrations.md 所述 V2.10.7 发布镜像表。
- `copy_from`/`copy_id` 复制链在 `visualization_link_jump*`、`visualization_linkage*`、`visualization_outer_params*` 及 `snapshot_*` 表中均有物理列（见 schema-visualization.md）。
- `findApp*` 聚合的实体（core_chart_view、core_dataset_group/table/field、core_datasource、core_datasource_task、visualization_linkage*、visualization_link_jump*）即模板导入时的依赖闭包。
