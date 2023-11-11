# Functions for calculating distances
from scipy import spatial
from embeddings import compute_service_embeddings
import pandas as pd


def compute_semantic_distances_for_class_pairs(embeddings_dict):
    """Compute pairwise semantic distances."""
    distances = []
    for class_name1, embedding1 in embeddings_dict.items():
        for class_name2, embedding2 in embeddings_dict.items():
            distance = 1 - spatial.distance.cosine(embedding1, embedding2)
            distances.append([class_name1, class_name2, distance])
    return pd.DataFrame(distances, columns=['class1', 'class2', 'semantic_distance'])


def compute_static_distances_for_service_pairs(class_graph, communities):
    """
    Compute static distances between service pairs based on class graph distances.
    
    Parameters:
    - class_graph (DataFrame): DataFrame containing class graph data.
    - communities (DataFrame): DataFrame containing community data for each class.
    
    Returns:
    - dict: Dictionary of static distances between service pairs.
    """
    # Merge class graph and communities DataFrames and filter inter-service pairs
    merged_df = class_graph.merge(communities, left_on='class1', right_on='class_name').merge(
        communities, left_on='class2', right_on='class_name', suffixes=('_1', '_2')
    )
    inter_service_df = merged_df[merged_df['service_1'] != merged_df['service_2']]
    return inter_service_df.groupby(['service_1', 'service_2'])['static_distance'].sum().to_dict()


def compute_semantic_distances_for_service_pairs(embeddings_dict, communities):
    """
    Compute semantic distances between service pairs based on their embeddings.
    
    Parameters:
    - embeddings_dict (dict): Dictionary mapping class names to their embeddings.
    - communities (DataFrame): DataFrame containing community data for each class.
    
    Returns:
    - dict: Dictionary of semantic distances between service pairs.
    """
    service_embeddings = compute_service_embeddings(embeddings_dict, communities)
    
    services = list(service_embeddings.keys())
    semantic_distances = {}
    for i, s1 in enumerate(services):
        for j, s2 in enumerate(services):
            if i != j:
                distance = 1 - spatial.distance.cosine(service_embeddings[s1], service_embeddings[s2])
                semantic_distances[(s1, s2)] = distance
    
    return semantic_distances