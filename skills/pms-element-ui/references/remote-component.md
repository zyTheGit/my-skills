# 远程组件接入

> qiankun 微前端架构下的 UMD 远程组件打包与加载

---

## 核心特性

- UMD 格式打包
- manifest.json 清单
- 宿主动态加载

---

## 目录结构

```text
remote-components/
  build.js      # 通用构建脚本
  config.js     # 远程组件配置清单

src/remote-components/
  enterprise-approval.js
```

---

## 新增远程组件步骤

### 1. 创建入口文件

```js
import EnterpriseApproval from '@/views/list-of-enterprise-applications/approval.vue'

EnterpriseApproval.install = function install(Vue) {
  Vue.component(EnterpriseApproval.name || 'EnterpriseApproval', EnterpriseApproval)
}

export { EnterpriseApproval }
export default EnterpriseApproval
```

### 2. 增加组件配置

```js
module.exports = [
  {
    name: 'enterprise-approval',
    componentName: 'EnterpriseApproval',
    globalName: 'EnterpriseApprovalRemote',
    entry: 'src/remote-components/enterprise-approval.js',
  }
]
```

---

## 配置字段说明

| 字段 | 说明 |
|------|------|
| `name` | 远程组件目录名，必须唯一 |
| `componentName` | 宿主系统注册和渲染的组件名 |
| `globalName` | UMD 全局变量名，必须唯一 |
| `entry` | 远程组件入口文件，相对项目根目录 |

---

## 构建命令

| 命令 | 作用 |
|------|------|
| `npm run build:remote` | 构建所有远程组件 |
| `npm run build:remote -- enterprise-approval` | 只构建指定组件 |
| `npm run build:dev:with-remotes` | 先构建子应用，再输出远程组件 |

---

## 构建输出

```text
dist-dev/
  remote-components/
    enterprise-approval/
      manifest.json
      EnterpriseApprovalRemote.umd.min.js
      EnterpriseApprovalRemote.css
```

---

## 宿主依赖检查

远程构建默认启用 `VUE_APP_CDN_MODE=true`，以下依赖需宿主提供全局变量：

| 依赖 | 全局变量 |
|------|----------|
| `vue` | `Vue` |
| `vue-router` | `VueRouter` |
| `vuex` | `Vuex` |
| `@custom/element-ui` | `ELEMENT` |
| `@custom/pms-request` | `PmsRequest` |

---

## 常见问题排查

| 现象 | 优先检查 |
|------|----------|
| 待办点击后没有进入远程组件页 | `pcUrl` 是否带 `remoteComponent=1` |
| manifest 404 | `REMOTE_COMPONENT_OUTPUT_DIR` 是否指向当前部署目录 |
| 组件加载后没有渲染 | `globalName` 是否和构建出的 UMD 全局变量一致 |
| 样式丢失 | manifest 是否包含 `payload.styles` |
| 本地地址失败、线上同源正常 | 本地静态服务是否开启 CORS |

---

## 注意事项

- 远程组件构建和正常 qiankun 子应用构建可以共存
- manifest 地址必须是 `http:` 或 `https:`
- 资源路径必须包含 `/remote-components/`
- 每个脚本和样式都必须声明 `sha256`