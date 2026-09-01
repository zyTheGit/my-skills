# Progress 进度条

## 核心特性

- 支持线性和环形两种样式
- 支持多种状态（成功/警告/异常）
- 支持自定义格式
- 常用于任务进度展示

## 基础用法

```vue
<el-progress :percentage="50"></el-progress>
<el-progress :percentage="100" status="success"></el-progress>
<el-progress :percentage="100" status="warning"></el-progress>
<el-progress :percentage="50" status="exception"></el-progress>
```

## 环形进度条

```vue
<el-progress type="circle" :percentage="25"></el-progress>
<el-progress type="circle" :percentage="100" status="success"></el-progress>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| percentage | 百分比 | number | 0 |
| type | 类型 | line / circle | line |
| stroke-width | 线宽 | number | 6 |
| text-inside | 文字在进度条内 | boolean | false |
| status | 状态 | success / warning / exception / - | - |
| show-text | 显示文字 | boolean | true |

## 自定义格式

```vue
<el-progress :percentage="100" :format="format"></el-progress>

<script>
methods: {
  format(p) {
    return p === 100 ? '完成' : p + '%';
  }
}
</script>
```