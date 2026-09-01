# URL 工具函数

> URL 查询参数解析与构建工具

---

## 核心特性

- 解析查询参数
- 构建查询字符串
- 全局 SDK 集成

---

## 解析查询参数

### 使用全局 SDK

```javascript
const params = window.$utils.parseQuery(url)
```

### 自定义解析函数

```javascript
export function parseQuery(url = window.location.href) {
  const query = {}
  const search = url.split('?')[1]

  if (search) {
    search.split('&').forEach(param => {
      const [key, value] = param.split('=')
      query[decodeURIComponent(key)] = decodeURIComponent(value || '')
    })
  }

  return query
}
```

### 使用示例

```javascript
const url = 'https://example.com?page=1&sort=name'
const params = parseQuery(url)
// { page: '1', sort: 'name' }
```

---

## 构建查询字符串

### 使用全局 SDK

```javascript
const queryString = window.$utils.buildQuery(params)
```

### 自定义构建函数

```javascript
export function buildQuery(params) {
  return Object.keys(params)
    .filter(key => params[key] !== null && params[key] !== undefined)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&')
}
```

### 使用示例

```javascript
const params = { page: 1, sort: 'name', keyword: 'test' }
const queryString = buildQuery(params)
// "page=1&sort=name&keyword=test"
```

---

## 完整示例

```javascript
// 获取当前页面参数
const currentParams = parseQuery()

// 合并新参数
const newParams = { ...currentParams, page: 2 }

// 构建新 URL
const newUrl = `${window.location.pathname}?${buildQuery(newParams)}`
```

---

## 注意事项

- 参数值需进行 URL 编码
- 空值和 undefined 会被过滤
- 特殊字符需正确处理