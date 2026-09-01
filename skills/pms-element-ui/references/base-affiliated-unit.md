# BaseAffiliatedUnit 所属单位选择器

**功能说明**：用于选择所属单位的弹窗组件，基于 `el-base-pro-table` 实现单选功能。

## 基础用法

点击输入框打开弹窗，在表格中选择单位后点击确定。

```vue
<template>
  <div>
    <el-base-affiliated-unit
      v-model="selectedUnit"
      placeholder="请选择所属单位"
      @change="handleChange"
    />
    <p v-if="selectedUnit" style="margin-top: 10px;">已选择: {{ selectedUnit }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedUnit: ''
    };
  },
  methods: {
    handleChange(row) {
      console.log('选中的行数据:', row);
    }
  }
};
</script>
```

## 自定义列配置

可以通过 `columns` 属性自定义表格列。

```vue
<el-base-affiliated-unit
  v-model="selectedUnit"
  :columns="customColumns"
  label-key="name"
  value-key="id"
  placeholder="请选择单位"
  @change="handleChange"
/>
```

## 禁用状态

通过 `disabled` 属性禁用组件。

```vue
<el-base-affiliated-unit
  v-model="selectedUnit"
  disabled
  placeholder="禁用状态"
/>
```

## 自定义请求地址

通过 `url` 和 `api-params` 自定义数据请求。

```vue
<el-base-affiliated-unit
  v-model="selectedUnit"
  url="/api/custom/units"
  :api-params="{ type: 'company' }"
  placeholder="请选择单位"
  @change="handleChange"
/>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| value / v-model | 绑定值 | string / number / object | - | - |
| label-key | 显示文本对应的字段名 | string | - | orgName |
| value-key | 值对应的字段名 | string | - | orgCode |
| placeholder | 输入框占位符 | string | - | 请选所属单位 |
| disabled | 是否禁用 | boolean | true / false | false |
| size | 输入框尺寸 | string | medium/small/mini | - |
| clearable | 是否可清空 | boolean | true / false | true |
| dialog-title | 弹窗标题 | string | - | 选择单位 |
| dialog-width | 弹窗宽度 | string | - | 800px |
| append-to-body | 是否将弹窗插入到 body | boolean | true / false | true |
| url | 数据请求地址 | string | - | /common-user/client/org/page |
| api-params | 额外的请求参数 | object | - | {} |
| table-height | 表格高度 | string / number | - | 400 |
| search-placeholder | 搜索框占位符 | string | - | 请输入关键词搜索 |
| columns | 自定义表格列配置 | array | - | 默认显示序号、组织机构代码、企业名称 |

## Events

| 事件名称 | 说明 | 回调参数 |
|----------|------|----------|
| change | 选中值变化时触发 | 选中的行数据 |
| input | v-model 更新时触发 | 绑定的值 |

## Methods

| 方法名 | 说明 | 参数 |
|--------|------|------|
| refresh | 刷新表格数据 | - |
| getSelectedRow | 获取选中的行数据 | - |
| fetchData | 获取表格数据（内部使用） | params |

## 注意事项

- 默认请求地址为 `/common-user/client/org/page`
- 支持自定义列配置和请求地址
- 选中后返回整行数据对象
