# Select 选择器

> 下拉选择器组件，支持单选、多选、搜索、分组

---

## 核心特性

- 支持单选和多选
- 可搜索过滤
- 选项分组展示
- 多选标签折叠

---

## 基础用法

```vue
<el-select v-model="value" placeholder="请选择">
  <el-option
    v-for="item in options"
    :key="item.value"
    :label="item.label"
    :value="item.value">
  </el-option>
</el-select>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| v-model | 绑定值 | string/number/boolean/object/array | — |
| multiple | 是否多选 | boolean | false |
| disabled | 是否禁用 | boolean | false |
| clearable | 可清空 | boolean | false |
| filterable | 可搜索 | boolean | false |
| collapse-tags | 折叠标签 | boolean | false |

---

## 多选模式

```vue
<el-select v-model="value" multiple placeholder="请选择">
  <el-option label="选项一" value="1"></el-option>
  <el-option label="选项二" value="2"></el-option>
</el-select>
```

---

## 分组选项

```vue
<el-select v-model="value" placeholder="请选择">
  <el-option-group
    v-for="group in options"
    :key="group.label"
    :label="group.label">
    <el-option
      v-for="item in group.options"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
  </el-option-group>
</el-select>
```

---

## 注意事项

- 多选时绑定值为数组
- 大量选项建议配合 `filterable` 使用
- 远程搜索可使用 `remote` 和 `remote-method`