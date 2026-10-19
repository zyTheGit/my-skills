# MicroKeepAliveView 微前端页签保活

`MicroKeepAliveView` 用于 `qiankun + Vue 2 + 多页签` 场景。它在子应用内部替代普通 `router-view`，根据「微应用名 + 主应用页签 ID + 子应用路由」生成缓存 key，并在主应用关闭页签或业务主动清理时删除子应用内部的 vnode 缓存。

---

## 30 秒结论

- **解决什么问题**：同一个子应用在主应用里打开多个页签时，每个页签内的页面各自保活、互不污染；关闭某个页签只清该页签下的页面缓存。
- **子应用要做的**：根组件把 `router-view` 换成 `MicroKeepAliveView`；`main.js` 创建 runtime 并订阅事件；需要保活的页面加 `meta.keepAlive: true`。
- **主应用要做的**：打开/切换页签发 `app:resume`，关闭页签发 `app:drop-cache`。
- **缓存 key 格式**：`appName::tabId::routeKey`，例如 `newUpmsWeb::1168302029918352441558::/role`。

---

## 子应用改造清单

| 文件 | 改动 | 是否必须 |
|------|------|----------|
| `App.vue` | `router-view` 换成 `MicroKeepAliveView` | 必须 |
| `main.js` 的 `mount` | 创建 runtime、`provide` 注入、调用 4 个订阅 | 必须 |
| `main.js` 的 `unmount` | 调用 `runtime.teardown()` | 必须 |
| `router/index.js` | 需要保活的页面加 `meta.keepAlive: true` | 必须 |
| 页面组件 | 按需加 `microKeepAlive` 选项、`activated`/`deactivated`/`beforeDropCache` | 按需 |
| 主应用 | 打开/切换/关闭页签时发送三类事件 | 必须 |

---

## 接入示例

### App.vue

```vue
<template>
  <div id="app">
    <MicroKeepAliveView v-if="isQiankunRuntime" />
    <router-view v-else />
  </div>
</template>
```

> `MicroKeepAliveView` 内部已包含 `router-view`，不要再在外面包一层。

### main.js

```js
export async function mount(props = {}) {
  routerInstance = createRouter()
  microKeepAliveRuntime = createMicroKeepAliveRuntime({
    ...props,
    appName: 'newUpmsWeb',
    basename: '/new-upms-web',
    keepAliveMax: 20
  })
  microKeepAliveRuntime.bindRouterRestore(routerInstance)
  microKeepAliveRuntime.onResume()
  microKeepAliveRuntime.onPause()
  microKeepAliveRuntime.onDropCache()
  instance = new Vue({
    router: routerInstance,
    provide: { microKeepAliveRuntime },
    render: h => h(App)
  }).$mount(container)
}

export async function unmount() {
  if (instance) { instance.$destroy(); instance = null }
  if (microKeepAliveRuntime) { microKeepAliveRuntime.teardown(); microKeepAliveRuntime = null }
}
```

### router/index.js

```js
export const routes = [
  { path: '/role', component: () => import('@/views/role/index.vue'), meta: { keepAlive: true } },
  {
    path: '/detail/:id',
    component: () => import('@/views/detail/index.vue'),
    meta: { keepAlive: true, cacheKey(route) { return `/detail/${route.params.id}` } }
  },
  { path: '/submit', component: () => import('@/views/submit/index.vue'), meta: { noCache: true } }
]
```

### 页面组件

```js
export default {
  name: 'RolePage',
  microKeepAlive: {
    shouldCache(route, context) { return route.query.cache !== 'false' && Boolean(context.tabId) },
    cacheKey(route) { return `/detail/${route.query.id || 'new'}` },
    beforeDropCache({ route, cacheKey, payload }) { console.log('缓存即将被清理:', route.fullPath, cacheKey, payload.reason) }
  },
  mounted() { this.initPage() },
  activated() { this.startPolling() },
  deactivated() { this.stopPolling() },
  beforeDestroy() { this.stopPolling() }
}
```

---

## 缓存策略

| 优先级 | 规则 |
|--------|------|
| 不缓存 | `route.meta.noCache === true` |
| 页面 hook | `microKeepAlive.shouldCache` 显式返回 `true` |
| 默认 | `route.meta.keepAlive === true` |

`routeKey` 解析：页面 `microKeepAlive.cacheKey` → `route.meta.cacheKey` → `route.fullPath || route.path`。

---

## 手动清理缓存

```js
export default {
  inject: { microKeepAliveRuntime: { default: null } },
  methods: {
    dropCurrentTabCache() {
      const runtime = this.microKeepAliveRuntime
      if (!runtime || !window.$eventBus) return
      const cacheKey = runtime.getRouteCacheKey(this.$route)
      if (!cacheKey) return
      const tabPrefix = cacheKey.split('::').slice(0, 2).join('::') + '::'
      window.$eventBus.emit('app:drop-cache', {
        appName: 'newUpmsWeb',
        dropKeys: [tabPrefix],
        reason: 'manual-drop-current-tab',
        timestamp: Date.now()
      }, { sticky: true })
    }
  }
}
```

> 清当前正在渲染的页面缓存不会立即销毁实例，需配合路由跳转。

---

## 主应用事件协议

### app:resume

```js
{
  appName: 'newUpmsWeb',
  tabId: '1168302029918352441558',
  tabName: '角色管理',
  tabPath: '/new-upms-web/role',
  subRoute: '/role',
  reason: 'active-tab-change',
  timestamp: Date.now()
}
```

### app:pause

字段与 `app:resume` 相同，`reason` 通常为 `tab-deactivate`。

### app:drop-cache

```js
{
  appName: 'newUpmsWeb',
  reason: 'close-tab',
  scope: 'current-tab',
  tabId: '1168302029918352441558',
  dropKeys: ['newUpmsWeb::1168302029918352441558::'],
  timestamp: Date.now()
}
```

清理粒度：

| 粒度 | dropKeys 示例 |
|------|---------------|
| 精确页面 | `['newUpmsWeb::tab-1::/role']` |
| 整个页签 | `['newUpmsWeb::tab-1::']` |
| 整个子应用 | `['newUpmsWeb::']` |

---

## 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| 重复渲染/缓存 key 不一致 | 同层又包了一层 `router-view` | 只用 `MicroKeepAliveView` |
| 切回页签不恢复轮询 | 轮询只写在 `mounted` | 用 `activated`/`deactivated` |
| 监听 `app:resume` 被误触发 | 只判断 `appName` | 同时匹配 `subRoute`/`tabPath`，并在 `beforeDestroy` 解绑 |
| 缓存没清掉 | 主应用未发 `app:drop-cache` | 关闭页签必发 `appName::tabId::` |
| unmount 后串事件 | 未 `teardown()` | 清理事件订阅 |

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\micro-keep-alive-view.md`
