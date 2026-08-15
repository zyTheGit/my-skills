# pi 平台 API 参考

核心方法论见父级 `SKILL.md`。

## 基础

```javascript
// 获取可用 agent
subagent({ action: "list" })

// 启动一个
subagent({ workflowScript: `return runs.run("k", { agent: "name", task: "..." })`, async: true })

// 并行多个
subagent({ workflowScript: `return (await runs.all([...])).map(r => r.output)`, async: true })

// 查看状态
subagent({ action: "status", view: "fleet" })
subagent({ action: "interrupt", id: "run-id" })
```

## 五种模式

### A：前后端并行

```javascript
subagent({ workflowScript: `
  const r = await runs.all([
    { key: "be", agent: "cloudfn-writer", task: "实现云函数..." },
    { key: "fe", agent: "page-builder", task: "新建页面..." },
    { key: "audit", agent: "security", task: "审计代码，只读不修改" }
  ]);
  return { be: r[0].output, fe: r[1].output, audit: r[2].output };
`, async: true })
```

### B：多页面并行

```javascript
subagent({ workflowScript: `
  return (await runs.all([
    { key: "a", agent: "page-builder", task: "构建页面 A" },
    { key: "b", agent: "page-builder", task: "构建页面 B" }
  ])).map(r => r.output);
`, async: true })
```

### C：实现 + 审查并行

```javascript
subagent({ workflowScript: `
  const r = await runs.all([
    { key: "impl", agent: "worker", task: "实现功能..." },
    { key: "review", agent: "reviewer", task: "审查 diff，只读不修改" }
  ]);
  return { impl: r[0].output, review: r[1].output };
`, async: true })
```

### D：设计 + 实现流水线

```javascript
subagent({ workflowScript: `
  const plan = await runs.run("design", { agent: "architect", task: "设计技术方案" });
  const [ui, be] = await runs.all([
    { key: "ui", agent: "ui-ux", task: "设计 UI" },
    { key: "be", agent: "cloudfn-writer", task: "实现后端: " + plan.output }
  ]);
  const fe = await runs.run("fe", { agent: "page-builder", task: "实现前端，UI: " + ui.output });
  return { ui: ui.output, be: be.output, fe: fe.output };
`, async: true })
```

### E：分阶段修复

```javascript
subagent({ async: true, workflowScript: `
  // 阶段1：并行规划
  const plans = await runs.all([
    { key: "a", agent: "reviewer", task: "分析问题集群 A，输出修复方案。不要修改文件。" },
    { key: "b", agent: "reviewer", task: "分析问题集群 B，输出修复方案。不要修改文件。" }
  ]);
  // 阶段2：单一 writer 修复
  const fix = await runs.run("fix", { agent: "worker", task: "逐一修复：\n" + plans.map(p => p.output).join("\n") });
  // 阶段3：并行验证
  const vals = await runs.all([
    { key: "va", agent: "reviewer", task: "验证集群 A 修复结果。不要修改文件。" },
    { key: "vb", agent: "reviewer", task: "验证集群 B 修复结果。不要修改文件。" }
  ]);
  return { fix: fix.output, validations: vals.map(v => v.output) };
` })
```

## Worktree 隔离

```javascript
subagent({ workflowScript: `
  return (await runs.all([
    { key: "a", agent: "worker", task: "实现功能 A", worktree: true },
    { key: "b", agent: "worker", task: "实现功能 B", worktree: true }
  ])).map(r => ({ key: r.key, paths: r.artifactPaths }));
` })
```

## 验收

```javascript
// 验证合约
runs.run("impl", { agent: "worker", task: "...", acceptance: {
  level: "checked", evidence: ["changed-files", "commands-run", "residual-risks"]
}})

// 简写 gate
runs.run("impl", { agent: "worker", task: "...", gate: "npm test" })
```

## 子 agent 通信

```javascript
// 子 agent 请求
contact_supervisor({ reason: "need_decision", message: "应该优先可读性还是性能？" })
contact_supervisor({ reason: "progress_update", message: "发现需要额外重构模块 Y。" })

// 父 agent 回复
subagent_supervisor({ action: "pending" })
subagent_supervisor({ action: "reply", message: "优先可读性。" })
```

## 异步等待

```javascript
subagent_wait({ id: "run-id" })           // 等特定
subagent_wait({ all: true })              // 等全部
subagent_wait({ timeoutMs: 600000 })      // 带超时
subagent_wait({ id: "run-id", nonBlocking: true })  // 非阻塞订阅
```

交互式对话中通常不调用 `subagent_wait`，返回控制权给用户。

## 常用参数

| 参数 | 说明 |
|------|------|
| `async: true` | 异步（推荐默认） |
| `context: "fresh"` | 干净上下文 |
| `context: "fork"` | 继承父会话 |
| `worktree: true` | 工作区隔离 |
| `gate: "cmd"` | 验证命令 |
| `output: "path"` | 输出路径 |
| `outputMode: "file-only"` | 仅文件输出 |
| `timeoutMs` | 超时毫秒 |