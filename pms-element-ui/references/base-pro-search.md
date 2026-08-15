# BaseProSearch 高级搜索

## 核心特性

- 通过 `columns` 配置自动渲染搜索项
- 支持展开/收起、联动等功能
- 支持 PageHeader 标题

## 基础用法

```vue
<el-base-pro-search
  :columns="columns"
  :model.sync="searchForm"
  @search="handleSearch"
  @reset="handleReset"
/>
```

## PageHeader 标题

```vue
<el-base-pro-search
  show-page-header
  :page-header="{ title: '返回', content: '用户详情' }"
  :columns="columns"
  @back="handleBack"
  @search="handleSearch"
/>
```

## 搜索项联动

```javascript
columns: [
  {
    title: '省份', dataIndex: 'province', search: {
      type: 'Select', options: [...], linkage: [{ reset: ['city'], fetch: (value) => Promise.resolve(cityMap[value]) }]
    }
  },
  {
    title: '城市', dataIndex: 'city', search: {
      type: 'Select', disabled: (model) => !model.province
    }
  }
]
```

## 搜索组件类型

| 类型 | 说明 |
|-----|------|
| Input | 输入框 |
| Select | 下拉选择 |
| DatePicker | 日期选择 |
| DateRange | 日期范围 |
| TimePicker | 时间选择 |
| InputNumber | 数字输入 |
| Cascader | 级联选择 |
| Radio | 单选组 |
| Checkbox | 多选组 |
| Switch | 开关 |
| BaseDictionary | 字典 |
| BaseOrgantCascader | 组织机构级联选择 |
