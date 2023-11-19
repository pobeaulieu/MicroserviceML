from helpers.service_community_helpers import print_communities, save_communities_to_csv
from common.distances import compute_semantic_distances_for_class_pairs
from common.visualization import visualize_class_distance_heatmap
from common.normalization import filter_and_normalize_distances
from community_detection.community_tuning import fine_tune_all_services
from helpers.results_helpers import generate_services_clustering_results
from helpers.embedding_helpers import load_embeddings_from_csv, write_embeddings_to_csv, create_class_embeddings_for_system
import networkx as nx
from community_detection.community_detection import CommunityDetection
from common.utils import load_call_graph
import os
from config.device_setup import set_device
from embedding.embedding_model import select_model_and_tokenizer


####################################################################################################
# PHASE 2: TYPE-BASED SERVICE CLUSTERING
####################################################################################################

def run_typed_service_identification(version, system, phase2_embedding_model, phase2_clustering_model):
    filename = f"generated_data/class_embeddings/{version}_{system}_{phase2_embedding_model}_embeddings.csv"

    tokenizer, model = select_model_and_tokenizer(phase2_embedding_model)
    if phase2_embedding_model != 'word2vec': model.to(set_device())

    # if embeddings are already generated, load them from CSV, else generate them
    if not os.path.exists(filename):
        # Generate embeddings
        print(f"Generating embeddings for {system}...")
        class_embeddings = create_class_embeddings_for_system(system, phase2_embedding_model, model, tokenizer, is_phase2=True)
        write_embeddings_to_csv(version, system, phase2_embedding_model, class_embeddings)
    
    class_names, class_labels, class_embeddings = load_embeddings_from_csv(filename)
    class_labels_dict, class_embeddings_dict = dict(zip(class_names, class_labels)), dict(zip(class_names, class_embeddings))
    static_df = load_call_graph(system)

    if system == 'cargotracker': # temporary fix
        # Replace 'org.eclipse' with 'net.java' in both class1 and class2 columns
        static_df['class1'] = static_df['class1'].str.replace('org.eclipse', 'net.java', regex=False)
        static_df['class2'] = static_df['class2'].str.replace('org.eclipse', 'net.java', regex=False)

    semantic_df = compute_semantic_distances_for_class_pairs(class_embeddings_dict)
    static_df = filter_and_normalize_distances(static_df, class_labels_dict)
    semantic_df = filter_and_normalize_distances(semantic_df, class_labels_dict)
    merged_df = static_df.merge(semantic_df, on=['class1', 'class2'], how='outer')
    class_graph = merged_df.fillna({'static_distance': 0, 'semantic_distance': 0})

    # Visualizations (optional)
    visualize_class_distance_heatmap(class_graph, 'static_distance', "Static Distances Between Classes")
    visualize_class_distance_heatmap(class_graph, 'semantic_distance', "Semantic Distances Between Classes")

    G = nx.from_pandas_edgelist(class_graph[class_graph['static_distance'] != 0], 'class1', 'class2', ['static_distance'])
    cd = CommunityDetection(G, class_labels_dict, optimize_hyperparameters_flag=False)  # Set optimize_hyperparameters_flag=True if you wish optimize parameters of clustering algorithms

    # Fine-tuning clusters using static distance
    distances = [(row['class1'], row['class2'], row['static_distance']) for _, row in class_graph.iterrows()]  # OR other distances

    print(f"Running {phase2_clustering_model} algorithm...")
    
    communities = {
        'Application': cd.detect_communities('Application', phase2_clustering_model),
        'Entity': cd.detect_communities('Entity', phase2_clustering_model),
        'Utility': cd.detect_communities('Utility', phase2_clustering_model)
    }

    fine_tuned_communities = {
        label_type: fine_tune_all_services(services, distances)
        for label_type, services in communities.items()
    }

    # Print the communities (optional)
    for label_type, services in fine_tuned_communities.items():
        print_communities(label_type, services)

    save_communities_to_csv(fine_tuned_communities, version, system, phase2_embedding_model, phase2_clustering_model)
    generate_services_clustering_results([phase2_clustering_model], phase2_embedding_model, version, system, matching_threshold= 0.8)

