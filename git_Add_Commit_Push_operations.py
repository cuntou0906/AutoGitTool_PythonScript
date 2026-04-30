import subprocess
import os
import json
from Config_parse import RepoConfigParser


class GitPush_AutoGit():
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.local_repos = []
        self.remote_urls = []
        self.PushRepo_ErrorNum = 0  # 记录推送失败的仓库数量
        self.Addparser = RepoConfigParser(self.config_file_path)

    def run_git_command(self, command, repo_dir):
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
            self.run_git_command(f"git remote add origin {remote_url}", repo_dir)

    def update_gitignore(self,repo_dir, file_path):
        """Add a file path to .gitignore if it's not already present."""
        gitignore_path = os.path.join(repo_dir, '.gitignore')
        # Read existing .gitignore content
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as gitignore_file:
                lines = gitignore_file.readlines()
        else:
            lines = []

        # Get the relative path for the file
        relative_path = os.path.relpath(file_path, repo_dir)
        relative_path = relative_path.replace('\\', '/')  # Replace backslashes with forward slashes

        # Check if the relative path is already in .gitignore
        if relative_path + '\n' not in lines:
            print(f"添加文件{file_path} 到.gitignore (文件大小超过100MB)！")
            with open(gitignore_path, 'a', encoding='utf-8') as gitignore_file:
                gitignore_file.write(f"{relative_path}\n")

    def is_tracked(self, file_path, repo_dir):
        """Check if a file is tracked by git."""
        result = subprocess.run(
            f"git ls-files --error-unmatch \"{file_path}\"",
            cwd=repo_dir,
            text=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Check if the command was successful
        if result.returncode == 0:
            return True
        else:
            # If the file is not tracked, return False
            return False

    def git_add_commit_push(self,repo_dir, message, remote='origin', branch='master'):
        """Add, commit, and push changes to the remote repository."""
        print("处理大文件：更新.gitignore！")
        # Find all files in the repo directory
        for root, dirs, files in os.walk(repo_dir):
            # Ignore the .git directory
            if '.git' in dirs:
                dirs.remove('.git')  # This will prevent os.walk from going into the .git directory

            for file in files:
                file_path = os.path.join(root, file)
                # Check file size
                if os.path.getsize(file_path) > 100 * 1024 * 1024:  # 100MB
                    self.update_gitignore(repo_dir, file_path)
                    # Remove the file from git tracking if it is tracked
                    # if is_tracked(file_path, repo_dir):
                    #     run_git_command(f"git rm --cached \"{file_path}\"", repo_dir)

        # Use 'git add .' to include all changes except those in .gitignore
        print("Adding changes...")
        AddInfo = self.run_git_command("git add .", repo_dir)

        print("Committing changes...")
        CommitInfo = self.run_git_command(f"git commit -m \"{message}\"", repo_dir)
        
        print("Pushing changes...")
        PushInfo = self.run_git_command(f"git push {remote} {branch}", repo_dir)
        if PushInfo:
            print("推送至远程仓库成功!")

        return PushInfo

    def git_pull(self, repo_dir, remote='origin', branch='master'):
        """Pull changes from the remote repository."""
        print("Pulling changes...")
        self.run_git_command(f"git pull {remote} {branch}", repo_dir)

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
                    print(f"Error: 本地仓库 {repo_directory} 不存在！")
                    self.PushRepo_ErrorNum = self.PushRepo_ErrorNum + 1
                else:
                    # Configure origin
                    self.configure_origin(repo_directory, remote_url)

                    # Perform git operations
                    Total_push_Info = self.git_add_commit_push(repo_directory, "Your commit message")

                    if not Total_push_Info:
                        print(f"推送至远程仓库失败！请检查网络或远程仓库配置是否正确。")
                        self.PushRepo_ErrorNum = self.PushRepo_ErrorNum + 1
                    
        print(f"\n##############################################################") 
        print(f"总共{len(self.local_repos)}个仓库处理完成！推送失败的仓库数量：{self.PushRepo_ErrorNum} 个。")
        print(f"##############################################################\n") 

if __name__ == "__main__":
    GitPush_AutoGitObj = GitPush_AutoGit('Config_Address.json')
    GitPush_AutoGitObj.process_result()
    
    
