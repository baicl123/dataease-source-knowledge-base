# 目录结构

> 版本：**v2.10.7**。以下结构均来自 `git ls-files` 实际清单（非推测）。

## 1. 仓库根

```
dataease/
├── pom.xml                # 根 POM（parent=spring-boot-starter-parent 3.3.0；modules=[sdk]）
├── core/                  # 聚合模块：core-frontend + core-backend
│   ├── pom.xml
│   ├── core-backend/      # Spring Boot 后端（Java 21）
│   └── core-frontend/     # Vue3 前端
├── sdk/                   # 能力层（独立 Maven 多模块）
│   ├── api/  (api-base / api-permissions / api-sync)
│   ├── common/            # CommunityTokenFilter、公共工具
│   ├── distributed/       # 分布式 Feign 客户端
│   └── extensions/        # datasource / view / datafilling
├── drivers/               # JDBC 驱动 jar（clickhouse/db2/mssql/mysql/oracle/postgresql/redshift/impala）
├── installer/             # 安装部署脚本（install.sh, dectl, quick_start.sh, uninstall.sh, install.conf）
├── mapFiles/              # 地图数据（GeoJSON/SVG，3394 个，非源码）
├── staticResource/        # 静态资源
├── de-xpack/              # 企业版扩展（git submodule 指针，OSS 仓内为空）
├── docs/                  # DataEase 官方文档（上游，非本知识库分析对象）
└── .github/               # CI 配置
```

## 2. 后端源码结构（core-backend，基准 `src/main/`）

```
java/io/dataease/
├── CoreApplication.java        # 启动类（@SpringBootApplication(exclude=QuartzAutoConfiguration)）
├── ai/        copilot/         # AI 辅助分析
├── chart/     visualization/   # 图表计算、可视化
├── commons/                     # 公共基类/工具/上下文
├── config/                      # 配置（DeMvcConfig 等）
├── dataset/   datasource/      # 数据集 / 数据源（核心领域）
├── defeign/                      # Feign 客户端定义（含权限 Feign）
├── engine/                       # Calcite SQL 引擎
├── exportCenter/ job/ msgCenter/ operation/  # 导出/任务/消息/操作日志
├── home/      menu/             # 工作台、菜单
├── interceptor/                  # MybatisInterceptor（MyBatis SQL 拦截）
├── license/   map/ template/ resource/ font/  # 许可证/地图/模板/资源/字体
├── listener/  startup/          # 监听器、启动
├── share/                        # 分享/嵌入（JWT 链接令牌、LinkInterceptor）
├── substitute/permissions/*      # 登录/鉴权/组织/用户**兜底服务**
├── system/                       # 系统参数、菜单
├── websocket/                    # 实时推送
resources/
├── application.yml + application-{standalone,distributed,desktop}.yml
├── db/  ehcache/  i18n/  logback-spring.xml  mybatis/  saffron.properties  sql/  template/
```

## 3. 前端源码结构（core-frontend，基准 `src/`）

```
src/
├── views/        # 页面：dashboard, panel, visualized, data-visualization,
│                 #   system, share, login, copilot, template, mobile, wizard, canvas...
├── components/   # 公共组件（de-board, dashboard, data-visualization, cron, grid-table...）
├── api/          # 接口封装（auth.ts, login.ts, user.ts, org.ts, dataset.ts,
│                 #   datasource.ts, chart.ts, relation/, setting/, variable.ts...）
├── router/  store/  # 路由、Pinia 状态
├── permission.ts  permissionMobile.ts   # 前端路由守卫（菜单/权限控制）
├── locales/  hooks/  directive/  plugins/  websocket/  utils/  models/  config/  style/
```

## 4. SDK 源码结构（sdk，基准 `src/main/java/io/dataease/`）

```
api/
├── api-base/        # 基础 API 契约
├── api-permissions/ # 权限领域（auth/user/role/org/relation/dataset/embedded/apikey/setting/variable/login）
└── api-sync/        # 同步 API
common/auth/filter/CommunityTokenFilter.java   # 全局 JWT 鉴权 Filter
distributed/                                   # Feign 客户端（PermissionFeignService 等）
extensions/
├── extensions-datasource/  extensions-view/  extensions-datafilling/
```

## 5. 说明

- `mapFiles/`（3394 文件）为地图 GeoJSON/SVG 数据，**不计入源码覆盖率**，但登记于 `source-map.json`。
- `drivers/`（8 个 jar）为二进制依赖，非源码。
- `docs/`（DataEase 官方文档）属上游资料，本知识库不重复分析。
