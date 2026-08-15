# 格式化工具函数

> 日期、数字、金额格式化工具

---

## 核心特性

- 日期格式化
- 数字千分位
- 金额格式化
- 全局 SDK 集成

---

## 日期格式化

### 使用全局 SDK

```javascript
window.$utils.formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss')
```

### 自定义格式化函数

```javascript
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}
```

---

## 数字格式化

### 千分位格式化

```javascript
export function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 示例
formatNumber(1234567) // "1,234,567"
```

### 金额格式化

```javascript
export function formatMoney(amount, symbol = '¥', precision = 2) {
  return symbol + parseFloat(amount).toFixed(precision).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 示例
formatMoney(1234567.89) // "¥1,234,567.89"
```

---

## 常用格式模板

| 模板 | 输出示例 |
|------|----------|
| `YYYY-MM-DD` | 2024-01-15 |
| `YYYY-MM-DD HH:mm:ss` | 2024-01-15 10:30:00 |
| `YYYY年MM月DD日` | 2024年01月15日 |
| `HH:mm:ss` | 10:30:00 |

---

## 注意事项

- 日期输入需验证有效性
- 金额计算注意精度问题
- 时区处理需统一标准
