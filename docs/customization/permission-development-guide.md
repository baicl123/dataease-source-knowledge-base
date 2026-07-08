# DataEase 权限二次开发建议（v2.10.7）

> Task 9 交付物：基于源码验证的权限架构分析与二次开发方案，重点围绕 RBAC / ACL / ABAC 三种模型在 DataEase 社区版中的落地路径。

## 0. 文档定位与证据基础

本文档所有结论均回溯至源码（文件路径 + 行号）。社区版（无有效 License）的权限实状态用 ✅/❌ 标注。

| 层级 | 机制 | 社区版状态 | 关键源码 |
|------|------|-----------|----------|
| L1 请求认证 | `TokenFilter` + JWT | ✅ 有效 | `sdk/common/.../auth/filter/TokenFilter.java` |
| L1b 社区令牌校验 | `CommunityTokenFilter` | ✅ 有效（仅 `!licenseValid()` 时） | `sdk/common/.../auth/filter/CommunityTokenFilter.java` |
| L2 API 路径鉴权 | `@DeApiPath` 注解 | ❌ 无处理器 | `sdk/common/.../auth/DeApiPath.java` |
| L3 方法级声明鉴权 | `@DePermit` + SpEL | ❌ 无 AOP 处理器 | `sdk/common/.../auth/DePermit.java` |
| L4 业务资源 ACL | `CorePermissionManage.checkAuth()` | ❌ 桩方法，恒返回 `true` | `core/core-backend/.../system/manage/CorePermissionManage.java:11` |
| L5 数据集行/列权限 | `PermissionManage` + Feign API | ❌ API 为 null，权限不注入 | `core/core-backend/.../dataset/manage/PermissionManage.java:97` |
| L6 分享链接鉴权 | `LinkInterceptor` + `@DeLinkPermit` | ✅ 有效（但有安全隐患） | `core/core-backend/.../share/` + `config/DeMvcConfig.java` |

---

## 0.1 二次开发切入点速览

> 以下要点从 `docs/architecture/security-model.md` §6 抽取，作为二次开发总入口的概览。完整方案见本文第 3 节。

1. **统一策略引擎**：在 `AuthApi` 实现层引入 Casbin（RBAC/ABAC 模型），替换/增强现有分散的权限判断。
2. **行/列权限增强**：扩展 `RowPermissionsApi`/`ColumnPermissionsApi` 的规则表达能力，结合 `SysVariablesApi` 做上下文感知 ABAC。
3. **认证源扩展**：实现 `loginServer` Bean 或 `de-xpack` 认证扩展，接入企业 IdP（OIDC/SAML/LDAP）。
4. **前端守卫对齐**：`core-frontend/src/permission.ts` 的菜单/按钮级控制需与后端 `AuthApi` 权限树保持一致。

## 1. 权限架构全景（源码验证）

### 1.1 请求认证链路（L1）

```
TokenFilter.doFilter()
  ├── WhitelistUtils.match(uri)          → 白名单直接放行
  ├── ModelUtils.isDesktop()             → 桌面版：setDesktopUser(userId=1, oid=1)
  ├── linkToken 非空                      → TokenUtils.validateLinkToken() → setUserInfo
  └── token 非空                          → TokenUtils.validate() → setUserInfo
        └── finally: UserUtils.removeUser()   → ThreadLocal 清理
```

**关键事实**（`TokenFilter.java:24-100`）：
- `TokenFilter` 是**主 Servlet Filter**，负责所有非白名单请求的 JWT 校验与用户上下文注入。
- `TokenUserBO` 仅含 `userId` + `defaultOid`（`sdk/common/.../auth/bo/TokenUserBO.java`）。
- `AuthUtils` 使用 `ThreadLocal<TokenUserBO>` 存储当前用户（`sdk/common/.../utils/AuthUtils.java:10`）。
- **SysAdmin 硬编码为 userId=1**（`AuthUtils.java:8`：`SYS_ADMIN_UID = 1L`）。
- 异常处理：无 License 时返回 401；有 License 时 rethrow（企业版接管）。

