### Table 表格

**功能说明**：用于展示多条结构类似的数据，支持排序、筛选、自定义模板、树形数据、展开行、合计行、新增行飞入动画等特性。

**基础用法**：

```vue
<template>
  <el-table
    stripe
    border
    header-color
    :data="tableData"
    style="width: 100%">
    <el-table-column type="selection" width="48" />
    <el-table-column
      type="index"
      label="序号"
      class-name="serial-numbertext-center"
      width="60" />
    <el-table-column prop="date" label="日期" width="180" />
    <el-table-column prop="name" label="姓名" width="180" />
    <el-table-column prop="address" label="地址" />
    <el-table-column fixed="right" label="操作" width="100">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
```

**新增行飞入动画**：设置 `row-animation` 启用，数据中通过 `_isNew: true` 标识新增行，动画完成后自动清除标识。

```vue
<el-table
  :data="tableData"
  row-animation
  :row-animation-duration="500"
  :row-animation-delay="100"
  @row-animation-end="onAnimationEnd">
  <el-table-column type="index" label="序号" width="60" />
  <el-table-column prop="date" label="日期" width="180" />
  <el-table-column prop="name" label="姓名" width="180" />
  <el-table-column prop="address" label="地址" />
</el-table>
```

**常用属性**：

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| data | 显示的数据 | array | - |
| height | 表格高度，数字单位 px | string/number | - |
| max-height | 表格最大高度 | string/number | - |
| stripe | 是否为斑马纹 | boolean | false |
| border | 是否带纵向边框 | boolean | false |
| size | 表格尺寸（medium/small/mini） | string | - |
| fit | 列宽是否自撑开 | boolean | true |
| show-header | 是否显示表头 | boolean | true |
| highlight-current-row | 是否高亮当前行 | boolean | false |
| highlight-selection-row | 是否高亮复选框选中行（仅 selection 有效）【新】 | boolean | false |
| current-row-key | 当前行的 key，只写属性 | string/number | - |
| row-key | 行数据 Key，用于优化渲染、reserve-selection 及树形数据 | function(row)/string | - |
| row-class-name | 行的 className 回调 | function({row, rowIndex})/string | - |
| row-style | 行的 style 回调 | function({row, rowIndex})/object | - |
| cell-class-name | 单元格 className 回调 | function({row, column, rowIndex, columnIndex})/string | - |
| cell-style | 单元格 style 回调 | function({row, column, rowIndex, columnIndex})/object | - |
| empty-text | 空数据时显示文本，也可通过 `slot="empty"` 设置 | string | 暂无数据 |
| default-expand-all | 是否默认展开所有行 | boolean | false |
| expand-row-keys | 展开行的 keys 数组，需设置 row-key | array | - |
| default-sort | 默认排序列的 prop 和顺序 | object | - |
| tooltip-effect | tooltip effect 属性（dark/light） | string | dark |
| show-summary | 是否在表尾显示合计行 | boolean | false |
| sum-text | 合计行第一列文本 | string | 合计 |
| summary-method | 自定义合计计算方法 | function({ columns, data }) | - |
| span-method | 合并行或列的计算方法 | function({ row, column, rowIndex, columnIndex }) | - |
| select-on-indeterminate | 部分行选中时点击表头多选框的行为 | boolean | true |
| select-on-row-click | 多选表格中是否支持点击行切换选中状态【新】 | boolean | true |
| indent | 树形数据树节点缩进 | number | 16 |
| lazy | 是否懒加载子节点数据 | boolean | - |
| load | 加载子节点数据的函数，lazy 为 true 时生效 | function(row, treeNode, resolve) | - |
| tree-props | 渲染嵌套数据的配置选项 | object | { hasChildren: 'hasChildren', children: 'children' } |
| header-color | 表格头部增加背景灰色【新】 | boolean | false |
| row-animation | 是否启用新增行飞入动画【新】 | boolean | false |
| new-row-key | 标识新增行的字段名【新】 | string | _isNew |
| row-animation-duration | 飞入动画持续时间（毫秒）【新】 | number | 500 |
| row-animation-delay | 多行动画间隔延迟（毫秒）【新】 | number | 50 |
| auto-remove-new-flag | 动画完成后是否自动清除新增标识【新】 | boolean | true |

