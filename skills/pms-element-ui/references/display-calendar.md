# Calendar 日历

## 核心特性

- 支持日期选择和范围选择
- 支持自定义单元格内容
- 支持周起始日配置
- 常用于日程安排、日期选择

## 基础用法

```vue
<el-calendar v-model="value"></el-calendar>

<script>
export default {
  data() {
    return {
      value: new Date()
    }
  }
}
</script>
```

## 自定义内容

```vue
<el-calendar>
  <template slot="dateCell" slot-scope="{ date, data }">
    <p :class="data.isSelected ? 'is-selected' : ''">
      {{ data.day.split('-').slice(1).join('-') }}
    </p>
  </template>
</el-calendar>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | Date/string/number | - |
| range | 时间范围 | Array | - |
| first-day-of-week | 周起始日 | Number (1-7) | 1 |

## dateCell scoped slot 参数

| 参数 | 说明 | 类型 |
|----|------|------|
| date | 单元格代表的日期 | Date |
| data | { type, isSelected, day } | Object |

## el-calendar-new 新日历

```vue
<el-calendar-new
  v-model="value"
  :first-day-of-week="7"
  :show-footer="true"
/>
```