**CommunityTokenFilter**（`sdk/common/.../auth/filter/CommunityTokenFilter.java`）：
- 仅在 `!LicenseUtil.licenseValid()` 时强制执行（社区版守卫）。
- 校验 JWT 中的 `uid` + `oid` 声明（HMAC256，`CommunityTokenFilter.java:52`）。
- `TokenFilter` 先执行（设 ThreadLocal），`CommunityTokenFilter` 后执行（二次校验声明一致性）。

### 1.2 API 路径鉴权（L2）——社区版空转

`@DeApiPath`（`sdk/common/.../auth/DeApiPath.java`）：
```java
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE})    // 标注在 API 接口类上
public @interface DeApiPath {
    String[] value() default {};           // 路径匹配
    AuthResourceEnum rt();                  // 资源类型：DATASET / PANEL / ...
}
```

**使用点**（`sdk/api/` 下 10+ 个 API 接口）：`ChartDataApi`、`DatasetTreeApi`、`DatasourceApi`、`DataVisualizationApi`、`RowPermissionsApi`、`ColumnPermissionsApi`、`OrgApi`、`RoleApi`、`UserApi` 等。

**社区版状态**：全代码库无 `@DeApiPath` 的 AOP 处理器 / 拦截器。[Inference] 由企业版 `de-xpack` 的 AOP 切面解析 `@DeApiPath` 并校验资源路径权限。

### 1.3 方法级声明鉴权（L3）——社区版空转

`@DePermit`（`sdk/common/.../auth/DePermit.java`）：
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface DePermit {
    String[] value() default {};    // SpEL 鉴权表达式数组（&运算，非||）
    String busiFlag() default "";    // 业务标志 SpEL
}
```

**使用点**（`sdk/api/api-base/` 下 ~20 个 API 方法）：

| API 接口 | 方法 | SpEL 表达式 | 含义 |
|----------|------|------------|------|
| `ChartDataApi` | exportView | `#p0.dvId+':export_view'` | 导出仪表板视图 |
| `ChartDataApi` | exportDetail | `#p0.dvId+':export_detail'` | 导出明细数据 |
| `DatasetTreeApi` | save/move/rename/delete | `#p0.id+':manage'` | 数据集管理权 |
| `DatasetTreeApi` | export | `#p0.id+':export'` | 数据集导出权 |
| `DatasourceApi` | save/update/delete | `#p0+':manage'` | 数据源管理权 |
| `DatasourceApi` | validate/checkApiDs | `#p0+':read'` | 数据源读权 |
| `DataVisualizationApi` | findById | `#p0.id+':read'` | 仪表板读权 |
| `DataVisualizationApi` | saveCanvas/move | `#p0.pid+':manage'` | 仪表板管理权 |

**SpEL 模式**：`<资源ID表达式>:<权限类型>`，权限类型对应 `AuthEnum`（READ/USER/EXPORT/MANAGE/AUTH）。

**社区版状态**：全代码库无 `@DePermit` 的 AOP 处理器。[Inference] 由企业版 AOP 切面解析 SpEL，调用 `CorePermissionManage.checkAuth()` 或等效 Feign 服务。

### 1.4 业务资源 ACL（L4）——社区版桩方法

`CorePermissionManage`（`core/core-backend/.../system/manage/CorePermissionManage.java`）：
```java
@Component
public class CorePermissionManage {
    @XpackInteract(value = "corePermissionManage", replace = true)
    public boolean checkAuth(BusiPerCheckDTO dto) {
        return true;    // 桩方法：社区版永远放行
    }
}
```

**`BusiPerCheckDTO`**（`sdk/api/api-permissions/.../auth/dto/BusiPerCheckDTO.java`）：
```java
public class BusiPerCheckDTO {
    private Long id;           // 资源 ID（数据集/仪表板/数据源等）
    private AuthEnum authEnum;  // 权限类型
}
```

**`AuthEnum`**（`sdk/common/.../constant/AuthEnum.java`）：

| 枚举值 | weight | 含义 |
|--------|--------|------|
| READ | 1 | 读取/查看 |
| USER | 2 | 使用 |
| EXPORT | 4 | 导出 |
| EXPORT_VIEW | 5 | 导出视图 |
| EXPORT_DETAIL | 6 | 导出明细 |
| MANAGE | 7 | 管理（编辑/删除） |
| AUTH | 9 | 授权（分配权限给他人） |

