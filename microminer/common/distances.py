# Functions for calculating distances
from scipy.spatial import distance as sp_distance
from microminer.common.normalization import normalize_distances
import pandas as pd


def compute_semantic_distances_for_class_pairs(embeddings_dict):
    """Compute pairwise semantic distances."""
    distances = []
    for class_name1, embedding1 in embeddings_dict.items():
        for class_name2, embedding2 in embeddings_dict.items():
            distance = 1 - sp_distance.cosine(embedding1, embedding2)
            distances.append([class_name1, class_name2, distance])
    return pd.DataFrame(distances, columns=['class1', 'class2', 'semantic_distance'])


def compute_static_distances_for_service_pairs(static_distances_df, class_to_service_map):
    """
    Compute and normalize static distances between distinct service pairs.

    Parameters:
    - static_distances_df (pd.DataFrame): DataFrame with columns 'class1', 'class2', 'static_distance'.
    - class_to_service_map (dict): Mapping of class names to service names.

    Returns:
    - dict: Dictionary of normalized static distances between distinct service pairs.
    """
    service_pairs_distances = {}
    for _, row in static_distances_df.iterrows():
        class1_service = class_to_service_map.get(row['class1'])
        class2_service = class_to_service_map.get(row['class2'])

        if class1_service and class2_service and class1_service != class2_service:
            service_pair = (class1_service, class2_service)
            static_distance = row['static_distance']

            if service_pair not in service_pairs_distances:
                service_pairs_distances[service_pair] = static_distance
            else:
                service_pairs_distances[service_pair] += static_distance

    return normalize_distances(service_pairs_distances)


def compute_semantic_distances_for_service_pairs(semantic_distances_df, class_to_service_map):
    """
    Compute mean semantic distances between distinct service pairs.

    Parameters:
    - semantic_distances_df (pd.DataFrame): DataFrame with columns 'class1', 'class2', 'semantic_distance'.
    - class_to_service_map (dict): Mapping of class names to service names.

    Returns:
    - dict: Dictionary of mean semantic distances between distinct service pairs.
    """
    service_pairs_distances = {}
    service_pairs_counts = {}
    for _, row in semantic_distances_df.iterrows():
        class1_service = class_to_service_map.get(row['class1'])
        class2_service = class_to_service_map.get(row['class2'])

        if class1_service and class2_service:
            service_pair = tuple(sorted([class1_service, class2_service]))  # Order is not important

            if class1_service != class2_service:
                semantic_distance = row['semantic_distance']

                if service_pair not in service_pairs_distances:
                    service_pairs_distances[service_pair] = semantic_distance
                    service_pairs_counts[service_pair] = 1
                else:
                    service_pairs_distances[service_pair] += semantic_distance
                    service_pairs_counts[service_pair] += 1

    for service_pair in service_pairs_distances:
        service_pairs_distances[service_pair] /= service_pairs_counts[service_pair]

    return service_pairs_distances


