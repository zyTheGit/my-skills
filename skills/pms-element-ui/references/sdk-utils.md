# Min-Web3 SDK - window.$utils

## 二、Min-Web3 全局 SDK

> 基于 qiankun 微前端架构的全局 SDK，包含通信、权限、工具、历史管理、性能监控、错误处理等模块

### 快速开始

所有全局 SDK 在主应用启动时自动挂载到 `window` 对象，子应用可直接使用：

```javascript
// 子应用中直接使用
if (window.__POWERED_BY_QIANKUN__) {
  // 打开新标签页
  window.$utils.openTab({
    appName: 'app-user',
    name: 'user-detail-123',
    path: '/app-user/detail/123',
    title: '用户详情'
  });
  
  // 检查权限
  if (window.$permission.check('user:edit')) {
    // 有编辑权限
  }
  
  // 通过 mainStore 获取主应用数据（响应式）
  const userInfo = this.$mainStore.state.user.userInfo;
  
  // 发送消息给主应用
  window.$eventBus.emit('message:fromApp', {
    appName: 'app-user',
    type: 'USER_UPDATED',
    data: { id: 123 }
  });
}
```

---

### window.$utils - 工具 SDK

提供标签页管理、日期格式化、本地存储、防抖节流等通用工具。

#### 标签页管理

**openTab(tab) - 打开新标签页**

```javascript
window.$utils.openTab({
  appName: 'app-user',
  name: 'user-detail-123',
  path: '/app-user/detail/123',
  title: '用户详情',
  keepAlive: true  // 切换标签时保留组件状态
});
```

**closeCurrentTab() - 关闭当前标签页**

```javascript
await window.$utils.closeCurrentTab();
```

**closeCurrentAndOpenTab(tab) - 关闭当前并打开新标签页**

```javascript
await window.$utils.closeCurrentAndOpenTab({
  appName: 'app-user',
  name: 'user-list',
  path: '/app-user/list',
  title: '用户列表'
});
```

**updateTabSubRoute(tabName, subRoute) - 更新标签页子路由**

```javascript
// 子应用路由守卫中调用
router.afterEach((to) => {
  if (window.__POWERED_BY_QIANKUN__ && window.$utils) {
    const tabName = 'user-list';
    window.$utils.updateTabSubRoute(tabName, to.fullPath);
  }
});
```

**getActiveTab() / getAllTabs()**

```javascript
const activeTab = window.$utils.getActiveTab();
const tabs = window.$utils.getAllTabs();
```

#### 日期工具

**formatDate(date, format)**

```javascript
window.$utils.formatDate(new Date()); // '2024-01-15 10:30:00'
window.$utils.formatDate(new Date(), 'YYYY-MM-DD'); // '2024-01-15'
```

**getRelativeTime(date) - 相对时间**

```javascript
window.$utils.getRelativeTime(Date.now() - 30000);   // '刚刚'
window.$utils.getRelativeTime(Date.now() - 60000);   // '1分钟前'
window.$utils.getRelativeTime(Date.now() - 3600000); // '1小时前'
```

#### 本地存储

```javascript
// 永久存储
window.$utils.storage.set('user', { name: '张三', age: 25 });

// 带过期时间（1小时）
window.$utils.storage.set('token', 'xxx-token', 3600000);

// 读取
const user = window.$utils.storage.get('user');

// 带默认值
const count = window.$utils.storage.get('count', 0);

// 删除
window.$utils.storage.remove('user');
window.$utils.storage.clear();

// 检查
if (window.$utils.storage.has('token')) {
  // token 存在且未过期
}
```

#### 函数工具

**debounce(fn, delay) - 防抖**

```javascript
const debouncedSearch = window.$utils.debounce((keyword) => {
  api.search(keyword);
}, 500);
```

**throttle(fn, delay) - 节流**

```javascript
const throttledScroll = window.$utils.throttle(() => {
  console.log('滚动位置:', window.scrollY);
}, 200);
```

#### 对象工具

**deepClone(obj) - 深拷贝**

```javascript
const copy = window.$utils.deepClone(original);
```

**isEmpty(value) - 判断空值**

```javascript
window.$utils.isEmpty(null);       // true
window.$utils.isEmpty('');         // true
window.$utils.isEmpty([]);         // true
window.$utils.isEmpty({});         // true
```

#### URL 工具

**parseQuery(url) / buildQuery(params)**

```javascript
const params = window.$utils.parseQuery('/page?id=123&name=test');
// { id: '123', name: 'test' }

const query = window.$utils.buildQuery({ id: 123, name: '张三' });
// 'id=123&name=%E5%BC%A0%E4%B8%89'
```
