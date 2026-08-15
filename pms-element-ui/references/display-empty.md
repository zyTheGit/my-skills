# Empty 空状态

## 核心特性

- 支持自定义图片
- 支持自定义描述
- 支持插槽自定义内容
- 常用于无数据时的占位提示

## 基础用法

```vue
<el-empty description="暂无数据"></el-empty>
```

## 自定义图片

```vue
<el-empty :image="require('@/assets/empty.png')">
  <el-button type="primary">按钮</el-button>
</el-empty>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| image | 自定义图片 URL | string | - |
| image-size | 图片大小 | number | - |
| description | 描述文字 | string / slot | '暂无数据' |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| default | 底部内容（如操作按钮） |
| image | 自定义图片 |
| description | 自定义描述 |

## 注意事项

- 默认使用内置插图，可通过 `image` 属性替换