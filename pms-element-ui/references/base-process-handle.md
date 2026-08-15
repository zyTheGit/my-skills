# BaseProcessHandle 流程处理页

**功能说明**：搭建标准"三栏流程处理页面"--左侧流程日志（内置 el-base-pro-process）、中间业务内容预览（插槽）、右侧审批表单（内置 el-base-pro-form，支持接口联动）。

## 重要说明

- **待办跳转**：通用-待办中心-应用配置，pc 路径示例 `/message-web/test?taskId=[taskId]&businessCode=[businessCode]&instId=[instId]`；详情路径配置 `type=detail` 会自动隐藏底部按钮栏并设置右侧表单禁用
- **提交待办**：自定义提交按钮成功后需调用 `window.$eventBus.emit('todo:refresh')` 刷新待办数量；非通用待办列表跳转需传 `isInitiator=1`（我的待办显示"催一下"）
- **判断我的待办**：待办返回的 `accountId` 与缓存用户信息 `mainAccountId` 对比，相同即为我的待办
- **远程组件接入**：中间内容区可由业务子应用以远程组件方式提供，在 `pcUrl` 配置 `manifest.json` 地址，通过消息中心跳转到 `/message-web/process-handle` 加载

## 默认接口行为（新）

组件内置 6 个接口（调用一般需 `instId`、`serviceCode`、`taskId`）：

1. 正向节点及候选人：`POST /{serviceCode}/assignee/getForwardNodeAssignee`，参数 `{ taskId }`
2. 反向节点及历史处理人：`POST /{serviceCode}/assignee/getBackwardNodeAssignee`，参数 `{ taskId }`
3. 查看态右侧表单回显（`disabled=true` 且 `auto-load-right-form=true`）：`POST /{serviceCode}/log/info`，参数 `{ taskId, instId }`
4. 提交审批：`POST /{serviceCode}/task/approval`
5. 提交按钮是否显示（`disabled=false` 时调用）：`POST /{serviceCode}/task/btnPermission`
6. 流程关闭（仅发起人办理页）：`POST /{serviceCode}/process/stop`，参数 `{ taskId }`

`serviceCode` / `taskId` 优先级：`$route.params` > `$route.query` > 对应 props（`service-code` / `task-id`）

## 默认右侧表单字段

| 标题 | dataIndex | 说明 |
|------|-----------|------|
| 审批 | `actionName` | 默认 `agree`，可选 `agree/oppose` |
| 意见 | `opinion` | 审批意见 |
| 附件 | `attachmentOpinions` | 上传后转为 `{ fileId, fileName }[]` |
| 流程节点 | `targetNodeId` | 节点下拉 |
| 审核人 | `assignees` | 审批人下拉（默认多选） |

## 基础用法

```vue
<el-base-process-handle
  ref="processHandle"
  content="项目立项流程办理"
  :approval-submit-data="{ businessCode: 'BIZ_001' }"
  :footer-bleed="24"
  :left-width="360"
  :right-form-column-merges="rightFormColumnMerges"
  @submit="onSubmit"
  @cancel="onCancel"
>
  <template slot="content-center">业务正文/审批详情</template>
</el-base-process-handle>
```

## Attributes

### 布局相关

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| content | 页头内容（传给 el-page-header） | string | '' |
| show-back / show-left / show-center / show-right / show-footer | 各区域是否显示 | boolean | true |
| disabled | 是否禁用右侧表单（查看态） | boolean | false |
| footer-bleed | 底部按钮栏向两侧外扩（px） | number | 0 |
| footer-bleed-bottom | 底部按钮栏向下外扩（px） | number | 0 |

### 左侧流程相关

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| inst-id | 流程实例 ID | string | '' |
| process-default-data | 左侧流程默认数据 | array | [] |
| process-show-urge-button | 是否显示催办按钮（需配合 isInitiator） | boolean | false |
| manual-control-urge-button | 手动控制催办按钮显隐（须 true 才显示） | boolean | true |
| process-status-images | 自定义流程状态图标 | object | null |
| process-urge-handler | 自定义催办处理函数 | function | null |
| auto-load-logs | 是否自动调用审批日志接口 | boolean | true |

### 右侧表单相关

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| right-form-mode | 表单模式 | string | edit |
| right-form-columns | 右侧表单列定义（完整覆盖默认列） | array | null |
| right-form-column-merges | 在默认/传入列基础上增删改插 | array/function | null |
| right-form-initial-values | 右侧表单初始值 | object | null |
| right-form-values | 外部传入表单值（常用于查看态） | object | null |
| right-form-props | 透传给 el-base-pro-form 的额外参数 | object | {} |
| right-import-props / right-import-listeners | 附件上传组件参数/事件 | object | {} |
| right-import-button-text | 附件上传按钮文案 | string | 上传文件 |
| right-attachment-tip | 附件提示文案（不传时自动拼接） | string | '' |

