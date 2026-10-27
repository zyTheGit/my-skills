# BaseWorkMap 五省地图

基于 ECharts 封装的五省地图组件，支持下钻高亮、GeoJSON 监听、坐标系转换及 3D 挤出效果，配置数据遵从 ECharts 配置项规范。

## 基础用法

```vue
<template>
  <!-- 在 finish 事件后才能安全获取 ECharts 实例 -->
  <el-base-work-map
    height="500px"
    :mouse-wheel-zoom="true"
    :map-padding="{ left: 180 }"
    @finish="chartFinish"
  />
</template>

<script>
export default {
  methods: {
    chartFinish(chartInstance) {
      console.log('ECharts 实例:', chartInstance);
    },
  },
};
</script>
```

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| height | 图表容器高度 | string / number | `100%` |
| map-padding | 地图可视边距，可传 Number 或 `{ top, right, bottom, left }` | number / object | 0 |
| default-center | 默认展示中心区域坐标 | array | `[108.320004, 23.62402]` |
| coord-system | 传入坐标的坐标系，组件会转成 WGS84 绘制 | string | `WGS84` |
| default-zoom | 默认缩放大小，`1` 为铺满当前底图 | number | 1.2 |
| default-province-code | 默认选中省份编码 | number | — |
| defalut-city-code | 默认选中市区编码 | number | — |
| overview-city-codes | 总览时追加到 `geo-change` regions 的市级编码 | array | `[]` |
| isolate-selected | 选中省/市时是否只显示当前区域 | boolean | false |
| show-toolbar | 是否展示工具栏 | boolean | true |
| mouse-wheel-zoom | 是否开启鼠标滚轮缩放 | boolean | false |
| roam | 是否开启平移或缩放 | boolean / string | `move` |
| show-province-label | 是否显示省份名称 | boolean | — |
| show-city-label | 是否显示市区名称 | boolean | — |
| default-area-color | 省份默认样式 | object / string | 线性渐变 |
| active-area-color | 省份选中样式 | object / string | 线性渐变 |

## Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| finish | ECharts 实例创建完成 | chartInstance, `{ geoJson, regions }` |
| geo-change | GeoJSON 注册/更新时触发 | `{ geoJson, regions }` |
| chart-click | 点击图表触发，可用于下钻 | `{ name, adcode, level, center, parentAdcode, ... }` |
| refresh | 点击工具栏刷新时触发 | chartInstance |
| plus | 点击工具栏放大时触发 | currentZoom, chartInstance |
| minus | 点击工具栏缩小时触发 | currentZoom, chartInstance |
| georoam | 缩放和平移时触发 | currentOption, params |
| region-hover | 省份悬停抬升/离开时触发 | `{ name, adcode, hovering, offset }` |

## Methods

| 方法名 | 说明 | 参数 |
|--------|------|------|
| getChartInstance | 获取当前 ECharts 实例 | — |
| getGeoJson | 获取当前视图业务 GeoJSON | — |
| getRegionList | 获取已加载区划摘要列表 | — |
| setOption | 设置配置项并下钻 | `[provinceCode, cityCode], option` |

## 下钻示例

```vue
<template>
  <el-base-work-map
    ref="baseWorkMapRef"
    height="500px"
    @chart-click="handleChartClick"
    @refresh="handleRefresh"
  />
</template>

<script>
export default {
  data() {
    return {
      provinceCode: null,
      cityCode: null,
    };
  },
  methods: {
    handleChartClick(params) {
      const adcode = Number(params && params.adcode);
      if (!adcode) return;
      if (params.level === 'province') {
        this.provinceCode = adcode;
        this.cityCode = null;
        this.$refs.baseWorkMapRef.setOption([this.provinceCode], {
          geo: { zoom: 1.8, center: params.center },
        });
        return;
      }
      if (params.level === 'city') {
        this.cityCode = adcode;
        this.$refs.baseWorkMapRef.setOption(
          [this.provinceCode, this.cityCode],
          { geo: { zoom: 3, center: params.center } },
        );
      }
    },
    handleRefresh() {
      this.provinceCode = null;
      this.cityCode = null;
    },
  },
};
</script>
```

## 注意事项

- 底图 GeoJSON 为 WGS84，传入 `GCJ-02` / `BD-09` 坐标时组件会自动转换
- `finish` 事件触发后才可安全调用 `getChartInstance` 或自定义 ECharts 配置
- `zoom=1` 表示铺满当前已注册底图；总览约 1.2，省视图约 1.8，市视图约 3
- `isolate-selected` 开启后只显示当前区域，缩放下限为 0.85
- `overview-city-codes` 中的市级编码只进入 `regions`，不进入底图和 `geoJson`

> 源文档：examples/docs/zh-CN/base-work-map.md
