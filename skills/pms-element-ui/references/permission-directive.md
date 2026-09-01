# 权限指令 v-permission

> 基于 Vue 指令的按钮级权限控制

---

## 核心特性

- 声明式权限控制
- 无权限自动移除元素
- 支持单权限和多权限

---

## 注册指令

```javascript
// main.js
Vue.directive('permission', {
  inserted: function (el, binding, vnode) {
    const { value } = binding
    const permissions = store.getters && store.getters.permissions

    if (value && !permissions.includes(value)) {
      el.parentNode && el.parentNode.removeChild(el)
    }
  }
})
```

---

## 基础用法

### 单权限

```vue
<el-button v-permission="'user:add'">新增用户</el-button>
<el-button v-permission="'user:edit'">编辑用户</el-button>
<el-button v-permission="'user:delete'">删除用户</el-button>
```

### 多权限（数组形式）

```vue
<el-button v-permission="['admin', 'editor']">管理内容</el-button>
```

---

## 权限命名规范

| 模块 | 权限标识 | 说明 |
|------|----------|------|
| 用户管理 | user:add | 新增用户 |
| 用户管理 | user:edit | 编辑用户 |
| 用户管理 | user:delete | 删除用户 |
| 角色管理 | role:add | 新增角色 |
| 菜单管理 | menu:view | 查看菜单 |

---

## 完整示例

```vue
<template>
  <div>
    <el-button v-permission="'user:add'" @click="handleAdd">新增</el-button>
    <el-button v-permission="'user:edit'" @click="handleEdit">编辑</el-button>
    <el-button v-permission="'user:delete'" @click="handleDelete">删除</el-button>
  </div>
</template>
```

---

## 注意事项

- 指令在元素插入 DOM 后执行
- 无权限时元素会被直接移除，不会隐藏
- 建议配合后端权限接口动态返回权限列表
