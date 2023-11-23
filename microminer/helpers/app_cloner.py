import os
import shutil
import subprocess
import pygit2
import time

def clone_and_copy_java_contents(github_url, target_dir='src_code/tmp'):
    """
    Clones a specified GitHub repository and copies the contents of src/main/java/
    to a temporary folder inside the target directory. Returns True if successful, False otherwise.
    Also creates a 'src_code_formatted' folder inside 'tmp' and calls format_code.sh.

    :param github_url: URL of the GitHub repository to clone.
    :param target_dir: Target directory to copy the contents to. Defaults to 'src_code/tmp'.
    """
    success = False
    try:
        # Clone the repository
        repo = pygit2.clone_repository(github_url, 'temp_repo')

        # Construct source and target paths
        src_path = os.path.join(repo.workdir, 'src/main/java/')
        target_path = os.path.join(target_dir)

        # Check if src/main/java/ exists
        if not os.path.exists(src_path):
            raise FileNotFoundError("The src/main/java/ directory does not exist in the repository.")

        # Create target directory if it doesn't exist
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # Copy the contents
        for item in os.listdir(src_path):
            s = os.path.join(src_path, item)
            d = os.path.join(target_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        success = True
    except Exception as e:
        # Log the exception if needed
        # print(f"An error occurred: {e}")
        success = False
    finally:
        # Ensure all Git resources are released
        repo.free()

        # Delay to ensure that all file handles are released
        time.sleep(1)

        # Attempt to remove the directory
        try:
            shutil.rmtree('temp_repo')
        except Exception as e:
            # If removal fails, log the exception and attempt a force removal
            # print(f"Failed to remove temp_repo: {e}")
            subprocess.run(['rm', '-rf', 'temp_repo'], shell=True)

        # Create the src_code_formatted folder and call format_code.sh if copying was successful
        if success:
            formatted_dir = os.path.join(target_path, 'src_code_formatted')
            if not os.path.exists(formatted_dir):
                os.makedirs(formatted_dir)

            # Call the format_code.sh script using Git Bash, adjust the path as needed
            subprocess.run(['bash', '../format_code.sh'], cwd='src_code/tmp')

    return success


# Example usage
# result = clone_and_copy_java_contents('https://github.com/user/repo.git')
