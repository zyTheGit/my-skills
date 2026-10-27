# 导航类组件

## Tabs 标签页

### 基础用法

```vue
<el-tabs v-model="activeName" @tab-click="handleClick">
  <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
  <el-tab-pane label="配置管理" name="second">配置管理</el-tab-pane>
  <el-tab-pane label="角色管理" name="third">角色管理</el-tab-pane>
</el-tabs>
```

### 无下划线

使用 `lineless` 属性隐藏下划线：

```vue
<el-tabs v-model="activeName" lineless>
  <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
  <el-tab-pane label="配置管理" name="second">配置管理</el-tab-pane>
</el-tabs>
```

### 卡片样式

```vue
<el-tabs v-model="activeName" type="card" closable @tab-remove="removeTab">
  <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
  <el-tab-pane label="配置管理" name="second">配置管理</el-tab-pane>
</el-tabs>
```

### 尺寸设置

使用 `size` 属性设置标签页尺寸，支持 `large` 和 `xlarge`：

```vue
<!-- 默认尺寸 -->
<el-tabs v-model="activeName">
  <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
</el-tabs>

<!-- 大尺寸 -->
<el-tabs v-model="activeName" size="large">
  <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
</el-tabs>

<!-- 超大尺寸 -->
<el-tabs v-model="activeName" size="xlarge">
  <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
</el-tabs>
```

### 动态增减标签页

```vue
<el-tabs v-model="editableTabsValue" type="card" editable @edit="handleTabsEdit">
  <el-tab-pane
    :key="item.name"
    v-for="item in editableTabs"
    :label="item.title"
    :name="item.name"
  >
    {{ item.content }}
  </el-tab-pane>
</el-tabs>
```

### Tabs Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
|-----|------|------|--------|--------|
| value / v-model | 绑定值，选中选项卡的 name | string | — | 第一个选项卡的 name |
| type | 风格类型 | string | card / border-card | — |
| closable | 标签是否可关闭 | boolean | — | false |
| lineless | 隐藏下划线 | boolean | — | false |
| addable | 标签是否可增加 | boolean | — | false |
| editable | 标签是否同时可增加和关闭 | boolean | — | false |
| tab-position | 选项卡所在位置 | string | top / right / bottom / left | top |
| stretch | 标签的宽度是否自撑开 | boolean | — | false |
| size | 标签页尺寸 | string | large / xlarge | — |
| before-leave | 切换标签之前的钩子 | Function(activeName, oldActiveName) | — | — |

## Breadcrumb 面包屑

### 基础用法

```vue
<el-breadcrumb separator="/">
  <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
  <el-breadcrumb-item><a href="/">活动管理</a></el-breadcrumb-item>
  <el-breadcrumb-item>活动列表</el-breadcrumb-item>
  <el-breadcrumb-item>活动详情</el-breadcrumb-item>
</el-breadcrumb>
```

### 图标分隔符

```vue
<el-breadcrumb separator-class="el-icon-arrow-right">
  <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
  <el-breadcrumb-item>活动管理</el-breadcrumb-item>
  <el-breadcrumb-item>活动列表</el-breadcrumb-item>
</el-breadcrumb>
```

## Steps 步骤条

### 基础用法

```vue
<el-steps :active="active" finish-status="success">
  <el-step title="步骤 1" description="这是一段很长很长很长的描述性文字"></el-step>
  <el-step title="步骤 2" description="这是一段很长很长很长的描述性文字"></el-step>
  <el-step title="步骤 3" description="这段就没那么长了"></el-step>
</el-steps>

<el-button @click="next">下一步</el-button>
```

### 竖向步骤条

```vue
<el-steps direction="vertical" :active="1">
  <el-step title="步骤 1"></el-step>
  <el-step title="步骤 2"></el-step>
  <el-step title="步骤 3"></el-step>
</el-steps>
```

---

## 常用布局示例

### 后台管理布局

```vue
<el-container style="height: 100vh">
  <!-- 侧边栏 -->
  <el-aside width="200px">
    <el-menu
      :default-active="$route.path"
      router
      :collapse="isCollapse">
      <el-menu-item index="/dashboard">
        <i class="el-icon-menu"></i>
        <span slot="title">首页</span>
      </el-menu-item>
      <el-submenu index="/system">
        <template slot="title">
          <i class="el-icon-setting"></i>
          <span>系统管理</span>
        </template>
        <el-menu-item index="/system/user">用户管理</el-menu-item>
        <el-menu-item index="/system/role">角色管理</el-menu-item>
      </el-submenu>
    </el-menu>
  </el-aside>

  <!-- 主内容区 -->
  <el-container>
    <!-- 顶部导航 -->
    <el-header>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{$route.meta.title}}</el-breadcrumb-item>
      </el-breadcrumb>
    </el-header>

    <!-- 内容区 -->
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</el-container>
```

