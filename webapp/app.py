from flask import Flask, render_template, request, redirect, url_for

import sys
from pipeline.mock import MockImplementation
from pipeline.interface import MicroMinerInterface
import os


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

    # Perform any processing with the form data if needed

    pipeline = MockImplementation()

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
