# Switch 开关

> 在两种对立状态间切换，通常为开/关

---

## 核心特性

- 布尔值切换
- 自定义开启/关闭值
- 切换前确认钩子
- 自定义颜色和文字

---

## 基础用法

```vue
<el-switch v-model="value" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value / v-model | 绑定值 | boolean/string/number | — |
| size | 尺寸 | large/medium/small | medium |
| disabled | 是否禁用 | boolean | false |
| width | 宽度（px） | number | 40 |
| desc-type | 描述类型 | text/icon | — |
| active-text / inactive-text | 开启/关闭文字 | string | — |
| active-value / inactive-value | 开启/关闭值 | boolean/string/number | true/false |
| active-color / inactive-color | 背景色 | string | #409EFF/#C0CCDA |
| before-change | 变化前钩子 | function(nextValue, oldValue) | — |
| validate-event | 触发表单验证 | boolean | true |

---

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 状态变化时触发 | 新值 |

---

## 异步确认示例

```vue
<el-switch
  v-model="value"
  :before-change="handleBeforeChange">
</el-switch>

methods: {
  handleBeforeChange(newValue, oldValue) {
    return new Promise((resolve) => {
      this.$confirm('确定要切换吗？').then(() => resolve()).catch(() => resolve(false));
    });
  }
}
```

---

## 注意事项

- `before-change` 返回 false 或 rejected Promise 可阻止切换
- `desc-type="text"` 显示文字，`desc-type="icon"` 显示图标