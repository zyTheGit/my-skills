# Avatar 头像

## 核心特性

- 支持文字、图片、图标类型
- 支持自定义形状和尺寸
- 支持加载失败容错
- 常用于用户头像展示

## 基础用法

```vue
<el-avatar icon="el-icon-user-solid"></el-avatar>
<el-avatar src="https://cube.elemecdn.com/3/7c/3ea6beec248251eecd09f3b1d5a7epng"></el-avatar>
<el-avatar>用户</el-avatar>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| size | 尺寸 | number / string | large |
| shape | 形状 | circle / square | circle |
| src | 图片地址 | string | - |
| icon | 图标类名 | string | - |
| fit | 图片填充模式 | fill/contain/cover/none/scale-down | cover |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| error | 图片加载失败 | (event) |

## 注意事项

- `size` 可设为 `large`、`medium`、`small` 或具体像素值
- 当 `src` 存在时，优先显示图片