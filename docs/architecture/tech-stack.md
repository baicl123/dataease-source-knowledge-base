# DataEase 技术栈

> 版本：**v2.10.7**。版本号取自根 `pom.xml` 与 `core/core-frontend/package.json` 的 dependencyManagement / dependencies。

## 1. 后端（Java）

| 类别 | 组件 | 版本 | 作用 |
|------|------|------|------|
| 框架 | Spring Boot | 3.3.0 | 应用框架（parent） |
| 语言 | Java | 21 | 编译目标 `maven.compiler.source/target=21` |
| 微服务 | Spring Cloud / Spring Cloud Alibaba | 2023.0.1 / 2023.0.1.0 | 分布式（Feign、注册发现，distributed 模式） |
| ORM | MyBatis-Plus / MyBatis-Spring | 3.5.6 / 3.0.3 | 持久层 |
| SQL 引擎 | Apache Calcite | 1.35.18 | 跨数据源查询解析/优化（engine 包） |
| 元数据库 | H2 | 2.2.220 | 内置元数据存储 |
| 缓存 | Ehcache | 3.10.8 | 多级缓存（`@EnableCaching`） |
| 鉴权 | Auth0 java-jwt | 3.12.1 | JWT 令牌签发/校验（`CommunityTokenFilter`、分享链接） |
| API 文档 | Knife4j | 4.4.0 | Swagger UI / OpenAPI |
| 模板 | Velocity | 2.3 | 动态 SQL / 代码生成（`MybatisPlusGenerator`） |
| 导入导出 | EasyExcel | 3.3.4 | Excel 读写 |
| PDF | iTextPDF | 8.0.4 | 报表导出 PDF |
| 截图 | Selenium | 4.19.1 | 仪表板截图/导出 |
| 驱动 | mysql-connector-j | 8.2.0 | MySQL 连接 |
| 工具 | Guava / commons-* / Lombok / BouncyCastle | 33.0 / 2.16+ / / 1.78 | 通用工具、加密 |
| 调度 | Quartz | (exclude AutoConfig) | 定时任务（`@EnableScheduling` + 手动 Quartz） |

## 2. 前端（Vue）

| 类别 | 组件 | 版本 | 作用 |
|------|------|------|------|
| 框架 | Vue | 3.3.4 | 组合式 API |
| 语言 | TypeScript | 4.9.3 | 类型系统 |
| 构建 | Vite | 4.1.3 | 开发/构建（多模式：base/distributed/lib） |
| 状态 | Pinia | 2.0.32 | 全局状态 |
| 路由 | Vue Router | 4.1.3 | 前端路由 + `permission.ts` 守卫 |
| 国际化 | Vue I18n | 9.2.2 | 多语言（`locales`） |
| UI | Element Plus（secondary）/ Vant | 0.6.8 / 4.8.3 | PC/移动端组件库 |
| 图表 | ECharts / AntV G2Plot / L7 / S2 | 5.5.1 / 2.4.29 / 2.22 / 1.49 | 可视化与地图 |
| HTTP | Axios | 1.3.3 | 接口请求 |
| 加密 | crypto-js / jsencrypt | 4.1.1 / 3.3.2 | 前端加解密 |
| 安全 | xss | 1.0.14 | XSS 防护 |
| 富文本 | TinyMCE | 5.8.2 | 文本编辑 |
| 报表 | exceljs / jspdf / html2canvas | 4.4 / 2.5.1 / 1.4.1 | 导出 |

## 3. 构建与依赖管理要点

- 根 `pom.xml` 的 `<modules>` 仅含 `sdk`；`core` 为独立聚合模块（`core-frontend`+`core-backend`），需单独构建。
- 统一版本在根 `pom.xml` 的 `dependencyManagement` 中收敛（避免子模块漂移）。
- 前端构建区分 `base` / `distributed` / `lib` 三种模式（对应后端部署 profile）。
- 企业扩展 `de-xpack` 以 **git submodule** 形式引入（本仓库仅指针，无内容），承载 LDAP/CAS/OIDC 等高级鉴权。
