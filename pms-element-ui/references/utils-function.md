# 函数工具函数

> 防抖、节流等高频函数优化工具

---

## 核心特性

- 防抖（Debounce）
- 节流（Throttle）
- 全局 SDK 集成

---

## 防抖

### 概念

在事件停止触发后延迟执行，适用于搜索输入、窗口调整等场景。

### 使用全局 SDK

```javascript
const debouncedFn = window.$utils.debounce(fn, 500)
```

### 自定义防抖函数

```javascript
export function debounce(fn, delay = 300) {
  let timer = null
  return function (...args) {
    clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}
```

### 使用示例

```vue
<template>
  <el-input @input="handleSearch" placeholder="搜索..."></el-input>
</template>

<script>
export default {
  methods: {
    handleSearch: debounce(function (keyword) {
      this.searchApi(keyword)
    }, 500)
  }
}
</script>
```

---

## 节流

### 概念

在指定时间间隔内只执行一次，适用于滚动加载、拖拽等场景。

### 使用全局 SDK

```javascript
const throttledFn = window.$utils.throttle(fn, 500)
```

### 自定义节流函数

```javascript
export function throttle(fn, delay = 300) {
  let lastTime = 0
  return function (...args) {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      fn.apply(this, args)
    }
  }
}
```

### 使用示例

```javascript
window.addEventListener('scroll', throttle(function () {
  this.checkLoadMore()
}, 200))
```

---

## 场景对比

| 场景 | 推荐方案 |
|------|----------|
| 搜索输入 | 防抖 |
| 表单验证 | 防抖 |
| 滚动加载 | 节流 |
| 按钮点击 | 节流 |
| 拖拽事件 | 节流 |

---

## 注意事项

- 防抖需手动清理定时器（组件销毁时）
- 节流首次调用立即执行
- 根据实际场景调整延迟时间