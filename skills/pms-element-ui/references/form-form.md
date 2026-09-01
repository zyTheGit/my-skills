# Form 表单

> 表单容器组件，用于数据收集和表单验证

---

## 核心特性

- 支持数据绑定（`:model`）
- 内置表单验证规则
- 支持自定义验证函数
- 提供完整的表单控制方法

---

## 基础用法

```vue
<el-form :model="form" :rules="rules" ref="form" label-width="120px">
  <el-form-item label="用户名" prop="username">
    <el-input v-model="form.username"></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="password">
    <el-input v-model="form.password" type="password"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="submitForm">提交</el-button>
    <el-button @click="resetForm">重置</el-button>
  </el-form-item>
</el-form>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| model | 表单数据对象 | object | — |
| rules | 表单验证规则 | object | — |
| ref | 引用 | string | — |
| label-width | 标签宽度 | string | — |
| label-position | 标签位置 | left/right/top | right |
| inline | 行内表单模式 | boolean | false |
| size | 组件尺寸 | medium/small/mini | — |
| disabled | 禁用全部表单项 | boolean | false |

---

## 表单验证规则

| 规则 | 说明 |
|-----|------|
| required | 必填项 |
| min / max | 最小/最大值 |
| length | 长度限制 |
| type | 类型（email, url, number 等）|
| pattern | 正则表达式 |
| validator | 自定义验证函数 |

```javascript
rules: {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '格式不正确', trigger: 'blur' }
  ]
}
```

---

## 常用方法

| 方法 | 说明 |
|-----|------|
| validate | 整个表单验证 |
| validateField | 部分字段验证 |
| resetFields | 重置表单 |
| clearValidate | 清除验证状态 |

```javascript
this.$refs.form.validate((valid) => {
  if (valid) {
    // 验证通过
  }
});
```

---

## 注意事项

- `prop` 必须与 `rules` 中的字段名对应
- `trigger` 建议使用 `blur` 或 `change`
- 重置前需先设置初始值