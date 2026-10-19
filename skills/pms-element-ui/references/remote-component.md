# 远程组件接入

> 消息中心统一流程处理页：业务端接入手册（`processHandle.schemaVersion: 1`）。

---

## 核心定位

业务子应用把现有审批页拆成「远程组件」，由消息中心的统一流程处理页负责外壳、布局、审批日志、公共审批表单和底部按钮。业务端只做 4 个决定：Center 内容、右侧表单、提交方式、字段联动/自定义按钮。

---

## 目录结构

```text
remote-components/
  build.js                      # 构建 + 签名 + 生成 manifest，不要改
  config.js                     # 远程组件清单，唯一需要编辑的配置
  process-config-builder.cjs    # 构建期辅助函数，与宿主逐字一致
  process-config-contract.cjs   # 协议版本常量，与宿主逐字一致

src/remote-components/
  project-audit.js              # 远程入口
src/views/project-audit/
  ProjectAuditCenter.vue        # 中间业务详情组件
```

> 签名私钥由环境变量 `REMOTE_COMPONENT_SIGN_PRIVATE_KEY` 注入，脚手架不含密钥文件。

---

## 新增远程组件步骤

### 1. config.js

```js
const { approvalPage } = require('./process-config-builder.cjs')

module.exports = [{
  name: 'project-audit',
  componentName: 'ProjectAuditCenter',
  globalName: 'ProjectAuditRemote',
  entry: 'src/remote-components/project-audit.js',
  processHandle: approvalPage({ title: '项目审批', center: 'ProjectAuditCenter' }),
}]
```

### 2. 入口

```js
import ProjectAuditCenter from '@/views/project-audit/ProjectAuditCenter.vue'
export { ProjectAuditCenter }
export default ProjectAuditCenter
```

### 3. vue.config.js

```js
configureWebpack: config => {
  const isRemoteComponentBuild = Boolean(process.env.VUE_APP_REMOTE_COMPONENT)
  if (isRemoteComponentBuild) {
    config.output = { ...config.output, globalObject: 'window' }
  } else {
    config.output = { ...config.output, library: 'businessWeb', libraryTarget: 'umd', globalObject: 'window' }
  }
}
```

### 4. package.json

```json
{
  "scripts": {
    "build:remote": "node remote-components/build.js",
    "build:dev:with-remotes": "npm run build:dev && npm run build:remote"
  }
}
```

### 5. 构建

```powershell
$env:REMOTE_COMPONENT_SIGN_PRIVATE_KEY = '<由 CI 或运维注入>'
$env:REMOTE_COMPONENT_OUTPUT_DIR = 'dist'  # 默认 dist-dev
npm run build:remote
```

产物：`dist/remote-components/project-audit/manifest.json`、`ProjectAuditRemote.umd.min.js`、`ProjectAuditRemote.css`。

---

## Center 组件

### Props

```js
props: {
  processContext: { type: Object, required: true }, // taskId, instId, businessCode, serviceCode, type, disabled, bizQuery
  active: { type: Boolean, default: true },
}
```

> 不要再读 `this.$route.query`；业务参数从 `bizQuery` 取。

### 公开方法

| 方法 | 说明 |
|------|------|
| `validate()` | 提交前校验，返回 `false` 中断提交 |
| `getData()` | 提交时读取区域数据 |
| `applyPatch(changes, meta)` | 接收另一侧字段同步 |

### 上报字段

```js
this.$emit('form-change', {
  changes: { 'project.name': detail.projectName, workOid: detail.workOid },
  source: 'business-load',
})
```

---

## 右侧表单

省略 `right` 时使用宿主公共审批表单。

```js
const { approvalPage, defaultForm } = require('./process-config-builder.cjs')

processHandle: approvalPage({
  center: 'ProjectAuditCenter',
  form: defaultForm({ hide: ['attachmentOpinions'] }),
})
```

自研右侧组件时：`right: 'WeekPlanAuditForm'`，并删除 `form`。

---

## 提交方式（四选一）

| 配置 | 执行方 | 场景 |
|------|--------|------|
| 省略 / `'approval'` | 统一页 | 业务数据已提前保存 |
| `businessSubmit(method)` | 适配器 | 一个业务接口同时保存并审批 |
| `saveThenApprove(method)` | 适配器 + 统一页 | 先保存业务，再公共审批 |
| `componentSubmit(region, method)` | Center / Right | 必须使用组件内部专有状态 |

---

## 底部按钮

默认三个标准按钮：流程关闭、取消、提交。

```js
const { approvalPage, customAction, standardActions } = require('./process-config-builder.cjs')

processHandle: approvalPage({
  center: 'ProjectAuditCenter',
  actions: standardActions({
    extra: [customAction('saveDraft', { label: '暂存', type: 'primary', plain: true, validate: 'none', afterSuccess: 'stay' })],
  }),
  advanced: { adapter: 'processHandleAdapter' },
})
```

适配器：`processHandleAdapter.actions.saveDraft(context)` 返回 `{ success, message, data }`。

---

## 待办路由

后端 `pcUrl`：

```text
/child/project-web/remote-components/project-audit/manifest.json?remoteComponent=1&id=1001
```

消息中心识别 `remoteComponent=1` 后跳转：

```text
/message-web/process-handle?remoteManifest=/child/project-web/remote-components/project-audit/manifest.json&id=1001
```

---

## 常见错误速查

| 现象 | 优先检查 |
|------|----------|
| 待办点击后没有进入远程组件页 | `pcUrl` 是否带 `remoteComponent=1` |
| manifest 404 | `REMOTE_COMPONENT_OUTPUT_DIR` 是否指向当前部署目录 |
| 组件加载后没有渲染 | `globalName` 是否和构建出的 UMD 全局变量一致 |
| 样式丢失 | manifest 是否包含 `payload.styles` |
| 本地地址失败、线上同源正常 | 本地静态服务是否开启 CORS |
| 构建提示缺少私钥 | `REMOTE_COMPONENT_SIGN_PRIVATE_KEY` 是否注入 |
| 验签失败 | manifest/JS/CSS 是否同批发布、宿主 pms-request 版本是否匹配 |

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\remote-component.md`
