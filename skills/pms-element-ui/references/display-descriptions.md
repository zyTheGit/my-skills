# Descriptions 描述列表

## 核心特性

- 以键值对形式展示信息
- 支持多列布局
- 支持边框和方向控制
- 常用于详情页展示

## 基础用法

```vue
<el-descriptions title="用户信息">
  <el-descriptions-item label="用户名">kooriookami</el-descriptions-item>
  <el-descriptions-item label="手机号">18100000000</el-descriptions-item>
</el-descriptions>
```

## 常用属性（Descriptions）

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| border | 是否显示边框 | boolean | false |
| column | 每行列数 | number | 3 |
| direction | 排列方向 | vertical / horizontal | horizontal |
| size | 尺寸 | medium / small / mini | - |
| title | 标题文本 | string | - |
| extra | 操作区文本 | string | - |
| colon | 是否显示冒号 | boolean | true |

## 常用属性（Descriptions Item）

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| label | 标签文本 | string | - |
| span | 列跨度 | number | 1 |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| title | 自定义标题 |
| extra | 自定义操作区 |

## 注意事项

- 支持 `label-class-name`、`content-style` 等样式自定义