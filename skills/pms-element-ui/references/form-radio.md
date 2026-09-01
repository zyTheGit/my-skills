# Radio 单选框

> 在一组互斥选项中进行单选

---

## 核心特性

- 单选互斥
- 按钮风格样式
- 分段控件样式
- 自动生成选项

---

## 基础用法

```vue
<el-radio v-model="radio" label="1">备选项</el-radio>
<el-radio v-model="radio" label="2">备选项</el-radio>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | string/number/boolean | — |
| label | Radio 的值 | string/number/boolean | — |
| disabled | 是否禁用 | boolean | false |
| border | 显示边框 | boolean | false |
| size | 尺寸 | medium/small/mini | — |

---

## Radio-group 扩展属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| options | 自动生成选项 | array | — |
| optionsProps | 字段映射 | object | — |
| optionType | 选项类型 | radio/button | radio |
| buttonStyle | 按钮风格 | default/segmented/separated | default |
| text-color | 激活文本颜色 | string | — |
| fill | 激活填充色 | string | — |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| input | 值变化时触发 | 选中的 label 值 |

---

## 按钮风格示例

```vue
<el-radio-group v-model="radio" option-type="button">
  <el-radio label="1">选项一</el-radio>
  <el-radio label="2">选项二</el-radio>
</el-radio-group>
```

---

## 注意事项

- `buttonStyle="segmented"` 为紧凑分段控件
- `buttonStyle="separated"` 为独立圆角按钮
- 选项过多建议使用 Select 替代