**调用点**（5 处）：

| 调用方 | 文件:行号 | 场景 | AuthEnum |
|--------|-----------|------|----------|
| `ChartDataManage` | `ChartDataManage.java:122` | 图表取数前校验数据集读权 | READ |
| `DatasetDataManage` | `DatasetDataManage.java:663` | 数据集数据预览 | READ（推断） |
| `DatasetDataManage` | `DatasetDataManage.java:828` | 数据集数据查询 | READ（推断） |
| `DatasetSQLManage` | `DatasetSQLManage.java:501` | 数据集 SQL 执行 | READ（推断） |
| `ResourceService` | `ResourceService.java:23` | 资源树访问 | READ（推断） |

### 1.5 数据集行/列权限（L5）——社区版不注入

`PermissionManage`（`core/core-backend/.../dataset/manage/PermissionManage.java`）：

```java
@Service
public class PermissionManage {
    @Autowired(required = false)
    private RowPermissionsApi rowPermissionsApi;        // 社区版为 null

    @Autowired(required = false)
    private ColumnPermissionsApi columnPermissionsApi;  // 社区版为 null
    ...
}
```

**列权限**（`filterColumnPermissions()`, 行 51-91）：
- 从 `ColumnPermissionsApi.list()` 获取用户级 + 角色级列权限规则。
- `ColumnPermissions` 结构：`{ enable: bool, columns: [{ id, selected, opt, desensitizationRule }] }`。
- `opt` 取值：`show`（显示）或 `desensitization`（脱敏）。
- 脱敏规则（`ColumnPermissionItem.DesensitizationRule`）：
  - `CompleteDesensitization` → `******`
  - `KeepFirstAndLastThreeCharacters` → `XXX***XXX`
  - `KeepMiddleThreeCharacters` → `***XXX***`
  - `custom` → `RetainBeforeMAndAfterN` / `RetainMToN`
- **白名单**：角色级规则支持 `whiteListUser`，白名单内用户不受该规则约束。
- **社区版**：API 为 null → `columnPermissions()` 返回空列表 → 所有字段可见。

**行权限**（`getRowPermissionsTree()`, 行 137-226）：
- 从 `RowPermissionsApi.list()` 获取三类规则：user / role / sysParams。
- 权限树结构（`DatasetRowPermissionsTreeObj`）：
  ```
  TreeObj = { logic: "AND"|"OR", items: [TreeItem] }
  TreeItem = { type: "item"|"tree", fieldId, field, filterType: "logic"|"enum",
               term: "eq"|"not_eq"|"lt"|"le"|"gt"|"ge"|"in"|"not in"|"like"|"null"|...,
               value, enumValue, subTree: TreeObj }
  ```
- **白名单**：支持 userId / roleId / deptId 三维白名单，命中则跳过规则。
- **系统变量替换**：`${sysParams.userId}` / `${sysParams.userEmail}` / `${sysParams.userName}` / 自定义变量 `${variableId}`。
- **SysAdmin 旁路**：`AuthUtils.isSysAdmin(userId)` → 返回空列表（行 151）。
- **社区版**：API 为 null → 返回空列表 → 无行级过滤。

**行权限→SQL 注入**（`WhereTree2Str.java`）：
- `transFilterTrees(SQLMeta, List<DataSetRowPermissionsTreeDTO>, ...)` 将权限树转为 SQL WHERE。
- 多个权限树之间用 **OR** 拼接（非 export），export 类型用 **AND** 拼接（行 57-61）。
- 单个树内用 `logic`（AND/OR）拼接子条件，递归处理 subtree。
- 支持跨数据源（isCross）的类型转换与方言适配。

### 1.6 `@XpackInteract` 插桩机制

```java
@XpackInteract(value = "corePermissionManage", replace = true)  // 完全替换
@XpackInteract(value = "chartViewManage")                       // 包装（before/after）
```

- **来源**：`io.dataease.license.config.XpackInteract`——不在 OSS 源码中，[Inference] 来自 `de-xpack` 的 JAR 依赖。
- `replace = true`：企业版完全替换方法体（如 `checkAuth`）。
- 不指定 `replace`：企业版在方法前后织入逻辑（AOP 环绕通知）。
- **使用范围**：17+ 个 manage 类（chart/dataset/datasource/visualization/export/job/menu/msg/share/system）。
- **社区版行为**：无 License 时注解不生效，方法体原样执行（桩方法返回 `true`）。

