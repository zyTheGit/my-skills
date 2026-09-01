# BaseDictionary 字典下拉框

## 核心特性

- 自动加载数据字典，无需手动请求
- 支持多应用、多字典类型
- 支持缓存机制，减少重复请求
- 可作为独立组件使用

## 基础用法

```vue
<el-base-dictionary
  v-model="value"
  app-code="upms"
  dist-type-code="user_info_sex"
/>
```

## 自定义字典数据

```vue
<el-base-dictionary
  v-model="value"
  :data="[{ label: '男', value: '1' }, { label: '女', value: '0' }]"
/>
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| value / v-model | 绑定值 | string / number | — | — |
| app-code | 应用编码 | string | — | — |
| dist-type-code | 字典类型编码 | string | — | — |
| data | 自定义字典数据 | array | — | — |
| placeholder | 占位文本 | string | — | 请选择 |
| disabled | 是否禁用 | boolean | — | false |
| clearable | 是否可清空 | boolean | — | true |

## Events

| 事件名 | 说明 | 回调参数 |
|-------|------|---------|
| change | 值改变时触发 | value: any |
