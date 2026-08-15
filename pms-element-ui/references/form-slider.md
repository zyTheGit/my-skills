# Slider 滑块

> 通过拖动滑块在一个固定区间内选择值

---

## 核心特性

- 范围选择（双滑块）
- 垂直模式
- 间断点标记
- 输入框联动

---

## 基础用法

```vue
<el-slider v-model="value1"></el-slider>
<el-slider v-model="value" range show-stops :max="10"></el-slider>
<el-slider v-model="value" vertical height="200px"></el-slider>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | number/array | 0 |
| min | 最小值 | number | 0 |
| max | 最大值 | number | 100 |
| step | 步长 | number | 1 |
| disabled | 是否禁用 | boolean | false |
| show-input | 显示输入框 | boolean | false |
| show-stops | 显示间断点 | boolean | false |
| show-tooltip | 显示 tooltip | boolean | true |
| range | 范围选择 | boolean | false |
| vertical | 垂直模式 | boolean | false |
| height | 垂直模式高度 | string | — |
| marks | 标记 | object | — |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 值变化（松开鼠标） | 新值 |
| input | 数据变化（拖动时） | 新值 |

---

## 带标记示例

```vue
<el-slider v-model="value" :marks="marks"></el-slider>

data() {
  return {
    marks: {
      0: '0°C',
      50: '50°C',
      100: '100°C'
    }
  }
}
```

---

## 注意事项

- `range` 为 true 时绑定值必须是数组 `[min, max]`
- 垂直模式下 `height` 属性必填
- `show-input` 仅在非 range 模式下生效
- `change` 松开鼠标触发，`input` 拖动时连续触发