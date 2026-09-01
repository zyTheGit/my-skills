### BaseProTable 高级表格

**功能说明**：通过 columns 配置自动渲染搜索栏和表格列，集成搜索、分页、工具栏、列设置、数据请求、列宽规则、字典映射、操作列权限、视图切换等功能。

**基础用法**：

```vue
<el-base-pro-table
  :columns="columns"
  :request="fetchData"
  show-index
  show-single-selection
  :search-model.sync="searchForm"
  :enable-column-rules="true"
  @request-success="onSuccess"
/>
```

```javascript
// request 接收 { page, pageSize, ...搜索参数, sort, order }，返回 { data, total, success }
columns: [
  { title: '名称', dataIndex: 'name', search: true, width: 160 },
  { title: '状态', dataIndex: 'status', valueType: 'tag',
    valueEnum: { 1: { text: '正常', status: 'success' } },
    search: { type: 'Select', options: [{ label: '正常', value: 1 }] } },
  { title: '金额', dataIndex: 'amount', valueType: 'money', fieldProps: { symbol: '¥', precision: 2 } }
]
```

**常用属性**：
| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| columns | 列配置数组 | Array | [] |
| data | 表格数据（手动模式） | Array | [] |
| request | 数据请求函数（自动模式）【新】 | Function(params) | null |
| url | 请求 URL（自动模式） | String | '' |
| manual | 是否手动触发请求 | Boolean | false |
| default-params | 默认请求参数 | Object | {} |
| params-mapping | 参数映射配置 | Object | 见注意事项 |
| response-mapping | 响应映射配置 | Object | 见注意事项 |
| before-request | 请求前转换参数 | Function(params) | null |
| data-transform | 数据转换函数 | Function(data) | null |
| on-request-success | 请求成功回调 | Function(data, response) | null |
| on-request-error | 请求失败回调 | Function(error) | null |
| total | 数据总数（手动模式） | Number | 0 |
| table-title | 表格标题 | String | '' |
| show-search | 是否显示搜索区域 | Boolean | true |
| search-model | 搜索表单数据（.sync） | Object | {} |
| search-default-row-count | 搜索收起时显示行数 | Number | 1 |
| search-show-page-header | 搜索栏显示 PageHeader | Boolean | false |
| empty-text | 全局空值显示文本 | String | '-' |
| height / max-height | 表格高度 / 最大高度 | String/Number | - |
| stripe | 是否斑马纹 | Boolean | false |
| border | 是否显示边框 | Boolean | true |
| row-key | 行唯一标识 | String/Function | - |
| enable-column-rules | 是否启用内置列宽规则 | Boolean | true |
| column-rules | 列宽规则配置 | Object | 见注意事项 |
| show-selection | 是否显示复选框列 | Boolean | false |
| show-single-selection | 是否显示单选列 | Boolean | false |
| selectable | 复选框可选判断 | Function(row, index) | - |
| single-selectable | 单选框可选判断 | Function(row, index) | - |
| selectionProps | 复选框 props | Object | - |
| show-index | 是否显示序号列 | Boolean | false |
| index-label / index-width / index-fixed | 序号列标题 / 宽度 / 固定 | String/Number/Boolean | 序号/60/false |
| index-method | 序号计算方法 | Function(index) | - |
| show-actions | 是否显示操作列 | Boolean | false |
| actions | 操作列按钮配置 | Array | [] |
| actions-max | 操作按钮最大显示数（0 禁用折叠） | Number | 3 |
| actions-more-trigger | 折叠触发方式（hover/click） | String | hover |
| show-pagination | 是否显示分页 | Boolean | true |
| current-page / page-size | 当前页码 / 每页条数（.sync） | Number | 1 / 10 |
| page-sizes | 每页条数选项 | Array | [10,20,50,100] |
| pagination-layout | 分页布局 | String | prev,pager,next,jumper,sizes |
| show-toolbar | 是否显示工具栏 | Boolean | true |
| show-density | 是否显示密度切换 | Boolean | true |
| show-column-setting | 是否显示列设置 | Boolean | true |
| show-fullscreen-btn | 是否显示全屏按钮 | Boolean | true |
| show-view-switcher | 是否显示视图切换按钮 | Boolean | false |
| view-mode | 当前视图模式 table/card（.sync） | String | '' |
| is-in-dialog | 弹框中样式 | Boolean | false |

