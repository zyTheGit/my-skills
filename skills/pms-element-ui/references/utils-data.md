# 数据处理工具函数

> 深拷贝、空值判断等数据操作工具

---

## 核心特性

- 安全的深拷贝
- 空值判断
- 类型安全

---

## 深拷贝

### 使用全局 SDK

```javascript
const copy = window.$utils.deepClone(original)
```

### 自定义深拷贝

```javascript
export function deepClone(obj) {
  // 基础类型直接返回
  if (obj === null || typeof obj !== 'object') return obj

  // 特殊对象类型
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof RegExp) return new RegExp(obj)

  // 递归克隆
  const clone = Array.isArray(obj) ? [] : {}
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key])
    }
  }
  return clone
}
```

### 使用示例

```javascript
const original = { name: 'test', data: [1, 2, 3] }
const copy = deepClone(original)

copy.name = 'modified'
console.log(original.name) // 'test'（互不影响）
```

---

## 空值判断

### 使用全局 SDK

```javascript
window.$utils.isEmpty(value)
```

### 自定义判断函数

```javascript
export function isEmpty(value) {
  return value === null || value === undefined || value === ''
}

// 扩展：判断空对象
export function isObjectEmpty(obj) {
  return isEmpty(obj) || Object.keys(obj).length === 0
}

// 扩展：判断空数组
export function isArrayEmpty(arr) {
  return isEmpty(arr) || arr.length === 0
}
```

---

## 注意事项

- 深拷贝对循环引用会栈溢出
- 大对象深拷贝性能较差
- 考虑使用结构化克隆 API
