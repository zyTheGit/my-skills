# Version Service 版本管理与对比

微前端架构下的构建版本标识与对比方案。核心原则：**谁构建谁打标**——构建时把 git 分支、commit、构建时间固化进产物，而不是事后在服务器补标记。

## 版本信息构成

构建产物根目录生成 `version.json`，同时向页面/运行时注入构建信息：

| 字段 | 说明 |
| --- | --- |
| `version` | 版本号。`release/1.0.13` 分支取 `1.0.13`；其他分支原样作为版本标识 |
| `branch` | 构建所在分支名 |
| `commit` | 构建 commit 短 hash（10 位） |
| `buildTime` | 构建时间（ISO 8601），每次构建都会变化 |
| `env` | 构建环境，对应 `VUE_APP_ENV`（dev / test / release / uat / production） |

## 主应用 vs 子应用注入方式

由于 qiankun 沙箱的存在，主、子应用的注入方式不同，接入子应用时必读：

| 应用 | 注入方式 | 说明 |
| --- | --- | --- |
| 主应用 | HTML 内联脚本挂 `window.__BUILD_INFO__` + `<meta name="app-version">` | 主应用 HTML 即页面主文档，内联脚本直接生效 |
| 子应用 | 编译期常量 `process.env.VUE_APP_BUILD_INFO`（DefinePlugin 注入） | 子应用 HTML 内联脚本在 qiankun 沙箱中写入 proxy window，主应用读不到，**只能**走编译期常量 |

两者数据源为同一次构建的 `readBuildInfo()`，内容一致。

## 确认线上版本的途径

| 途径 | 操作 | 适用场景 |
| --- | --- | --- |
| `version.json` | 访问 `/main/version.json` 或 `/child/<name>/version.json` | 运维/测试验证部署结果，无需登录 |
| 页面源码 | 查看主应用 HTML 的 `<meta name="app-version">`、`<meta name="app-commit">` | 快速目视确认 |
| 控制台 | 执行 `window.__BUILD_INFO__` 或 `window.$versionService.getRuntimeVersions()` | 开发排查，可看完整版本组合 |

## window.$versionService API

主应用启动时挂载为只读全局对象，主/子应用均可调用：

| 方法 | 说明 |
| --- | --- |
| `getCurrentBuildInfo()` | 获取当前页面运行的主应用构建版本，返回 `BuildInfo` 或 `null` |
| `fetchRemoteBuildInfo()` | 获取主应用线上部署的版本（fetch 产物根目录 `version.json`），失败抛错 |
| `compareBuildInfo(current, remote)` | 对比两份版本信息，内部归一化，返回 `BuildInfoComparison` |
| `checkRemoteUpdate()` | 主应用一键检测更新，返回 `{ current, remote, comparison }`，当前构建信息不可用时返回 `null` |
| `fetchAppBuildInfo(appName)` | 按 qiankun 注册名获取子应用线上部署的版本；清单未加载或名称未知时抛错 |
| `registerAppBuildInfo(info)` | 子应用 mount 时上报自己的构建版本，输入无效返回 `null` |
| `getRuntimeVersions()` | 返回当前页面实际运行的版本组合 `{ main, apps }` |

`getRuntimeVersions()` 的 `apps` key 为 qiankun 注册名，只包含当前页面已加载过的子应用。

## 版本对比语义

`compareBuildInfo` 以 **commit 为部署一致性判据**：同一 commit 即同一部署版本（`buildTime` 不参与一致性判定）。commit 短 hash 与全量 hash 按前缀匹配视为同一提交。

| status | 含义 |
| --- | --- |
| `same` | 同一 commit，当前页面运行的就是线上部署的那份 |
| `remote-newer` | commit 不同且线上更新（按 `buildTime` 判定），典型场景：发版后用户未刷新 |
| `local-newer` | 当前页面比线上新，常见于灰度、回滚 |
| `different` | 有差异但无法判定先后（`buildTime` 缺失或相同） |
| `unknown` | 输入无效（version 与 commit 全缺失等） |

版本对比以应用为单位，主应用和各子应用各自对比"运行中 vs 线上"，互不干扰。

## 典型用法

**子应用检测自身是否有新部署：**

```javascript
async function checkSelfUpdate() {
  const current = JSON.parse(process.env.VUE_APP_BUILD_INFO)
  const remote = await window.$versionService.fetchAppBuildInfo('newUpmsWeb')
  const comparison = window.$versionService.compareBuildInfo(current, remote)

  if (comparison.status === 'remote-newer') {
    // 提示用户刷新页面
  }
}
```

**主应用检测更新：**

```javascript
const result = await window.$versionService.checkRemoteUpdate()
if (result.comparison.status === 'remote-newer') {
  // 提示用户刷新页面
}
```

**排查运行时版本组合：**

```javascript
const versions = window.$versionService.getRuntimeVersions()
console.table(versions.apps)
```

## 子应用接入要点

1. **`vue.config.js` 构建时采集并注入**
   - 通过 `readBuildInfo()` 采集分支、commit、构建时间、环境
   - 生成 `version.json` 到产物根目录
   - 子应用统一用 `process.env.VUE_APP_BUILD_INFO` 注入，不走 HTML 内联脚本

2. **`src/main.js` mount 时上报**
   - 从 `props.name` 取 qiankun 注册名，避免硬编码
   - 调用 `window.$versionService.registerAppBuildInfo({ appName, ...buildInfo })`
   - 独立运行或版本服务不可用时静默跳过

## 注意事项

1. **nginx 缓存**：`index.html` 与 `version.json` 必须配置 `Cache-Control: no-cache`，否则验证部署会失真。
2. **CI 构建**：detached HEAD 时 git 命令拿不到分支名，兜底链为 `VUE_APP_RELEASE_BRANCH` > `GIT_BRANCH` > git 命令。release 分支构建建议显式传 `VUE_APP_RELEASE_BRANCH`。
3. **构建产物混淆与 `drop_console` 不影响版本信息**：主应用在 HTML 内联脚本，子应用是 DefinePlugin 编译期常量。
4. **`fetchAppBuildInfo` 依赖登录后的子应用清单**，清单未加载时调用会抛错，由调用方处理。
5. **dev 环境跨端口**：子应用 devServer 需配置 `Access-Control-Allow-Origin: *`，主应用 dev 环境下 `fetchAppBuildInfo` 才能跨端口取到 `version.json`。
6. **安全权衡**：`version.json` 会公开 commit hash 和分支名，内网系统通常可接受；如有顾虑可精简为只保留 `version` + `buildTime`。

> 源文档：examples/docs/zh-CN/version-service.md
