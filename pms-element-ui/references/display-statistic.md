# Statistic 统计数值

## 核心特性

- 展示突出的数字值
- 支持千分位和小数精度
- 支持倒计时模式
- 常用于数据面板、KPI展示

## 基础用法

```vue
<el-statistic
  group-separator=","
  :precision="2"
  :value="value"
  title="增长">
</el-statistic>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value | 数值 | string / number | - |
| decimal-separator | 小数点字符 | string | . |
| group-separator | 千分位分隔符 | string | , |
| precision | 小数精度 | number | - |
| title | 标题文本 | string / slot | - |
| prefix | 前缀 | string / slot | - |
| suffix | 后缀 | string / slot | - |
| rate | 倍率 | number | 1000 |

## 倒计时属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| time-indices | 开启倒计时 | boolean | false |
| value | 未来时间戳 | number | - |
| format | 倒计时格式 | string | 'HH:mm:ss' |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 倒计时变化 | - |
| finish | 倒计时完成 | - |

## 方法

| 方法名 | 说明 | 参数 |
|-------|------|------|
| suspend | 暂停/恢复倒计时 | boolean |

## 注意事项

- 自定义内容通过 `slot="formatter"` 提供
- 倒计时追加时间后总时间必须仍为未来时间戳