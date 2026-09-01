# ThemeProvider 运行时主题切换

> 基于 CSS 变量的运行时主题切换方案

---

## 核心特性

- 运行时切换，无需重新编译
- 自动持久化到 localStorage
- CSS 变量引用链自动更新

---

## 基础用法

```javascript
import { getThemeProvider } from 'element-ui/src/themes/theme-provider'

const themeProvider = getThemeProvider()

// 切换主题
themeProvider.setTheme('dark')   // 暗色主题
themeProvider.setTheme('light')  // 亮色主题
```

### CSS 变量方式

```javascript
document.documentElement.style.setProperty(
  '--el-color-primary',
  newColor
)
```

---

## API 参考

| 方法 | 说明 |
|------|------|
| `setTheme(name, save?)` | 切换主题，`save` 默认 true |
| `getTheme()` | 获取当前主题名 |
| `setVariable(name, value)` | 设置单个 CSS 变量 |
| `getVariable(name)` | 获取 CSS 变量值 |
| `setVariables(vars)` | 批量设置 CSS 变量 |
| `reset()` | 重置为默认主题 |
| `getAvailableThemes()` | 列出可用主题 |

---

## 核心 CSS 变量

| 变量 | 亮色默认值 |
|------|-----------|
| `--el-color-primary` | #3C6CFE |
| `--el-color-success` | #53C31B |
| `--el-color-warning` | #F4AB1C |
| `--el-color-danger` | #FF6160 |
| `--el-color-text-primary` | #333333 |
| `--el-border-color-base` | #D9D9D9 |
| `--el-background-color-base` | #F5F7FA |

---

## 代码示例

```vue
<template>
  <el-button @click="toggleTheme">切换主题</el-button>
</template>

<script>
import { getThemeProvider } from 'element-ui/src/themes/theme-provider'

export default {
  methods: {
    toggleTheme() {
      const provider = getThemeProvider()
      const current = provider.getTheme()
      provider.setTheme(current === 'light' ? 'dark' : 'light')
    }
  }
}
</script>
```

---

## 注意事项

- 需引入 `index-css-vars.css` 替代默认 `index.css`
- CSS 变量采用引用链，修改主色自动更新派生色
- **不兼容 IE**（IE 不支持 CSS 自定义属性）
- 主题默认持久化到 localStorage