**Column 配置项**：
| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| dataIndex | 数据字段名（必填） | String | - |
| title | 列标题 | String | - |
| width / minWidth | 列宽度 / 最小宽度 | String/Number | - |
| fixed | 固定列（true/false/left/right） | Boolean/String | false |
| hideInTable | 是否在表格中隐藏（仍可用于搜索） | Boolean | false |
| ellipsis / lineClamp | 是否省略显示 / 多行截断行数 | Boolean/Number | false |
| ruleType | 列规则类型（启用列宽规则时生效） | String | auto |
| nowrap | 强制不换行（启用列宽规则时生效） | Boolean | false |
| valueType | 展示类型（text/tag/link/image/switch/progress/date/money/index） | String | text |
| valueEnum | 值枚举映射，支持简写/完整格式 | Object | - |
| valueDict | 字典映射配置（异步加载）【新】 | Object | - |
| fieldProps | valueType 组件属性 | Object | - |
| onClick | 点击回调（link/switch） | Function(row, index) | - |
| sortable | 是否可排序（true/false/custom） | Boolean/String | false |
| filters / filterMethod | 筛选选项 / 筛选方法 | Array/Function | - |
| filterType / filterPlaceholder / filterHighlight | 表头筛选类型（search=关键字筛选）、占位文本、是否高亮 | String/String/Boolean | select/输入关键字/true |
| formatter | 格式化函数 | Function(row, column, cellValue, index) | - |
| render | 自定义渲染函数 | Function(h, {row, column, $index}) | - |
| search | 搜索配置（true 或对象） | Boolean/Object | false |
| component / componentProps / componentEvents | 自定义单元格组件 / props / 事件 | VueComponent/Object | - |

**search 配置项**：
| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| type | 搜索组件类型（Input/Select/DatePicker/DateRange/TimePicker/InputNumber/Cascader/Radio/Checkbox/Switch） | String | Input |
| field | 搜索字段名 | String | dataIndex |
| title | 搜索标签 | String | column.title |
| options | 选项数据（Select/Radio/Checkbox） | Array/Function | - |
| props | 组件属性 | Object | - |
| defaultValue | 默认值 | any | - |
| placeholder | 占位文本 | String | - |
| order | 排序顺序 | Number | - |
| span | 占用列数 | Number | - |
| show | 是否显示 | Boolean/Function(model) | true |
| disabled | 是否禁用 | Boolean/Function(model) | false |
| linkage | 联动配置（数组含 reset/optionsKey/fetch，或函数） | Array/Function | - |

**Action 配置项**：
| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| label | 按钮文字 | String/Function(row, index) | - |
| type | 按钮类型 | String | text |
| icon | 图标 | String | - |
| disabled | 是否禁用 | Boolean/Function(row, index) | false |
| loading | 是否加载中 | Boolean | false |
| show | 是否显示 | Boolean/Function(row, index) | true |
| permission | 权限校验配置（String/Array/Object/Function），无权限时隐藏 | String/Array/Object/Function | - |
| permissionMode | 数组权限校验方式（any/all） | String | any |
| props | 透传给 el-button 的属性 | Object | - |
| fontColor | 按钮文字颜色 | String | - |
| onClick | 点击事件 | Function(row, index) | - |

