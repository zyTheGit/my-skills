# Carousel 走马灯

## 核心特性

- 支持自动播放
- 支持多种切换效果
- 支持指示器和箭头
- 常用于图片轮播展示

## 基础用法

```vue
<el-carousel height="150px">
  <el-carousel-item v-for="item in 4" :key="item">
    <h3>{{ item }}</h3>
  </el-carousel-item>
</el-carousel>
```

## 常用属性

| 参数 | 说明 | 类型 | 默认值 |
|-----|------|------|--------|
| height | 轮播高度 | string | - |
| trigger | 指示器触发方式 | click / hover | hover |
| autoplay | 是否自动播放 | boolean | true |
| interval | 自动播放间隔（ms） | number | 3000 |
| indicator-position | 指示器位置 | outside / none | inside |
| arrow | 切换箭头显示 | always / hover / never | hover |
| type | 类型（card 为卡片模式） | string | - |
| loop | 是否循环显示 | boolean | true |
| direction | 展示方向 | horizontal / vertical | horizontal |

## 常用事件

| 事件名 | 说明 | 参数 |
|-------|------|------|
| change | 幻灯片切换时触发 | (activeIndex, oldIndex) |

## 方法

| 方法名 | 说明 | 参数 |
|-------|------|------|
| setActiveItem | 手动切换到指定幻灯片 | index |
| prev | 切换到上一张 | - |
| next | 切换到下一张 | - |

## 注意事项

- `type="card"` 启用卡片模式，允许点击两侧幻灯片切换