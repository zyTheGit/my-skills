# DateTimePicker 日期时间选择器

> 在同一选择器中选择日期和时间

---

## 核心特性

- 日期+时间组合选择
- 日期时间范围选择
- 默认时间配置
- 面板联动控制

---

## 基础用法

```vue
<el-date-picker v-model="value1" type="datetime" placeholder="选择日期时间"></el-date-picker>

<el-date-picker v-model="value2" type="datetimerange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | Date/array | — |
| type | 显示类型 | string | date |
| format | 显示格式 | string | yyyy-MM-dd HH:mm:ss |
| default-time | 默认时间 | string/array | — |
| time-arrow-control | 箭头选择时间 | boolean | false |
| unlink-panels | 取消面板联动 | boolean | false |
| value-format | 绑定值格式 | string | — |

---

## picker-options 配置

| 参数 | 说明 | 类型 |
|-----|------|------|
| shortcuts | 快捷选项 | array |
| disabledDate | 禁用日期函数 | function(date) |
| cellClassName | 单元格类名 | function(date) |
| firstDayOfWeek | 周起始日 | 1-7 |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 值变化时触发 | — |
| blur | 失去焦点 | — |
| focus | 获得焦点 | — |

---

## 注意事项

- 范围模式 `default-time` 为两个字符串数组
- 使用 `el-date-picker` 标签配合 `type="datetime"`
- `unlink-panels` 可取消左右面板联动