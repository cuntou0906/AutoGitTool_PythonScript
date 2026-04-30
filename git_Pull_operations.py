#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File          : git_Pull_operations.py
# @Version       : 1.0.0
# @Description   : This File is about ...
# @Time          : 2026/05/01 00:08
# @Author        : cuntou0906
# @Email         : 1084895390@qq.com

import subprocess
import os
import json
from Config_parse import RepoConfigParser

class GitPull_AutoGit(Exception):

    def __init__(self,config_file_path):

        self.Addparser = RepoConfigParser(config_file_path)
        self.pullRepo_ErrorNum = 0  # 记录拉取失败的仓库数量
        self.local_repos = None       # 本地仓库路径列表
        self.remote_urls = None       # 远程仓库URL列表

    def run_git_command(self,command, repo_dir):
        """Run a git command in the specified repository directory."""
        try:
            result = subprocess.run(
                command,
                cwd=repo_dir,
                text=True,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Only print if there is meaningful output
            output = result.stdout.strip()
            if output:
                print(output)
            return True
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.strip()
            if error_output:
                print(f"Error: {error_output}")
            return False

    def configure_origin(self, repo_dir, remote_url):
        """Configure the origin remote for the repository."""
        try:
            # Check if origin already exists
            result = subprocess.run(
                "git remote get-url origin",
                cwd=repo_dir,
                text=True,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            current_url = result.stdout.strip()
            if current_url != remote_url:
                print(f"将目前远端URL仓库Origin：{current_url} 更新为：{remote_url}！")
                self.run_git_command(f"git remote set-url origin {remote_url}", repo_dir)
            else:
                print(f"远端URL仓库Origin已经设置为 {remote_url}.")
        except subprocess.CalledProcessError:
            # If origin does not exist, add it
            print(f"配置远端URL仓库Origin为：{remote_url}...")
            GitRemoteInfo = self.run_git_command(f"git remote add origin {remote_url}", repo_dir)


    def git_pull(self, repo_dir, remote='origin', branch='master'):
        """Pull changes from the remote repository."""
        print("Pulling changes...")
        return self.run_git_command(f"git pull {remote} {branch}", repo_dir)

    def git_clone(self, repo_dir, repo_url, branch='master'):
        """Clone a remote repository."""
        # print("Cloning repository...")
        try:
            # 使用subprocess.run执行git clone命令
            subprocess.run(['git', 'clone', repo_url, repo_dir, '--branch', branch], check=True)
            print(f"远程仓库已成功克隆到 {repo_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"克隆失败: {e}")
            self.pullRepo_ErrorNum = self.pullRepo_ErrorNum + 1
            return

    def process_result(self):

        # 判断解析是否成功
        if self.Addparser.is_success():
            self.local_repos, self.remote_urls = self.Addparser.get_paths_and_urls()
        else:
            print("配置文件解析失败，请重试:", self.Addparser.error_message)
            return
            
        # Ensure the lists are of the same length
        if len(self.local_repos) != len(self.remote_urls):
            print("Error: 本地存储库和远程url的数量必须匹配，且一一对应！")
        else:
            # Iterate over each repository
            for repo_directory, remote_url in zip(self.local_repos, self.remote_urls):

                print(f"\n##############################################################")
                print(f"处理仓库: {repo_directory}")
                # Ensure the directory exists
                if not os.path.isdir(repo_directory):
                    print(f"本地仓库 {repo_directory} 不存在！,正在创建仓库目录...")
                    #创建文件夹
                    os.makedirs(repo_directory)
                
               # 检查是否是一个Git仓库，如果不是则初始化为Git仓库
                if not self.is_git_repo(repo_directory):
                    # 不是git仓库，直接克隆远程仓库到本地
                    # Configure origin
                    # self.configure_origin(repo_directory, remote_url)
                    # Perform git operations             
                    CloneInfo = self.git_clone(repo_directory, remote_url)
                    if not CloneInfo:
                        print(f"从远程仓库克隆失败！请检查网络或远程仓库配置是否正确。")
                        self.pullRepo_ErrorNum = self.pullRepo_ErrorNum + 1
                    pass
                else:
                    # 以下执行的操作是为了处理已经存在的Git仓库，确保它们正确配置了远程仓库，并且能够成功拉取最新的更改。       
                    # Configure origin
                    self.configure_origin(repo_directory, remote_url)
                    # Perform git operations             
                    PullInfo = self.git_pull(repo_directory) 
                    if not PullInfo:
                        print(f"从远程仓库拉取失败！请检查网络或远程仓库配置是否正确。")
                        self.pullRepo_ErrorNum = self.pullRepo_ErrorNum + 1

        print(f"\n##############################################################") 
        print(f"总共{len(self.local_repos)}个仓库处理完成！拉取失败的仓库数量：{self.pullRepo_ErrorNum} 个。")
        print(f"##############################################################\n") 

    def is_git_repo(self,folder_path):
        try:
            # 进入指定目录
            result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=folder_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # 如果命令执行成功，说明是一个Git仓库
            if result.returncode == 0:
                return True
            else:
                return False
            
        except FileNotFoundError:
            # 如果git命令不可用，可能是因为没有安装git或者不在PATH中
            return False         

if __name__ == "__main__":
    GitPull_AutoGitObj = GitPull_AutoGit('Config_Address.json')
    GitPull_AutoGitObj.process_result()
    
