# Cascader 级联选择器

> 多级数据选择组件，支持动态加载

---

## 核心特性

- 多级数据联动
- hover/click 展开触发
- 动态加载数据
- 多选模式

---

## 基础用法

```vue
<el-cascader
  v-model="value"
  :options="options"
  :props="{ expandTrigger: 'hover' }"
  @change="handleChange">
</el-cascader>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | array | — |
| options | 数据源 | array | — |
| props | 配置项 | object | — |
| expandTrigger | 展开触发方式 | click/hover | click |
| clearable | 可清空 | boolean | false |
| filterable | 可搜索 | boolean | false |
| disabled | 禁用 | boolean | false |
| checkStrictly | 父子不关联 | boolean | false |

---

## props 配置

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value | 指定选项值字段 | string | value |
| label | 指定选项标签字段 | string | label |
| children | 指定子选项字段 | string | children |
| disabled | 指定选项禁用字段 | string | disabled |
| emitPath | 是否返回完整路径 | boolean | true |

---

## 数据结构示例

```javascript
options: [
  {
    value: 'zhinan',
    label: '指南',
    children: [
      { value: 'sheji', label: '设计', children: [...] }
    ]
  }
]
```

---

## 注意事项

- 绑定值为数组，表示选中的路径
- `emitPath: false` 时只返回最后一级的值
- 动态加载使用 `lazy` 和 `lazyLoad` 属性