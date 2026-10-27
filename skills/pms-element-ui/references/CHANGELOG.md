# 知识库更新日志

> 完整更新历史。最新 3 条摘录同步到知识库根 README.md 的更新日志章节。

## 2026-09-26
- 新增：BaseApprovalResult 审批结果卡片组件文档（独立使用 / 嵌入 ProForm、状态推导规则、bleed 外扩）
- 新增：BaseVirtualTree 虚拟树组件文档（大数据量、与 el-tree API 一致、node-key 必填）
- 新增：BaseWorkMap 五省地图组件文档（ECharts 下钻、geo-change 事件、坐标系转换、overview-city-codes）
- 新增：版本管理文档（window.$versionService，微前端构建版本标识与对比），收录于 08-主题和工具
- 新增：references/CHANGELOG.md，README 更新日志外移至此（README 瘦身）
- 更新：BaseProForm 新增字段联动章节（form.show / form.linkage、immediate、afterFetch 自动选中唯一选项示例）
- 更新：BaseProProcess / BaseProcessHandle 新增自定义审批日志与子流程接口（logs-handler / process-logs-handler / log-url 等）
- 更新：BaseProcessHandle 新增插槽（form-${field} 右侧表单字段插槽等）
- 更新：BaseImport 的 use-file-module-config 默认值改为 false，补充 resolve 接口说明
- 更新：Input 新增 show-overflow-tooltip 文本超长悬浮显示（默认开启）
- 更新：远程组件文档大幅更新（签名私钥改环境变量 REMOTE_COMPONENT_SIGN_PRIVATE_KEY 注入等）
- 更新：MicroKeepAliveView 对标源文档重写为子应用接入手册结构（30 秒结论、改造前后对比）
- 更新：BaseImgPreviewer / BaseFilePreviewer 新增 default-fit-to-window 默认适应窗口参数
- 更新：组件总数 90->93，业务组件 21->24
- 更新：拆分历史遗留超长文件（01/05/06/07），概览文件全部瘦身为索引

## 2026-08-11
- 新增：BaseMapLocation 地图选点组件文档（百度地图 API，inline/dialog 双模式）
- 更新：BaseChunkUpload 重写，修正 API 描述，补充 uploadListType、item-append/item-actions 插槽、beforeRemove 等
- 更新：BaseImport 重写，补充 uploadMethod、responseHandler、uploadData、complete 事件、目录上传（directory/drag-directory）等新 API
- 更新：BaseProTable 补充列宽规则（enable-column-rules/column-rules/ruleType）、valueDict 字典映射、操作列权限（permission/permissionMode）等
- 更新：BaseProProcess 重写，补充子流程节点、会签/或签、抽屉模式、接口模式、完整数据结构
- 更新：BaseProcessHandle 重写，补充三栏布局、6 个内置接口、right-form-column-merges 合并规则、disabled 查看态
- 更新：Table 补充新增行飞入动画（row-animation）、highlight-selection-row、select-on-row-click、header-color、filter-type 关键字筛选等
- 更新：Upload 补充 directory、drag-directory 目录上传
- 更新：组件总数 89->90，业务组件 20->21（新增 BaseMapLocation）

## 2026-07-29
- 新增：远程组件接入说明（qiankun 微前端架构）
- 更新：08-主题和工具.md 新增第九章"远程组件接入"
- 更新：README.md 导航目录补充远程组件内容

## 2026-06-11
- 新增：MicroKeepAliveView 微前端页签保活组件文档
- 更新：Input 新增 trim 属性（自动清除输入值空格）
- 更新：组件总数 88→89，业务组件 19→20

## 2026-06-09
- 增量更新：新增 26 个 Element 组件文档
- 新增（表单）：InputNumber、Radio、Checkbox、Switch、TimePicker、DateTimePicker、Rate、Slider、ColorPicker、Transfer
- 新增（数据展示）：Descriptions、Image、Carousel、Collapse、Timeline、Statistic、Result、Skeleton、Tree
- 新增（布局）：Container
- 新增（反馈）：Tooltip
- 新增（其他）：Avatar、Divider
- 新增（主题工具）：Typography 排版规范、ThemeProvider 运行时主题切换
- 更新：03-表单组件 7→17 节，04-数据展示 9→18 节，05-布局导航 9→10 节，06-反馈 10→11 节，07-其他 5→7 节，08-主题工具 6→8 节

## 2026-05-13
- 新增：BasePageFooter 页面底部操作栏组件文档
- 新增：BaseViewSwitcher 视图切换组件文档
- 更新：BaseProTable 新增 single-selectable 单项禁用控制
- 更新：BaseProProcess 新增 status-images、auto-load-logs、抽屉事件/方法、Slots
- 更新：BaseProcessHandle 新增 footer-bleed、left-width 等属性及待办说明
- 修正：02-基础业务组件.md 章节编号
- 更新：组件总数 86→88

## 2026-04-23
- 新增：BaseToolBar 工具栏组件文档
- 更新：Tabs 标签页新增 lineless（隐藏下划线）和 size（尺寸）属性

## 2026-04-09
- 初始化知识库
- 完成所有组件文档整理
