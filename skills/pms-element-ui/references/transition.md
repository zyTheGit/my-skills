# 过渡动画

> Element UI 内置过渡动画与自定义动画

---

## 核心特性

- 5 种内置过渡动画
- 简洁易用
- 支持自定义扩展

---

## 内置过渡动画

| 动画名称 | 效果描述 |
|----------|----------|
| `el-fade-in-linear` | 线性淡入 |
| `el-fade-in` | 淡入 |
| `el-zoom-in-center` | 中心缩放进入 |
| `el-zoom-in-top` | 顶部缩放进入 |
| `el-zoom-in-bottom` | 底部缩放进入 |

---

## 基础用法

```vue
<template>
  <transition name="el-fade-in-linear">
    <div v-show="visible">内容</div>
  </transition>

  <transition name="el-zoom-in-center">
    <div v-show="visible">内容</div>
  </transition>
</template>
```

---

## 自定义过渡动画

### 淡入淡出

```css
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
```

### 滑动效果

```css
.slide-enter-active, .slide-leave-active {
  transition: all .5s;
}
.slide-enter, .slide-leave-to {
  transform: translateX(100px);
  opacity: 0;
}
```

### 弹跳效果

```css
.bounce-enter-active { animation: bounce-in .5s; }
.bounce-leave-active { animation: bounce-out .5s; }
@keyframes bounce-in {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
@keyframes bounce-out {
  0% { transform: scale(1); }
  100% { transform: scale(0); }
}
```

---

## 使用示例

```vue
<template>
  <transition name="fade">
    <el-alert v-if="showAlert" type="success" @close="showAlert = false">
      操作成功！
    </el-alert>
  </transition>
</template>
```

---

## 注意事项

- 过渡元素需有明确的进入/离开状态
- 复杂动画建议使用 `<transition>` 包裹
- 避免过多动画影响性能