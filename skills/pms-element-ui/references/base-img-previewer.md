# BaseImgPreviewer 图片预览

**功能说明**：图片查看预览组件，支持放大、旋转等操作。

## 基础用法

```vue
<el-base-img-previewer
  v-model="visible"
  :src="imageUrl"
/>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| value / v-model | 是否显示预览 | boolean | - |
| src | 图片地址 | string | - |

## Events

| 事件名 | 说明 | 参数 |
|--------|------|------|
| close | 关闭预览 | - |

## 注意事项

- 支持鼠标滚轮缩放
- 支持键盘左右键切换图片
