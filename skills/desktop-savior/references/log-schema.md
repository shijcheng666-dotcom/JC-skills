# 日志、索引与撤回规范

在用户确认第一份移动计划后，于归档根目录建立元数据目录：

```text
_桌面救星/
├─ desktop_rescue_profile.md
├─ desktop_rescue_log.csv
├─ desktop_rescue_index.csv
└─ runs/
   └─ <run_id>_plan.md
```

在 Windows 上写 CSV 时使用 UTF-8 with BOM，以便 Excel 正确显示中文。日志和索引只记录整理所需的最小元数据，不记录文件正文、证件号码、账号、密钥、照片人物或聊天内容。

## `desktop_rescue_log.csv`

用途：不可篡改式操作审计。每次扫描、计划、创建目录、移动、跳过、冲突、失败、恢复、删除计划与删除执行都追加一行；不得通过修改旧记录掩盖历史。发生分类修正时，追加新的 `reclassify` 或 `restore` 记录并关联原运行，不回写篡改既有移动记录。

字段：

```text
run_id
timestamp
action
source_path
target_path
item_type
extension
size_bytes
last_modified
asset_status
context_tags
protection_flag
confidence
reason
user_confirmed
status
error_message
reverses_run_id
```

建议值：

- `action`: `scan`、`plan`、`create_dir`、`move`、`skip`、`conflict`、`error`、`restore`、`reclassify`、`delete_plan`、`trash`
- `item_type`: `file`、`folder`、`shortcut`、`system`、`unknown`
- `asset_status`: `active`、`archive`、`memory`、`resource`、`sensitive`、`pending`
- `protection_flag`: `none`、`active`、`version_group`、`creative_asset`、`media_original`、`sensitive`
- `confidence`: `high`、`medium`、`low`、`user_rule`
- `status`: `planned`、`success`、`skipped`、`conflict`、`failed`
- `reverses_run_id`: 恢复操作填被撤回的原始运行批次；其他操作留空。

## `desktop_rescue_index.csv`

用途：当前检索表。只为成功移动、整体移动的文件夹，以及明确要求“保留原位仅索引”的项目建立记录。

字段：

```text
item_name
current_path
original_path
asset_status
context_tags
classification_path
keywords
extension
item_type
size_bytes
last_modified
protection_flag
archived_at
last_action
last_run_id
```

索引规则：

- 整体移动文件夹时，只索引文件夹本身；除非用户明确授权递归索引内部内容。
- `context_tags` 使用用户认可的项目、经历、事件、主题、年份或作品名，以 `|` 分隔。
- 敏感资料只记录路径、类型与 `sensitive` 标记；不要记录任何敏感正文、具体内容类别或推测性标签。目录名应使用用户指定或用户认可的中性名称。
- 对“保留原位仅索引”的高保护项目，`current_path` 与 `original_path` 相同，`last_action` 标为 `indexed_only`。
- 恢复成功后更新 `current_path`、`last_action=restore` 与 `last_run_id`，但保留原始日志。

## `desktop_rescue_profile.md`

用途：记录用户确认过的整理偏好，而非替用户建立隐私档案。

推荐结构：

```markdown
# 桌面救星整理偏好

## 范围
- 目标目录：
- 归档根目录：
- 主分类维度：状态 / 项目经历 / 事件时间 / 主题 / 混合
- 最近运行：

## 已确认规则
- 活跃资料：
- 文件夹：
- 版本组：
- 照片与视频：
- 创作资料：
- 敏感资料：
- 快捷方式与系统文件：

## 分类结构

## 已确认语境标签与项目别名

## 忽略范围

## 增量整理规则

## 备注
```

不要记录：证件号码、账户、密钥、私密内容摘要、照片人物身份、聊天正文或用户未明确要求持久保存的个人信息。

## 运行快照 `runs/<run_id>_plan.md`

在执行前保存已确认计划快照，内容包括：运行编号、确认时间、每批项目的源路径/目标路径、分类依据、保护标记、用户确认范围。

使用快照来解释或撤回一次整理；不要把未确认的计划写为已执行。

## 查找流程

1. 读取索引，先匹配 `item_name`、`original_path`、`current_path`、`context_tags`、`classification_path`、`keywords`。
2. 返回有限数量的高相关候选项，并说明匹配字段。
3. 若用户询问“为什么被移动”，再查日志与运行快照，说明时间、理由、确认状态和运行编号。
4. 若无结果，在用户已授权的归档根目录内按名称搜索；不要扩大到整个 Home。

## 撤回流程

1. 获取用户指定的 `run_id` 或时间范围。
2. 从日志选择 `action=move` 且 `status=success` 的记录。
3. 生成反向计划，逐项检查当前路径与原路径冲突。
4. 让用户确认后，每批最多恢复 10 项。
5. 对每项写入新的 `restore` 日志，填写 `reverses_run_id`；恢复失败或冲突不覆盖，留在待确认。
