from flask import Flask, render_template, request
import pygit2

import os
from datetime import datetime
import shutil
import subprocess
  
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pipeline', methods=['POST'])
def pipeline():
    repo_url = request.form.get('repo_url')
    
    return f"Values if the form: {repo_url}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port, host='0.0.0.0')