**常用事件**：
| 事件名 | 说明 | 参数 |
|--------|------|------|
| search | 搜索事件 | searchForm |
| reset | 重置事件 | searchForm |
| back | 返回事件 | - |
| selection-change | 选择项变化 | selection |
| single-selection-change | 单选变化 | row |
| sort-change | 排序变化 | { column, prop, order } |
| pagination-change | 分页变化（含 size-change、current-change） | { page, size } |
| search-field-change | 搜索字段变化 | { field, dataIndex, value, column, model } |
| search-expand-change | 搜索展开/收起 | expanded |
| link-click | link 点击 | { column, row, index } |
| switch-change | switch 变化 | { column, row, value, index } |
| action-click | 操作按钮点击 | { action, row, index } |
| refresh / reload | 手动刷新 / 手动重载 | - |
| request-success | 请求成功 | (data, response) |
| request-error | 请求失败 | error |
| density-change | 密度切换 | density |
| column-setting-change | 列设置变化 | config |
| view-change | 视图切换 | viewMode |

**常用方法**：
| 方法名 | 说明 | 参数 |
|--------|------|------|
| refresh | 刷新当前页数据 | - |
| reload | 重置到第一页并刷新 | - |
| runRequest | 手动触发请求 | params |
| getSelectedRows / clearSelection | 获取选中行 / 清空选择 | - |
| toggleRowSelection / toggleAllSelection | 切换某行选中 / 切换全选 | (row, selected) |
| toggleRowExpansion | 切换某行展开 | (row, expanded) |
| setCurrentRow | 设置当前行 | row |
| clearSort / clearFilter | 清除排序 / 清除筛选 | columnKeys |
| sort | 手动排序 | (prop, order) |
| doLayout | 重新布局表格 | - |
| getSearchModel / setSearchModel | 获取 / 设置搜索表单数据 | model |
| setSingleSelectionValue | 设置单选模式当前选中值 | value |
| clearSearchModel | 清空搜索表单但不触发 reset 事件 | - |
| getColumnSettingConfig / setColumnSettingConfig | 获取 / 设置列设置配置 | config |
| getDictService | 获取字典服务实例 | - |
| getTableRef / getSearchRef | 获取 el-table / 搜索组件引用 | - |

**插槽**：
| 插槽名 | 说明 | 作用域参数 |
|--------|------|------------|
| tableTitle | 表格标题 | - |
| tableTitleExtra | 标题额外区域 | - |
| toolbar | 工具栏 | - |
| header-{dataIndex} | 自定义表头 | { column, index } |
| {dataIndex} / column-{dataIndex} | 自定义列内容 | { row, column, $index, config } |
| actions | 自定义操作列 | { row, $index, column } |
| empty | 空数据内容 | - |
| pageHeaderContent | 搜索栏标题内容 | - |
| searchActions | 搜索栏操作按钮 | - |
| search-{field} | 自定义搜索项（field 优先 search.field，否则 dataIndex） | { column, model, value, setValue } |
| paginationLeft | 分页器左侧插槽 | - |
| cardList | 卡片视图内容（需配合 show-view-switcher） | { data, loading, columns } |

**注意事项**：
- params-mapping 默认 { current:'page', pageSize:'pageSize', search:null, sort:'sort', order:'order' }；response-mapping 默认 { data:'data', total:'total', success:'success' }
- column-rules 默认：fewColumnThreshold:4, charsFewColumns:32, charsManyColumns:22, charsSmallScreen:18, smallScreenBreakpoint:1366, textMinWidth:248, textMaxWidth:384, defaultLineClamp:2
- valueType 支持 text/tag/link/image/switch/progress/date/money/number/index；映射优先级 valueDict > valueEnum > formatter；ruleType 可选 auto/long-text/nowrap/operation/status/code/datetime/short-name；列宽规则：少列(≤4)建议30-35字，多列20-25字，小屏15-20字，文字最多2行超出显示省略号+提示
- 弹框中：el-dialog 设 custom-class="table-in-dialog"，无工具栏设 :show-toolbar="false"；permission 支持 String/Array/{menuCode,buttonCode}/Function(row,index)，无 window.$permission 时默认放行；其他 el-table 原生属性/事件透传，搜索栏属性加 search 前缀
**参考文档**：C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-pro-table.md
