# Tag 标签

## 核心特性

- 支持多种类型（success/info/warning/danger）
- 支持可关闭标签
- 支持自定义颜色和尺寸
- 常用于标记、分类、状态展示

## 基础用法

```vue
<el-tag>默认</el-tag>
<el-tag type="success">成功</el-tag>
<el-tag type="info">信息</el-tag>
<el-tag type="warning">警告</el-tag>
<el-tag type="danger">危险</el-tag>
```

## 可移除标签

```vue
<el-tag
  v-for="tag in tags"
  :key="tag.name"
  closable
  :type="tag.type"
  @close="handleClose(tag)">
  {{ tag.name }}
</el-tag>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| type | 类型 | success / info / warning / danger | - |
| size | 尺寸 | medium / small / mini | medium |
| effect | 主题 | dark / light / plain | light |
| closable | 是否可关闭 | boolean | false |
| round | 圆角 | boolean | false |
| hit | 描边效果 | boolean | false |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| close | 关闭时触发 | (event) |