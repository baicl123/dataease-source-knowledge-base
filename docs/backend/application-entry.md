# 应用入口与代码生成器（包根）后端分析（v2.10.7）

> 范围：`core/core-backend/src/main/java/io/dataease/` 包根下的 2 个 .java 文件（不在任何子包内，故由本篇补齐，以确保后端 Java 文件 100% 覆盖）。

## 1. CoreApplication.java（应用启动类）

- 路径：`core/core-backend/src/main/java/io/dataease/CoreApplication.java`
- 注解：
  - `@SpringBootApplication(exclude = {QuartzAutoConfiguration.class})` —— 显式排除 Spring Boot 的 Quartz 自动配置，改用项目自管的 Quartz 调度（见 `docs/backend/job-msg-resource.md`）。
  - `@EnableCaching` —— 开启 Spring 缓存抽象（底层 Ehcache，配置见 `ehcache/` 资源与 `docs/backend/foundation.md`）。
  - `@EnableScheduling` —— 开启 Spring 定时任务（与排除 QuartzAutoConfig 并存：轻量任务走 `@Scheduled`，重任务走编程式 Quartz）。
- `main` 方法：构造 `SpringApplication` 时通过 `context.addInitializers(new EhCacheStartListener())` 注册自定义 `ApplicationContextInitializer`（`EhCacheStartListener`，位于 `io.dataease.listener`，见 foundation 文档），用于在容器启动早期初始化 Ehcache。
- 结论：这是整个后端（core-backend）的引导入口，承载缓存/调度/Quartz 开关等全局行为。

## 2. MybatisPlusGenerator.java（代码生成器）

- 路径：`core/core-backend/src/main/java/io/dataease/MybatisPlusGenerator.java`
- 职责：基于 MyBatis-Plus `AutoGenerator` 的**数据库表 → Entity/Mapper/Service/Controller 代码生成器**脚手架（开发期工具，不参与运行时）。
- 关键要素：
  - 数据源配置（`DataSourceConfig`）、全局配置（`GlobalConfig`，含输出目录）、包名策略（`PackageConfig`）、策略配置（`StrategyConfig`，指定表名前缀、驼峰命名、Lombok/`@RestController` 等）。
  - 模板引擎：Velocity（`velocity-engine-core`，见 `docs/architecture/tech-stack.md`）。
- 结论：属于"工具代码"，按 AGENTS.md 仍需登记覆盖；运行时无调用，仅用于快速生成样板代码（DAO 层大量自动生成类即来源于此模式）。

## 3. 相关文档

- [基础架构与配置](foundation.md)
- [任务/导出/消息/资源](job-msg-resource.md)
- [集成与 SDK 能力层](integration-sdk.md)（含 Ehcache/Quartz 相关 SDK）
- [整体架构 - 构建与部署](../architecture/build-deploy.md)
