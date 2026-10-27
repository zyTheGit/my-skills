# BaseVirtualTree 虚拟树

面向大数据量（数千到数十万节点）的树形控件，外观与 `el-tree` 保持一致，但仅渲染视口内行，内存与渲染开销随可见行数增长，支持展开、搜索、勾选等高负载操作。

## 基础用法

```vue
<template>
  <!-- node-key 为必填项；height 为数字时按 px 处理 -->
  <el-base-virtual-tree
    :data="data"
    node-key="id"
    :height="320"
    :default-expanded-keys="['n-0']"
    @node-click="handleNodeClick"
  />
</template>

<script>
function makeTree(depth, fanout, prefix = 'n', level = 1) {
  const nodes = [];
  for (let i = 0; i < fanout; i++) {
    const id = `${prefix}-${i}`;
    const node = { id, label: `${level} 级节点 ${id}` };
    if (level < depth) node.children = makeTree(depth, fanout, id, level + 1);
    nodes.push(node);
  }
  return nodes;
}

export default {
  data() {
    return {
      // 冻结数据可减少 Vue 响应式开销
      data: Object.freeze(makeTree(3, 20)),
    };
  },
  methods: {
    handleNodeClick(data, node) {
      console.log(data.id, 'level', node.level);
    },
  },
};
</script>
```

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| data | 展示数据 | array | — |
| node-key | 节点唯一标识字段（必填） | string | — |
| props | 配置选项 `{ label, children, disabled }` | object | `{ children: 'children', label: 'label', disabled: 'disabled' }` |
| height | 滚动容器高度，数字按 px 处理 | number / string | — |
| row-height | 行高，需与主题一致 | number | 32 |
| buffer | 视口上下额外渲染行数 | number | 10 |
| empty-text | 无数据提示文本 | string | `暂无数据` |
| highlight-current | 是否高亮当前节点 | boolean | false |
| default-expand-all | 是否默认展开所有节点 | boolean | false |
| default-expanded-keys | 默认展开节点 key 数组 | array | — |
| expand-on-click-node | 点击节点时是否展开/折叠 | boolean | true |
| accordion | 是否手风琴模式 | boolean | false |
| show-checkbox | 是否显示复选框 | boolean | false |
| check-strictly | 父子节点是否不关联 | boolean | false |
| default-checked-keys | 默认勾选节点 key 数组 | array | — |
| filter-node-method | 节点过滤方法 | Function | — |
| render-content | 节点渲染函数 | Function | — |

## Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| node-click | 节点被点击 | data, node, component |
| node-contextmenu | 节点右键点击 | event, data, node, component |
| check-change | 节点选中状态变化 | data, checked, indeterminate |
| check | 复选框被点击 | data, { checkedNodes, checkedKeys, halfCheckedNodes, halfCheckedKeys } |
| current-change | 当前选中节点变化 | data, node |
| node-expand | 节点展开 | data, node, component |
| node-collapse | 节点折叠 | data, node, component |

## Methods

| 方法名 | 说明 | 参数 |
|--------|------|------|
| filter | 按条件过滤节点 | value |
| getNode | 根据 key/data 获取节点对象 | key / data |
| getNodePath | 获取从根到该节点的数据数组 | key / data |
| getCheckedKeys | 获取已勾选节点 key 数组 | leafOnly |
| setCheckedKeys | 通过 keys 设置勾选 | keys, leafOnly |
| setChecked | 设置某个节点勾选状态 | key/data, checked, deep |
| getCurrentKey | 获取当前选中节点 key | — |
| setCurrentKey | 设置当前选中节点 | key |
| expandNode | 展开节点 | key/data, expandParent |
| collapseNode | 折叠节点 | key/data |
| expandAll | 展开全部节点 | — |
| collapseAll | 折叠全部节点 | — |
| expandToLevel | 展开到第 N 级 | level |
| scrollToNode | 展开祖先并滚动到节点 | key/data, block |

## Scoped Slot

| 插槽名 | 说明 | 作用域参数 |
|--------|------|------------|
| — | 自定义节点内容 | `{ node, data }` |

## 注意事项

- 组件自身是滚动容器，必须有确定高度（`height` 属性或父容器 `flex` 约束）
- 每行高度固定为 `row-height`，自定义节点内容建议不要超出一行
- 不支持 `lazy` / `load` 懒加载，需分批加载时请合并后重新赋值 `data`
- 不支持 `draggable` 及节点拖拽事件
- 不提供 `append` / `remove` 等节点增删方法，修改数据后重新赋值 `data`（整树重建）
- 组件不会向节点写入属性，可直接传入 `Object.freeze` 后的数据

> 源文档：examples/docs/zh-CN/base-virtual-tree.md
