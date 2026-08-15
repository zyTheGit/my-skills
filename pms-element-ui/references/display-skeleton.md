# Skeleton 骨架屏

## 核心特性

- 内容加载时显示占位预览
- 支持多种形状变体
- 支持动画效果
- 比旋转动画更直观

## 基础用法

```vue
<el-skeleton :rows="6" :loading="loading" animated>
  <template slot="template">
    <el-skeleton-item variant="image" style="width: 240px; height: 240px;" />
    <el-skeleton-item variant="h3" style="width: 50%;" />
  </template>
  <template>
    <!-- loading=false 时显示真实 UI -->
    <el-card>...</el-card>
  </template>
</el-skeleton>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| animated | 是否开启动画 | boolean | false |
| count | 模板重复次数 | number | 1 |
| loading | 是否显示骨架屏 | boolean | true |
| rows | 段落行数 | number | 4 |
| throttle | 渲染延迟（ms） | number | 0 |

## Skeleton Item 属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| variant | 显示形状 | p/h1/h3/text/caption/button/image/circle/rect | text |

## 注意事项

- `count` 不宜过大，避免性能问题
- `throttle` 可防止 API 响应过快时的闪烁