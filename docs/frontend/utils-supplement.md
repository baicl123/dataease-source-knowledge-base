# 工具函数与配置补充分析（v2.10.7）

## 1. 职责与架构位置

本文档是 `infrastructure.md` 的补充，覆盖 **56 个文件**，包括：
- **utils/**（39 files）— 通用工具函数、画布操作、加密解密、权限检查、校验等
- **config/**（4 files）— axios 配置与拦截器
- **directive/**（3 files）— Vue 自定义指令（权限控制、点击外部）
- **plugins/**（3 files）— Vue 插件注册（Element Plus、i18n）
- **models/**（8 files）— 类型定义（图表、树节点）

所有文件位于 `core/core-frontend/src/` 下。

## 2. 文件清单与关键导出

### 2.1 utils/ — 工具函数（39 files）

| 文件 | 关键导出函数/变量 | 职责 | 备注 |
|------|-------------------|------|------|
| `encryption.ts` | `rsaEncryp(word)`, `symmetricDecrypt(data, keyStr)` | RSA 加密 + AES 解密 | 核心安全模块，配合登录加密 |
| `validate.ts` | `isExternal(path)`, `validUsername(str)`, `PHONE_REGEX`, `EMAIL_REGEX` | URL 外部链接判断、用户名验证、正则常量 | 被 Menu/Header 使用 |
| `url.ts` | `formatDataEaseBi(url)` | URL 拼接（嵌入式 baseUrl 前缀） | 嵌入式/DataEaseBi 场景 |
| `CanvasInfoTransUtils.ts` | `defaultConditionTrans(canvasInfo)` | 画布信息转换：提取所有查询条件 | 仪表板查询条件核心工具 |
| `CrossPermission.ts` | `check(data, id, weight)`, `compareStorage(oldVal, newVal)` | 跨页面权限检查 | 编辑面板时检查资源访问权限 |
| `check.ts` | `checkArrayRepeat(arrayData, key)` | 数组重复检查 | 简单工具 |
| `utils.ts` | `deepCopy`, `isMobile`, `isTablet`, `isInIframe`, `isLink`, `checkPlatform`, `setTitle`, `getLocale`, `exportPermission`, `formatExt`, `cutTargetTree`, `deepCopyArray`, 等 30+ 个导出 | 通用工具集 | 最核心的工具文件，被广泛引用 |
| `canvasStyle.ts` | `getStyle`, `adaptCurTheme`, `colorRgb`, `seriesAdaptor`, `recursionTransObj`, 等 30+ 个导出 | 画布样式处理（主题色、缩放、旋转） | 仪表板编辑器核心样式工具 |
| `canvasUtils.ts` | `findComponentById`, `componentSwitch`, `initCanvasDataPrepare`, `historyAdaptor`, `isDashboard`, `checkJoinGroup`, 等 30+ 个导出 | 画布组件操作（查找、初始化、历史适配） | 仪表板编辑器核心操作工具 |
| `style.ts` | `getStyle`, `getShapeStyle`, `createGroupStyle`, `groupStyleRevert`, `getCanvasStyle`, 等 15 个导出 | 组件样式获取/合成 | 与 canvasStyle.ts 配合使用 |
| `translate.ts` | `calculateRotatedPointCoordinate`, `changeStyleWithScale`, `sin`, `cos`, `mod360`, `toPercent` | 坐标旋转/缩放变换 | 编辑器拖拽旋转核心数学工具 |
| `changeComponentsSizeWithScale.ts` | `changeComponentSizeWithScale`, `changeSizeWithScale`, `changeRefComponentsSizeWithScalePoint` | 组件尺寸缩放 | 仪表板缩放适配 |
| `calculateComponentPositionAndSize.ts` | `calculateComponentPositionAndSize`, `calculateRadioComponentPositionAndSize` | 组件位置/尺寸计算 | 编辑器拖拽位置计算 |
| `decomposeComponent.ts` | `decomposeComponent(component, regionStyle, detailStyle)` | 组件样式分解 | 组件样式拆分 |
| `components.ts` | `findComponent(key)`, `findComponentAttr(component)`, `componentsMap` | 组件映射表 | 注册表模式 |
| `componentUtils.ts` | `filterEnumMapSync`, `filterEnumParams` | 组件枚举参数工具 | 过滤组件联动 |
| `attr.ts` | `positionData`, `styleData`, `fieldType`, `fieldTypeText`, `optionMap`, 等 13 个导出 | 组件属性常量 | 编辑器属性面板配置 |
| `ShapeUtils.ts` | `checkJoinGroup`, `checkJoinTab`, `itemCanvasPathCheck`, `canvasIdMapCheck` | 图形组件分组/画布路径检查 | 大屏图形工具 |
| `imgUtils.ts` | `imgUrlTrans`, `downloadCanvas`, `download2AppTemplate`, `dataURLToBlob`, `findStaticSource` | 图片URL转换/下载导出 | 截图/导出相关 |
| `treeSortUtils.ts` | `treeSort`, `sortCircle`, `sortPer`, `treeParentWeight`, `weightCheckCircle` | 用户树排序 | 被 copilot、资源树使用 |
| `ModelUtil.ts` | `isDesktop()` | 判断是否为桌面客户端 | 缓存 `app.desktop` 标记 |
| `logout.ts` | `logoutHandler(justClean?)` | 登出处理（清理 store + 路由跳转） | 支持 OIDC/CAS 登出 |
| `loading.ts` | `tryShowLoading(id)`, `tryHideLoading(id)` | 全屏 Loading 控制 | 配合 axios loading 配置 |
| `toast.ts` | `toast(message)` | 错误提示快捷方法 | 封装 `ElMessage.error` |
| `eventBus.ts` | mitt 实例 | 事件总线 | `core/core-frontend/src/utils/eventBus.ts` |
| `events.ts` | 事件常量 | 事件名称定义 | [Inference] 全局事件名常量 |
| `generateID.ts` | `generateID()` | UUID 生成 | 组件 ID 生成 |
| `propTypes.ts` | Props 类型 | Vue Props 类型工具 | [Inference] |
| `runAnimation.ts` | 动画运行 | 动画播放逻辑 | [Inference] |
| `sizeAdaptor.ts` | `customAttrTrans`, `customStyleTrans`, `componentScalePublic`, `recursionTransObj` | 尺寸适配（移动端/主题） | 与 canvasStyle 类似但侧重适配 |
| `ParseUrl.ts` | `parseUrl` | URL 解析 | re-export |
| `RemoteJs.ts` | `loadScript(url, jsId?)` | 动态加载 JS 脚本 | 用于钉钉 JSAPI 等场景 |
| `timeUitils.ts` | `getRange`, `getTimeBegin` | 时间范围工具 | 查询组件时间处理 |
| `viewUtils.ts` | `viewFieldTimeTrans(viewDataInfo, params)` | 视图字段时间转换 | [Inference] |
| `DeShortcutKey.ts` | `keycodes[]`, `listenGlobalKeyDown()`, `releaseAttachKey()` | 全局快捷键 | 编辑器快捷键支持 |
| `treeDraggble.ts` | `treeDraggble` | 可拖拽树 | [Inference] |
| `treeDraggbleChart.ts` | `treeDraggbleChart` | 图表可拖拽树 | [Inference] |
| `animationClassData.ts` | `animationClassData` | 动画类数据 | [Inference] |

### 2.2 config/ — axios 配置（4 files）

| 文件 | 关键内容 | 职责 |
|------|----------|------|
| `config/axios/service.ts` | `service`（axios 实例）, `PATH_URL`, `cancelRequestBatch`, `cancelMap` | HTTP 请求核心：拦截器、超时、请求取消、版本更新检测 |
| `config/axios/config.ts` | `config` 对象（`base_url`, `result_code`, `request_timeout`, `default_headers`） | 基础配置常量 |
| `config/axios/index.ts` | `request` 对象（`get/post/delete/put` 方法） | 封装 service，简化调用 |
| `config/axios/refresh.ts` | `configHandler(config)`, `isExpired()`, `delayExecute()` | Token 自动刷新机制 |

### 2.3 directive/ — 自定义指令（3 files）

| 文件 | 导出 | 职责 |
|------|------|------|
| `directive/index.ts` | `installDirective(app)` | 注册 `v-permission` 和 `v-click-outside` |
| `directive/Permission/index.ts` | `checkPermission(el, binding)` | 权限指令：无权限时移除元素 |
| `directive/ClickOutside/index.ts` | `vClickOutside` | 点击元素外部时触发回调 |

### 2.4 plugins/ — Vue 插件（3 files）

| 文件 | 关键内容 | 职责 |
|------|----------|------|
| `plugins/element-plus/index.ts` | `setupElementPlus(app)`, `setupElementPlusIcons(app)` | 注册 `ElLoading`、`ElScrollbar` 和所有 Element Plus 图标 |
| `plugins/vue-i18n/index.ts` | `setupI18n(app)`, `i18n` | 国际化初始化，支持远程 i18n 文件加载 |
| `plugins/vue-i18n/helper.ts` | `setHtmlPageLang(locale)` | HTML lang 属性设置 |

### 2.5 models/ — 类型定义（8 files）

| 文件 | 关键导出 | 职责 |
|------|----------|------|
| `models/tree/TreeNode.ts` | `interface BusiTreeNode`, `interface BusiTreeRequest` | 业务树节点通用类型定义 |
| `models/chart/chart.d.ts` | `interface Chart` | 图表对象类型定义（218 行） |
| `models/chart/chart-attr.d.ts` | `interface ChartAttr` | 图表属性类型定义（1384 行，最大的类型文件） |
| `models/chart/chart-style.d.ts` | `interface ChartStyle` | 图表样式类型定义（328 行） |
| `models/chart/chart-senior.d.ts` | 高级设置类型 | 图表高级配置接口（275 行） |
| `models/chart/chart-plugin.d.ts` | `interface ChartPlugin` | 图表插件接口 |
| `models/chart/editor.d.ts` | `type EditorProperty` | 编辑器属性联合类型 |
| `models/chart/map.d.ts` | `interface AreaNode` | 地图区域节点接口 |

## 3. 核心工具详解

### 3.1 encryption.ts — 加密模块

**文件**：`utils/encryption.ts`

| 函数 | 签名 | 流程 | 使用场景 |
|------|------|------|----------|
| `rsaEncryp` | `(word: string) => string` | ① 从缓存取 `dekey` → ② 按 separator 拆分 → ③ AES 解密 k1 得 RSA 公钥 pk → ④ RSA 加密 word | 登录时加密用户名/密码 |
| `symmetricDecrypt` | `(data: string, keyStr: string) => string` | Base64 解码 keyStr → AES-CBC 解密 data（iv=`0000000000000000`） | [Inference] 对称解密（数据集密码等） |

**依赖**:
- `crypto-js`: AES-CBC + PKCS7 加解密
- `jsencrypt`: RSA 加密
- `js-base64`: Base64 编解码

**安全流程** (`views/login/index.vue:82-86`):
```
1. queryDekey() → 服务端返回加密后的 RSA 公钥
2. rsaEncryp():
   a. Base64 解码分隔符 "-pk_separator-" 加 "=" 结尾
   b. 按分隔符拆分 dekey → k1(密文RSA公钥), k2(AES密钥)
   c. aesDecrypt(k1, k2) → 明文 RSA 公钥
   d. JSEncrypt.encrypt(word) → 加密后的用户名/密码
3. loginApi({ name: encryptedName, pwd: encryptedPwd })
```

### 3.2 validate.ts — 校验模块

**文件**：`utils/validate.ts`

| 导出 | 类型 | 说明 |
|------|------|------|
| `isExternal(path)` | 函数 | 判断路径是否外部链接（`http(s):` / `mailto:` / `tel:` / `/api/pluginCommon/staticInfo`） |
| `validUsername(str)` | 函数 | 检查用户名是否为 `admin` 或 `cyw`（仅用于特定校验场景） |
| `PHONE_REGEX` | 常量 | 手机号正则 `^1[3\|4\|5\|7\|8][0-9]{9}$` |
| `EMAIL_REGEX` | 常量 | 邮箱正则 |

**使用场景**:
- `isExternal` 被 `Menu.vue:32` 和 `Header.vue:69` 使用，判断菜单项是内部路由还是外部链接
- `PHONE_REGEX`/`EMAIL_REGEX` 用于 System Settings、User Management 中的表单校验

### 3.3 CrossPermission.ts — 跨权限检查

**文件**：`utils/CrossPermission.ts`

| 函数 | 签名 | 说明 |
|------|------|------|
| `check` | `(data, id?: string, weight?: number) => boolean` | 检查是否具有资源（ID）的访问权限（weight 级别） |
| `compareStorage` | `(oldVal?: string, newVal?: string) => boolean` | 比较缓存版本（功能未完成，被注释） |

**`check` 函数流程**:
1. 检查 weight 参数（默认 1）
2. 从 data 对象中 `getNode(data, id)` 获取节点权限值
3. 若 `node < weight`：弹出 `ElMessageBox.confirm` 提示无权访问，确认后 `window.close()`
4. 使用全局变量 `window['cross-panel-' + id]` 防止重复弹窗
5. 通过时关闭已有的确认框

**使用场景**: 编辑仪表板/大屏时检查用户对该资源的访问权限。

### 3.4 check.ts — 数组重复检查

**文件**：`utils/check.ts`

```typescript
export default function checkArrayRepeat(arrayData, key) {
  // O(n^2) 双重循环检查数组中是否存在 key 属性值重复的元素
}
```

**使用**：仪表板保存前检查组件 ID 是否重复。

### 3.5 CanvasInfoTransUtils.ts — 画布信息转换

**文件**：`utils/CanvasInfoTransUtils.ts`

```typescript
export default function defaultConditionTrans(canvasInfo) {
  // 1. 解析 componentData JSON 获取所有 VQuery 组件
  // 2. 提取所有查询条件 filterItem → allFilter[]
  // 3. 构建 componentMap（filterId → component 映射）
  // 4. 若有 reportFilterInfo，替换默认过滤条件
  // 5. 返回 { sourceFilter, defaultFilter, sourceDefaultFilter, componentMap }
}
```

**核心逻辑**:
- 遍历画布所有组件，找到 `component === 'VQuery'` 的组件
- 收集所有 `propValue` 中的过滤条件
- 如果存在保存的 `reportFilterInfo`，用保存值替换默认值
- 返回三个版本的过滤条件数组和一个组件映射表

### 3.6 axios 拦截器（service.ts / refresh.ts）

**Token 自动刷新** (`config/axios/refresh.ts:47-92`):
```typescript
export const configHandler = config => {
  // 1. 桌面端/链接公开访问 直接放行
  // 2. 添加 X-DE-TOKEN 请求头
  // 3. 检查 token 是否过期（90秒过期阈值）
  // 4. 过期时调用 refreshApi 刷新
  // 5. 将并发请求缓存到 requestStore，刷新后统一重发
}
```

**关键响应处理** (`config/axios/service.ts`):
- `result_code = 0` 或 `50002` → 正常返回
- `80001` → 强制重新登录
- `DE-GATEWAY-FLAG` 响应头 → 清理缓存跳转登录页
- `DE-FORBIDDEN-FLAG` 响应头 → 提示权限变更
- `x-de-execute-version` 响应头 → 检测系统升级

## 4. 配置/指令/插件/模型

### 4.1 axios 配置（config/）

`service.ts` 是整个应用的 **HTTP 请求核心**，处理以下职责：

1. **实例创建** (`service.ts:77-83`): 通过 `getTimeOut()` 同步请求 `/sysParameter/requestTimeOut` 获取超时配置
2. **请求拦截器** (`service.ts:95-149`): Token 添加、语言 Headers、GET 参数编码、请求取消、Loading 触发
3. **响应拦截器** (`service.ts:152-262`):
   - 文件流直接返回
   - `code === 0` 或 `50002` 返回 `response.data`
   - 静态文件（地图/插件/i18n）直接返回
   - 其他 code 显示错误消息
4. **版本更新检测** (`service.ts:285-298`): 响应头 `x-de-execute-version` 变化时提示刷新
5. **请求取消** (`service.ts:300-317`): 支持按 URL 批量取消请求

### 4.2 Vue 自定义指令（directive/）

**`v-permission`** (`directive/Permission/index.ts`):
- 从 `interactiveStore` 获取用户权限数据
- 检查元素 `binding.value` 数组中每个权限的 `menuAuth && anyManage`
- 缺少任一权限时，直接从 DOM 移除元素（`el.parentNode.removeChild(el)`）
- 使用方式：`v-permission="['panel']"`

**`v-click-outside`** (`directive/ClickOutside/index.ts`):
- 标准点击外部检测指令
- `beforeMount` 时绑定 `document.click` 事件
- `unmounted` 时解绑事件

### 4.3 Vue 插件（plugins/）

**Element Plus 插件** (`plugins/element-plus/index.ts`):
- `setupElementPlus`: 注册 `ElLoading` 插件 + `ElScrollbar` 全局组件
- `setupElementPlusIcons`: 遍历 `@element-plus/icons-vue` 全部注册为全局组件
- 使用自定义 element-plus 分支 `element-plus-secondary`

**i18n 插件** (`plugins/vue-i18n/index.ts`):
- `setupI18n`: 创建 vue-i18n 实例并挂载到 app
- `createI18nOptions`: 根据 `localeStore.getCurrentLocale.lang` 动态加载对应语言包
- 支持远程 i18n：若 `cMap['custom']` 为 true，通过 `loadRemoteI18n` 加载动态 i18n 文件
- 从 `legacy: false`（Composition API 模式）

### 4.4 类型定义（models/）

**`models/tree/TreeNode.ts`** — 最广泛使用的类型：
```typescript
interface BusiTreeNode {
  id: string | number
  pid: string | number
  name: string
  leaf?: boolean
  weight: number
  ext?: number
  extraFlag: number
  extraFlag1: number
  children?: BusiTreeNode[]
}

interface BusiTreeRequest {
  busiFlag?: string
  leaf?: boolean
  weight?: number
  sortType?: string
  resourceTable?: string
}
```

**`models/chart/**`** — 图表系统完整类型定义（7 个 .d.ts 文件，共 2364 行）：
- `chart.d.ts`: 图表核心对象（id, title, type, data 等）
- `chart-attr.d.ts`: 图表属性配置（1384 行，最大的类型文件）
- `chart-style.d.ts`: 图表样式配置（颜色、字体、边距等）
- `chart-senior.d.ts`: 高级配置（联动、钻取、跳转等）
- `chart-plugin.d.ts`: 插件标记接口
- `editor.d.ts`: 编辑器属性联合类型
- `map.d.ts`: 地图区域节点类型

## 5. 风险与待确认

| 编号 | 问题 | 状态 |
|------|------|------|
| UB-1 | `CrossPermission.compareStorage` 函数体内部被注释（`/* unfinished please do not delete */`），实际只做了 `===` 比较 | [Need Verification] |
| UB-2 | `validate.validUsername` 仅检查 `['admin', 'cyw']`，用途不明确 | [Need Verification] |
| UB-3 | `encryption.ts` 中 `aesDecrypt` 的 IV 固定为 `0000000000000000`，AES 加密使用 `CryptoJS.enc.Utf8.parse` 且无需 IV 传递 — 安全性可能依赖服务端不传 IV 的设计 | [Need Verification] |
| UB-4 | `eventBus.ts` 和 `events.ts` 的具体内容未深读，需确认事件类型和发布订阅模式 | [Need Verification] |
| UB-5 | `canvasStyle.ts` 和 `style.ts` 有多个同名函数（如 `getStyle`、`getComponentRotatedStyle`），存在代码重复 | [Need Verification] |
| UB-6 | `graphics/` 和 `custom-component/` 目录未纳入分析范围，可能存在更多大屏/图形相关工具 | [Need Verification] |
| UB-7 | `treeDraggble.ts` 和 `treeDraggbleChart.ts` 使用 `export {}` 语法而非 `export default`，需确认是否为 mixin 或模块 | [Need Verification] |
| UB-8 | `DeShortcutKey.ts` 中 `keycodes` 包含 21 个按键（退格、方向键、B/C/D/E/G/L/P/S/U/V/X/Y/Z），未完全确认各按键的绑定功能 | [Need Verification] |
| UB-9 | `sizeAdaptor.ts` 中 `recursionTransObj`、`recursionThemTransObj` 等函数与 `canvasStyle.ts` 中的同名函数职责差异不清 | [Need Verification] |

## 6. 相关文档

| 文档 | 说明 |
|------|------|
| [infrastructure.md](infrastructure.md) | 基础设施分析（应用初始化、路由、store、hooks） |
| [auth-router.md](auth-router.md) | 路由守卫与认证流程 |
| [api-request.md](api-request.md) | API 请求封装与拦截器 |
| [misc-views.md](misc-views.md) | 应用框架与辅助视图分析（layout/login/copilot 等） |
| [de-viz.md](de-viz.md) | 可视化编辑引擎分析（canvasStyle/canvasUtils/style/translate 等的消费方） |
