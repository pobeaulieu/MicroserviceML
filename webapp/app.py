import asyncio
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import os, sys

app = Flask(__name__)
socketio = SocketIO(app)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Set the current working directory to the 'pipeline' directory
from microminer.pipeline import MicroMinerPipeline
from microminer.config.enums import Phase1EmbeddingModel, Phase1ClassifierModel, Phase2EmbeddingModel, Phase2ClusteringModel, Phase3ClusteringModel

# Global variables to store results
global_results = {
    'repo_url': None,
    'graph_path': None,
    'phase1_model_llm': None,
    'phase1_model_ml': None,
    'phase2_model': None,
    'num_microservices': None,
    'phase3_model': None,
    'result1': None,
    'result2': None,
    'result3': None
}

@app.route('/')
def index():
    return render_template('index.html')
 
@socketio.on('pipeline')
def pipeline(data):
    print("Received pipeline event:", data)
    # Handle the pipeline logic here

    repo_url = data['repo_url']
    graph_file = data['call_graph_file']
    phase1_model_llm = data['phase1_model_llm']
    phase1_model_ml = data['phase1_model_ml']
    phase2_model = data['phase2_model']
    num_microservices = data['num_microservices']
    phase3_model = data['phase3_model']

    # socketio.emit('pipeline_progress', {'message': 'Cloning Repository'})

    # Save the file to disk
    with open('graph.csv', 'wb') as file:
        file.write(graph_file)
        
    pipeline = MicroMinerPipeline(
        github_url=repo_url, 
        path_to_call_graph= "graph.csv", 
        embeddings_model_name_phase_1=Phase1EmbeddingModel.codebert.name, 
        classification_model_name_phase_1=Phase1ClassifierModel.svm.name,
        embeddings_model_name_phase_2=Phase2EmbeddingModel.word2vec.name,
        clustering_model_name_phase_2=Phase2ClusteringModel.GirvanNewman.name,
        clustering_model_name_phase_3=Phase3ClusteringModel.custom_cmeans.name,
    )

    pipeline.clean_up()

    #socketio.emit('pipeline_progress', {'message': 'Cloning Repository'})
    pipeline.clone_and_prepare_src_code()
    #socketio.sleep(30)
    #socketio.emit('pipeline_progress', {'message': 'Phase 1 in Progress'})
    result1 =pipeline.execute_phase_1()
    #socketio.sleep(30)

    #socketio.emit('pipeline_progress', {'message': 'Phase 2 in Progress'})
    result2 = pipeline.execute_phase_2()
    #socketio.sleep(30)

    #socketio.emit('pipeline_progress', {'message': 'Phase 3 in Progress'})
    result3 = pipeline.execute_phase_3()
    #socketio.sleep(30)


    pipeline.clean_up()
    
    # Update global results
    global_results.update({
        'repo_url': repo_url,
        'phase1_model_llm': phase1_model_llm,
        'phase1_model_ml': phase1_model_ml,
        'phase2_model': phase2_model,
        'num_microservices': num_microservices,
        'phase3_model': phase3_model,
        'result1': result1,
        'result2': result2,
        'result3': result3
    })

    # Emit 'pipeline_complete' event with information
    socketio.emit('pipeline_complete')

@app.route('/results')
def results():
    return render_template('results.html', **global_results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    socketio.run(app, debug=True, port=port, host='127.0.0.1')
