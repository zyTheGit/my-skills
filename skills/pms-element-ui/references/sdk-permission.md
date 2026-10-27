# Min-Web3 SDK - 权限与校验

### window.$permission - 权限 SDK

统一的权限校验工具，支持按钮级权限控制。

**check(permission) - 检查单个权限**

```javascript
if (window.$permission.check('user:add')) {
  // 显示添加按钮
}
```

**checkAny(permissions) - 检查任一权限**

```javascript
if (window.$permission.checkAny(['user:add', 'user:edit'])) {
  // 显示操作按钮
}
```

**checkAll(permissions) - 检查所有权限**

```javascript
if (window.$permission.checkAll(['user:view', 'user:edit', 'user:delete'])) {
  // 显示高级管理功能
}
```

**在 Vue 组件中使用**

```vue
<template>
  <el-button v-if="hasAddPermission" @click="handleAdd">新增</el-button>
</template>

<script>
export default {
  computed: {
    hasAddPermission() {
      return window.$permission?.check('user:add') ?? false;
    }
  }
}
</script>
```

**权限指令**

```vue
<el-button v-permission="'user:add'">新增</el-button>
```

**权限码命名规范**

```javascript
'user:view'    // 查看用户
'user:add'     // 新增用户
'user:edit'    // 编辑用户
'user:delete'  // 删除用户
'order:export' // 导出订单
```

---

### 表单校验工具

`window.$utils.validators` 提供统一的表单校验逻辑：

**校验手机号**

```javascript
window.$utils.validators.validatePhone('13800138000');   // true
```

**校验身份证号**

```javascript
window.$utils.validators.validateIdCard('11010519491231002X');
```

**校验邮箱**

```javascript
window.$utils.validators.validateEmail('demo@example.com'); // true
```

**校验密码强度**

```javascript
const result = window.$utils.validators.validatePasswordStrength('Abc123!@#xyz');
// {
//   valid: false,
//   rules: {
//     length: true,
//     complexity: true,
//     noSequence: false
//   }
// }
```

校验规则：
- 长度需为 **10-20 位**
- 必须同时包含 **大写字母 / 小写字母 / 数字 / 特殊字符**
- 不能包含常见简单序列（如 `123`、`abc`、`qwerty`、`password` 等）

---

### 最佳实践

**1. 安全访问全局对象**

```javascript
// 推荐：使用可选链
window.$utils?.openTab(tab);
window.$permission?.check('user:add');

// 或者先检查环境
if (window.__POWERED_BY_QIANKUN__ && window.$utils) {
  window.$utils.openTab(tab);
}
```

**2. 标签页命名规范**

```javascript
// 推荐：使用 业务名-唯一标识 格式
const tabName = `user-detail-${userId}`;
const tabName = `order-edit-${orderId}`;

// 列表页可以使用固定名称
const tabName = 'user-list';
```

**3. 事件类型命名规范**

```javascript
// 推荐：使用 模块:动作 格式
'route:restore'     // 路由恢复
'route:update'      // 路由更新
'message:fromApp'   // 来自子应用的消息
```
