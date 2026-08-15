# Transfer 穿梭框

> 双面板组件，用于在源列表和目标列表之间移动数据项

---

## 核心特性

- 双面板数据迁移
- 可搜索过滤
- 自定义渲染
- 无限滚动加载

---

## 基础用法

```vue
<el-transfer v-model="value" :data="data"></el-transfer>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值（右侧 key 数组） | array | — |
| data | 数据源 | array | [] |
| filterable | 可搜索 | boolean | false |
| titles | 面板标题 | array | ['列表1','列表2'] |
| target-order | 右侧排序策略 | original/push/unshift | original |
| props | 字段别名映射 | object | — |
| render-content | 自定义渲染函数 | function | — |
| format | 勾选文案格式 | object | — |

---

## 数据格式

```javascript
data() {
  return {
    data: [
      { key: 1, label: '选项一', disabled: false },
      { key: 2, label: '选项二', disabled: false }
    ],
    value: []
  }
}
```

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 右侧列表变化 | (value, direction, movedKeys) |
| left-check-change | 左侧勾选变化 | (checkedKeys, changedKeys) |
| right-check-change | 右侧勾选变化 | (checkedKeys, changedKeys) |
| load | 滚动到底部触发 | — |

---

## 注意事项

- `data` 数组每项必须有 `key` 字段
- `render-content` 使用 JSX（h 函数）
- `format` 使用 `${checked}` 和 `${total}` 占位符