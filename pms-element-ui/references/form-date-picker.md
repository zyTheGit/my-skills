# DatePicker 日期选择器

> 日期选择组件，支持多种日期类型和范围选择

---

## 核心特性

- 支持年/月/日/周/日期时间
- 日期范围选择
- 快捷选项配置
- 禁用日期配置

---

## 基础用法

```vue
<el-date-picker
  v-model="value"
  type="date"
  placeholder="选择日期"
  value-format="yyyy-MM-dd">
</el-date-picker>
```

---

## 日期类型

| type | 说明 |
|-----|------|
| year | 年 |
| month | 月 |
| date | 日 |
| dates | 多个日期 |
| week | 周 |
| datetime | 日期时间 |
| datetimerange | 日期时间范围 |
| daterange | 日期范围 |
| monthrange | 月份范围 |

---

## 日期范围

```vue
<el-date-picker
  v-model="value"
  type="daterange"
  range-separator="至"
  start-placeholder="开始日期"
  end-placeholder="结束日期"
  value-format="yyyy-MM-dd">
</el-date-picker>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | string/Date/array | — |
| type | 显示类型 | string | date |
| format | 显示格式 | string | yyyy-MM-dd |
| value-format | 绑定值格式 | string | — |
| picker-options | 配置项 | object | {} |
| placeholder | 占位文本 | string | — |

---

## 注意事项

- 范围选择时绑定值为数组
- 使用 `value-format` 控制存储格式
- 快捷选项通过 `picker-options.shortcuts` 配置