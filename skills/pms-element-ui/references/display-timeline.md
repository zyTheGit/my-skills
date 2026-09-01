# Timeline 时间线

## 核心特性

- 以垂直时间轴展示时间流信息
- 支持多种节点类型和颜色
- 支持倒序排列
- 常用于操作日志、流程追踪

## 基础用法

```vue
<el-timeline :reverse="reverse">
  <el-timeline-item
    v-for="(activity, index) in activities"
    :key="index"
    :timestamp="activity.timestamp">
    {{ activity.content }}
  </el-timeline-item>
</el-timeline>
```

## 常用属性（Timeline）

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| reverse | 是否倒序排列节点 | boolean | false |

## 常用属性（Timeline Item）

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| timestamp | 时间戳文本 | string | - |
| hide-timestamp | 隐藏时间戳 | boolean | false |
| placement | 时间戳位置 | top / bottom | bottom |
| type | 节点类型 | primary/success/warning/danger/info | - |
| color | 节点颜色 | string | - |
| size | 节点尺寸 | normal / large | normal |
| icon | 节点图标类名 | string | - |
| hollow | 空心圆样式 | boolean | false |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| default | 内容 |
| dot | 自定义节点标记 |

## 注意事项

- 与 Steps 组件区分：Timeline 展示时间流，Steps 展示步骤进度
- `hollow` 属性创建描边圆圈样式