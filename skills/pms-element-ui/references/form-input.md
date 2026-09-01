# Input 输入框

> 文本输入框组件，支持多种输入类型和格式化

---

## 核心特性

- 支持文本、密码、文本域等多种类型
- 自动清除空格功能
- 字数统计显示
- 前后置图标/内容插槽

---

## 基础用法

```vue
<el-input v-model="input" placeholder="请输入内容"></el-input>
```

---

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| type | 类型 | string | text |
| maxlength | 最大长度 | number | — |
| show-word-limit | 显示字数统计 | boolean | false |
| placeholder | 占位文本 | string | — |
| clearable | 可清空 | boolean | false |
| show-password | 显示密码切换 | boolean | false |
| trim | 自动清除空格 | boolean/string | false |
| disabled | 禁用 | boolean | false |
| prefix-icon | 头部图标 | string | — |
| suffix-icon | 尾部图标 | string | — |

---

## 文本域

```vue
<el-input
  type="textarea"
  :rows="2"
  placeholder="请输入内容"
  v-model="textarea"
  :autosize="{ minRows: 2, maxRows: 4 }">
</el-input>
```

---

## 复合型输入框

```vue
<el-input placeholder="请输入内容" v-model="input">
  <template slot="prepend">Http://</template>
</el-input>

<el-input placeholder="请输入内容" v-model="input">
  <template slot="append">.com</template>
</el-input>
```

---

## 自动清除空格

| 值 | 说明 |
|-----|------|
| trim / trim="both" | 清除前后空格 |
| trim="start" / trim="left" | 只清除前面空格 |
| trim="end" / trim="right" | 只清除后面空格 |

```vue
<el-input v-model="value" trim placeholder="自动清除前后空格" />
```

---

## 注意事项

- 密码框使用 `type="password"` + `show-password`
- 文本域可用 `autosize` 自适应高度
- `trim` 在输入时实时生效