**Table-column 常用属性**：

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| type | 列类型（selection/index/expand） | string | - |
| index | type=index 时自定义索引 | number/function(index) | - |
| column-key | column 的 key，用于 filter-change 事件标识 | string | - |
| label | 显示的标题 | string | - |
| prop | 对应列内容的字段名 | string | - |
| width | 列的宽度 | string | - |
| min-width | 列最小宽度，按比例分配剩余宽度 | string | - |
| fixed | 列固定在左侧或右侧（true/left/right） | string/boolean | - |
| render-header | 列标题 Label 区域渲染函数 | function(h, { column, $index }) | - |
| sortable | 是否可排序，设为 'custom' 代表远程排序 | boolean/string | false |
| sort-method | 排序方法，仅 sortable 为 true 时有效 | function(a, b) | - |
| sort-by | 指定排序属性 | string/array/function(row, index) | - |
| sort-orders | 排序策略轮转顺序，元素为 ascending/descending/null | array | ['ascending', 'descending', null] |
| resizable | 是否可拖动改变宽度（需 border 为 true） | boolean | true |
| formatter | 格式化内容 | function(row, column, cellValue, index) | - |
| show-overflow-tooltip | 内容过长隐藏时显示 tooltip | boolean | false |
| align | 对齐方式（left/center/right） | string | left |
| header-align | 表头对齐方式 | string | - |
| class-name | 列的 className | string | - |
| label-class-name | 当前列标题的自定义类名 | string | - |
| selectable | 仅 type=selection 有效，决定 CheckBox 是否可勾选 | function(row, index) | - |
| reserve-selection | 数据更新后保留选中（需指定 row-key） | boolean | false |
| filters | 数据过滤选项，元素需有 text 和 value | array[{ text, value }] | - |
| filter-placement | 过滤弹出框定位 | string | - |
| filter-multiple | 过滤选项是否多选 | boolean | true |
| filter-type | 筛选类型，search 显示关键字输入框【新】 | string | select |
| filter-placeholder | 关键字筛选输入框占位文本【新】 | string | 输入关键字 |
| filter-highlight | 关键字筛选后是否高亮对应文字【新】 | boolean | true |
| filter-method | 数据过滤方法 | function(value, row, column) | - |
| filtered-value | 选中的数据过滤项 | array | - |

**常用事件**：

| 事件名 | 说明 | 参数 |
|-----|------|------|
| select | 手动勾选数据行 Checkbox 时触发 | selection, row |
| select-all | 手动勾选全选 Checkbox 时触发 | selection |
| selection-change | 选择项发生变化时触发 | selection |
| cell-mouse-enter | 单元格 hover 进入时触发 | row, column, cell, event |
| cell-mouse-leave | 单元格 hover 退出时触发 | row, column, cell, event |
| cell-click | 单元格被点击时触发 | row, column, cell, event |
| cell-dblclick | 单元格被双击时触发 | row, column, cell, event |
| row-click | 某行被点击时触发 | row, column, event |
| row-contextmenu | 某行被鼠标右键点击时触发 | row, column, event |
| row-dblclick | 某行被双击时触发 | row, column, event |
| header-click | 某列表头被点击时触发 | column, event |
| header-contextmenu | 某列表头被鼠标右键点击时触发 | column, event |
| sort-change | 排序条件发生变化时触发 | { column, prop, order } |
| filter-change | 筛选条件发生变化时触发 | filters |
| current-change | 当前行发生变化时触发 | currentRow, oldCurrentRow |
| header-dragend | 拖动表头改变列宽时触发 | newWidth, oldWidth, column, event |
| expand-change | 行展开或关闭时触发 | row, (expandedRows \| expanded) |
| row-animation-end | 新增行飞入动画播放完成时触发【新】 | row |

**常用方法**：

| 方法名 | 说明 | 参数 |
|-----|------|------|
| clearSelection | 多选表格，清空用户选择 | - |
| toggleRowSelection | 切换某行选中状态 | row, selected |
| toggleAllSelection | 切换所有行选中状态 | - |
| toggleRowExpansion | 切换某行展开状态 | row, expanded |
| setCurrentRow | 单选表格，设定选中行，无参则取消高亮 | row |
| clearSort | 清空排序条件 | - |
| clearFilter | 清空过滤条件，可传 columnKey 数组清除指定列 | columnKey |
| doLayout | 重新布局，隐藏切换为显示时可能需要调用 | - |
| sort | 手动排序 | prop, order |

**插槽**：

| 插槽名 | 说明 | 作用域参数 |
|-----|------|------|
| append | 插入至表格最后一行之后的内容，位于合计行之上 | - |
| empty | 空数据时显示的内容 | - |

**Table-column Scoped Slot**：

| 插槽名 | 说明 | 作用域参数 |
|-----|------|------|
| - | 自定义列内容 | { row, column, $index } |
| header | 自定义表头内容 | { column, $index } |

**注意事项**：

- 使用 `reserve-selection`、树形数据或展开行时，必须设置 `row-key` 属性
- `header-color` 配合序号列 `class-name="serial-numbertext-center"` 可启用新样式表格
- 新增行飞入动画通过数据项设置 `_isNew: true`（字段名可由 `new-row-key` 自定义）标识，动画完成后标识自动清除（可由 `auto-remove-new-flag` 控制）
- 输入框筛选：列设置 `filter-type="search"` 开启，默认按列值包含匹配；若列配置了 `formatter` 则按格式化后文本匹配，可通过 `filter-method` 自定义
- `sortable` 设为 `custom` 时需监听 `sort-change` 事件实现后端排序
- Table 或祖先元素由隐藏切换为显示时，可能需要调用 `doLayout` 重新布局
- 自定义列模板通过 `slot-scope` 获取 `{ row, column, $index }`

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\table.md`
