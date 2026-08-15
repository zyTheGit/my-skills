# 自定义主题配置

> 通过 SCSS 变量实现主题深度定制

---

## 核心特性

- SCSS 变量驱动
- 支持运行时切换
- 无需重新编译

---

## 基础用法

### 1. 创建样式文件

新建 `element-variables.scss`：

```scss
/* 主题色 */
$--color-primary: teal;

/* icon 字体路径（必需） */
$--font-path: '~element-ui/lib/theme-chalk/fonts';

/* 引入 Element UI */
@import "~element-ui/packages/theme-chalk/src/index";
```

### 2. 引入自定义主题

```javascript
import Vue from 'vue'
import Element from 'element-ui'
import './element-variables.scss'

Vue.use(Element)
```

---

## 主题切换

### 动态切换主题色

```javascript
const theme = {
  primary: '#409EFF',
  success: '#67C23A'
};

Object.keys(theme).forEach(key => {
  document.documentElement.style.setProperty(
    `--color-${key}`,
    theme[key]
  )
})
```

### 完整主题配置对象

```javascript
export const themeConfig = {
  primary: '#409EFF',
  success: '#67C23A',
  warning: '#E6A23C',
  danger: '#F56C6C',
  info: '#909399'
}
```

---

## 常用 SCSS 变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `$--color-primary` | 主色 | #409EFF |
| `$--color-success` | 成功色 | #67C23A |
| `$--border-radius-base` | 基础圆角 | 4px |
| `$--border-color-base` | 基础边框色 | #DCDFE6 |
| `$--font-size-base` | 基础字号 | 14px |

---

## 注意事项

- 修改 `$--font-path` 后需重启开发服务器
- 生产环境建议预编译主题
- 避免频繁切换主题影响性能
