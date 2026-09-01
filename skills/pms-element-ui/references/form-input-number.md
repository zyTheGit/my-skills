# InputNumber 计数器

> 数字输入框组件，仅允许输入标准数值

---

## 核心特性

- 支持最小/最大值限制
- 步长控制
- 数值精度控制
- 控制按钮位置可选

---

## 基础用法

```vue
<el-input-number v-model="num" @change="handleChange" :min="1" :max="10" label="描述文字"></el-input-number>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | number | 0 |
| min | 最小值 | number | -Infinity |
| max | 最大值 | number | Infinity |
| step | 步长 | number | 1 |
| step-strictly | 只能输入 step 倍数 | boolean | false |
| precision | 数值精度 | number | — |
| size | 组件尺寸 | large/small | — |
| disabled | 是否禁用 | boolean | false |
| controls | 显示控制按钮 | boolean | true |
| controls-position | 按钮位置 | right | — |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 值变化时触发 | (currentValue, oldValue) |
| blur | 失去焦点 | (event) |
| focus | 获得焦点 | (event) |

```vue
<el-input-number v-model="num" @change="handleChange"></el-input-number>
```

---

## 高精度示例

```vue
<el-input-number v-model="num" :precision="2" :step="0.1"></el-input-number>
```

---

## 注意事项

- `precision` 必须为非负整数
- `precision` 不能小于 `step` 的小数位数
- 未设置 `min` 时默认值为 0