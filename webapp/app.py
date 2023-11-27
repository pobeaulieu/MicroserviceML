import asyncio
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import os, sys, uuid, zipfile, io
from datetime import datetime

app = Flask(__name__)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Set the current working directory to the 'pipeline' directory
from microminer.pipeline import MicroMinerPipeline
from microminer.config.enums import Phase1EmbeddingModel, Phase1ClassifierModel, Phase2EmbeddingModel, Phase2ClusteringModel, Phase3ClusteringModel

# Dictionnary runid -> Result
results_by_run_id_dict = {}

def generate_run_id():
    return str(uuid.uuid4())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    run_id = request.args.get('run_id')
    if run_id in results_by_run_id_dict:
        result_data = results_by_run_id_dict[run_id]
        return render_template('results.html', **result_data)
    else:
        # Redirect to a page indicating that the run ID is not found
        return redirect(url_for('index'))

@app.route('/pipeline', methods=['POST'])
def pipeline():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        run_id = generate_run_id()
        repo_url = request.form.get('repo_url')
        phase1_model_embedding = request.form.get('phase1_model_embedding')
        phase1_model_ml = request.form.get('phase1_model_ml')
        phase2_model = request.form.get('phase2_model')
        phase2_model_embedding = request.form.get('phase2_model_embedding')
        num_microservices = request.form.get('num_microservices')
        phase3_model = request.form.get('phase3_model')
        call_graph_file = request.files.get('call_graph_file')
        max_d = request.form.get('max_d')
        alpha_phase_2 = request.form.get('alpha_phase_2')
        alpha_phase_3 = request.form.get('alpha_phase_3')

        num_microservices = int(num_microservices) if num_microservices else -1
        max_d = float(max_d) if max_d else -1
        alpha_phase_2 = float(alpha_phase_2) if alpha_phase_2 else 0.5
        alpha_phase_3 = float(alpha_phase_3) if alpha_phase_3 else 0.5

        # Save the file to disk
        graph_path = "graph.csv"
        call_graph_file.save(graph_path)

        print("Running pipeline with parameters: ")
        print('repo_url', repo_url)
        print('call_graph_file', call_graph_file)
        print('phase1_model_embedding', phase1_model_embedding)
        print('phase1_model_ml', phase1_model_ml)
        print('phase2_model', phase2_model)
        print('phase2_model_embedding', phase2_model_embedding)
        print('alpha_phase_2', alpha_phase_2)
        print('phase3_model', phase3_model)
        print('num_microservices', num_microservices)
        print('max_d', max_d)
        print('alpha_phase_3', alpha_phase_3)

        pipeline = MicroMinerPipeline(
            github_url=repo_url, 
            path_to_call_graph=graph_path, 
            embeddings_model_name_phase_1=phase1_model_embedding, 
            classification_model_name_phase_1=phase1_model_ml,
            embeddings_model_name_phase_2= phase2_model_embedding,
            alpha_phase_2 = alpha_phase_2,
            clustering_model_name_phase_2=phase2_model,
            clustering_model_name_phase_3=phase3_model,
            num_clusters = num_microservices,
            max_d = max_d,
            alpha_phase_3 = alpha_phase_3,
        )

        pipeline.clean_up()

        pipeline.clone_and_prepare_src_code()
        result1 = pipeline.execute_phase_1()
        result2 = pipeline.execute_phase_2()
        result3 = pipeline.execute_phase_3()

        pipeline.clean_up()

        results_by_run_id_dict[run_id] = {
        'repo_url': repo_url,
        'timestamp': timestamp,
        'phase1_model_embedding': phase1_model_embedding,
        'phase1_model_ml': phase1_model_ml,
        'phase2_model': phase2_model,
        'phase2_model_embedding': phase2_model_embedding,
        'num_microservices': num_microservices,
        'phase3_model': phase3_model,
        'alpha_phase_2': alpha_phase_2,
        'alpha_phase_3': alpha_phase_3,
        'max_d': max_d,
        'result1': result1,
        'result2': result2,
        'result3': result3
        }

        return jsonify({'run_id': run_id})
    finally:
        # Clean up, regardless of whether an exception occurred
        pipeline.clean_up()


@app.route('/download_results/<run_id>', methods=['GET'])
def download_results(run_id):
    if run_id in results_by_run_id_dict:
        # results['config'] = {}
        # results['config']['run_id'] = result_data['run_id']
        # results['config']['timestamp'] = result_data['timestamp']
        # results['config']['github_url'] = result_data['repo_url']
        # # results['config']['path_to_call_graph'] = pipeline.path_to_call_graph
        # # results['config']['embeddings_model_name_phase_1'] = pipeline.embeddings_model_name_phase_1
        # # results['config']['classification_model_name_phase_1'] = pipeline.classification_model_name_phase_1
        # # results['config']['alpha_phase_2'] = pipeline.alpha_phase_2
        # # results['config']['embeddings_model_name_phase_2'] = pipeline.embeddings_model_name_phase_2
        # # results['config']['clustering_model_name_phase_2'] = pipeline.clustering_model_name_phase_2
        # # results['config']['clustering_model_name_phase_3'] = pipeline.clustering_model_name_phase_3
        # # results['config']['num_clusters'] = pipeline.num_clusters
        # # results['config']['max_d'] = pipeline.max_d
        # # results['config']['alpha_phase_3'] = pipeline.alpha_phase_3
        # # results['phase_1'] = result_phase_1
        # # results['phase_2'] = result_phase_2
        # # results['phase_3'] = result_phase_3
        result_data = results_by_run_id_dict[run_id]

        # Create a BytesIO object to store the zip file in memory
        zip_buffer = io.BytesIO()

        # Create a ZipFile object
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for i, (result_key, result_content) in enumerate(result_data.items()):
                # Convert the result_content (dictionary) to a string
                result_content_str = str(result_content)
                zip_file.writestr(f'{result_key}.txt', result_content_str)

        # Set the BytesIO object position to the beginning
        zip_buffer.seek(0)

        # Return the zip file as a response
        return send_file(zip_buffer, download_name=f"{result_data['timestamp']}.zip", as_attachment=True)
    else:
        # Redirect to a page indicating that the run ID is not found
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port, host='127.0.0.1')