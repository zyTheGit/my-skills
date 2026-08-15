# Badge 徽章

## 核心特性

- 支持数字角标
- 支持最大值显示（如 99+）
- 支持多种类型
- 常用于消息提醒、数量展示

## 基础用法

```vue
<el-badge :value="12" class="item">
  <el-button size="small">评论</el-button>
</el-badge>

<el-badge :value="3" class="item">
  <el-button size="small">回复</el-button>
</el-badge>

<el-badge :value="200" :max="99" class="item">
  <el-button size="small">评论</el-button>
</el-badge>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value | 显示值 | string / number | - |
| max | 最大值 | number | - |
| is-dot | 是否显示圆点 | boolean | false |
| hidden | 是否隐藏 | boolean | false |
| type | 类型 | primary / success / warning / danger / info | danger |

## 注意事项

- `is-dot` 只显示小红点，不显示数字
- `max` 超过时显示 `{max}+`