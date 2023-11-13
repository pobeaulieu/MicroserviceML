from flask import Flask, render_template, request
import pygit2

import os
from datetime import datetime
import shutil
import subprocess
  
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def copy_and_execute_script(repo_folder):
    # Copy format_code.sh into the repository folder
    script_path = os.path.join(os.path.dirname(__file__), 'format_code.sh')
    
    # Define the destination directory next to the script
    dest_dir = os.path.join(os.path.dirname(script_path), 'src_code_formatted')
    
    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    # Copy the format_code.sh script into the destination directory
    shutil.copy(script_path, dest_dir)

    # Execute format_code.sh script
    script_name = os.path.join(dest_dir, 'format_code.sh')

    # Print statements for debugging
    print(f"Script path: {script_name}")
    print(f"Repo folder: {repo_folder}")

    subprocess.run(['bash', script_name], cwd=repo_folder)

    # Delete remaining contents of the folder, except src_code_formatted
    for item in os.listdir(repo_folder):
        item_path = os.path.join(repo_folder, item)
        if item != 'src_code_formatted' and os.path.isdir(item_path):
            shutil.rmtree(item_path)
        elif item != 'src_code_formatted' and os.path.isfile(item_path):
            os.remove(item_path)


@app.route('/pipeline', methods=['POST'])
def pipeline_executed():
    repo_url = request.form.get('repo_url')

    # Create a timestamped folder within 'src_code' for each cloned repository
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    destination = os.path.join('src_code', timestamp)

    if not repo_url:
        return "Repository URL is required."

    try:

        repo = pygit2.clone_repository(repo_url, destination, checkout_branch="master")

        copy_and_execute_script(destination)
        return f"Repository cloned successfully to {destination} and script executed."
    except Exception as e:
        return f"Error cloning repository: {e}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')