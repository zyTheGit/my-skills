# Tree 树形控件

## 核心特性

- 以树形结构展示层级数据
- 支持复选框和单选
- 支持懒加载
- 支持拖拽排序
- 常用于菜单、分类等场景

## 基础用法

```vue
<el-tree
  :data="data"
  show-checkbox
  node-key="id"
  :props="defaultProps"
  @node-click="handleNodeClick">
</el-tree>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| data | 树形数据 | array | - |
| node-key | 节点唯一标识字段 | string | - |
| props | 配置项 { children, label, disabled, isLeaf } | object | - |
| show-checkbox | 显示复选框 | boolean | false |
| check-strictly | 父子节点独立 | boolean | false |
| default-expand-all | 默认展开所有节点 | boolean | false |
| accordion | 同级只展开一个 | boolean | false |
| lazy | 懒加载子节点 | boolean | false |
| load | 懒加载处理函数 | function(node, resolve) | - |
| draggable | 是否可拖拽 | boolean | false |
| filter-node-method | 自定义过滤函数 | function | - |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| node-click | 节点点击 | (data, node, component) |
| check-change | 复选框变化 | (data, checked, indeterminate) |
| current-change | 选中节点变化 | (data, node) |
| node-expand | 节点展开 | (data, node) |
| node-collapse | 节点折叠 | (data, node) |

## 方法

| 方法名 | 说明 | 参数 |
|-------|------|------|
| filter | 过滤节点 | (value) |
| getCheckedNodes | 获取选中节点 | (leafOnly) |
| setCheckedKeys | 设置选中 key | (keys) |
| expandAll / collapseAll | 展开/折叠所有 | - |

## 注意事项

- 懒加载场景下 `expandAll` 会递归加载并返回 Promise，需使用 `await`