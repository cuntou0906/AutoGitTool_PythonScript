# AutoGitTool_PythonScript
​    	Python脚本：面向多个git仓库的自动添加，提交，推送，拉取操作！

### 适用范围

   	针对每个仓库，仅适用于单个分支，默认`master`，可依据代码进行修改！

### 简单上手

  在`Config_Address.json配置：
1. 设置本地仓库路径至列表`local_repos`

2. 设置远程仓库URL至列表`remote_urls`

3. 项目默认采用了uv结构，在安装了uv情况下，可以直接使用uv运行git_Add_Commit_Push_operations.py实现添加、提交、推送，使用uv运行git_Pull_operations.py实现拉取，或者采用python运行。

   ```bash
   uv run git_Add_Commit_Push_operations.py
   uv run git_Pull_operations.py
   ```

   ```bash
   python run git_Add_Commit_Push_operations.py
   python run git_Pull_operations.py
   ```

### 注意事项​  

1.   注意`local_repos`本地仓库和远端`remote_urls`必须一一对应！！！否则仓库提交就乱了！
2.   同一个远端仓库在不同电脑上的本地仓库路径可能不一样，需要对应修改`local_repos`变量！
3.   大于100 MB的文件会被添加至`.gitignore`文件中，不被`git`索引！（这是`git`本身的限制，当然可以尝试进行扩展，采用大文件`git`索引！）
