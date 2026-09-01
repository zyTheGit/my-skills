# BaseLayout 基础布局

**功能说明**：应用整体布局框架，支持左侧栏、底部操作区和主体内容区域。

## 基础用法

```vue
<template>
  <div class="demo-base-layout-content">
    <el-base-layout containerHeight="100%">
      <el-base-pro-table
        :columns="columns"
        :data="tableData"
        :total="total"
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :search-model.sync="searchForm"
        show-selection
        show-index
        @search="handleSearch"
        @reset="handleReset"
      />
    </el-base-layout>
  </div>
</template>
```

## 展示侧边栏

使用 `slot="left"` 自定义左侧内容：

```vue
<el-base-layout containerHeight="100%">
  <el-base-pro-table ... />
  <template slot="left">
    <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
  </template>
</el-base-layout>
```

## 带底部按钮栏

使用 `slot="footer"` 展示底部按钮栏：

```vue
<el-base-layout containerHeight="100%">
  <el-base-pro-table ... />
  <template slot="left">...</template>
  <template slot="footer">
    <el-button type="primary">保存</el-button>
    <el-button>取消</el-button>
  </template>
</el-base-layout>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| collapsible | 左侧栏是否可以折叠 | boolean | - | true |
| initialExpanded | 左侧栏初始是否展开 | boolean | - | true |
| leftExpandedWidth | 左侧栏展开时的宽度 | string | - | 20% |
| leftCollapsedWidth | 左侧栏收起时的宽度 | string | - | 22px |
| footerHeight | 底部按钮栏高度 | string | - | 60px |
| containerHeight | 布局容器高度 | string | - | 100vh |

## Slots

| 名称 | 说明 |
|------|------|
| — | 主体内容 |
| left | 左侧栏内容 |
| footer | 底部操作区域 |

## 注意事项

- 默认高度为 `100vh`，可根据实际父容器情况传入 `'100%'`
- 左侧栏支持折叠/展开切换
