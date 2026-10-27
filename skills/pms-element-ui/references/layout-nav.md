# 布局与容器组件

## Layout 布局

### 基础布局

```vue
<el-container>
  <el-header>Header</el-header>
  <el-main>Main</el-main>
  <el-footer>Footer</el-footer>
</el-container>

<el-container>
  <el-aside width="200px">Aside</el-aside>
  <el-main>Main</el-main>
</el-container>
```

### 常见布局

**上中下布局**：

```vue
<el-container>
  <el-header>Header</el-header>
  <el-container>
    <el-aside width="200px">Aside</el-aside>
    <el-main>Main</el-main>
  </el-container>
  <el-footer>Footer</el-footer>
</el-container>
```

## Menu 菜单

### 侧栏菜单

```vue
<el-menu
  :default-active="activeIndex"
  :collapse="isCollapse"
  :unique-opened="true"
  background-color="#545c64"
  text-color="#fff"
  active-text-color="#ffd04b"
  @select="handleSelect">

  <el-submenu index="1">
    <template slot="title">
      <i class="el-icon-location"></i>
      <span>导航一</span>
    </template>
    <el-menu-item index="1-1">选项1</el-menu-item>
    <el-menu-item index="1-2">选项2</el-menu-item>
  </el-submenu>

  <el-menu-item index="2">
    <i class="el-icon-menu"></i>
    <span slot="title">导航二</span>
  </el-menu-item>

  <el-menu-item index="3">
    <i class="el-icon-setting"></i>
    <span slot="title">导航三</span>
  </el-menu-item>
</el-menu>
```

### 顶部菜单

```vue
<el-menu :default-active="activeIndex" mode="horizontal" @select="handleSelect">
  <el-menu-item index="1">处理中心</el-menu-item>
  <el-submenu index="2">
    <template slot="title">我的工作台</template>
    <el-menu-item index="2-1">选项1</el-menu-item>
    <el-menu-item index="2-2">选项2</el-menu-item>
  </el-submenu>
  <el-menu-item index="3">消息中心</el-menu-item>
</el-menu>
```

## Dropdown 下拉菜单

### 基础用法

```vue
<el-dropdown>
  <span class="el-dropdown-link">
    下拉菜单<i class="el-icon-arrow-down el-icon--right"></i>
  </span>
  <el-dropdown-menu slot="dropdown">
    <el-dropdown-item>黄金糕</el-dropdown-item>
    <el-dropdown-item>狮子头</el-dropdown-item>
    <el-dropdown-item>螺蛳粉</el-dropdown-item>
    <el-dropdown-item disabled>双皮奶</el-dropdown-item>
    <el-dropdown-item divided>蚵仔煎</el-dropdown-item>
  </el-dropdown-menu>
</el-dropdown>
```

### 触发方式

```vue
<el-dropdown trigger="click">
  <span class="el-dropdown-link">
    下拉菜单<i class="el-icon-arrow-down el-icon--right"></i>
  </span>
  <el-dropdown-menu slot="dropdown">
    <el-dropdown-item>黄金糕</el-dropdown-item>
    <el-dropdown-item>狮子头</el-dropdown-item>
  </el-dropdown-menu>
</el-dropdown>
```

## PageHeader 页头

### 基础用法

```vue
<el-page-header @back="goBack" content="详情页面"></el-page-header>
```

## Backtop 回到顶部

### 基础用法

```vue
<el-backtop target=".page-component__scroll .el-scrollbar__wrap" :visibility-height="100">
  <i class="el-icon-caret-top"></i>
</el-backtop>
```

## 常用布局示例

> 完整的后台管理布局示例代码见 [nav-components.md](./nav-components.md) 末尾。

## Container 布局容器

**功能说明**：用于快速搭建页面基本结构的布局容器组件，基于 flex 布局。

### 基础用法

```vue
<el-container>
  <el-header>Header</el-header>
  <el-container>
    <el-aside width="200px">Aside</el-aside>
    <el-main>Main</el-main>
  </el-container>
</el-container>
```

### 常用属性

| 组件 | 参数 | 说明 | 类型 | 默认值 |
|------|------|------|------|--------|
| el-container | direction | 排列方向。有 header/footer 时自动为 vertical，否则 horizontal | horizontal / vertical | auto |
| el-header | height | 头部高度 | string | 60px |
| el-aside | width | 侧边栏宽度 | string | 300px |
| el-footer | height | 底部高度 | string | 60px |

### 注意事项

- 采用 flex 布局
- `el-container` 的子元素只能是 `el-header`、`el-aside`、`el-main`、`el-footer`
- 这些子元素的父元素必须是 `el-container`
