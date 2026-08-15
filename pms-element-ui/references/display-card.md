# Card 卡片

## 核心特性

- 支持标题和操作区
- 支持阴影效果
- 支持自定义内容
- 常用于信息卡片展示

## 基础用法

```vue
<el-card class="box-card">
  <div slot="header" class="clearfix">
    <span>卡片名称</span>
    <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
  </div>
  <div v-for="o in 4" :key="o" class="text item">
    {{ '列表内容 ' + o }}
  </div>
</el-card>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| header | 卡片标题 | string / slot | - |
| shadow | 阴影显示时机 | always / hover / never | always |
| body-style | 内容样式 | object | { padding: '20px' } |

## 插槽

| 插槽名 | 说明 |
|-------|------|
| default | 卡片内容 |
| header | 卡片头部（可包含标题和操作按钮） |

## 注意事项

- `shadow` 控制阴影：`always` 始终显示，`hover` 悬停显示，`never` 不显示