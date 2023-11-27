import os
import shutil
import subprocess
import pygit2
import time

def clone_and_copy_java_contents(github_url, target_dir='src_code/tmp'):
    """
    Clones a specified GitHub repository and copies the contents of src/main/java/
    to a temporary folder inside the target directory. Returns True if successful, False otherwise.
    Also creates a 'src_code_formatted' folder inside 'tmp' and calls a Python function
    to replace the functionality of format_code.sh.

    :param github_url: URL of the GitHub repository to clone.
    :param target_dir: Target directory to copy the contents to. Defaults to 'src_code/tmp'.
    """
    success = False
    repo = None
    try:
        # Clone the repository
        repo = pygit2.clone_repository(github_url, 'temp_repo')

        # Construct source and target paths
        src_path = os.path.join('temp_repo', 'src/main/java/')
        target_path = os.path.join(target_dir)

        # Check if src/main/java/ exists
        if not os.path.exists(src_path):
            raise FileNotFoundError("The src/main/java/ directory does not exist in the repository.")

        # Create target directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)

        # Copy the contents
        for item in os.listdir(src_path):
            s = os.path.join(src_path, item)
            d = os.path.join(target_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        # Format and copy Java files
        format_and_copy_java_files(target_path)

        success = True
    except Exception as e:
        print(f"An error occurred: {e}")
        success = False
    finally:
        if repo:
            # Ensure all Git resources are released
            repo.free()

        # Delay to ensure that all file handles are released
        time.sleep(1)

    return success

def copy_and_overwrite(src, dst):
    """
    Copies files or directories from src to dst. Overwrites if dst already exists.
    """
    if os.path.isdir(src):
        if not os.path.isdir(dst):
            os.makedirs(dst)
        files = os.listdir(src)
        for f in files:
            copy_and_overwrite(os.path.join(src, f), os.path.join(dst, f))
    else:
        shutil.copy2(src, dst)

def format_and_copy_java_files(src_dir):
    formatted_dir = os.path.join(src_dir, 'src_code_formatted')
    os.makedirs(formatted_dir, exist_ok=True)

    for root, dirs, files in os.walk(src_dir):
        # Skip the formatted directory to avoid double copying
        if 'src_code_formatted' in dirs:
            dirs.remove('src_code_formatted')
        
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, src_dir)
                formatted_path = relative_path.replace(os.path.sep, '.')
                copy_and_overwrite(file_path, os.path.join(formatted_dir, formatted_path))


def remove_tmp_dir():
    """
    Removes the contents of 'tmp' directory inside 'src_code' and 'temp_repo'.
    """
    try:
        tmp_dir = 'src_code/tmp'
        temp_repo_dir = 'temp_repo'

        # Remove the contents of 'tmp' directory
        if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
            for file_name in os.listdir(tmp_dir):
                file_path = os.path.join(tmp_dir, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

        # Remove the contents of 'temp_repo' directory
        if os.path.exists(temp_repo_dir) and os.path.isdir(temp_repo_dir):
            for file_name in os.listdir(temp_repo_dir):
                file_path = os.path.join(temp_repo_dir, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

    except Exception as e:
        # If removal fails, log the exception and attempt a force removal
        print(f"Failed to remove contents of 'tmp' directory: {e}")
        subprocess.run(['rm', '-rf', 'src_code/tmp/*'], shell=True)

        print(f"Failed to remove contents of 'temp_repo' directory: {e}")
        subprocess.run(['rm', '-rf', 'temp_repo/*'], shell=True)
