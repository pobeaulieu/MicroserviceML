from helpers.service_community_helpers import print_communities, save_communities_to_csv
from common.distances import compute_semantic_distances_for_class_pairs
from common.visualization import visualize_class_distance_heatmap
from common.normalization import filter_and_normalize_distances
from community.community_tuning import fine_tune_all_services
from helpers.results_helpers import generate_services_clustering_results
from helpers.embedding_helpers import load_embeddings_from_csv
import networkx as nx
from community.community_detection import CommunityDetection
from common.utils import load_call_graph

####################################################################################################
# PHASE 2: TYPE-BASED SERVICE CLUSTERING
####################################################################################################

def run_typed_service_identification(version, system, phase1_model, phase2_model):
    filename = f"generated_data/class_embeddings/{version}_{system}_{phase1_model}_embeddings.csv"

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

    print(f"Running {phase2_model} algorithm...")
    
    communities = {
        'Application': cd.detect_communities('Application', phase2_model),
        'Entity': cd.detect_communities('Entity', phase2_model),
        'Utility': cd.detect_communities('Utility', phase2_model)
    }

    fine_tuned_communities = {
        label_type: fine_tune_all_services(services, distances)
        for label_type, services in communities.items()
    }

    # Print the communities (optional)
    for label_type, services in fine_tuned_communities.items():
        print_communities(label_type, services)

    save_communities_to_csv(fine_tuned_communities, version, system, phase1_model, phase2_model)
    generate_services_clustering_results([phase2_model], phase1_model, version, system, matching_threshold= 0.8)

