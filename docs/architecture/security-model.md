# 安全模型（鉴权与权限）

> 版本：**v2.10.7**。本文是 TASKS.md 第 9 项（二次开发·权限检查 RBAC/ACL/ABAC）的**基石**，所有结论均附源码证据。
> 配套：`docs/diagrams/architecture.md`（图 3 认证流、图 4 权限域）。

## 1. 核心结论（先讲重点）

1. DataEase **不依赖 Spring Security / Shiro**，而是**自研可插拔鉴权架构**。
2. 社区版全局鉴权由 `sdk/common` 的 **`CommunityTokenFilter`**（Servlet `Filter`）完成，校验 JWT。
3. 权限领域被抽象为 `sdk/api/api-permissions` 的**一套完整 API**（用户/角色/组织/关系/菜单+业务资源/数据集行列/嵌入/APIKey/设置/变量/登录MFA）。
4. 在 **distributed** 模式，这些 API 通过 **Feign** 远程调用（独立权限微服务）。
5. **企业版高级鉴权（LDAP/CAS/OIDC 等）位于 `de-xpack`**（git submodule，本 OSS 仓仅指针、无内容）。
6. 数据集**行/列权限**（`RowPermissionsApi`/`ColumnPermissionsApi`）是 **ABAC 雏形**。

## 2. 认证（Authentication）

### 2.1 全局过滤器：`CommunityTokenFilter`

证据：`sdk/common/src/main/java/io/dataease/auth/filter/CommunityTokenFilter.java`

- 实现 `jakarta.servlet.Filter`（L28），`doFilter` 逻辑见 L33-L68。
- 取令牌：`ServletUtils.getToken()`（L35，头部 `DE-TOKEN`）。
- 取当前用户：`AuthUtils.getUser()` → `TokenUserBO`（含 `userId`、`defaultOid`）（L36）。
- 校验：当 `token` 非空且 `!LicenseUtil.licenseValid()`（社区/无有效许可证）时，用 HMAC256（`secret` 取自 `loginServer` Bean 的 `userCacheBO().getPwd()`，或 `SubstituleLoginConfig.getPwd()` 兜底）校验 JWT 的 `uid` + `oid` 声明（L37-L56）。
- 失败：返回 **401** 并带 `DE-GATEWAY-FLAG` 头（L57-L64）。
- 注意（行为观察）：`!LicenseUtil.licenseValid()` 为真才强制执行——**企业版（有效许可证）下由 `de-xpack` 接管鉴权**，社区过滤器放行。

### 2.2 分享/嵌入令牌

证据：`core/core-backend/src/main/java/io/dataease/share/`

- `util/LinkTokenUtil.java`：用 HMAC256 签发 JWT，声明 `uid`/`resourceId`/`oid`（L15-L17）。
- `interceptor/LinkInterceptor.java`：唯一被 `DeMvcConfig` 全局注册的 `HandlerInterceptor`（`config/DeMvcConfig.java` L47-L49），处理 `/link/**` 匿名访问。
- `interceptor/DeLinkAop.java`：AOP 校验链接令牌（L57/L72 解码 JWT）。

## 3. 授权（Authorization）领域 API

证据：`sdk/api/api-permissions/src/main/java/io/dataease/api/permissions/<domain>/api/*.java`

| 域 | 接口 | 说明 |
|----|------|------|
| 登录 | `LoginApi` | 账号/MFA 登录，签发令牌 |
| 用户 | `UserApi` | 用户 CRUD、启用、改密、绑定 |
| 角色 | `RoleApi` | 角色 CRUD、挂载/卸载用户、外部用户 |
| 组织 | `OrgApi` | 组织机构树（懒加载） |
| 关系 | `RelationApi` | 用户-角色-组织关系 |
| 鉴权 | `AuthApi` | **菜单权限树** + **业务资源权限树**（双向：资源→对象 / 对象→资源） |
| 数据集 | `RowPermissionsApi` / `ColumnPermissionsApi` | **行级 / 列级**权限规则（ABAC 雏形） |
| 嵌入 | `EmbeddedApi` | 嵌入/分享配置 |
| APIKey | `ApiKeyApi` | 接口密钥 |
| 设置 | `PerSettingApi` | 权限开关设置 |
| 变量 | `SysVariablesApi` | 系统变量（可用于权限表达式） |

内部交互接口 `InteractiveAuthApi`（`auth/api/InteractiveAuthApi.java`，`@Hidden`）提供菜单ID、资源树同步、权限校验 `checkAuth`、权限查询 `queryAuth` 等供内部调用。

## 4. RBAC / ACL / ABAC 映射

| 模型 | DataEase 对应实现 | 证据 |
|------|-------------------|------|
| **RBAC** | 用户→角色→权限（菜单/业务资源）；组织树提供数据范围 | `RoleApi`/`UserApi`/`OrgApi`/`AuthApi` |
| **ACL** | 业务资源权限树以"资源↔对象"双向授权（对象可为用户/角色/组织） | `AuthApi.busiPermission` / `busiTargetPermission` |
| **ABAC（雏形）** | 数据集行/列权限基于规则条件（字段+运算符+值），可含系统变量 | `RowPermissionsApi` / `ColumnPermissionsApi` / `SysVariablesApi` |

> 当前开源版**未引入统一策略引擎**（如 Casbin）。`AuthApi` 的实现层（`de-xpack` 或兜底 `Substitule*`）是接入 Casbin 做统一 RBAC/ABAC 的最佳切面。

## 5. 兜底与企业边界

- `core/core-backend/.../substitute/permissions/*`：
  - `SubstituleAuthServer.java` —— **整段被注释**（`/* ... */`），仅为桌面版离线兜底的占位实现（实现 `AuthApi`）。
  - `SubstituleLoginServer.java` / `SubstituleOrgServer.java` / `SubstituteUserServer.java` —— 同类兜底。
- `de-xpack`（企业版扩展）：git submodule，**本仓仅为空指针**。LDAP/CAS/OIDC、细粒度审计等高级能力在此实现，不随 OSS 源码发布。

## 6. 二次开发切入点

> 二次开发的完整方案、四套实现路径（A/B/C/D）、Casbin 集成、安全加固与实施检查清单，已集中收录于
> [`docs/customization/permission-development-guide.md`](../customization/permission-development-guide.md)（Task 9 交付物）。该文档的 §0.1 也保留了本架构相关的切入点速览。

## 7. 待验证项

- [Need Verification] 社区版 `loginServer` Bean 的真实实现位置（`SubstituleLoginServer` 为兜底，正式签发逻辑疑似在 `de-xpack` 或 `sdk` 某 `server` 包）。
- [Need Verification] `CommunityTokenFilter` 中 `licenseValid()` 为假才强制——需确认企业版完整鉴权链路（de-xpack）的确切类名与注册方式。
- [Inference] `substitute` 命名疑似历史遗留，不代表"用户替换"语义，实为"权限服务离线时的替补"。
