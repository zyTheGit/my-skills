# 反馈组件 - 弹窗与确认

## Dialog 对话框

### 基础用法

```vue
<el-button type="text" @click="dialogVisible = true">点击打开 Dialog</el-button>

<el-dialog
  title="提示"
  :visible.sync="dialogVisible"
  width="30%"
  :before-close="handleClose">
  <span>这是一段信息</span>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
  </span>
</el-dialog>
```

### 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| visible | 是否显示 | boolean | false |
| title | 标题 | string | - |
| width | 宽度 | string | 50% |
| fullscreen | 是否全屏 | boolean | false |
| modal | 是否显示遮罩层 | boolean | true |
| close-on-click-modal | 点击遮罩关闭 | boolean | true |
| before-close | 关闭前的回调 | function | - |

### 自定义内容

```vue
<el-dialog :visible.sync="dialogVisible">
  <el-form :model="form">
    <el-form-item label="活动名称">
      <el-input v-model="form.name"></el-input>
    </el-form-item>
  </el-form>
  <span slot="footer">
    <el-button @click="dialogVisible = false">取消</el-button>
    <el-button type="primary" @click="handleConfirm">确定</el-button>
  </span>
</el-dialog>
```

---

## MessageBox 消息弹框

### 基础用法

```javascript
// 警告框
this.$alert('消息内容', '标题', {
  confirmButtonText: '确定',
  callback: action => {
    this.$message({
      type: 'info',
      message: `action: ${action}`
    });
  }
});

// 确认框
this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  type: 'warning'
}).then(() => {
  this.$message.success('删除成功!');
}).catch(() => {
  this.$message.info('已取消删除');
});

// 提示框
this.$prompt('请输入邮箱', '提示', {
  confirmButtonText: '确定',
  cancelButtonText: '取消',
  inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
  inputErrorMessage: '邮箱格式不正确'
}).then(({ value }) => {
  this.$message.success('你的邮箱是: ' + value);
});
```

---

## Drawer 抽屉

### 基础用法

```vue
<el-button @click="drawer = true" type="primary">从右往左开</el-button>

<el-drawer
  title="我是标题"
  :visible.sync="drawer"
  direction="rtl"
  :before-close="handleClose">
  <span>我来啦!</span>
</el-drawer>
```

### 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| visible | 是否显示 | boolean | false |
| direction | 打开方向 | string | rtl |
| title | 标题 | string | - |
| size | 窗体大小 | string / number | '30%' |
| modal | 是否显示遮罩层 | boolean | true |

---

## Popconfirm 气泡确认框

### 基础用法

```vue
<el-popconfirm title="确定删除吗？" @confirm="handleDelete">
  <el-button slot="reference">删除</el-button>
</el-popconfirm>
```
