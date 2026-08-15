# BasePageFooter 页面底部操作栏

**功能说明**：承载页面底部操作区，支持默认取消/确认按钮和自定义操作区，支持 static/fixed 两种布局模式。

## 基础用法

```vue
<el-page-form-footer @cancel="handleCancel" @confirm="handleConfirm" />
```

## 固定模式

```vue
<el-page-form-footer anchor=".app-main" mode="fixed" />
```

- `mode="fixed"` 时，组件根据锚点容器实时同步 `left` 和 `width`
- `anchor` 支持 HTMLElement、组件实例或选择器字符串

## 自定义操作区

```vue
<el-page-form-footer :loading="loading">
  <template slot-scope="scope">
    <el-button @click="scope.cancel">返回列表</el-button>
    <el-button type="primary" :loading="scope.loading" @click="scope.confirm">提交审批</el-button>
  </template>
</el-page-form-footer>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| show-cancel | 是否显示取消按钮 | boolean | — | true |
| show-confirm | 是否显示确认按钮 | boolean | — | true |
| cancel-text | 取消按钮文案 | string | — | 取消 |
| confirm-text | 确认按钮文案 | string | — | 确认 |
| confirm-type | 确认按钮类型 | string | primary/success/warning/danger | primary |
| anchor | 跟随的目标容器 | HTMLElement/VueComponent/string | — | null |
| full | 是否同步锚点宽度 | boolean | — | true |
| mode | 布局模式 | string | static/fixed | static |
| loading | 确认按钮加载状态 | boolean | — | false |
| disabled | 默认按钮禁用状态 | boolean | — | false |

## Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| cancel | 点击取消按钮时触发 | — |
| confirm | 点击确认按钮时触发 | — |

## Slots

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义底部操作区，作用域参数：loading、disabled、confirm、cancel |
