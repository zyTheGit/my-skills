# MicroKeepAliveView 微前端页签保活

## 核心特性

- qiankun + 多页签场景下子应用页面缓存
- 保持子应用状态，避免重复渲染
- 支持手动刷新和关闭页签

## 基础用法

```vue
<micro-keep-alive-view />
```

## 在路由中使用

```javascript
// 路由配置
{
  path: '/app/list',
  component: MicroKeepAliveView,
  meta: { keepAlive: true }
}
```

## Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| name | 缓存名称标识 | string | — | — |
| max | 最大缓存数量 | number | — | 10 |
| include | 包含的组件名列表 | array | — | [] |
| exclude | 排除的组件名列表 | array | — | [] |

## Events

| 事件名 | 说明 | 回调参数 |
|-------|------|---------|
| activated | 组件激活时触发 | — |
| deactivated | 组件失活时触发 | — |

## 使用场景

- 多页签切换时保持表单状态
- 列表页返回时保留筛选条件
- 避免子应用重新加载
