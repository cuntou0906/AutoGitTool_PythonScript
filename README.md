# AutoGitTool_PythonScript
​    Python脚本：面向多个仓库的自动添加，提交，推送，拉取操作！

### 适用范围

​    针对每个仓库，仅适用于单个分支，默认`master`，可依据代码进行修改！

### 简单上手

1. 设置本地仓库路径至列表`local_repos`
2. 设置远程仓库URL至列表`remote_urls`

### 注意事项

1.   注意`local_repos`本地仓库和远端`remote_urls`必须一一对应！！！否则仓库提交就乱了！
2.   同一个远端仓库在不同电脑上的本地仓库路径可能不一样，需要对应修改`local_repos`变量！
3.   大于100 MB的文件会被添加至`.gitignore`文件中，不被`git`索引！（这是`git`本身的限制，当然可以尝试进行扩展，采用大文件`git`索引！）