### 1.7 分享链接鉴权（L6）

- `LinkInterceptor`（`core/core-backend/.../share/`）：注册在 `DeMvcConfig` 中，拦截分享链接路径。
- `@DeLinkPermit`：标注在 API 方法上，声明需要链接令牌校验。
- `LinkTokenUtil`：JWT 签发与校验，密钥硬编码 `link-pwd-fit2cloud`（`auth-core.md` 已记录安全风险）。
- `SubstituleLoginServer`：社区版登录服务（仅 admin，HMAC256 对称密钥）。

---

## 2. 权限模型映射

### 2.1 RBAC（基于角色的访问控制）

**DataEase 已有 RBAC 雏形**：

| 概念 | 源码体现 | 社区版状态 |
|------|----------|-----------|
| 用户 (User) | `api-permissions/.../user/api/UserApi` | ✅ 接口存在 |
| 角色 (Role) | `api-permissions/.../role/api/RoleApi` | ✅ 接口存在 |
| 组织 (Org) | `api-permissions/.../org/api/OrgApi` | ✅ 接口存在 |
| 用户-角色关联 | `RowPermissionsApi.getUserById(userId).getRoleIds()` | ❌ 实现缺失 |
| 角色-资源授权 | `BusiPerCheckDTO` + `AuthEnum` | ❌ `checkAuth` 桩 |
| 权限权重 | `AuthEnum` weight 体系（1/2/4/5/6/7/9） | ❌ 未执行 |

**RBAC 权限层级**（推断自 `AuthEnum` weight 设计）：
```
READ(1) < USER(2) < EXPORT(4) < EXPORT_VIEW(5) < EXPORT_DETAIL(6) < MANAGE(7) < AUTH(9)
```
[Inference] 权重设计暗示权限继承：拥有 MANAGE(7) 的用户隐含拥有 READ(1) 至 EXPORT_DETAIL(6)。

### 2.2 ACL（访问控制列表）

**DataEase 的 ACL 体现**：业务资源双向授权。
- `@DePermit` SpEL 表达式 `<resourceId>:<permission>` 本质是 ACL 查询。
- `CorePermissionManage.checkAuth(BusiPerCheckDTO)` 是 ACL 检查入口。
- 社区版 ACL 表完全为空（`checkAuth` 恒 `true`）。

### 2.3 ABAC（基于属性的访问控制）

**DataEase 的 ABAC 雏形**：数据集行/列权限。

| ABAC 要素 | DataEase 实现 |
|-----------|--------------|
| 主体属性 | userId, roleId, deptId, sysParams (userName/userEmail/userAccount), 自定义系统变量 |
| 资源属性 | datasetId, fieldId, 字段类型 (deType/deExtractType) |
| 环境属性 | 白名单 (whiteListUser/whiteListRole/whiteListDept) |
| 操作 | READ / EXPORT（exportData 标志区分 WHERE 拼接策略） |
| 规则引擎 | `DatasetRowPermissionsTreeObj` 递归表达式树 + `WhereTree2Str` SQL 生成 |

**ABAC 规则结构**：
```
规则 = { 授权对象: user|role|sysParams, 数据集ID, 启用状态, 表达式树, 白名单 }
表达式树 = { logic: AND|OR, items: [条件项|子树] }
条件项 = { 字段, 过滤类型: logic|enum, 操作符, 值 }
```

---

## 3. 二次开发方案

### 3.1 方案 A：最小侵入——实现 `CorePermissionManage.checkAuth()`（RBAC + ACL）

**目标**：让社区版拥有业务资源 ACL 能力（图表/数据集/数据源/仪表板的 READ/MANAGE/AUTH 校验）。

**改动范围**：仅 1 个文件 + 1 张表。

**步骤**：

