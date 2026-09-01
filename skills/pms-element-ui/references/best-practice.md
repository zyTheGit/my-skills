# 最佳实践

> 项目配置统一管理与工具函数组织

---

## 核心特性

- 统一配置文件
- 工具函数模块化
- 便于维护扩展

---

## 统一配置文件

创建 `config/index.js`：

```javascript
export default {
  // 主题配置
  theme: {
    primary: '#409EFF',
    success: '#67C23A',
    warning: '#E6A23C',
    danger: '#F56C6C',
    info: '#909399'
  },

  // 表格配置
  table: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50, 100]
  },

  // 上传配置
  upload: {
    maxSize: 20,
    accept: {
      image: '.jpg,.jpeg,.png,.gif',
      document: '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx',
      excel: '.xls,.xlsx'
    }
  }
}
```

---

## 工具函数统一管理

### 目录结构

```
utils/
├── index.js          # 统一导出
├── format.js         # 格式化函数
├── validate.js       # 验证函数
└── permission.js     # 权限函数
```

### 统一导出

```javascript
// utils/index.js
import * as format from './format'
import * as validate from './validate'
import * as permission from './permission'

export default { format, validate, permission }
```

---

## 使用示例

```javascript
import utils from '@/utils'

utils.format.formatDate(new Date())
utils.validate.isEmail('test@example.com')
utils.permission.checkPermission('user:add')
```

---

## 注意事项

- 配置文件集中管理，便于切换环境
- 工具函数按职责分类，避免单文件过大
- 统一入口导出，简化导入路径