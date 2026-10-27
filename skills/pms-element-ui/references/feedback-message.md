# 反馈组件 - 消息与提示

## Message 消息提示

### 基础用法

```javascript
// 成功消息
this.$message.success('成功');

// 警告消息
this.$message.warning('警告');

// 错误消息
this.$message.error('错误');

// 普通消息
this.$message('这是一条消息提示');

// 可关闭的消息
this.$message({
  message: '恭喜你，这是一条成功消息',
  type: 'success',
  showClose: true
});
```

### 配置项

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| message | 消息文字 | string / VNode | - |
| type | 主题 | string | info |
| duration | 显示时间(ms) | number | 3000 |
| showClose | 显示关闭按钮 | boolean | false |
| center | 文字居中 | boolean | false |

---

## Notification 通知

### 基础用法

```javascript
// 基本通知
this.$notify({
  title: '标题',
  message: '这是一条通知消息'
});

// 成功通知
this.$notify.success({
  title: '成功',
  message: '这是一条成功的提示消息'
});

// 警告通知
this.$notify.warning({
  title: '警告',
  message: '这是一条警告的提示消息'
});

// 使用 HTML 片段
this.$notify({
  title: 'HTML 片段',
  dangerouslyUseHTMLString: true,
  message: '<strong>这是 <i>HTML</i> 片段</strong>'
});
```

### 配置项

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| title | 标题 | string | - |
| message | 消息文字 | string / VNode | - |
| type | 主题 | string | - |
| duration | 显示时间(ms) | number | 4500 |
| position | 自定义弹出位置 | string | top-right |
| offset | 偏移距离 | number | 0 |

---

## Alert 警告

### 基础用法

```vue
<el-alert title="成功提示" type="success"></el-alert>
<el-alert title="消息提示" type="info"></el-alert>
<el-alert title="警告提示" type="warning"></el-alert>
<el-alert title="错误提示" type="error"></el-alert>
```

### 可关闭的警告

```vue
<el-alert
  title="不可关闭的 alert"
  type="success"
  closable
  show-icon>
</el-alert>
```

---

## Popover 气泡弹出框

### 基础用法

```vue
<el-popover
  placement="top-start"
  title="标题"
  width="200"
  trigger="hover"
  content="这是一段内容">
  <el-button slot="reference">hover 激活</el-button>
</el-popover>
```

---

## Tooltip 文字提示

**功能说明**：鼠标悬停时显示文本提示，常用于展示上下文信息。

### 基础用法

```vue
<el-tooltip effect="dark" content="顶部提示" placement="top">
  <el-button>悬停查看</el-button>
</el-tooltip>
```

### 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| effect | 主题 | dark / light | dark |
| content | 提示文本（或使用 `slot="content"`） | string | — |
| placement | 引出位置 | top / top-start / top-end / bottom / bottom-start / bottom-end / left / left-start / left-end / right / right-start / right-end | bottom |
| value / v-model | 是否显示 | boolean | false |
| disabled | 是否禁用 | boolean | false |
| offset | 出现位置的偏移量 | number | 0 |
| transition | 定义渐变动画 | string | el-fade-in-linear |
| visible-arrow | 是否显示箭头 | boolean | true |
| open-delay | 出现前的延迟（ms） | number | 0 |
| manual | 手动控制模式 | boolean | false |
| enterable | 鼠标是否可进入 tooltip | boolean | true |
| hide-after | 自动隐藏延迟（ms），0 为不自动隐藏 | number | 0 |
| popper-class | 为 popper 添加类名 | string | — |
| tabindex | tabindex 属性 | number | 0 |

### 注意事项

- tooltip 内容不支持 `router-link`，请使用 `vm.$router.push` 替代
- 禁用的表单元素内部不会触发 mouseenter，需在外层包裹一个容器元素
