# Tooltip 文字提示

## 核心特性

- 鼠标悬停时显示提示
- 支持多种方向
- 支持自定义内容
- 常用于按钮、图标等元素的解释说明

## 基础用法

```vue
<el-tooltip content="顶部提示" placement="top">
  <el-button>上</el-button>
</el-tooltip>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| content | 提示文字 | string / slot | - |
| placement | 出现位置 | top/bottom/left/right | bottom |
| effect | 主题 | dark / light | dark |
| disabled | 是否禁用 | boolean | false |
| offset | 偏移距离 | number | 12 |
| visible | 是否可见 | boolean | - |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| default | 触发元素 |
| content | 提示内容（可包含HTML） |

## 注意事项

- 使用 `effect="light"` 适配浅色主题