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

### 联动规则速查

| 场景 | 推荐写法 |
|------|----------|
| 只做显隐控制 | 使用 `form.show`，不要引入 `linkage` |
| 单字段变化后清空下游字段并刷新选项 | 使用对象写法：`set + clearOptions + fetch + optionsKey` |
| 初始化加载选项，仅一条时自动选中并触发下游 | 使用 `trigger: 'init'` + `afterFetch` 中的 `ctx.setFieldValue` |
| 编辑/查看回显时也要自动执行一次联动 | 使用 `immediate: true` 或 `trigger: ['change', 'init']` |
| 依赖多个字段共同决定结果 | 使用 `watch` + `when` |
| 需要串行执行多个动作或复杂异步流程 | 使用 `run(ctx)` |

### 初始化时自动选中唯一选项并触发下游联动

第一个下拉的选项通过 `trigger: 'init'` 在表单初始化时加载；当接口只返回一条数据时，在 `afterFetch` 里用 `ctx.setFieldValue` 自动选中。联动上下文中的 `setFieldValue` 默认会继续触发后续联动，因此第二个下拉的选项加载会自动执行。

```javascript
{
  dataIndex: 'deviceType',
  title: '设备类型',
  form: {
    type: 'Select',
    optionsKey: 'autoSelectTypeOptions',
    linkage: {
      trigger: 'init',
      optionsKey: 'autoSelectTypeOptions',
      fetch: () => this.fetchDeviceTypes(),
      afterFetch: (options, ctx) => {
        // 只有一条数据时默认选中；!ctx.ownerValue 避免覆盖编辑回显的已有值
        if (options.length === 1 && !ctx.ownerValue) {
          ctx.setFieldValue(ctx.ownerField, options[0].value);
        }
      }
    }
  }
},
{
  dataIndex: 'deviceModel',
  title: '设备型号',
  form: {
    type: 'Select',
    optionsKey: 'autoSelectModelOptions',
    linkage: {
      watch: 'deviceType',
      set: () => ({ deviceModel: undefined }),
      optionsKey: 'autoSelectModelOptions',
      fetch: (value) => {
        // 清空设备类型时不发请求，只清空型号选项
        if (!value) return [];
        return this.fetchDeviceModels(value);
      }
    }
  }
}
```

清空第一个下拉时不会再触发请求，可按需调整：

- `if (!value) return []`：清空时第二个下拉的值和选项都被清掉，但不发请求；
- 加 `when: (ctx) => !!ctx.value`：清空时整条规则跳过，第二个下拉保持原样；
- 把 `set` 和 `fetch` 拆成两条规则：实现只清值、保留选项。

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
