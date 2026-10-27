# 快速开始 - 安装与配置

## 一、安装与配置

### npm 安装

```bash
npm i element-ui -S
```

### CDN 引入

```html
<!-- 引入样式 -->
<link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
<!-- 引入组件库 -->
<script src="https://unpkg.com/element-ui/lib/index.js"></script>
```

### 完整引入

```javascript
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';

Vue.use(ElementUI);

new Vue({
  el: '#app',
  render: h => h(App)
});
```

### 按需引入

```bash
npm install babel-plugin-component -D
```

配置 `.babelrc`：

```json
{
  "presets": [["es2015", { "modules": false }]],
  "plugins": [
    [
      "component",
      {
        "libraryName": "element-ui",
        "styleLibraryName": "theme-chalk"
      }
    ]
  ]
}
```

### 全局配置

```javascript
import Vue from 'vue';
import Element from 'element-ui';
Vue.use(Element, { size: 'small', zIndex: 3000 });
```

## 三、端口约定

| 应用 | 端口 | 说明 |
|------|------|------|
| main-app | 8080 | 主应用（Shell） |
| app-user | 8081 | 用户管理子应用 |
| app-vue2 | 8082 | Vue2 示例子应用 |

## 四、环境变量

```bash
VUE_APP_ROUTER_MODE=history
VUE_APP_USER_ENTRY=http://localhost:8081
VUE_APP_VUE2_ENTRY=http://localhost:8082
```

---

**相关文档**：
- [02-基础业务组件.md](../02-基础业务组件.md) - 业务组件使用指南
- [08-主题和工具.md](../08-主题和工具.md) - 主题定制和更多工具函数
