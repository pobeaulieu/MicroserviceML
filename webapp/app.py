from flask import Flask, render_template, request, redirect, url_for

import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Set the current working directory to the 'pipeline' directory
from pipeline.mock import MockImplementation


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pipeline')  # Assuming you are submitting a form with POST method
def pipeline():
    repo_url = request.args.get('repo_url')
    graph_path = request.args.get('call_graph_file')

    # Get values from optional parameters form
    phase1_model_llm = request.args.get('phase1_model_llm')
    phase1_model_ml = request.args.get('phase1_model_ml')
    phase2_model = request.args.get('phase2_model')
    num_microservices = request.args.get('num_microservices')
    phase3_model = request.args.get('phase3_model')

    print(num_microservices)

    pipeline = MockImplementation(
        github_url=repo_url, 
        embeddings_model_name_phase_1=phase1_model_llm, 
        classification_model_name_phase_1= phase1_model_ml, 
        clustering_model_name_phase_2= phase2_model, 
        embeddings_model_name_phase_2= None, #TODO
        call_graph= graph_path, 
        clustering_model_name_phase_3= phase3_model, 
        num_clusters= num_microservices, 
        max_d= None #TODO
    )

    print(pipeline)
    
    result1 = pipeline.execute_phase_1()
    result2 = pipeline.execute_phase_2()
    result3 = pipeline.execute_phase_3()

    return render_template('results.html',
                           repo_url=repo_url,
                           graph_path=graph_path,
                           phase1_model_llm=phase1_model_llm,
                           phase1_model_ml=phase1_model_ml,
                           phase2_model=phase2_model,
                           num_microservices=num_microservices,
                           phase3_model=phase3_model,
                           result1=result1,
                           result2=result2,
                           result3=result3)
                           
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port, host='0.0.0.0')
