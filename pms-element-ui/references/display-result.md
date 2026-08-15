# Result 结果页

## 核心特性

- 对操作结果进行反馈
- 支持多种图标类型
- 支持自定义内容
- 常用于提交成功/失败提示

## 基础用法

```vue
<el-result icon="success" title="操作成功" subTitle="请按照指引操作">
  <template slot="extra">
    <el-button>取消</el-button>
    <el-button type="primary">确认</el-button>
  </template>
</el-result>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| title | 标题文本 | string | - |
| sub-title | 副标题文本 | string | - |
| icon | 图标类型 | success / warning / info / error | info |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| icon | 自定义图标 |
| title | 自定义标题 |
| subTitle | 自定义副标题 |
| extra | 底部操作区 |

## 注意事项

- 使用 `icon` 插槽可提供完全自定义的图标（如图片）