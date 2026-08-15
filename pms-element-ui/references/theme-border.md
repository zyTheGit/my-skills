# 主题边框样式

> Element UI 边框、圆角、阴影规范

---

## 核心特性

- 统一的圆角规范
- 分级阴影系统
- 响应式边框设计

---

## 圆角规范

| 类型 | 值 | 应用场景 |
|------|-----|----------|
| 大圆角 | 4px | 卡片容器、弹窗 |
| 小圆角 | 2px | 按钮、输入框 |
| 圆形 | 50% | 头像、图标按钮 |

---

## 阴影规范

### 基础阴影

用于下拉菜单、悬浮提示等轻量浮层：

```css
box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
```

### 浮层阴影

用于对话框、抽屉等大型浮层：

```css
box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
```

---

## 代码示例

```vue
<template>
  <div class="card-container">
    <!-- 大圆角卡片 -->
    <el-card style="border-radius: 4px">
      内容区域
    </el-card>

    <!-- 圆形头像 -->
    <el-avatar shape="circle" :size="40">
      <img src="avatar.png" />
    </el-avatar>
  </div>
</template>
```

```css
/* 自定义阴影 */
.custom-shadow {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* 悬停阴影效果 */
.hover-shadow:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
```

---

## 注意事项

- 阴影不宜过重，避免视觉疲劳
- 圆角保持一致性，同一页面使用相同圆角值
- 深色模式下需调整阴影颜色
