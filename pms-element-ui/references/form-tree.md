# Tree 树形控件

> 树形数据展示和选择组件

---

## 核心特性

- 树形数据展示
- 节点展开/折叠
- 复选框选择
- 拖拽排序

---

## 基础用法

```vue
<el-tree
  :data="data"
  :props="defaultProps"
  @node-click="handleNodeClick">
</el-tree>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| data | 数据源 | array | — |
| props | 配置项 | object | — |
| show-checkbox | 显示复选框 | boolean | false |
| node-key | 节点唯一标识 | string | — |
| default-expand-all | 默认展开所有 | boolean | false |
| expand-on-click-node | 点击节点展开 | boolean | true |
| check-strictly | 父子不关联 | boolean | false |
| default-checked-keys | 默认勾选 | array | — |
| highlight-current | 高亮选中 | boolean | false |
| draggable | 可拖拽 | boolean | false |
| allow-drop | 拖拽放置规则 | function | — |

---

## props 配置

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| label | 节点标签字段 | string | label |
| children | 子节点字段 | string | children |
| disabled | 禁用字段 | string | disabled |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| node-click | 节点点击 | (data, node, component) |
| check-change | 勾选状态变化 | (data, checked) |
| node-expand | 节点展开 | (data, node) |
| node-collapse | 节点折叠 | (data, node) |
| node-drag-start | 拖拽开始 | (draggingNode, ev) |
| node-drop | 拖拽放置 | (draggingNode, dropNode, ev) |

---

## 数据结构示例

```javascript
data() {
  return {
    data: [
      {
        label: '一级 1',
        children: [{
          label: '二级 1-1',
          children: [{ label: '三级 1-1-1' }]
        }]
      }
    ],
    defaultProps: {
      children: 'children',
      label: 'label'
    }
  }
}
```

---

## 注意事项

- `node-key` 建议设置，配合 `show-checkbox` 使用
- `check-strictly` 为 true 时父子节点不联动
- 大量数据建议使用懒加载 `lazy` 和 `load` 属性