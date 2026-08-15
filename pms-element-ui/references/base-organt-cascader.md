# BaseOrgantCascader 组织机构级联选择器

**功能说明**：基于组织架构的级联选择器，支持单选、多选和搜索过滤。

## 基础用法

```vue
<template>
  <div>
    <el-base-organt-cascader
      v-model="selectedOrgant"
      :api-params="apiParams"
      filterable
      clearable
      placeholder="请选择组织机构"
      @change="handleChange"
    />
    <p v-if="selectedOrgant">已选择: {{ selectedOrgant }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedOrgant: null,
      apiParams: { id: '-1' }
    };
  },
  methods: {
    handleChange(val, selectedOptions) {
      console.log('选中值:', val);
      console.log('选中选项:', selectedOptions);
    }
  }
};
</script>
```

## 多选用法

```vue
<el-base-organt-cascader
  v-model="selectedOrgants"
  :api-params="apiParams"
  :show-all-levels="false"
  :props="{ multiple: true, label: 'orgName', value: 'orgCode', checkStrictly: true }"
  placeholder="请选择组织机构"
  @change="handleChange"
/>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| value / v-model | 绑定值 | - | - | - |
| props | 配置选项 | object | - | `{ label: 'orgName', value: 'orgCode', children: 'children' }` |
| api-params | 请求参数 | object | - | `{id: '-1'}` |
| placeholder | 占位符 | string | - | 请选择 |
| disabled | 是否禁用 | boolean | true / false | false |
| clearable | 是否可清除 | boolean | true / false | false |
| filterable | 是否可搜索 | boolean | true / false | false |
| filter-method | 自定义搜索方法 | function | - | - |
| separator | 选项分隔符 | string | - | / |
| show-all-levels | 是否显示所有级别 | boolean | true / false | true |
| collapse-tags | 是否折叠标签 | boolean | true / false | false |
| popper-class | 下拉菜单的类名 | string | - | - |
| append-to-body | 是否将下拉菜单插入到 body 中 | boolean | true / false | true |

## Props 配置

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| multiple | 是否多选 | boolean | - | false |
| checkStrictly | 是否严格的遵守父子节点不互相关联 | boolean | - | false |
| value | 指定选项的值为选项对象的某个属性值 | string | — | 'orgCode' |
| label | 指定选项标签为选项对象的某个属性值 | string | — | 'orgCode' |
| children | 指定选项的子选项为选项对象的某个属性值 | string | — | 'children' |
| disabled | 指定选项的禁用为选项对象的某个属性值 | string | — | 'disabled' |
| leaf | 指定选项的叶子节点的标志位为选项对象的某个属性值 | string | — | 'leaf' |

## Events

| 事件名称 | 说明 | 回调参数 |
|----------|------|----------|
| change | 当绑定值变化时触发 | (value, selectedOptions) |
| focus | 当获得焦点时触发 | event |
| blur | 当失去焦点时触发 | event |
| expand-change | 当展开节点发生变化时触发 | value |
| visible-change | 当下拉菜单显示/隐藏时触发 | visible |
| remove-tag | 当移除标签时触发 | removedTagValue |

## 注意事项

- 默认从根节点 `id: '-1'` 开始加载
- 多选模式下建议设置 `checkStrictly: true` 实现独立选择
