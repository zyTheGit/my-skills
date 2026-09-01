# Checkbox 多选框

> 从一组选项中进行多选，单个可在两种状态间切换

---

## 核心特性

- 支持单个勾选和组多选
- 半选状态（indeterminate）
- 边框样式
- 自动生成选项

---

## 基础用法

```vue
<el-checkbox v-model="checked">备选项</el-checkbox>

<el-checkbox-group v-model="checkList" :options="options" :options-props="optionsProps" />
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | string/number/boolean | — |
| label | 选中时的值 | string/number/boolean | — |
| true-label / false-label | 选中/未选中值 | string/number | — |
| disabled | 是否禁用 | boolean | false |
| indeterminate | 半选状态（仅样式） | boolean | false |
| border | 显示边框 | boolean | false |

---

## Checkbox-group 扩展属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| min | 最小可选数量 | number | — |
| max | 最大可选数量 | number | — |
| options | 自动生成选项 | array | — |
| optionsProps | 字段映射 | object | — |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 值变化时触发 | 更新后的值 |

---

## 全选/半选示例

```vue
<el-checkbox :indeterminate="isIndeterminate" v-model="checkAll">全选</el-checkbox>
```

---

## 注意事项

- `indeterminate` 仅为视觉样式，需自行管理
- `el-checkbox-group` 无子内容且传入 `options` 时自动生成选项
- 选项过多建议使用 Select 替代