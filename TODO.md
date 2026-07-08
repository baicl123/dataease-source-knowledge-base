# TODO.md

本文件记录知识库的未来计划与未启动的结构性内容。已规划的 9 个分析任务见 `TASKS.md`。

## 待办任务

- [ ] **Task 8：建立版本升级机制**
  - 当前 `scripts/scan_source.py` 已可复用做版本目录差异扫描。
  - 尚无升级指南文档（如 `docs/upgrade/version-upgrade.md`）。
  - 需产出：变更摘要、影响范围、兼容性风险、增量更新流程。
  - 完成后引入版本快照归档目录 `versions/`。

## 未来可选内容（原 README 模板规划，尚未启动）

- [ ] `docs/glossary/`：术语表（如 Calcite、Snapshot、Xpack、DeApiPath 等）。
- [ ] `docs/adr/`：架构决策记录（如：为何选 Casbin 做权限引擎、snapshot_* 发布镜像模型的设计取舍）。
- [ ] `docs/plugin/`：插件/扩展机制专文（extensions-datasource / extensions-view / extensions-datafilling）。

> 注：上述 API、部署等内容已分别在 `docs/frontend/api-layer.md`、`docs/backend/api-permissions.md`、`docs/architecture/build-deploy.md` 中覆盖，无需重复建目录。

## 同步计划

- [x] 乐享知识库首轮全量同步（v2.10.7，30 篇文档，2026-07-07）。
- [ ] 版本升级后增量同步乐享 / ima 知识库。
