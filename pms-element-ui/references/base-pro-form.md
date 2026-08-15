# BaseProForm 高级表单

## 核心特性

- 支持查看（view）、新增（add）、编辑（edit）三种模式
- 与 BaseProTable 共享 columns 配置
- 内置抽屉容器
- 支持分组展示、字段脱敏、自定义渲染

## 默认布局

- **抽屉模式**：默认一行显示一个表单字段（span=24）
- **内联模式**：默认一行最多显示三个表单字段（span=8）

## 基础用法

```vue
<el-base-pro-form
  :visible.sync="visible"
  :mode="mode"
  :columns="columns"
  :initial-values="formData"
  @submit="handleSubmit"
  @cancel="handleCancel"
/>
```

## 表单分组

```javascript
columns: [
  { title: '姓名', dataIndex: 'name', form: { type: 'Input', group: '基本信息', order: 1 } },
  { title: '年龄', dataIndex: 'age', form: { type: 'InputNumber', group: '基本信息', order: 2 } },
  { title: '手机号', dataIndex: 'phone', form: { type: 'Input', group: '联系方式', order: 1, desensitize: { type: 'phone' } } }
]
```

## 字段联动

**优先使用 `form.show`** 控制字段显隐，复杂联动使用 `form.linkage`：

```javascript
{ title: '用户类型', dataIndex: 'userType', form: { type: 'Radio', options: [...] } },
{ title: '姓名', dataIndex: 'name', form: { type: 'Input', show: (model) => model.userType === 'personal' } },
{ title: '公司名称', dataIndex: 'companyName', form: { type: 'Input', show: (model) => model.userType === 'company' } }
```

## 内联模式

```vue
<!-- 抽屉模式 -->
<el-base-pro-form :drawer="true" mode="add" :columns="columns" />

<!-- 内联模式 -->
<el-base-pro-form :drawer="false" mode="edit" :columns="columns" />
```

## 查看模式（内联）

```vue
<el-base-pro-form
  :drawer="false"
  mode="view"
  :isInline="true"
  :columns="columns"
  :initial-values="formData"
  :view-column="3"
  :view-responsive="true"
  :view-border="true"
/>
```

**查看模式规则**：
1. `view-column` 表示期望列数上限（1-3）
2. `view-responsive=true` 时按容器宽度自适应
3. 标签列默认固定宽度 `164px`
4. 多列场景最小宽度为 `533px`
