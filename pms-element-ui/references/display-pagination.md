# Pagination 分页

## 核心特性

- 支持自定义每页条数
- 支持快速跳转
- 支持总数显示
- 支持多种布局模式

## 基础用法

```vue
<el-pagination
  @size-change="handleSizeChange"
  @current-change="handleCurrentChange"
  :current-page="currentPage"
  :page-sizes="[10, 20, 30, 40]"
  :page-size="10"
  layout="total, sizes, prev, pager, next, jumper"
  :total="400">
</el-pagination>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| total | 总条目数 | number | - |
| current-page | 当前页数 | number | 1 |
| page-size | 每页条数 | number | 10 |
| page-sizes | 每页条数选项 | number[] | [10,20,30,40,50,100] |
| layout | 布局 | string | 'prev, pager, next, jumper, ->, total' |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| size-change | 每页条数变化 | (size) |
| current-change | 当前页变化 | (currentPage) |

## 注意事项

- `layout` 可自定义显示元素：`total, sizes, prev, pager, next, jumper`