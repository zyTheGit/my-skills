# BaseIcon 基础图标

**功能说明**：提供文件类型图标支持，可通过 `name` 属性或 CSS 类名使用。

## 基础用法

```vue
<!-- 通过 name 属性使用 -->
<el-base-icon name="file-shujuku" />

<!-- 通过 CSS 类名使用 -->
<i class="el-base-icon-file-shujuku"></i>
```

## 文件图标列表

| 图标名称 | 说明 |
|---------|------|
| file-shujuku | 数据库文件 |
| file-yasuobao | 压缩包 |
| file-weizhiwenjian | 未知文件 |
| file-music | 音乐文件 |
| file-lianjiewenjian | 链接文件 |
| file-Pdf | PDF 文件 |
| file-shipin | 视频文件 |
| file-Excel | Excel 文件 |
| file-txt | 文本文件 |
| file-chengxu | 程序文件 |
| file-PPT | PPT 文件 |
| file-tupian | 图片文件 |
| file-word | Word 文件 |

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| name | 图标名称 | string | 必填 | - |
| size | 图标尺寸 | string / number | - | 22px |
| iconClass | 额外类名 | string | - | - |

## 注意事项

- `name` 属性为必填项
- 也可直接使用 CSS 类名格式：`el-base-icon-{name}`
