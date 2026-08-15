# BaseUploadList 文件列表管理

**功能说明**：文件列表管理组件，支持文件预览、删除等操作。

## 基础用法

```vue
<el-base-upload-list
  v-model="fileList"
  :max-count="10"
  @change="handleChange"
/>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| value / v-model | 文件列表数据 | array | - |
| max-count | 最大数量限制 | number | - |
| accept | 接受的文件类型 | string | - |

## Events

| 事件名 | 说明 | 参数 |
|--------|------|------|
| change | 文件列表变化 | (fileList) |
| remove | 文件移除 | (file, index) |

## 注意事项

- 通常与 `BaseChunkUpload` 配合使用
- 支持图片和文件两种展示模式
