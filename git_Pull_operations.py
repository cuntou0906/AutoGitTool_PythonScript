import subprocess
import os

def run_git_command(command, repo_dir):
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

def configure_origin(repo_dir, remote_url):
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
            run_git_command(f"git remote set-url origin {remote_url}", repo_dir)
        else:
            print(f"远端URL仓库Origin已经设置为 {remote_url}.")
    except subprocess.CalledProcessError:
        # If origin does not exist, add it
        print(f"配置远端URL仓库Origin为：{remote_url}...")
        run_git_command(f"git remote add origin {remote_url}", repo_dir)


def git_pull(repo_dir, remote='origin', branch='master'):
    """Pull changes from the remote repository."""
    print("Pulling changes...")
    run_git_command(f"git pull {remote} {branch}", repo_dir)

if __name__ == "__main__":
    # 注意local_repos本地仓库和远端remote_urls必须一一对应！！！否则仓库提交乱了
    # List of local repository paths
    local_repos = [
        "C:\\Users\\cunto\\Desktop\\tese",
        "C:\\Users\\cunto\\Desktop\\Repo2"
    ]

    # Corresponding list of remote repository URLs
    remote_urls = [
        "https://github.com/cuntou0906/tese.git",
        "https://github.com/cuntou0906/Repo2.git"
    ]

    # Ensure the lists are of the same length
    if len(local_repos) != len(remote_urls):
        print("Error: 本地存储库和远程url的数量必须匹配，且一一对应！")
    else:
        # Iterate over each repository
        for repo_directory, remote_url in zip(local_repos, remote_urls):
            print(f"\n处理仓库: {repo_directory}")
            # Ensure the directory exists
            if not os.path.isdir(repo_directory):
                print(f"Error: 本地仓库 {repo_directory} 不存在！")
            else:
                # Configure origin
                configure_origin(repo_directory, remote_url)
                
                # Perform git operations
                # git_add_commit_push(repo_directory, "Your commit message")
                
                git_pull(repo_directory) 