# Git 同步与推送故障排查 SOP (针对 Gemini 2.5/从属模型)

当你收到“修改并推送”指令，但运行 `git status` 却显示 `nothing to commit, working tree clean` 时，请严格按照以下步骤排查，不要直接放弃或认为任务已完成。

## 第零步：建立环境坐标 (防止 EISDIR 报错与路径迷失)
在执行任何读写前，必须确认你的“当前位置”：

### 1. 路径精准搜索 (拒绝盲目 dir)
如果你只知道文件夹名字(如 `astroship`)但不知道父路径，**严禁**直接 `dir D:\` 这种全盘扫描。
- **推荐做法**：使用带过滤条件的搜索命令。
  - **Windows (PowerShell)**: `dir D:\ -Filter "*astroship*" -Recurse -Directory -ErrorAction SilentlyContinue | Select-Object FullName`
  - **CMD**: `dir D:\*astroship* /s /ad /b`
- **目的**：通过过滤脚本直接获取绝对路径，不要用肉眼去长列表中翻找。

### 2. 环境定位
1. **环境定位**：运行 `pwd` (或 Windows 的 `cd`) 确认你的 CWD。
2. **区分目录与文件**：
   - 如果 `read_file` 报错 `EISDIR`：说明你读的是个**文件夹**。绝对不要重复尝试，立即改用 `list_files` 查看其内部。
   - 如果你不确定一个路径是文件还是文件夹：先运行 `ls -d "路径"` 或 `list_files` 验证。

## 第一步：确认文件状态与路径正确性 (防拼写错误)
当你尝试读取或写入文件遇到 `File not found` 错误时，**严禁**假设文件不存在。
1. **强制执行目录发现**：立即运行 `list_files` 或 `ls -a` 检查该目录下的所有文件名。
2. **肉眼对齐**：对比你预想的文件名（如 `.cursorules`）与 `list_files` 返回的真实名称（如 `.cursorrules`）。
3. **确认磁盘更新**：只有在确认文件名 100% 匹配后，使用 `read_file` 检查。
   - 如果内容未更新：说明之前的编辑工具（replace_in_file）匹配失败了，请尝试直接使用 `write_to_file` 覆盖整个文件。
   - 如果内容已更新：进入下一步检查 Git。

## 第二步：检查 Git 忽略规则 (核心)
如果磁盘有更新但 Git 没反应，极大概率是文件被 `.gitignore` 过滤了。
1. **运行检查命令**：
   `git check-ignore -v "你的文件路径"`
2. **分析结果**：
   - 如果输出了忽略规则（例如 `.gitignore:23:*.md`）：说明 Git 被禁止追踪该文件。
   - **对策**：使用强制添加指令 `git add -f "你的文件路径"`。

## 第三步：强制追踪与状态校准
不要只运行 `git add .`。请针对具体文件操作：
1. `git add -f "具体文件路径"`
2. `git status`
3. 此时如果显示 `modified` 或 `new file`，则可以继续。

## 第四步：Git 环境路径补救
如果你收到 `fatal: not a git repository`：
1. 确认你所在的当前工作目录。
2. 使用 `-C` 参数强制指定仓库执行（最稳妥）：
   `git -C "仓库绝对路径" add -A`
   `git -C "仓库绝对路径" commit -m "update"`

## 第五步：禁止“自动脑补”
- **严禁**：在没有看到 `git commit` 成功输出（如 `[master xxx] ...`）的情况下告诉用户已完成。
- **要求**：如果连续两次 `git status` 都显示 clean，必须向用户汇报“磁盘已更新但 Git 忽略了该文件”，并请求强制推送许可或自动尝试 `git add -f`。

---
*注：本 SOP 旨在解决“看得见更新，推不上去”的逻辑陷阱。*