1. **建表**（RBAC 授权关系表）：
   ```sql
   CREATE TABLE ext_resource_acl (
     id          BIGINT PRIMARY KEY AUTO_INCREMENT,
     resource_id BIGINT NOT NULL,          -- 资源 ID
     resource_type VARCHAR(32) NOT NULL,   -- DATASET / PANEL / DATASOURCE / ...
     auth_target_id BIGINT NOT NULL,       -- 授权对象 ID
     auth_target_type VARCHAR(16) NOT NULL, -- user / role / dept
     auth_enum   INT NOT NULL,             -- AuthEnum weight (1/2/4/7/9)
     created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     INDEX idx_resource (resource_id, resource_type),
     INDEX idx_target (auth_target_id, auth_target_type)
   );
   ```

2. **重写 `CorePermissionManage`**：
   ```java
   @Component
   public class CorePermissionManage {
       @Resource
       private ExtResourceAclMapper aclMapper;

       // 移除 @XpackInteract，或保留但社区版降级到本地实现
       public boolean checkAuth(BusiPerCheckDTO dto) {
           TokenUserBO user = AuthUtils.getUser();
           if (user == null || AuthUtils.isSysAdmin(user.getUserId())) {
               return true;
           }
           // 查询用户直接授权 + 角色授权 + 部门授权
           List<Integer> granted = aclMapper.queryAuthWeights(
               dto.getId(), user.getUserId());
           if (CollectionUtils.isEmpty(granted)) {
               return false;
           }
           // 权限权重比较：拥有 >= 请求权重的权限即通过
           return granted.stream().anyMatch(w -> w >= dto.getAuthEnum().getWeight());
       }
   }
   ```

3. **管理 API**：新增 `ExtAclController` 提供 CRUD 接口供管理员分配权限。

**优点**：改动极小，5 个 `checkAuth` 调用点立即生效，RBAC 权重体系天然支持权限继承。

**局限**：仅覆盖 L4（业务资源 ACL），不覆盖 L5（数据集行/列权限）。

### 3.2 方案 B：中等侵入——实现 `@DePermit` AOP 处理器（声明式鉴权）

**目标**：让社区版的 `@DePermit` SpEL 表达式生效，无需在每个方法体内手写 `checkAuth`。

**改动范围**：新增 1 个 AOP 切面类。

**步骤**：

1. **新增 `DePermitAspect`**：
   ```java
   @Aspect
   @Component
   public class DePermitAspect {
       @Resource
       private CorePermissionManage corePermissionManage;

       @Around("@annotation(dePermit)")
       public Object around(ProceedingJoinPoint pjp, DePermit dePermit) throws Throwable {
           TokenUserBO user = AuthUtils.getUser();
           if (user != null && AuthUtils.isSysAdmin(user.getUserId())) {
               return pjp.proceed();  // admin 旁路
           }
           // 解析 SpEL 表达式：#p0.id+':manage' → "123:manage"
           ExpressionParser parser = new SpelExpressionParser();
           EvaluationContext ctx = new StandardEvaluationContext(pjp.getArgs());
           for (String expr : dePermit.value()) {
               String resolved = parser.parseExpression(expr).getValue(ctx, String.class);
               // 解析 "resourceId:permission"
               String[] parts = resolved.split(":");
               Long resourceId = Long.valueOf(parts[0]);
               AuthEnum authEnum = AuthEnum.valueOf(parts[1].toUpperCase());
               BusiPerCheckDTO dto = new BusiPerCheckDTO(resourceId, authEnum);
               if (!corePermissionManage.checkAuth(dto)) {
                   throw new DEException(Translator.get("i18n_no_permission"));
               }
           }
           return pjp.proceed();
       }
   }
   ```

2. **依赖方案 A**：`DePermitAspect` 调用 `CorePermissionManage.checkAuth()`，因此需先完成方案 A。

**优点**：20 个已标注 `@DePermit` 的 API 方法自动获得鉴权，无需修改业务代码。

**注意**：SpEL 表达式中的权限类型字符串（如 `manage`、`read`、`export_view`）需与 `AuthEnum` 枚举名映射，注意大小写和下划线处理。

### 3.3 方案 C：完整侵入——实现 `RowPermissionsApi` / `ColumnPermissionsApi`（ABAC 行/列权限）

**目标**：让社区版拥有数据集行/列权限能力。

**改动范围**：新增 2 个 API 实现 + 2 张表 + 管理界面。

**步骤**：

