from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json
import os, sys
app = Flask(__name__)
socketio = SocketIO(app)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Set the current working directory to the 'pipeline' directory
from microminer.mock import MockImplementation

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
    graph_path = data['call_graph_file']
    phase1_model_llm = data['phase1_model_llm']
    phase1_model_ml = data['phase1_model_ml']
    phase2_model = data['phase2_model']
    num_microservices = data['num_microservices']
    phase3_model = data['phase3_model']


    print(num_microservices)

    pipeline = MockImplementation(
        github_url=repo_url, 
        embeddings_model_name_phase_1=phase1_model_llm, 
        classification_model_name_phase_1= phase1_model_ml, 
        clustering_model_name_phase_2= phase2_model, 
        #call_graph= graph_path, 
        clustering_model_name_phase_3= phase3_model, 
        num_clusters= num_microservices, 
        max_d= None, #TODO
        embeddings_model_name_phase_2= None, #TODO
    )

    # Emit messages back to the client
    socketio.emit('pipeline_progress', {'message': 'Cloning Repository'})
    socketio.sleep(1)
    socketio.emit('pipeline_progress', {'message': 'Phase 1 in Progress'})
    result1 = pipeline.execute_phase_1()
    socketio.emit('pipeline_progress', {'message': 'Phase 2 in Progress'})
    socketio.sleep(1)
    result2 = pipeline.execute_phase_2()
    socketio.sleep(1)
    socketio.emit('pipeline_progress', {'message': 'Phase 3 in Progress'})
    result3 = pipeline.execute_phase_3()

    print(result1)
    # Update global results
    global_results.update({
        'repo_url': repo_url,
        'graph_path': graph_path,
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
    socketio.run(app, debug=True, port=port, host='0.0.0.0')
