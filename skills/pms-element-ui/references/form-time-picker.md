# TimePicker 时间选择器

> 时间选择组件，支持固定时间点和任意时间点

---

## 核心特性

- TimeSelect：固定时间点
- TimePicker：任意时间点
- 时间范围选择
- 箭头选择模式

---

## 基础用法

```vue
<!-- 固定时间点 -->
<el-time-select v-model="value" :picker-options="{ start: '08:30', step: '00:15', end: '18:30' }" placeholder="选择时间"></el-time-select>

<!-- 任意时间点 -->
<el-time-picker v-model="value1" :picker-options="{ selectableRange: '18:30:00 - 20:30:00' }" placeholder="任意时间点"></el-time-picker>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | Date/string | — |
| readonly | 完全只读 | boolean | false |
| disabled | 禁用 | boolean | false |
| editable | 文本框可输入 | boolean | true |
| clearable | 显示清除按钮 | boolean | true |
| is-range | 时间范围选择 | boolean | false |
| arrow-control | 箭头选择 | boolean | false |
| value-format | 绑定值格式 | string | — |

---

## picker-options 配置

**TimeSelect**：`start`（默认 '09:00'）、`end`（默认 '18:00'）、`step`（默认 '00:30'）、`minTime`、`maxTime`

**TimePicker**：`selectableRange`（字符串或数组）、`format`（默认 'HH:mm:ss'）

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 值变化时触发 | — |
| blur | 失去焦点 | — |
| focus | 获得焦点 | — |

---

## 注意事项

- TimeSelect 和 TimePicker 是两个不同组件
- `is-range` 和 `arrow-control` 仅适用于 TimePicker
- 时间范围选择时绑定值为两个 Date 对象的数组