1. **建表**：
   ```sql
   -- 行权限规则
   CREATE TABLE ext_row_permissions (
     id          BIGINT PRIMARY KEY AUTO_INCREMENT,
     dataset_id  BIGINT NOT NULL,
     auth_target_id BIGINT NOT NULL,
     auth_target_type VARCHAR(16) NOT NULL,  -- user / role / sysParams
     enable      TINYINT DEFAULT 1,
     expression_tree TEXT,                    -- DatasetRowPermissionsTreeObj JSON
     white_list_user TEXT,                    -- JSON: [userId]
     white_list_role TEXT,
     white_list_dept TEXT,
     export_data TINYINT DEFAULT 0,
     INDEX idx_dataset (dataset_id)
   );

   -- 列权限规则
   CREATE TABLE ext_column_permissions (
     id          BIGINT PRIMARY KEY AUTO_INCREMENT,
     dataset_id  BIGINT NOT NULL,
     auth_target_id BIGINT NOT NULL,
     auth_target_type VARCHAR(16) NOT NULL,
     permissions TEXT NOT NULL,               -- ColumnPermissions JSON
     white_list_user TEXT,
     INDEX idx_dataset (dataset_id)
   );
   ```

2. **实现 `RowPermissionsApi`**：
   ```java
   @RestController
   @Tag(name = "行权限")
   @DeApiPath(value = "/dataset/rowPermissions", rt = DATASET)
   public class ExtRowPermissionsServer implements RowPermissionsApi {
       @Resource
       private ExtRowPermissionsMapper mapper;

       @Override
       public List<DataSetRowPermissionsTreeDTO> list(DatasetRowPermissionsTreeRequest req) {
           return mapper.list(req);
       }

       @Override
       public UserFormVO getUserById(Long id) {
           // 需实现用户查询（含角色 ID 列表）
           // 社区版可从 system 包的 CoreUserManage 获取
       }

       @Override
       public List<Item> authObjs(Long datasetId, String type) {
           return mapper.authObjs(datasetId, type);
       }
       // ... save / delete / pager / dataSetRowPermissionInfo / whiteListUsers
   }
   ```

3. **实现 `ColumnPermissionsApi`**：同理。

4. **`PermissionManage` 自动生效**：因为 `@Autowired(required = false)`，一旦 Spring 容器中有 `RowPermissionsApi` / `ColumnPermissionsApi` 的 Bean，`PermissionManage` 的行/列权限逻辑自动激活。

**优点**：覆盖 L5，数据集行/列权限完整生效，`WhereTree2Str` 的 SQL 注入链路无需修改。

**关键难点**：
- `getUserById(userId)` 需返回 `UserFormVO`（含 `roleIds`、`account`、`email`、`name`、`variables`），社区版用户表结构需自行补齐。
- 系统变量替换依赖 `UserFormVO.getVariables()`，需实现系统变量管理。
- 白名单 JSON 解析与 `PermissionManage` 的逻辑需严格对齐。

### 3.4 方案 D：引入 Casbin 作为统一权限引擎

**目标**：用 Casbin 统一管理 RBAC + ACL + ABAC，替代分散的桩方法与 Feign 接口。

**Casbin 模型设计**：

```ini
# model.conf — DataEase 权限模型
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act, eft

[role_definition]
g = _, _
g2 = _, _   # 用户-角色

[policy_effect]
e = some(where (p.eft == allow)) && !some(where (p.eft == deny))

[matchers]
# RBAC: 用户→角色→资源→操作
m = g2(r.sub, p.sub) && keyMatch(r.obj, p.obj) && keyMatch(r.act, p.act)
```

**集成切面**：

| Casvin 调用点 | 替换的 DataEase 组件 | 改动量 |
|---------------|----------------------|--------|
| `CorePermissionManage.checkAuth()` | L4 业务资源 ACL | 1 文件 |
| `DePermitAspect`（新增） | L3 方法级声明鉴权 | 1 新文件 |
| `ExtRowPermissionsServer`（新增） | L5 行权限 | 1 新文件 |
| `ExtColumnPermissionsServer`（新增） | L5 列权限 | 1 新文件 |

**Casbin 适配器**：

