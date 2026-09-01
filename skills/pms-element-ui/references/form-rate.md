# Rate 评分

> 星级评分组件

---

## 核心特性

- 星级评分（1-5星）
- 支持半星选择
- 自定义颜色和图标
- 只读模式显示分数

---

## 基础用法

```vue
<el-rate v-model="value1"></el-rate>
<el-rate v-model="value2" :colors="colors"></el-rate>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | number | 0 |
| max | 最大分值 | number | 5 |
| disabled | 只读模式 | boolean | false |
| allow-half | 允许半选 | boolean | false |
| low-threshold / high-threshold | 分层阈值 | number | 2/4 |
| colors | 层级颜色 | array/object | ['#F7BA2A'] |
| icon-classes | 层级图标类名 | array/object | — |
| void-icon-class | 未选中图标 | string | el-icon-star-off |
| show-text | 显示辅助文字 | boolean | false |
| show-score | 显示当前分数 | boolean | false |
| texts | 辅助文字数组 | array | — |
| score-template | 分数模板 | string | {value} |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 分值变化时触发 | 新值 |

---

## 自定义颜色示例

```vue
<el-rate v-model="value" :colors="['#999', '#e6a23c', '#f7ba2a']"></el-rate>
```

---

## 注意事项

- `show-text` 和 `show-score` 不能同时为 true
- 只读模式下支持小数分值显示
- `low-threshold` 和 `high-threshold` 控制颜色分层