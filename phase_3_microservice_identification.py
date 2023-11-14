import pandas as pd
from helpers.microservice_helpers import save_microservices_to_txt, save_microservices_to_csv
import networkx as nx
from common.graphs import remove_zero_weight_edges, print_graph, construct_dissimilarity_matrix, compute_edge_weight
from clustering.cluster_analysis import assign_clusters_based_on_comparative_ratios, merge_overlapping_clusters, identify_standalone_services
from common.normalization import normalize_data, normalize_memberships
from common.distances import compute_static_distances_for_service_pairs, compute_semantic_distances_for_service_pairs
from clustering.cmeans import determine_optimal_clusters, fuzzy_cmeans_clustering
from clustering.custom_cmeans import CustomFuzzyCMeans
from clustering.hierarchical_clustering import hierarchical_clustering, determine_optimal_max_d
from helpers.results_helpers import generate_microservices_clustering_results
from helpers.class_helpers import get_number_of_classes

####################################################################################################
# PHASE 3: MICROSERVICE IDENTIFICATION
####################################################################################################

def run_microservice_identification(version, system, phase1_model, phase2_model, phase3_model):
    filename = f"generated_data/graphs/service/{version}_{system}_service_graph.csv"

    # Load the data from CSV files
    communities_df = pd.read_csv(f"generated_data/service_communities/{phase2_model}/{version}_{system}_{phase1_model}_communities.csv")
    class_graph_df = pd.read_csv(f"generated_data/graphs/class/{version}_{system}_class_graph.csv")
    embeddings_df = pd.read_csv(f"generated_data/class_embeddings/{version}_{system}_{phase1_model}_embeddings.csv")

    # Extract class names and their embeddings from the embeddings DataFrame
    class_names = embeddings_df.iloc[:, 0].str.split(';', expand=True)[0]
    embeddings = embeddings_df.iloc[:, 1:].values
    class_embeddings_dict = dict(zip(class_names, embeddings))

    # Compute static and semantic distances between service pairs
    static_distances = compute_static_distances_for_service_pairs(class_graph_df, communities_df)
    semantic_distances = compute_semantic_distances_for_service_pairs(class_embeddings_dict, communities_df)

    # Normalize the distances between 0 and 1
    normalized_static_distances = normalize_data(static_distances)
    normalized_semantic_distances = normalize_data(semantic_distances)

    # Create the service graph DataFrame
    service_graph_data = [
        [s1, s2, normalized_static_distances.get((s1, s2), 0), normalized_semantic_distances.get((s1, s2), 0)]
        for s1, s2 in static_distances.keys()
    ]
    service_graph_df = pd.DataFrame(service_graph_data, columns=['service1', 'service2', 'static_distance', 'semantic_distance'])

    # Save the service graph DataFrame to a CSV file
    service_graph_df.to_csv(filename, index=False)

    service_graph_df = pd.read_csv(filename)

    services_graph = nx.DiGraph([
        (row['service1'], row['service2'], {"weight": compute_edge_weight(row['semantic_distance'], row['static_distance'], alpha=1.0)}) # adjust alpha here
        for _, row in service_graph_df.iterrows()
    ])

    remove_zero_weight_edges(services_graph)
    print_graph(services_graph, "weight")
    nodes_list = list(services_graph.nodes)

    # Construct the dissimilarity matrix
    dissimilarity_matrix = construct_dissimilarity_matrix(services_graph)

    if phase3_model == 'cmeans':
        cluster_range = get_number_of_classes(system) / 2
        optimal_clusters = determine_optimal_clusters(dissimilarity_matrix, cluster_range)
        print(f"Optimal number of clusters: {optimal_clusters}")
        memberships = fuzzy_cmeans_clustering(dissimilarity_matrix, nodes_list, optimal_clusters)
    elif phase3_model == 'custom_cmeans':
        memberships = CustomFuzzyCMeans().cluster_services(nodes_list, dissimilarity_matrix)
    elif phase3_model == 'hierarchical':
        optimal_max_d = determine_optimal_max_d(dissimilarity_matrix)
        memberships = hierarchical_clustering(dissimilarity_matrix, nodes_list, max_d=optimal_max_d)
    else:
        raise Exception('Invalid phase 3 model')
    
    # Normalize the memberships
    normalized_memberships = normalize_memberships(memberships)

    # Assign clusters to services based on comparative ratios
    clusters = assign_clusters_based_on_comparative_ratios(normalized_memberships)

    # Identify standalone services
    clusters = identify_standalone_services(clusters)

    # Merge overlapping clusters
    clusters = merge_overlapping_clusters(clusters)

    # Save the clusters to .txt and .csv files
    save_microservices_to_txt(clusters, communities_df, 
                           f"generated_data/microservice_clusters/custom_cmeans/{version}_{system}_{phase2_model}_microservices.txt")
    save_microservices_to_csv(clusters, communities_df, 
                           f"generated_data/microservice_clusters/custom_cmeans/{version}_{system}_{phase2_model}_microservices.csv")
    
    generate_microservices_clustering_results([phase3_model], phase2_model, phase1_model, version, system, matching_threshold=0.8)
