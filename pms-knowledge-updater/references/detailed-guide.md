# 详细更新流程

## 1. 确定更新范围

询问用户要更新哪些内容：

- **全部更新**：重新扫描所有文档，更新所有知识库文件
- **部分更新**：只更新特定类型的组件或特定文件
- **增量更新**：只更新新增或修改的文档

---

## 2. 扫描源文档目录

源文档目录：使用配置的路径（首次使用时会询问）

默认值：`C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN`

扫描步骤：1. 列出所有 `.md` 文件
2. 按文件名分类：
   - `base-*` 开头：基础业务组件
   - 表单组件：input, select, form 等
   - 数据展示：table, tag, badge 等
   - 布局导航：layout, menu, tabs 等
   - 反馈组件：dialog, message 等
   - 其他：button, icon 等
   - 文档：quickstart, installation 等

---

## 3. 更新策略详解

### 全量更新

适用于：首次创建知识库、大规模文档更新、结构调整

步骤：
1. 扫描所有源文档
2. 按分类重新整理
3. 重写知识库文件
4. 更新 README.md 和 SKILL.md

### 增量更新

适用于：少量文档更新、新增组件、修正错误

步骤：
1. 识别变更的文档
2. 定位对应的知识库文件
3. 更新相关章节
4. 保持其他内容不变

---

## 4. 更新检查清单

### 必需检查项

- [ ] 所有 `base-*` 组件都已包含在 `02-基础业务组件.md`
- [ ] 组件分类正确
- [ ] 代码示例格式正确
- [ ] 属性表格完整
- [ ] 中文说明清晰

### 可选检查项

- [ ] 更新了 README.md 中的统计数据
- [ ] 更新了 SKILL.md 中的触发关键词
- [ ] 添加了新的使用场景
- [ ] 更新了最后修改时间

---

## 5. 快速命令

```bash
# 查看源文档列表
ls C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\*.md

# 查看知识库文件
ls ../pms-element-ui/

# 对比文档数量
ls C:\zy\project\nfdw\pms-base-element\examples\docs\zh-CN\*.md | Measure-Object
ls ../pms-element-ui/*.md | Measure-Object
```