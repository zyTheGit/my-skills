# BaseFilePreviewer 文件预览

**功能说明**：文档文件预览组件，支持 PDF、Word、Excel 等常见格式。

## 基础用法

```vue
<el-base-file-previewer
  v-model="visible"
  :src="fileUrl"
/>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| value / v-model | 是否显示预览 | boolean | - |
| src | 文件地址 | string | - |

## Events

| 事件名 | 说明 | 参数 |
|--------|------|------|
| close | 关闭预览 | - |

## 支持的文件格式

| 格式 | 扩展名 |
|------|--------|
| PDF | .pdf |
| Word | .doc, .docx |
| Excel | .xls, .xlsx |
| PPT | .ppt, .pptx |
| 文本 | .txt |

## 注意事项

- 需要后端提供文件流接口
- 部分格式可能需要浏览器原生支持
