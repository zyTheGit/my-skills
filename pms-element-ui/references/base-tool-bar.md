# BaseToolBar 工具栏

## 核心特性

- 从 `BaseProTable` 中提取的独立工具栏组件
- 支持刷新、密度切换、列设置、全屏切换
- 可独立嵌入业务列表头部、卡片区右上角

## 基础用法

```vue
<el-base-tool-bar
  :show-refresh="true"
  :show-density="true"
  :show-fullscreen="true"
  :show-column-setting="false"
  :density="density"
  @refresh="handleRefresh"
  @density-change="handleDensityChange"
/>
```

## 列设置功能

```vue
<el-base-tool-bar
  :show-column-setting="true"
  :columns="columns"
  :column-state="columnState"
  @column-setting-confirm="handleColumnSettingConfirm"
/>
```

## 与列表头部组合使用

```vue
<div style="display: flex; align-items: center; justify-content: space-between;">
  <div>
    <div style="font-size: 16px; font-weight: 500;">项目列表</div>
  </div>
  <el-base-tool-bar :show-column-setting="false" @refresh="refreshTable" />
</div>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|-----|------|------|--------|--------|
| showRefresh | 是否显示刷新按钮 | boolean | — | true |
| showDensity | 是否显示密度切换 | boolean | — | true |
| showColumnSetting | 是否显示列设置 | boolean | — | true |
| showFullscreen | 是否显示全屏切换 | boolean | — | true |
| density | 当前表格密度 | string | default / medium / small / mini | default |
| isFullscreen | 当前是否全屏 | boolean | — | false |
| columns | 列设置使用的列配置 | array | — | [] |
| columnState | 列设置使用的列状态 | object | — | {} |

## Events

| 事件名 | 说明 | 回调参数 |
|-------|------|---------|
| refresh | 点击刷新按钮时触发 | — |
| density-change | 切换密度时触发 | density: string |
| fullscreen-toggle | 点击全屏切换时触发 | — |
| column-setting-confirm | 列设置确认时触发 | { state, config } |
