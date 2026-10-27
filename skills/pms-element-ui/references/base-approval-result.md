# BaseApprovalResult 审批结果

从 `el-base-process-handle` 查看态右侧表单抽出的审批结果卡片组件，复用同一套视觉样式（渐变底色、状态色文案、右侧印章图），也可独立使用或嵌入自定义表单。

## 基础用法

### 独立使用

```vue
<template>
  <div>
    <el-radio-group v-model="approvalValue">
      <el-radio-button label="agree">通过</el-radio-button>
      <el-radio-button label="oppose">不通过</el-radio-button>
      <el-radio-button label="takeback">撤回</el-radio-button>
    </el-radio-group>

    <!-- 状态与文案由 value 自动推导 -->
    <el-base-approval-result :value="approvalValue" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      approvalValue: 'agree',
    };
  },
};
</script>
```

### 在 ProForm 中复用

```vue
<template>
  <el-base-pro-form
    :drawer="false"
    :columns="columns"
    :initial-values="model"
    label-position="top"
    :is-show-footer="false"
  >
    <!-- bleed 让卡片左右贴到容器边缘 -->
    <template slot="form-approvalResult" slot-scope="{ column, value }">
      <el-base-approval-result
        :title="column.title"
        :value="value"
        :options="column.form.options"
        bleed
      />
    </template>
  </el-base-pro-form>
</template>
```

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| value | 审批值，用于推导状态与文案 | string / number | `''` |
| status | 显式指定状态，优先级最高 | string | `''` |
| label | 显式指定展示文案 | string | `''` |
| options | 审批选项，用于反查文案与状态 | array | `null` |
| title | 卡片标题；传 `''` 不渲染标题 | string | `审批结果` |
| show-image | 是否渲染右侧印章图 | boolean | `true` |
| image | 自定义印章图地址 | string | `''` |
| bleed | 是否左右外扩到容器内边距之外 | boolean | `false` |

## Slots

| 插槽名 | 说明 | 作用域参数 |
|--------|------|------------|
| title | 覆盖标题区 | `{ title }` |
| default | 覆盖文案区（印章图仍由组件渲染） | `{ status, label, value }` |

## 状态推导规则

状态按以下顺序命中：

1. `status` 显式指定 `success` / `danger` / `withdrawn`
2. `options` 中匹配 `value` 的选项 `status`
3. `value` 为 `takeback` 或 `撤回` → `withdrawn`
4. `value` 归一化后属于 `oppose` 系 → `danger`
5. `value` 归一化后属于 `agree` 系 → `success`
6. 未命中 → 中性渐变底色，无印章图

文案优先级：`label` → `options` 命中项 `label` → 状态兜底文案 → `value` 原始值 → `-`

## 注意事项

- 使用 `bleed` 嵌入 `el-base-pro-form` 时，form-item 需加 `formItemClass: 'el-base-approval-result-item'` 隐藏自带 label
- `bleed` 外扩量由 CSS 变量 `--el-base-approval-result-bleed` 控制，默认取 pro-form 容器内边距
- 状态类名：`is-success` / `is-danger` / `is-withdrawn`，可按需覆盖渐变底色与文案色

> 源文档：examples/docs/zh-CN/base-approval-result.md
