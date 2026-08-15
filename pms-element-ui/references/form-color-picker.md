# ColorPicker 颜色选择器

> 支持多种颜色格式的颜色选择组件

---

## 核心特性

- 支持透明度选择
- 预定义颜色列表
- 多种颜色格式输出
- 尺寸控制

---

## 基础用法

```vue
<el-color-picker v-model="color1"></el-color-picker>
<el-color-picker v-model="color" show-alpha></el-color-picker>
<el-color-picker v-model="color" :predefine="predefineColors"></el-color-picker>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | string | — |
| disabled | 是否禁用 | boolean | false |
| size | 尺寸 | medium/small/mini | — |
| show-alpha | 支持透明度 | boolean | false |
| color-format | 颜色格式 | hsl/hsv/hex/rgb | hex/rgb |
| popper-class | 下拉框类名 | string | — |
| predefine | 预定义颜色 | array | — |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 绑定值变化时触发 | — |
| active-change | 面板颜色变化时触发 | — |

---

## 预定义颜色示例

```vue
<el-color-picker v-model="color" :predefine="predefineColors"></el-color-picker>

data() {
  return {
    predefineColors: [
      '#409EFF', '#67C23A', '#E6A23C', '#F56C6C',
      '#909399', 'rgba(64,158,255,0.5)'
    ]
  }
}
```

---

## 注意事项

- `show-alpha` 为 true 时，`color-format` 默认从 hex 切换为 rgb
- 预定义颜色支持多种格式：hex、rgba、rgb、hsv、hsva、hsl、hsla
- `active-change` 每次交互都触发，注意性能