### 流程审批接口相关

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| task-id / service-code | 任务 ID / 服务编码（路由 params > query > props） | string | '' |
| is-initiator | 是否流程发起人，`y`/`1` 时允许显示流程关闭按钮 | string | '' |
| show-process-stop-button | 是否允许显示流程关闭按钮 | boolean | true |
| auto-load-right-form | disabled=true 时是否自动加载右侧表单 | boolean | true |
| auto-load-btn-permission | 是否自动调用按钮权限接口 | boolean | true |
| auto-load-task-nodes | 是否自动加载流程节点（仅 disabled=false） | boolean | true |
| right-form-request-url / -handler / -method | 查看态右侧表单接口路径 / 自定义请求方法 | string/function | /log/info |
| forward-task-node-request-url | 通过时节点接口路径 | string | /assignee/getForwardNodeAssignee |
| backward-task-node-request-url | 不通过时节点接口路径 | string | /assignee/getBackwardNodeAssignee |
| approval-submit-url / -handler / submit-request-method | 提交接口路径 / 自定义请求方法 | string/function | /task/approval |
| approval-submit-data | 提交接口额外参数（并入请求体） | object | {} |
| submit-options | 提交额外配置，如 `{crypto:{sm4:{fields:['xxx']}}}` | object | - |
| next-node-request-handler / -method | 自定义节点请求方法 | function | null |
| next-node-field / assignee-field / approval-field / opinion-field / attachment-field | 各字段名 | string | targetNodeId / assignees / actionName / opinion / attachmentOpinions |

## right-form-column-merges 合并规则

支持传 `Array` 或 `Function: (baseColumns, vm) => merges`，按顺序依次执行，前一条结果作为后一条输入。

| action | 说明 |
|--------|------|
| upsert（默认） | 存在则浅合并（字段对象+form），不存在则追加 |
| add | 直接追加新字段到末尾 |
| remove | 按 dataIndex 删除字段 |
| replace | 按 dataIndex 整列替换；找不到默认追加（`insertIfMissing:false` 关闭） |
| insertBefore / insertAfter | 插入到目标字段前/后；找不到则追加到末尾 |

## Slots

| 插槽名 | 说明 |
|-------|------|
| header-title / header-extra | 自定义页头内容 / 页头扩展 |
| title-left / content-left | 左栏标题（默认：审查日志）/ 内容（默认 el-base-pro-process） |
| title-center / content-center | 中栏标题（默认：内容预览）/ 内容 |
| title-right / content-right | 右栏标题（默认：信息填写）/ 内容（默认 el-base-pro-form） |
| rightAttachmentTip / footer | 右侧附件说明区域 / 底部按钮栏（默认：取消/提交） |
| form-${field} | 右侧表单字段插槽，如 form-actionName、form-attachmentOpinions |

## Events

| 事件名 | 说明 | 参数 |
|-------|------|------|
| back | 点击页头返回 | - |
| right-form-change | 右侧表单字段变化 | (payload) |
| right-form-values-change | 右侧表单回显值变化 | ({ values, source }) |
| right-form-values-error | 右侧表单回显接口失败 | ({ requestData, error }) |
| process-urge / process-branch-change | 左侧流程催办 / 分支切换 | (payload) |
| task-nodes-change | 节点数据加载成功 | ({ actionName, taskNodeList, nodeOptions, assigneeList }) |
| task-nodes-error / assignee-options-error | 节点 / 审批人加载失败 | ({ error }) |
| assignee-options-change | 审批人选项变化 | ({ nodeId, assigneeList, options }) |
| submit | 提交成功 | ({ formModel, requestData, response, success }) |
| submit-error | 提交失败/异常 | ({ formModel, error, success:false }) |
| submit-invalid | 表单校验未通过 | ({ formModel, instId, taskId }) |
| cancel | 点击取消 | ({ formModel }) |
| submit-btn-show | 是否有权限提交 | (boolean) |
| process-and-form-change | 审批日志和右侧表单全部有值时 | { process, form } |

## Methods

| 方法名 | 说明 |
|-------|------|
| validateRightForm | 校验右侧表单 |
| getRightFormModel | 获取右侧表单模型 |
| setRightFormFieldsValue(values, options) | 设置右侧表单值 |
| refreshProcess / setProcessData(data) | 刷新 / 手动设置左侧流程数据 |
| refreshTaskNodes(options) / setTaskNodes(nodes, options) | 刷新 / 手动设置节点数据 |
| submit(extraPayload) / cancel(extraPayload) | 触发提交 / 取消（含校验+接口） |
| mergeFormItems(baseColumns, merges) | 合并表单项工具方法 |

## 注意事项

- `disabled=true`（查看态）不会调用 `loadTaskNodes`，流程节点/审核人以只读文本展示（支持 `name`、`handleUserName` 别名）
- 后端把真实字段放在 `data.formData` 时，组件会自动合并到顶层参与回显
- 附件回显字段名须与 `attachment-field` 一致且值为数组
- `actionName=agree` 加载正向节点；切到 `oppose` 自动改为反向节点；选节点后自动刷新审核人下拉
- 可通过 `forward/backward-task-node-request-url`、`next-node-request-handler/method` 覆盖默认请求

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-process-handle.md`
