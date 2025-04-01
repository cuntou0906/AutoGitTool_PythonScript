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

def update_gitignore(repo_dir, file_path):
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
        with open(gitignore_path, 'a', encoding='utf-8') as gitignore_file:
            gitignore_file.write(f"{relative_path}\n")

def is_tracked(file_path, repo_dir):
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

def git_add_commit_push(repo_dir, message, remote='origin', branch='master'):
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
                print(f"添加文件{file_path} 到.gitignore (文件大小超过100MB)！")
                update_gitignore(repo_dir, file_path)
                # Remove the file from git tracking if it is tracked
                # if is_tracked(file_path, repo_dir):
                #     run_git_command(f"git rm --cached \"{file_path}\"", repo_dir)

    # Use 'git add .' to include all changes except those in .gitignore
    print("Adding changes...")
    run_git_command("git add .", repo_dir)

    print("Committing changes...")
    run_git_command(f"git commit -m \"{message}\"", repo_dir)
    
    print("Pushing changes...")
    if run_git_command(f"git push {remote} {branch}", repo_dir):
        print("推送至远程仓库成功!")

def git_pull(repo_dir, remote='origin', branch='master'):
    """Pull changes from the remote repository."""
    print("Pulling changes...")
    run_git_command(f"git pull {remote} {branch}", repo_dir)

if __name__ == "__main__":
    # 注意local_repos本地仓库和远端remote_urls必须一一对应！！！否则仓库提交乱了
    # List of local repository paths
    local_repos = [
        "C:\\Users\\cunto\\Desktop\\tese",
        "C:\\Users\\cunto\\Desktop\\Repo2",
        "C:\\Users\\cunto\\Desktop\\aaaa"
    ]

    # Corresponding list of remote repository URLs
    remote_urls = [
        "https://github.com/cuntou0906/tese.git",
        "https://github.com/cuntou0906/Repo2.git",
        "https://github.com/cuntou0906/fdafsd.git"
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
                git_add_commit_push(repo_directory, "Your commit message")
                
                # git_pull(repo_directory) 