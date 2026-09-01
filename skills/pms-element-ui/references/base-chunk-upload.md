# BaseChunkUpload 上传组件

**功能说明**：对 el-upload 进行改造以适配设计稿，不改变 el-upload 原参数、插槽和方法；新增 `uploadListType` 支持上传图片（picture）和上传附件（file）两种列表样式。

## 基础用法

### 上传图片

```vue
<el-base-chunk-upload
  accept=".png,.jpg,.jpeg"
  upload-list-type="picture"
  action="https://jsonplaceholder.typicode.com/posts/"
  auto-upload
  :file-list.sync="fileList"
  :file-operate-btn="['delete', 'view', 'edit']"
  multiple
  :limit="2"
  :on-change="_onChange"
  :on-exceed="_onExceed"
/>
```

### 上传附件

```vue
<el-base-chunk-upload
  action="/pms/base-file/client/upload/putFile"
  auto-upload
  accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.zip,.rar"
  :on-preview="_onPreview"
  :file-list.sync="fileList"
/>
```

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| action | 上传地址 | string | # |
| drag | 拖拽上传 | boolean | true |
| directory | 点击上传区域时是否只选择目录 | boolean | false |
| drag-directory | 拖拽时是否自动识别普通文件并递归展开文件夹 | boolean | false |
| show-upload-message | 是否显示内置文件大小和类型校验提示 | boolean | true |
| auto-upload | 开启自动上传 | boolean | false |
| show-file-list | 是否开启 el-upload 自带上传列表 | boolean | false |
| show-upload-file-list | 是否开启自带上传列表（show-file-list 为 true 时无效） | boolean | true |
| max-file-size | 限制单个文件大小（MB） | number | 20 |
| file-operate-btn | 文件操作按钮 | array | ['view'] |
| replace-item-actions | item-actions 是否替代默认操作按钮；关闭时追加在后 | boolean | false |
| upload-list-type | 上传列表类型（show-file-list==false 时生效） | string | file |
| upload-list-size | 上传列表尺寸（picture 时生效） | string | 268px |
| before-remove | 删除前钩子，返回 false 或 Promise.reject() 可阻止删除 | function(file, fileList) | - |
| on-change | 文件状态改变钩子 | function(file, fileList) | - |
| on-download | 点击下载时触发 | function(file, index) | - |
| on-preview | 点击预览时触发 | function(file, index) | - |
| on-rename-file | 点击重命名时触发 | function(file, newName) | - |
| limit | 最大允许上传个数 | number | - |
| on-exceed | 文件超出个数限制时钩子 | function(files, fileList) | - |

## Slots

| 插槽名 | 说明 | 作用域参数 |
|-------|------|-----------|
| default | 触发文件选择框的内容 | - |
| tips | 自定义提示内容 | - |
| item-actions | 文件项右侧自定义操作按钮，默认追加在内置按钮后 | { file, index } |
| item-append | 文件列表项后置内容，位于每个文件项末尾 | { file, index } |

## 注意事项

- 文件列表通过 `:file-list.sync` 双向绑定，而非 v-model
- `before-remove` 返回 `false`、`Promise.reject()` 阻止删除；返回 `true` 或 `Promise.resolve()` 继续删除
- `item-append` 插槽可为每个文件项末尾添加自定义内容，同时支持文件和图片类型
- `directory` / `drag-directory` 用于目录选择场景，递归展开文件夹内文件

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-chunk-upload.md`
