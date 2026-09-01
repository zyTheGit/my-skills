# 权限函数与路由守卫

> 函数式权限判断与路由级权限控制

---

## 核心特性

- 函数式权限判断
- 支持任意/全部权限校验
- 路由级权限拦截

---

## 权限函数

### 基础权限检查

```javascript
export function checkPermission(permission) {
  const permissions = store.getters && store.getters.permissions
  return permissions.includes(permission)
}
```

### 任意权限检查

```javascript
export function checkAnyPermission(permissions) {
  return permissions.some(permission => checkPermission(permission))
}
```

### 全部权限检查

```javascript
export function checkAllPermissions(permissions) {
  return permissions.every(permission => checkPermission(permission))
}
```

---

## 组件中使用

```vue
<template>
  <div>
    <el-button v-if="hasAddPermission" @click="handleAdd">新增</el-button>
    <el-button v-if="hasEditPermission" @click="handleEdit">编辑</el-button>
  </div>
</template>

<script>
import { checkPermission } from '@/utils/permission'

export default {
  computed: {
    hasAddPermission() {
      return checkPermission('user:add')
    },
    hasEditPermission() {
      return checkPermission('user:edit')
    }
  }
}
</script>
```

---

## 路由权限守卫

```javascript
router.beforeEach(async (to, from, next) => {
  const hasPermission = checkRoutePermission(to)

  if (hasPermission) {
    next()
  } else {
    next({ path: '/403' })
  }
})
```

### 路由元信息配置

```javascript
{
  path: '/admin',
  meta: { permission: 'admin' },
  component: AdminLayout
}
```

---

## 注意事项

- 权限列表应在登录后获取并存储
- 路由守卫需处理异步权限加载
- 建议配合刷新令牌机制维护权限状态