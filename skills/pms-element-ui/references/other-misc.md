# 其他组件 - 滚动与展示

## InfiniteScroll 无限滚动

### 基础用法

```vue
<ul class="infinite-list" v-infinite-scroll="load" infinite-scroll-disabled="disabled">
  <li v-for="i in count" :key="i" class="infinite-list-item">{{ i }}</li>
</ul>

<script>
export default {
  data() {
    return {
      count: 10
    };
  },
  methods: {
    load() {
      this.count += 2;
    }
  }
};
</script>
```

---

## Avatar 头像

**功能说明**：用图标、图片或字符展示用户或实体信息。

### 基础用法

```vue
<el-avatar :size="50" src="https://example.com/avatar.png"></el-avatar>
<el-avatar icon="el-icon-user-solid"></el-avatar>
<el-avatar>user</el-avatar>
```

### 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| icon | 图标类名 | string | — |
| size | 尺寸 | number / large / medium / small / mini | large |
| shape | 形状 | circle / square | circle |
| src | 图片 URL | string | — |
| fit | 填充模式（同 CSS object-fit） | fill / contain / cover / none / scale-down | cover |
| alt | 图片 alt 文本 | string | — |
| srcSet | 逗号分隔的 srcset 列表 | string | — |

### 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| error | 图片加载失败 | (event) |

### 插槽

| 插槽名 | 说明 |
|-------|------|
| default | 自定义头像内容 |

### 注意事项

- 三种展示类型：图标、图片、字符（插槽内容）
- `error` 事件处理函数返回 `false` 可阻止默认容错渲染

---

## Divider 分割线

**功能说明**：用于分隔内容区域的分割线。

### 基础用法

```vue
<span>上方文本</span>
<el-divider></el-divider>
<span>下方文本</span>

<el-divider content-position="left">左侧文本</el-divider>

<el-divider direction="vertical"></el-divider>
```

### 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| direction | 方向 | horizontal / vertical | horizontal |
| content-position | 文本位置 | left / right / center | center |

### 注意事项

- 分割线内可插入文本或图标内容，通过 `content-position` 控制位置

---

**相关文档**：
- [02-基础业务组件.md](./02-基础业务组件.md) - 业务组件操作按钮
- [06-反馈组件.md](./06-反馈组件.md) - 按钮操作反馈
