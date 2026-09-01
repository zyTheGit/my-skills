# Typography 排版规范

> Element UI 跨操作系统的统一字体标准

---

## 核心特性

- 统一字体族定义
- 六级字号规范
- 四级行高标准
- 纯设计参考（非 Vue 组件）

---

## 字体族

```
"Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif
```

---

## 字号规范

| 级别 | SCSS 变量 | 默认值 | 用途 |
|------|-----------|--------|------|
| Extra Small | `$--font-size-extra-small` | 12px | 辅助文字 |
| Small | `$--font-size-small` | 13px | 正文小号 |
| Base | `$--font-size-base` | 14px | 正文 |
| Medium | `$--font-size-medium` | 16px | 副标题 |
| Large | `$--font-size-large` | 18px | 标题 |
| Extra Large | `$--font-size-extra-large` | 20px | 主标题 |

---

## 行高级别

| 级别 | 值 | 适用场景 |
|------|-----|----------|
| 无行高 | 1 | 标题、按钮 |
| 紧凑 | 1.3 | 表格、列表 |
| 正常 | 1.5 | 正文段落 |
| 宽松 | 1.7 | 长文阅读 |

---

## 代码示例

```scss
// 使用 SCSS 变量
.title {
  font-size: $--font-size-large;
  line-height: 1.5;
}

.subtitle {
  font-size: $--font-size-medium;
  line-height: 1.3;
}
```

```javascript
// 通过全局 SDK 自定义
window.userThemeConfig.global = {
  fontSizeBase: 14,
  fontSizeSmall: 13,
  fontSizeLarge: 18
}
```

---

## 注意事项

- 字号通过 SCSS 变量驱动，可通过 `window.userThemeConfig.global` 自定义
- 本规范为设计参考，非 Vue 组件
- 不同操作系统字体渲染略有差异
