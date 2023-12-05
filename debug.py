from microminer.pipeline import MicroMinerPipeline
from microminer.config.enums import Phase1EmbeddingModel, Phase1ClassifierModel, Phase2EmbeddingModel, Phase2ClusteringModel, Phase3ClusteringModel
import os, subprocess
import json
from datetime import datetime

SYSTEM_GIT_URL_MAPPING = {'https://github.com/sadatrafsanjani/JavaFX-Point-of-Sales.git': 'pos', 
                          'https://github.com/rafaelsteil/jforum3.git': 'jforum',
                          'https://github.com/spring-projects/spring-petclinic.git': 'petclinic',
                          'https://github.com/javaee/cargotracker.git': 'cargotracker'}

# Define a list of configurations
configurations = [
    {
        'github_url': 'https://github.com/sadatrafsanjani/JavaFX-Point-of-Sales.git',
        'path_to_call_graph': 'call_graphs/pos_call_graph.csv',
        'embeddings_model_name_phase_1': Phase1EmbeddingModel.codebert.name,
        'classification_model_name_phase_1': Phase1ClassifierModel.logistic_regression.name,
        'embeddings_model_name_phase_2': Phase2EmbeddingModel.word2vec.name,
        'clustering_model_name_phase_2': Phase2ClusteringModel.Louvain.name,
        'clustering_model_name_phase_3': Phase3ClusteringModel.custom_cmeans.name,
        'alpha_phase_2': 0.5,
        'num_clusters': -1,
        'max_d': -1,
        'alpha_phase_3': 0.5,
        'version': 'v_team'
    }

    # Add more configurations here
]

last_trained_system_url = None

for config in configurations:
    current_system_url = config['github_url']
    system_name = SYSTEM_GIT_URL_MAPPING[current_system_url]
    config['training_system_names'] = [name for url, name in SYSTEM_GIT_URL_MAPPING.items() if url != current_system_url]

    pipeline = MicroMinerPipeline(
        github_url=config['github_url'],
        path_to_call_graph = f'call_graphs/{system_name}_call_graph.csv',
        embeddings_model_name_phase_1 = config.get('embeddings_model_name_phase_1', Phase1EmbeddingModel.codebert.name),
        classification_model_name_phase_1 = config.get('classification_model_name_phase_1', Phase1ClassifierModel.logistic_regression.name),
        embeddings_model_name_phase_2 = config.get('embeddings_model_name_phase_2', Phase2EmbeddingModel.word2vec.name),
        clustering_model_name_phase_2 = config.get('clustering_model_name_phase_2', Phase2ClusteringModel.Louvain.name),
        clustering_model_name_phase_3 = config.get('clustering_model_name_phase_3', Phase3ClusteringModel.custom_cmeans.name),
        alpha_phase_2 = config.get('alpha_phase_2', 0.5),
        num_clusters = config.get('num_clusters', -1),
        max_d = config.get('max_d', -1),
        alpha_phase_3 = config.get('alpha_phase_3', 0.5),
        training_system_names = config.get('training_system_names', ["pos", "jforum", "petclinic", "cargotracker"]),
        version = config.get('version', 'v_team')
    )

    pipeline.clean_up()

    # Execute training phase only if current system is different from the last trained system
    if current_system_url != last_trained_system_url:
        pipeline.execute_training_phase()
        last_trained_system_url = current_system_url

    # Execute other pipeline phases
    pipeline.clone_and_prepare_src_code()
    pipeline.execute_phase_1()
    pipeline.execute_phase_2()
    pipeline.execute_phase_3()

    results = pipeline.get_results()

    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')

    # Save results
    with open(f'results/{datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}_{pipeline.run_id}.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)

    pipeline.clean_up()

    # Invoke the metrics_generator script
    subprocess.run(['python', '-m', 'microminer.metrics.metrics_generator'])
