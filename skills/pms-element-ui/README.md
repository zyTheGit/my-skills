# PMS 组件库知识库

> 基于 pms-base-element 组件库的完整知识库，按照组件类型分类整理

---

## 📚 知识库导航

### 一、快速开始

- **[01-快速开始.md](./01-快速开始.md)** - 安装指南、快速上手、全局SDK使用
  - 组件库安装与配置
  - Min-Web3 全局 SDK（工具、请求、事件总线、权限等）

### 二、核心业务组件

- **[02-基础业务组件.md](./02-基础业务组件.md)** - **24个**核心业务组件（23个 base-* + MicroKeepAliveView）
  - **高级表格** (BaseProTable) - 企业级表格解决方案
  - **高级表单** (BaseProForm) - 支持查看/新增/编辑模式
  - **高级搜索** (BaseProSearch) - 复杂搜索条件组合
  - **流程组件** (BaseProProcess, BaseProcessHandle, BaseApprovalResult) - 流程审批
  - **选择器** (BaseOrgantCascader, BaseAffiliatedUnit, BaseDictionary) - 业务选择
  - **上传组件** (BaseChunkUpload, BaseUploadList) - 文件上传管理
  - **预览器** (BaseImgPreviewer, BaseFilePreviewer) - 文件预览
  - **地图** (BaseMapLocation, BaseWorkMap) - 地图选点与五省地图
  - **树形** (BaseTree, BaseVirtualTree) - 树形与大数据量虚拟树
  - **工具栏/底部栏/视图切换** (BaseToolBar, BasePageFooter, BaseViewSwitcher)
  - **微前端保活** (MicroKeepAliveView) - 子应用页面缓存

### 三、基础组件库

- **[03-表单组件.md](./03-表单组件.md)** - **17个**表单相关组件
- **[04-数据展示组件.md](./04-数据展示组件.md)** - **19个**数据展示组件
- **[05-布局导航组件.md](./05-布局导航组件.md)** - **10个**布局导航组件
- **[06-反馈组件.md](./06-反馈组件.md)** - **11个**反馈组件
- **[07-其他组件.md](./07-其他组件.md)** - **7个**其他组件

详细组件清单见各分类文件的"组件列表"表格。

### 四、主题和工具

- **[08-主题和工具.md](./08-主题和工具.md)** - 主题定制、国际化、权限、工具函数
  - 远程组件接入（qiankun 微前端）
  - 版本管理（window.$versionService）

---

## 🎯 使用建议

| 使用场景 | 推荐组件 |
|---------|---------|
| **列表页面** | BaseProTable + BaseProSearch |
| **表单页面** | BaseProForm + 表单组件 |
| **详情页面** | BaseProForm(view模式) + Descriptions |
| **流程审批** | BaseProProcess + BaseProcessHandle |
| **文件上传** | BaseChunkUpload + BaseUploadList |
| **地图/树形** | BaseMapLocation / BaseWorkMap / BaseVirtualTree |
| **组织选择** | BaseOrgantCascader |
| **字典选择** | BaseDictionary |

---

## 📊 组件统计

- **总组件数**：88个（业务组件 24 个）
- 其余：表单 17、数据展示 19、布局导航 10、反馈 11、其他 7

---

## 🔗 相关链接

- 组件库文档：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN`
- 全局SDK文档：见 `01-快速开始.md` 中的 Min-Web3 SDK 部分
- 权限控制：见 `08-主题和工具.md` 中的权限部分

---

## 📝 更新日志（完整历史见 [references/CHANGELOG.md](./references/CHANGELOG.md)）

### 2026-09-26
- 新增：BaseApprovalResult、BaseVirtualTree、BaseWorkMap 三个业务组件；版本管理文档
- 更新：BaseProForm 字段联动、流程组件自定义接口、Input 超长悬浮、远程组件、MicroKeepAliveView 等
- 更新：组件总数 90->93，业务组件 21->24；拆分历史超长文件（01/05/06/07）

### 2026-08-11
- 新增：BaseMapLocation 地图选点组件
- 更新：BaseChunkUpload、BaseImport、BaseProTable、BaseProProcess、BaseProcessHandle、Table、Upload 等
- 更新：组件总数 89->90，业务组件 20->21

### 2026-07-29
- 新增：远程组件接入说明（qiankun 微前端架构）

---

**最后更新时间**：2026-09-26
