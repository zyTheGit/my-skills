# 反馈组件 - Loading 与组合示例

## Loading 加载

加载数据时显示动效。

### 指令方式

```vue
<el-table v-loading="loading" element-loading-type="image" :data="tableData">
  <!-- 表格内容 -->
</el-table>
```

### 自定义文案和样式

```vue
<el-table
  v-loading="loading"
  element-loading-text="拼命加载中"
  element-loading-spinner="el-icon-loading"
  element-loading-background="rgba(0, 0, 0, 0.8)"
  :data="tableData">
</el-table>
```

### 整页加载

```vue
<el-button
  type="primary"
  @click="openFullScreen1"
  v-loading.fullscreen.lock="fullscreenLoading"
  element-loading-type="image">
  指令方式
</el-button>

<el-button type="primary" @click="openFullScreen2">服务方式</el-button>

<script>
export default {
  data() {
    return {
      fullscreenLoading: false
    }
  },
  methods: {
    openFullScreen1() {
      this.fullscreenLoading = true;
      setTimeout(() => { this.fullscreenLoading = false; }, 2000);
    },
    openFullScreen2() {
      const loading = this.$loading({ lock: true, type: 'image' });
      setTimeout(() => { loading.close(); }, 2000);
    }
  }
}
</script>
```

### 服务方式

```javascript
import { Loading } from 'element-ui';

const loading = Loading.service({
  lock: true,
  text: 'Loading',
  spinner: 'el-icon-loading',
  background: 'rgba(0, 0, 0, 0.7)'
});
this.$nextTick(() => {
  loading.close();
});
```

> 全屏 Loading 是单例的，多次调用返回同一实例。

### Options

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| target | Loading 覆盖的 DOM 节点 | object/string | — | document.body |
| body | 插入至 body | boolean | — | false |
| fullscreen | 全屏遮罩 | boolean | — | true |
| lock | 锁定屏幕滚动 | boolean | — | false |
| text | 加载文案 | string | — | — |
| spinner | 自定义加载图标类名 | string | — | — |
| background | 遮罩背景色 | string | — | — |
| customClass | 自定义类名 | string | — | — |
| type | 加载类型（如 image） | string | — | — |

---

## 常用组合示例

### 操作反馈

```javascript
// 提交成功
try {
  await this.submitForm();
  this.$message.success('提交成功');
  this.dialogVisible = false;
} catch (error) {
  this.$message.error('提交失败：' + error.message);
}

// 删除确认
this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
  type: 'warning'
}).then(async () => {
  await this.deleteFile();
  this.$message.success('删除成功');
  this.loadData();
}).catch(() => {
  // 取消操作
});
```
