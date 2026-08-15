# Upload 上传

> 文件上传组件，支持点击上传、拖拽上传、照片墙

---

## 功能说明

通过点击或拖拽上传文件，支持照片墙、文件缩略图、手动上传、目录上传等多种模式。

---

## 基础用法

```vue
<el-upload
  action="/api/upload"
  :on-preview="handlePreview"
  :on-remove="handleRemove"
  :before-remove="beforeRemove"
  multiple
  :limit="3"
  :on-exceed="handleExceed"
  :file-list="fileList">
  <el-button size="small" type="primary">点击上传</el-button>
  <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
</el-upload>
```

---

## 拖拽上传

```vue
<el-upload drag action="/api/upload" multiple>
  <i class="el-icon-upload"></i>
  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
  <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
</el-upload>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| action | 必选参数，上传地址 | string | - |
| headers | 设置上传请求头部 | object | - |
| multiple | 是否支持多选文件 | boolean | - |
| directory | 是否选择目录；开启后只能选择目录并上传目录内文件 | boolean | false |
| drag-directory | 拖拽时是否自动识别普通文件并递归展开文件夹 | boolean | false |
| data | 上传时附带的额外参数 | object | - |
| name | 上传的文件字段名 | string | file |
| with-credentials | 支持发送 cookie 凭证信息 | boolean | false |
| show-file-list | 是否显示已上传文件列表 | boolean | true |
| drag | 是否启用拖拽上传 | boolean | false |
| accept | 接受上传的文件类型（thumbnail-mode 模式下无效） | string | - |
| on-preview | 点击文件列表中已上传文件时的钩子 | function(file) | - |
| on-remove | 文件列表移除文件时的钩子 | function(file, fileList) | - |
| on-success | 文件上传成功时的钩子 | function(response, file, fileList) | - |
| on-error | 文件上传失败时的钩子 | function(err, file, fileList) | - |
| on-progress | 文件上传时的钩子 | function(event, file, fileList) | - |
| on-change | 文件状态改变时的钩子，添加、成功、失败都会调用 | function(file, fileList) | - |
| before-upload | 上传前钩子，返回 false 或 reject 则停止上传 | function(file) | - |
| before-remove | 删除前钩子，返回 false 或 reject 则停止删除 | function(file, fileList) | - |
| list-type | 文件列表类型 | string (text/picture/picture-card) | text |
| add-position | 新增区域在左侧还是右侧 | string (right/left) | right |
| auto-upload | 是否选取后立即上传 | boolean | true |
| file-list | 上传文件列表 | array | [] |
| http-request | 覆盖默认上传行为，自定义上传实现 | function | - |
| disabled | 是否禁用 | boolean | false |
| limit | 最大允许上传个数 | number | - |
| on-exceed | 文件超出限制时的钩子 | function(files, fileList) | - |

---

## 插槽

| 插槽名 | 说明 |
|--------|------|
| trigger | 触发文件选择框的内容 |
| tip | 提示说明文字 |

---

## 常用方法

| 方法名 | 说明 | 参数 |
|--------|------|------|
| clearFiles | 清空已上传文件列表（不支持在 before-upload 中调用） | - |
| abort | 取消上传请求 | file: fileList 中的 file 对象 |
| submit | 手动上传文件列表 | - |

---

## 注意事项

- `action` 必须配置有效上传地址
- 使用 `before-upload` 限制文件类型和大小
- 照片墙模式使用 `list-type="picture-card"`
- 手动上传需设置 `:auto-upload="false"` 并通过 `ref` 调用 `submit()`
- 可通过 `before-remove` 阻止文件移除操作
- `directory` 开启后仅可选择目录并上传其内文件
- `drag-directory` 仅影响拖拽行为，不改变点击选择器
- 文件缩略图可通过 `scoped-slot`（slot="file"）自定义模板

---

## 参考文档

源文档：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\upload.md`
