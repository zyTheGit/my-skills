# Collapse 折叠面板

## 核心特性

- 支持手风琴模式（同时只打开一个）
- 支持自定义标题内容
- 支持禁用状态
- 常用于FAQ、设置项等场景

## 基础用法

```vue
<el-collapse v-model="activeNames" @change="handleChange">
  <el-collapse-item title="一致性" name="1">
    <div>内容</div>
  </el-collapse-item>
</el-collapse>
```

## 常用属性（Collapse）

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| v-model | 当前激活面板 | string / array | - |
| accordion | 手风琴模式 | boolean | false |

## 常用属性（Collapse Item）

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| name | 唯一标识 | string / number | - |
| title | 面板标题 | string | - |
| disabled | 是否禁用 | boolean | - |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 激活面板变化时触发 | activeNames |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| default | 面板内容 |
| title | 自定义标题 |

## 注意事项

- `accordion` 开启后，只能同时展开一个面板