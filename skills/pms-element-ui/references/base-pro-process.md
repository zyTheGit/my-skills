# BaseProProcess 流程查看

**功能说明**：展示流程节点状态、待办人员、操作记录、审批意见，支持分支切换（网关分支）、催办（默认接口或自定义）、自动拉取流程日志（基于 inst-id）、子流程节点、会签/或签、抽屉模式。

## 基础用法

```vue
<el-base-pro-process
  title="项目立项审批流程"
  :show-urge-button="true"
  :inst-id="instId"
  :default-data="processList"
  :urge-handler="handleUrge"
  @urge="onUrge"
  @branch-change="handleBranchChange"
/>
```

## 接口模式（自动请求）

不传 `default-data`（或传空数组）且提供 `inst-id` 时，组件自动请求：

- 审批日志：`POST /{serviceCode}/processLogs`，参数 `{ instId }`
- 子流程日志（点击"查看子流程"懒加载）：`POST /{serviceCode}/processLogs/subProcess`，参数 `{ instId, nodeId, executionId }`（未开始卡片 executionId 为空）
- 催办（默认）：`POST /base-task/workItem/expedite`，参数 `{ instId }`

`serviceCode` 取自路由：`$route.params.serviceCode` 或 `$route.query.serviceCode` 或 `service-code`（props）。路由无 serviceCode 时自动请求会失败，改用 `default-data` 直接渲染。

## 节点状态（nodeStatus）

| 状态值 | 含义 | 显示效果 |
|--------|------|----------|
| completed | 已完成 | 通过图标 |
| running | 进行中 | 待处理图标，可催办 |
| rejected | 退回/驳回 | 退回图标，连线高亮 |
| notReached | 未到达 | 空心圆/分支图标 |

## 展示规则要点

1. running/notReached 节点优先展示 assignees；其他状态展示 handleUserName + handlePostName
2. 网关分支只按 `executed` 判断：仅 `executed=true` 展示，false/缺省隐藏
3. 经 executed 过滤后只剩一条可见分支时，不显示切换按钮直接展开
4. 存在 running 节点时，隐藏其之前/之外的 notReached 节点（保留真实链上 completed/rejected）
5. 全部 completed 时不展示纯 notReached 节点
6. 操作记录按 `actions[].group` 分组；未返回 group 按单组处理；每组只显示最后一个非空 opinion
7. **会签**：`multiInstanceType` 非空且有 `participants` 时，按参与人逐个展示独立操作记录，默认显示第一个，支持展开全部/收起
8. **或签**：待处理节点 assignees 多于 1 人时按岗位分组展示候选人，姓名最多两行超出悬浮查看，分组超 3 个支持展开/收起
9. **子流程**：`nodeType=subProcess` 时按 `subProcesses` 执行卡片展示，点击"查看子流程"懒加载内部时间线并覆盖主流程，"返回主流程"恢复

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| title | 流程标题 | string | '' |
| inst-id | 流程实例 ID（用于自动请求） | string | '' |
| service-code | 服务前缀 | string | '' |
| default-data | 流程数据 | array | [] |
| show-urge-button | 是否显示催办按钮 | boolean | false |
| status-images | 状态图标配置（pending/rejected/approved/branch） | object | 内置默认 |
| urge-handler | 自定义催办函数 (requestData, node, vm) | function | null |
| logs-handler | 自定义审批日志获取函数 (requestData, vm)，可直接返回节点数组或接口响应；缺省时请求 `log-url` 或 `/{serviceCode}/processLogs` | function | null |
| sub-process-handler | 自定义子流程日志获取函数 (requestData, card, vm)，可直接返回节点数组或接口响应；缺省时请求 `sub-process-url` 或 `{审批日志地址}/subProcess` | function | null |
| log-url | 自定义审批日志接口地址，优先级低于 `logs-handler`、高于 `service-code` 拼接 | string | '' |
| sub-process-url | 自定义子流程日志接口地址，优先级低于 `sub-process-handler`；缺省时在审批日志地址后拼 `/subProcess` | string | '' |
| drawer | 是否以抽屉方式展示审批日志 | boolean | false |
| visible | 抽屉显示状态，.sync / v-model | boolean | false |
| drawer-title | 抽屉标题，未传回退到 title / 审批日志 | string | '' |
| drawer-props | 透传给 el-drawer 的配置 | object | {} |
| size | 抽屉宽度/尺寸 | string | 500px |
| direction | 抽屉方向 | string | rtl |
| show-trigger | 抽屉模式是否显示默认触发按钮 | boolean | true |
| trigger-text | 默认触发按钮文案 | string | 查看审批日志 |
| trigger-type | 默认触发按钮类型 | string | text |
| auto-load-logs | 是否自动调用审批日志接口 | boolean | true |

## Events

| 事件名 | 说明 | 参数 |
|-------|------|------|
| urge | 点击催办后触发（默认/自定义均触发） | ({ instId, node, success }) |
| branch-change | 分支切换 | ({ node, branch, branchIndex }) |
| sub-process-open | 查看子流程加载成功并切换后 | ({ card, node, data }) |
| sub-process-back | 返回主流程后 | ({ card }) |
| update:visible | 抽屉显示状态变化 | (visible) |
| input | 抽屉显示状态变化（v-model 兼容） | (visible) |
| open / opened / close / closed | 抽屉打开/关闭动画各阶段 | - |

## Methods

| 方法名 | 说明 | 参数 |
|-------|------|------|
| refresh | 重新获取流程数据（接口模式） | - |
| getDataList | 手动触发重新拉取流程数据 | - |
| setData | 手动设置流程数据 | (data: Array) |
| openDrawer / closeDrawer | 打开/关闭审批日志抽屉（drawer=true 时） | - |

## Slots

| 插槽名 | 说明 | 作用域 |
|-------|------|--------|
| trigger | 自定义抽屉触发器（仅 drawer=true） | { open, close, visible } |
| drawer-title | 自定义抽屉标题 | - |

## 数据结构

**节点（default-data 项）**：`instId`、`nodeId`、`nodeName`、`nodeType`（userTask/gateway/subProcess）、`multiInstanceType`（会签类型）、`nodeStatus`、`handleTime`、`handleUserName`、`handleOrgName`、`handlePostName`、`actions`、`assignees`、`participants`（会签参与人）、`opinion`、`branches`、`subProcesses`（子流程卡片）

**操作记录 actions 项**：`actionName`、`actionLabel`、`actionTime`、`statusType`（completed/pending/rejected）、`group`（分组号）、`opinion`

**候选人 assignees 项**：`userId`、`userName`、`deptName`、`postName`

**会签参与人 participants 项**：`handleUserName`、`handleOrgName`、`handlePostName`、`status`、`actions`

**分支 branches 项**：`branchName`、`executed`（仅 true 时展示）、`nodes`（同顶层节点）

**子流程卡片 subProcesses 项**：`instId`、`nodeId`、`nodeName`、`status`（running/notStarted/completed）、`startTime`、`endTime`、`currentNodeName`、`approvalResult`、`executionId`（查看子流程接口入参，未开始为空）

## 注意事项

- 路由无 serviceCode 时自动请求会失败，改用 `default-data` 直接渲染
- 子流程节点未下发 nodeStatus 时按执行卡片推断（有进行中->running，否则有已完成->completed，否则全部未开始->notReached）
- 催办处理函数支持返回 boolean / { data: boolean } / { success: boolean }
- 审批意见长文本被两行截断后可通过 Tooltip 查看完整内容

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-pro-process.md`
