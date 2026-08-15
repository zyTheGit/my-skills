# BaseImport Excel 导入组件

**功能说明**：提供完整 Excel 导入工作流，支持弹框模式和内联模式，可无缝集成到 Element UI 表单。封装自 base-chunk-upload，默认上传需传 `scode` 和 `mcode`。

## 基础用法

### 推荐用法 - uploadMethod（新）

```vue
<el-base-import
  :visible.sync="dialogVisible"
  title="批量导入用户"
  :upload-method="customUpload"
  :upload-data="uploadData"
  :response-handler="handleResponse"
  @success="handleSuccess"
  @complete="handleComplete"
/>
```

### 内联模式 - 表单集成

```vue
<el-form-item label="导入用户文件" prop="userFile">
  <el-base-import
    is-inline
    v-model="form.userFile"
    :limit="3"
    manual-upload
    :upload-data="uploadData"
    @success="handleSuccess"
  />
</el-form-item>
```

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| visible | 对话框是否可见，支持 .sync（弹框模式） | boolean | false |
| is-inline | 是否为内联模式（只显示上传区域） | boolean | false |
| value / v-model | 文件列表（内联模式绑定） | array | [] |
| title | 对话框标题 | string | 导入 |
| width | 对话框宽度 | string | 500px |
| upload-method | 【新】自定义上传方法（优先级最高），返回 Promise | function(file, data) | - |
| upload-url | 【新】上传 URL，兼容旧版 import-url | string | - |
| upload-data | 【新】上传附加数据，兼容 import-data；含 scode/mcode 时自动解析文件限制 | object | {} |
| response-handler | 【新】响应处理器，自定义响应格式处理 | function(response) | - |
| custom-import | 自定义上传方法（兼容旧版） | function(file) | - |
| import-url | 文件上传 URL（兼容旧版） | string | - |
| import-data | 上传额外数据（兼容旧版） | object | {} |
| template-url | 模板下载 URL | string | - |
| template-options | 模板下载参数 | object | {} |
| template-download-method | 自定义模板下载方法，优先级高于 template-url | function | - |
| accept | 接受的文件类型 | string | .xls,.xlsx,.zip |
| max-file-size | 最大文件大小（MB） | number | 5 |
| limit | 最大上传数量 | number | 1 |
| manual-upload | 是否手动上传（建议仅用于弹框模式） | boolean | false |
| auto-confirm | 是否自动确认导入 | boolean | true |
| directory | 是否选择目录 | boolean | false |
| drag-directory | 拖拽时是否递归展开文件夹 | boolean | false |
| use-file-module-config | 是否根据 scode/mcode 请求文件模块限制 | boolean | true |
| before-remove | 删除前钩子，返回 false 或 reject 可阻止删除 | function(file, fileList) | - |
| show-upload-message | 是否显示内置上传提示 | boolean | true |
| replace-item-actions | item-actions 是否替代默认操作按钮 | boolean | false |
| ~~is-success~~ | 【已废弃】请用 response-handler | function(res) | - |
| ~~is-warning~~ | 【已废弃】请用 response-handler | function(res) | - |

## Events

| 事件名 | 说明 | 回调参数 |
|-------|------|---------|
| input | v-model 值变化 | (fileList) |
| change | 文件列表变化 | (fileList) |
| before-upload-dir | 目录模式文件入队前触发 | { files, filteredFiles, source, isDrag, isDirectory } |
| before-upload | 【新】上传前触发 | (file) |
| progress | 上传进度变化 | (file, percent) |
| success | 上传成功 | (file, processedResult) |
| error | 上传失败 | (file, processedResult) |
| complete | 【新】单文件上传完成（未开目录模式时触发） | (file, processedResult) |
| confirm | 点击确定或自动确认 | { fileList, checked } |
| upload-complete | 开启 directory/drag-directory 后批次完成触发 | { fileList, results, total, successCount, failCount } |
| update:visible | 对话框可见性变化 | (visible) |
| close | 对话框关闭 | - |
| template-download | 模板下载 | - |

## Methods

| 方法名 | 说明 | 返回值 |
|-------|------|--------|
| open / close | 打开 / 关闭对话框 | - |
| reset | 重置组件状态 | - |
| getFileList | 获取当前文件列表 | Array |
| getUploadedFileIds | 获取已成功上传的文件 ID 列表 | Array |
| validate | 触发表单验证 | Promise<Boolean> |
| setLoading | 设置确定按钮加载状态 | - |

## Slots

| 插槽名 | 说明 | 作用域参数 |
|-------|------|-----------|
| default | 触发文件选择框内容（仅内联模式） | - |
| tips | 自定义提示内容 | - |
| item-actions | 文件项右侧自定义操作按钮 | { file, index } |
| item-append | 文件列表项后置内容 | { file, index } |
| prepend | 文件列表项前置内容 | - |

## 上传方式优先级

1. **uploadMethod**（最高，推荐）- 完全自定义上传
2. **customImport**（兼容旧版）- 自定义导入方法
3. **uploadUrl / importUrl** - 上传到业务端接口
4. **默认方式** - 上传到文件服务器

## responseHandler 返回结构

```js
{
  success: Boolean,    // 是否成功
  status: String,      // 'success' | 'warning' | 'fail' | 自定义
  fileId: String,      // 文件 ID
  data: Object,        // 业务数据
  message: String,     // 提示消息
  rawResponse: Object  // 原始响应
}
```

## 注意事项

- 表单场景推荐内联模式（`is-inline`）配合 v-model 和表单验证
- `manual-upload` 仅建议用于弹框模式；开启后 `confirm` 先触发，再执行上传，需在 `success`/`complete` 中取 `fileId`
- `upload-data` 同时含 `scode`、`mcode` 且 `use-file-module-config` 为 true 时，自动请求 `/base-file/client/file/module/resolve` 解析文件类型和大小限制
- 目录模式（`directory`/`drag-directory`）依赖浏览器文件系统条目 API，不支持时回退为普通文件拖拽
- v2.0 起 `@success`/`@error` 第二参数为 processedResult（含完整结果），旧版仅 response.data
- `is-success`/`is-warning` 已废弃，改用 `response-handler`

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-import.md`
