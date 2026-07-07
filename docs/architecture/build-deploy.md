# 构建与部署

> 版本：**v2.10.7**。依据根 `pom.xml`、`core/pom.xml`、`installer/`、`Dockerfile`、`core/core-backend/.../resources/application-*.yml`。

## 1. Maven 多模块关系

```
dataease (root, packaging=pom)
├── modules: [ sdk ]                      # 根仅直接构建 sdk
└── sdk (pom)
    ├── api (api-base / api-permissions / api-sync)
    ├── common
    ├── distributed
    └── extensions (datasource / view / datafilling)

core (pom, 独立构建)
├── core-frontend (Vue, 产出静态资源)
└── core-backend (Spring Boot, 打包可执行 jar，内嵌前端)
```

**关键点**：根 POM 不聚合 `core`。`sdk` 先构建并安装到本地仓库，`core` 随后单独构建并依赖已安装的 `sdk` 构件。

## 2. 构建命令（推断）

```bash
# 1) 构建能力层
mvn -q -pl sdk -am clean install -DskipTests

# 2) 构建应用（前端 + 后端）
cd core
mvn clean package -DskipTests
# 前端需在 core-frontend 先执行 vite build（见 package.json build:base|distributed|lib）
```

> [Need Verification] 确切的官方构建顺序以 `installer/` 或 CI（`.github/workflows`）为准，建议后续核对。

## 3. 部署模式（Profile）

`core/core-backend/src/main/resources/application.yml` 引入三套 Profile：

| Profile | 文件 | 特征 |
|---------|------|------|
| standalone | `application-standalone.yml` | 单体；权限逻辑内置/企业包提供 |
| distributed | `application-distributed.yml` | 权限等领域服务以 Feign 微服务独立部署（`sdk/distributed`） |
| desktop | `application-desktop.yml` | 桌面版；使用 `substitute` 兜底服务（离线） |

## 4. 安装与运维脚本

`installer/` 目录：

- `install.sh` / `quick_start.sh` / `uninstall.sh`：一键安装/卸载
- `dectl`：DataEase 控制脚本（启停/状态/升级）
- `install.conf`：安装配置（端口、数据目录等）
- `README.md`、`LICENSE`：安装说明

## 5. 容器化

- 仓库根 `Dockerfile`：基于安装产物构建镜像。
- 官方也提供 `quick_start_v2.sh` 与 1Panel 应用商店部署（见上游 README）。

## 6. 部署形态小结

- **服务器版**（standalone / distributed）：Linux 服务器，单机或微服务。
- **桌面版**（desktop）：PC 客户端（`de-xpack` 桌面能力）。
- **嵌入/分享**：通过 `io.dataease.share` 的 JWT 链接令牌对外提供只读仪表板。
