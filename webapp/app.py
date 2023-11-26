import asyncio
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os, sys
import uuid

app = Flask(__name__)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Set the current working directory to the 'pipeline' directory
from microminer.pipeline import MicroMinerPipeline
from microminer.config.enums import Phase1EmbeddingModel, Phase1ClassifierModel, Phase2EmbeddingModel, Phase2ClusteringModel, Phase3ClusteringModel

global_results = {}

def generate_run_id():
    return str(uuid.uuid4())

def run_pipeline(data):
    run_id = generate_run_id()
    repo_url = data['repo_url']
    graph_file = data['call_graph_file']
    phase1_model_llm = data['phase1_model_llm']
    phase1_model_ml = data['phase1_model_ml']
    phase2_model = data['phase2_model']
    num_microservices = data['num_microservices']
    phase3_model = data['phase3_model']
    
    # Save the file to disk
    graph_file.save("graph.csv")

    pipeline = MicroMinerPipeline(
        github_url=repo_url, 
        path_to_call_graph="graph.csv", 
        embeddings_model_name_phase_1=Phase1EmbeddingModel.codebert.name, 
        classification_model_name_phase_1=Phase1ClassifierModel.svm.name,
        embeddings_model_name_phase_2=Phase2EmbeddingModel.word2vec.name,
        clustering_model_name_phase_2=Phase2ClusteringModel.GirvanNewman.name,
        clustering_model_name_phase_3=Phase3ClusteringModel.custom_cmeans.name,
    )

    pipeline.clean_up()

    pipeline.clone_and_prepare_src_code()
    result1 = pipeline.execute_phase_1()
    result2 = pipeline.execute_phase_2()
    result3 = pipeline.execute_phase_3()

    pipeline.clean_up()

    global_results[run_id] = {
    'repo_url': repo_url,
    'phase1_model_llm': phase1_model_llm,
    'phase1_model_ml': phase1_model_ml,
    'phase2_model': phase2_model,
    'num_microservices': num_microservices,
    'phase3_model': phase3_model,
    'result1': result1,
    'result2': result2,
    'result3': result3
    }

    return run_id 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():

    run_id = request.args.get('run_id')

    if run_id in global_results:
        result_data = global_results[run_id]
        return render_template('results.html', **result_data)
    else:
        # Redirect to a page indicating that the run ID is not found
        return redirect(url_for('index'))
    
@app.route('/pipeline', methods=['POST'])
def handle_pipeline():
    repo_url = request.form.get('repo_url')
    phase1_model_llm = request.form.get('phase1_model_llm')
    phase1_model_ml = request.form.get('phase1_model_ml')
    phase2_model = request.form.get('phase2_model')
    num_microservices = request.form.get('num_microservices')
    phase3_model = request.form.get('phase3_model')
    call_graph_file = request.files.get('call_graph_file')

    data = {
            'repo_url': repo_url,
            'call_graph_file': call_graph_file,
            'phase1_model_llm': phase1_model_llm,
            'phase1_model_ml': phase1_model_ml,
            'phase2_model': phase2_model,
            'num_microservices': num_microservices,
            'phase3_model': phase3_model
    }

    run_id = run_pipeline(data)
    return jsonify({'run_id': run_id})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port, host='127.0.0.1')