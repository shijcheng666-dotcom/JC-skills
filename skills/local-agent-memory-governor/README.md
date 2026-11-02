# 本地 Agent 记忆管家（Local Agent Memory Governor）

防止全局记忆无限膨胀占用 token，也防止项目级信息混入全局记忆干扰任务效果。对本地 Agent 的全局记忆仓库做审计、备份与回滚。

## 它做什么

- 审计：去重、识别并清理项目级信息、精简画像。
- 分级处理：低风险项备份后自动处理，中高风险项等待确认。
- 备份与回滚：处理前先备份，可从备份恢复。
- 首次使用时引导设定定期（每月或每周）自动修剪计划，用户拒绝则不强制。

## 文件结构

```text
local-agent-memory-governor/
├── SKILL.md
├── references/
│   └── memory-spec.md          # 默认判定基线
└── scripts/
    ├── memory_audit.py   / run-audit.cmd
    ├── memory_backup.py  / run-backup.cmd
    └── memory_restore.py / run-restore.cmd
```

## 注意事项

- 维护对象是桌面端**全局记忆仓库**，不是当前项目工作区。仓库位置可通过环境变量 `LOCAL_AGENT_MEMORY_DIR` 指定，否则按系统标准路径自动探测。
- 脚本会修改记忆文件，首次使用建议先让 AI 只做审计，确认报告后再允许清理。
- 许可状态见 [LICENSES/](../../LICENSES/)。
