# BaseTree 树形控件

**功能说明**：以树形结构展示层级数据，支持展开/折叠节点、拖拽、复选框等功能。

## 基础用法

```vue
<el-tree
  :data="data"
  show-checkbox
  node-key="id"
  :props="defaultProps"
  @node-click="handleNodeClick"
></el-tree>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| data | 树形数据 | array | - |
| node-key | 节点唯一标识字段（基于 key 的方法必填） | string | - |
| props | 配置项 `{ children, label, disabled, isLeaf }` | object | - |
| show-checkbox | 显示复选框 | boolean | false |
| check-strictly | 父子节点复选框独立 | boolean | false |
| default-expand-all | 默认展开所有节点 | boolean | false |
| accordion | 同级只展开一个 | boolean | false |
| lazy | 懒加载子节点（配合 `load`） | boolean | false |
| load | 懒加载处理函数 | function(node, resolve) | - |
| draggable | 是否可拖拽 | boolean | false |
| filter-node-method | 自定义过滤函数 | function | - |

## 常用事件

| 事件名 | 说明 | 参数 |
|--------|------|------|
| node-click | 节点点击 | (data, node, component) |
| check-change | 复选框变化 | (data, checked, indeterminate) |
| check | 复选框点击 | (data, { checkedKeys, checkedNodes }) |
| current-change | 当前选中节点变化 | (data, node) |
| node-expand | 节点展开 | (data, node, component) |
| node-collapse | 节点折叠 | (data, node, component) |

## 方法

| 方法名 | 说明 | 参数 |
|--------|------|------|
| filter | 过滤节点 | (value) |
| getCheckedNodes | 获取选中节点 | (leafOnly) |
| setCheckedNodes | 设置选中节点 | (nodes) |
| getCheckedKeys | 获取选中 key | (leafOnly) |
| setCheckedKeys | 设置选中 key | (keys) |
| getNode | 获取节点 | (key/data) |
| expandNode / collapseNode | 展开/折叠节点 | (key) |
| expandAll / collapseAll | 展开/折叠所有 | - |

## 注意事项

- 懒加载场景下 `expandAll` 会递归加载并返回 Promise，需使用 `await`
- 自定义内容通过 scoped slot（`slot-scope="{ node, data }"`）实现