```java
@Component
public class CasbinPermissionEngine {
    private Enforcer enforcer;

    @PostConstruct
    public void init() {
        String modelPath = "classpath:casbin/model.conf";
        String policyPath = "classpath:casbin/policy.csv"; // 或 DB adapter
        enforcer = new Enforcer(modelPath, policyPath);
    }

    public boolean checkAuth(Long resourceId, AuthEnum authEnum) {
        TokenUserBO user = AuthUtils.getUser();
        if (user == null || AuthUtils.isSysAdmin(user.getUserId())) return true;
        String sub = "user:" + user.getUserId();
        String obj = "resource:" + resourceId;
        String act = authEnum.name().toLowerCase();
        return enforcer.enforce(sub, obj, act);
    }

    public List<DataSetRowPermissionsTreeDTO> getRowPermissions(Long datasetId, Long userId) {
        // 从 Casbin policy 查询 ABAC 规则，转换为 DatasetRowPermissionsTreeDTO
        // 或使用 Casbin 的 ABAC 模型直接评估
    }
}
```

**优点**：
- 统一权限模型，RBAC/ACL/ABAC 一套引擎。
- Casbin 原生支持 RBAC with domains（对应 DataEase 的组织-角色-资源三层）。
- 策略热加载，无需重启。

**注意**：
- Casbin 的 ABAC 模型与 DataEase 的 `DatasetRowPermissionsTreeObj` 结构不同，需做适配层。
- 行权限的 SQL 注入仍需走 `WhereTree2Str`，Casbin 仅负责规则存储与查询。
- 引入 Casbin 增加 ~2MB 依赖（`org.casbin:jcasbin`）。

### 3.5 方案对比与推荐

| 方案 | 覆盖层 | 改动量 | 难度 | 推荐场景 |
|------|--------|--------|------|----------|
| A: 重写 checkAuth | L4 (ACL) | ⭐ | 低 | 仅需资源级 RBAC |
| B: @DePermit AOP | L3 (声明式) | ⭐⭐ | 中 | 已标注注解的 API 自动生效 |
| C: 实现 Feign API | L5 (行/列) | ⭐⭐⭐ | 高 | 需要数据级行/列权限 |
| D: Casbin 统一引擎 | L3+L4+L5 | ⭐⭐⭐⭐ | 高 | 需要完整权限体系 + 长期维护 |

**推荐路径**：A → B → C → D（渐进式）。
- **第一步**（方案 A）：1 个文件让 `checkAuth` 生效，立即获得资源级 RBAC。
- **第二步**（方案 B）：1 个 AOP 切面让 `@DePermit` 生效，20 个 API 自动鉴权。
- **第三步**（方案 C）：实现 Feign API，解锁数据集行/列权限。
- **第四步**（方案 D）：引入 Casbin 统一引擎，替代分散实现。

---

## 4. 安全加固建议（独立于权限模型）

### 4.1 分享链接密钥硬编码

**风险**：`LinkTokenUtil` 使用硬编码密钥 `link-pwd-fit2cloud`（`auth-core.md` 已记录）。攻击者可伪造分享链接令牌。

**建议**：
- 从配置文件或环境变量读取密钥：`link.token.secret=${DE_LINK_TOKEN_SECRET}`。
- 启动时校验密钥长度 ≥ 32 字节。
- 不同部署实例使用不同密钥。

### 4.2 AI Copilot SSL 校验关闭

**风险**：`ai-copilot` 的 `HttpClientUtil` 全局关闭证书校验（`NoopHostnameVerifier`），中间人攻击可截获 LLM API 令牌（`ai-copilot.md` 已记录）。

**建议**：
- 移除 `NoopHostnameVerifier`，使用默认证书校验。
- 若需自签证书，通过 TrustStore 配置而非全局关闭。

### 4.3 SysAdmin 硬编码

**风险**：`AuthUtils.SYS_ADMIN_UID = 1L` 硬编码，userId=1 的用户拥有全部权限旁路（行/列权限、checkAuth 均跳过）。

**建议**：
- 改为数据库配置：`sys_admin_uids` 表，支持多管理员。
- 或通过角色标记：`is_sys_admin` 字段在 `TokenUserBO` 中携带。

### 4.4 桌面版自动登录

**风险**：`TokenFilter.java:64-67`：桌面模式自动以 admin 身份登录（`setDesktopUser(userId=1, oid=1)`），无任何认证。

