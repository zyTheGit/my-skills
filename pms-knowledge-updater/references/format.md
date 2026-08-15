# 组件条目格式规范

## 标准格式

```markdown
### 组件名称

**功能说明**：一句话描述组件用途

**基础用法**：
```vue
<el-component v-model="value" />
```

**常用属性**：
| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| prop | 说明 | type | default |

**常用事件**：
| 事件名 | 说明 | 参数 |
|-------|------|------|
| event | 说明 | params |

**注意事项**：
- 注意点1
- 注意点2
```

---

## 示例：新增 BaseNewComponent

```markdown
### BaseNewComponent 新组件

**功能说明**：这是一个新的业务组件

**基础用法**：
```vue
<el-base-new-component v-model="value" />
```

**常用属性**：
| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| value | 绑定值 | any | - |

**参考文档**：[源文档路径]
```

---

## 特殊组件处理

### BaseProTable / BaseProForm

保留完整配置说明和所有示例代码，更新属性/事件/方法表格。

### Min-Web3 SDK 相关

同步更新全局工具函数：
- `window.$utils` 工具函数
- `window.$request` 请求方法
- `window.$permission` 权限控制
- `window.$eventBus` 事件总线