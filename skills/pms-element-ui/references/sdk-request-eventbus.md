# Min-Web3 SDK - 请求与事件总线

### window.$request - 请求方法

二次封装 `axios`，支持请求级别配置覆盖、加密加签、取消请求。

> **注意**：子应用使用 external 配置：`externals: process.env.NODE_ENV === 'production' ? {'@custom/pms-request': '$request'} : null`

#### 基础配置

```javascript
import { setupRequest, get, post } from '@custom/pms-request'

// 初始化配置（子应用不需要初始化）
setupRequest({
  baseURL: '/api',
  getToken: () => localStorage.getItem('token'),
  onAuthError: () => router.push('/login'),
  onError: (msg) => Message.error(msg),
})

// 发起请求
const users = await get({ url: '/users', params: { page: 1 } })
const result = await post({ url: '/users', data: { name: 'test' } })
```

#### 配置项

**基础配置**

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| baseURL | string | '' | API 基础地址 |
| timeout | number | 10000 | 超时时间（毫秒） |
| withCredentials | boolean | true | 是否携带 cookie |
| headers | object | { 'Content-Type': 'application/json' } | 默认请求头 |

**Token 配置**

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| getToken | () => string | null | 获取 token 函数 |
| tokenHeaderName | string | 'Authorization' | token 请求头名称 |
| tokenPrefix | string | 'Bearer ' | token 前缀 |

**错误处理配置**

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| authErrorCodes | number[] | [40101, 401] | 登录失效错误码 |
| onAuthError | (res) => void | null | 登录失效回调 |
| onError | (msg) => void | null | 错误提示回调 |
| onLoadingStart | () => void | null | Loading 开始回调 |
| onLoadingEnd | () => void | null | Loading 结束回调 |

#### 加密示例

```javascript
// 登录接口 - password 字段会被自动加密
await post({
  url: '/login',
  data: {
    username: 'admin',
    password: '123456',  // 会被加密
  },
  crypto: {
    sm4: {
      fields: ['password']
    }
  }
})
```

#### 取消请求

```javascript
import { get, cancelRequest, cancelAllRequests } from 'pms-base-request'

// 发起可取消的请求
get({ url: '/search', params: { q: 'test' }, cancelKey: 'search' })

// 取消指定请求
cancelRequest('search')

// 取消所有请求
cancelAllRequests()
```

---

### window.$eventBus - 事件总线

轻量级事件总线，用于主应用与子应用之间的事件通信。

> **注意**：状态数据（如 userInfo、token）应通过 `this.$mainStore` 响应式获取，eventBus 仅用于事件通知。

**on(event, callback, options) - 订阅事件**

```javascript
const unsubscribe = window.$eventBus.on('route:restore', (payload) => {
  console.log('收到路由恢复请求', payload);
}, { appName: 'app-user' });

// 在组件销毁时取消订阅
beforeDestroy() {
  unsubscribe();
}
```

**once(event, callback, options) - 订阅一次**

```javascript
window.$eventBus.once('app:ready', (data) => {
  console.log('应用就绪', data);
});
```

**emit(event, data, options) - 发布事件**

```javascript
window.$eventBus.emit('message:fromApp', {
  appName: 'app-user',
  type: 'USER_UPDATED',
  data: { id: 123, name: '张三' }
});
```

**off(event, callback) - 取消订阅**

```javascript
window.$eventBus.off('route:restore', myCallback);
```

**预定义事件**

| 事件名 | 方向 | 说明 |
|--------|------|------|
| `route:restore` | 主应用 → 子应用 | 通知子应用恢复路由 |
| `route:update` | 子应用 → 主应用 | 子应用通知主应用更新 subRoute |
| `message:fromApp` | 子应用 → 主应用 | 子应用发送消息给主应用 |

---

### 子应用获取主应用数据

子应用通过 `this.$mainStore` 响应式获取主应用的 Vuex 状态。

**在子应用中访问主应用 Store**

```javascript
// 子应用 main.js 中
export async function mount(props) {
  Vue.prototype.$mainStore = props.mainStore;
  Vue.prototype.$mainRouter = props.mainRouter;
}
```

**获取用户信息**

```javascript
export default {
  computed: {
    userInfo() {
      return this.$mainStore?.state?.user?.userInfo;
    },
    token() {
      return this.$mainStore?.state?.user?.token;
    },
    permissions() {
      return this.$mainStore?.state?.permission?.permissions || [];
    },
    activeTab() {
      return this.$mainStore?.state?.tabs?.activeTab;
    }
  }
}
```

**可用的 Store 模块**

| 模块 | 路径 | 说明 |
|------|------|------|
| user | `state.user.userInfo` | 用户信息 |
| user | `state.user.token` | 登录 token |
| permission | `state.permission.permissions` | 权限列表 |
| tabs | `state.tabs.tabs` | 所有标签页 |
| tabs | `state.tabs.activeTab` | 当前激活标签页 |
