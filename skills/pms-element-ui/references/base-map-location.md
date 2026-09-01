# BaseMapLocation 地图选点

**功能说明**：基于百度地图 JavaScript API 的位置选择组件，支持内联（inline）和弹框（dialog）两种模式。

**重要**：组件不会加载百度地图脚本，使用前需由宿主页面加载，所有百度地图 API 均从 `window.BMap` 获取。

```html
<script src="https://api.map.baidu.com/api?v=3.0&ak=YOUR_AK"></script>
```

## 位置值格式

`v-model`、`config.location` 及位置相关事件均使用以下结构：

```js
{ lng: 113.264385, lat: 23.129112, address: '广州市越秀区北京路', adcode: '440104' }
```

输入输出坐标均为 GCJ-02；显示时通过 `window.BMap.Convertor` 转为百度坐标。

## 基础用法

### 内联模式

```vue
<el-base-map-location
  v-model="location"
  mode="inline"
  :config="mapConfig"
  :height="420"
/>
```

### 弹框模式

```vue
<el-base-map-location
  v-model="location"
  mode="dialog"
  :visible.sync="visible"
  :config="mapConfig"
  title="选择项目位置"
  width="760px"
  :height="420"
/>
```

## Attributes

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| value / v-model | 当前选中位置 | Object / null | null |
| config | 地图配置 | Object | 见下表 |
| mode | 显示模式 | String | inline |
| visible | 弹框是否显示，支持 .sync | Boolean | false |
| title | 弹框标题 | String | 地图选点 |
| width | 弹框宽度 | String | 760px |
| height | 地图高度 | String / Number | 420 |
| append-to-body | 弹框是否插入 body | Boolean | true |
| close-on-click-modal | 点击遮罩是否关闭弹框 | Boolean | true |

## Config 配置

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| showSearch | 是否显示搜索栏 | Boolean | true |
| location | 初始位置；v-model 有有效坐标时优先用 v-model | Object | { lng: '', lat: '' } |
| zoom | 地图缩放级别 | Number | 11 |
| click | 是否允许点击地图选点 | Boolean | true |

## Events

| 事件名 | 说明 | 回调参数 |
|-------|------|---------|
| input | 更新 v-model | location |
| change | 位置确认后触发 | location |
| location-change | 位置确认后触发，兼容原地图组件 | location |
| select | 地图产生候选位置时触发 | location |
| confirm | 弹框点击确定时触发 | location |
| cancel | 弹框点击取消时触发 | - |
| update:visible | 弹框显示状态变化时触发 | visible |
| close | 弹框关闭时触发 | - |
| closed | 弹框关闭动画结束后触发 | - |
| error | 百度地图 API、搜索或坐标转换失败时触发 | Error |

## Methods

| 方法名 | 说明 | 参数 |
|-------|------|------|
| open | 请求打开弹框模式组件 | - |
| close | 请求关闭弹框模式组件 | - |
| clear | 清除当前标记和内部选中值 | - |
| getLocation | 根据当前搜索关键字执行搜索 | - |

## 注意事项

- 使用前必须由宿主页面加载百度地图 JavaScript API（`window.BMap`），否则组件无法工作
- 内联模式点击地图或搜索后立即更新 v-model；弹框模式需点击确定才更新
- 坐标统一使用 GCJ-02，组件内部自动转换为百度坐标显示

**参考文档**：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\base-map-location.md`
