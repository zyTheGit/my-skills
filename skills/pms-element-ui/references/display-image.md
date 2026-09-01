# Image 图片

## 核心特性

- 支持懒加载
- 支持图片预览
- 支持多种填充模式
- 保留原生 img 行为

## 基础用法

```vue
<el-image
  style="width: 100px; height: 100px"
  :src="url"
  :preview-src-list="srcList"
  fit="cover">
</el-image>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| src | 图片源 URL | string | - |
| fit | 填充模式 | fill/contain/cover/none/scale-down | - |
| lazy | 是否懒加载 | boolean | false |
| preview-src-list | 预览图片数组 | array | - |
| z-index | 预览遮罩层 z-index | number | 2000 |
| initial-index | 初始预览索引 | number | - |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| load | 图片加载成功 | (event) |
| error | 图片加载失败 | (event) |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| placeholder | 加载中占位内容 |
| error | 加载失败容错内容 |

## 注意事项

- 使用 `preview-src-list` 时，点击图片会打开全屏预览遮罩
- `fit` 同 CSS object-fit