**建议**：
- 桌面版启动时生成一次性令牌，写入本地文件，`TokenFilter` 校验令牌而非自动登录。
- 或限制桌面版仅监听 `127.0.0.1`。

### 4.5 白名单路径审计

**风险**：`WhitelistUtils.match(uri)` 决定是否跳过认证，白名单路径过多会扩大未认证攻击面。

**建议**：
- 定期审计白名单路径列表。
- 白名单仅允许 GET 请求（排除写操作）。
- 白名单路径不返回敏感数据。

---

## 5. 实施检查清单

### 5.1 方案 A 检查清单

- [ ] 创建 `ext_resource_acl` 表
- [ ] 重写 `CorePermissionManage.checkAuth()`（移除 `@XpackInteract` 或保留降级）
- [ ] 实现 `ExtResourceAclMapper`（MyBatis-Plus）
- [ ] 新增 `ExtAclController` CRUD API
- [ ] 验证 5 个调用点行为（ChartDataManage / DatasetDataManage ×2 / DatasetSQLManage / ResourceService）
- [ ] 验证 SysAdmin 旁路
- [ ] 验证无 Token 时的异常处理

### 5.2 方案 B 检查清单

- [ ] 新增 `DePermitAspect`
- [ ] SpEL 表达式解析与 `AuthEnum` 映射
- [ ] 验证 20 个 `@DePermit` 标注的 API 方法
- [ ] 验证 `busiFlag` SpEL 解析
- [ ] 验证 admin 旁路
- [ ] 验证权限不足时抛出 `DEException` 并返回国际化消息

### 5.3 方案 C 检查清单

- [ ] 创建 `ext_row_permissions` + `ext_column_permissions` 表
- [ ] 实现 `RowPermissionsApi` 全部 8 个方法
- [ ] 实现 `ColumnPermissionsApi` 全部 5 个方法
- [ ] `getUserById()` 返回完整 `UserFormVO`（含 roleIds / account / email / name / variables）
- [ ] 系统变量替换逻辑与 `PermissionManage.handleSysVariable()` 对齐
- [ ] 白名单 JSON 格式与 `PermissionManage` 解析逻辑对齐
- [ ] 验证 `WhereTree2Str.transFilterTrees()` SQL 生成正确
- [ ] 验证跨数据源（isCross）场景
- [ ] 验证 export 与非 export 的 OR/AND 拼接
- [ ] 验证列脱敏规则（4 种内置 + 自定义 M-N）

### 5.4 方案 D 检查清单

- [ ] 引入 `org.casbin:jcasbin` 依赖
- [ ] 设计 Casbin model.conf（RBAC with domains + ABAC）
- [ ] 实现 `CasbinPermissionEngine`
- [ ] 实现 Casbin Policy DB Adapter（MyBatis-Plus）
- [ ] `CorePermissionManage.checkAuth()` 委托 Casbin
- [ ] `DePermitAspect` 委托 Casbin
- [ ] 行权限规则从 Casbin 查询后转换为 `DatasetRowPermissionsTreeDTO`
- [ ] 策略热加载机制
- [ ] 性能压测（Casbin enforce 调用频率 = 每请求至少 1 次）

---

## 6. 相关文档

- [安全模型总览](../architecture/security-model.md) — 权限架构全景与 `@XpackInteract` 机制
- [权限领域 API（api-permissions）](../backend/api-permissions.md) — RBAC/ACL/ABAC 契约层
- [鉴权与分享（auth-core）](../backend/auth-core.md) — 登录/分享链接/JWT 签发
- [集成与 SDK 能力层](../backend/integration-sdk.md) — CommunityTokenFilter / LicenseUtil / Feign
- [数据集（Dataset）](../backend/dataset.md) — 数据集建模与查询链路
- [SQL 引擎（Engine）](../backend/engine.md) — ST4 SQL 构建与 Calcite 联邦查询
- [AI 与 Copilot](../backend/ai-copilot.md) — 外部 LLM 调用安全风险

---

*本文档基于 DataEase v2.10.7 源码分析，所有结论可通过文件路径+行号回溯验证。标注 [Inference] 的结论为基于代码结构的推断，需企业版源码确认。*
