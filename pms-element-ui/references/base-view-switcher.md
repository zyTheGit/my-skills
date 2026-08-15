# BaseViewSwitcher 视图切换

## 核心特性

- 支持 card/table 两种视图模式切换
- 适用于列表页展示方式切换场景
- 与 BaseProTable 配合使用

## 基础用法

```vue
<el-view-switcher v-model="viewMode" />
```

## 与表格组合使用

```vue
<div>
  <el-view-switcher v-model="viewMode" />
  <el-base-pro-table v-if="viewMode === 'table'" :columns="columns" :request="fetchData" />
  <div v-else class="card-list">
    <!-- 卡片列表内容 -->
  </div>
</div>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| value / v-model | 当前视图模式 | string | card / table | table |

## Events

| 事件名 | 说明 | 回调参数 |
|-------|------|---------|
| change | 视图模式切换时触发 | value: string |
