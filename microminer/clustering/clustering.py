from microminer.clustering.cmeans import determine_optimal_clusters, fuzzy_cmeans_clustering
from microminer.clustering.custom_cmeans import CustomFuzzyCMeans
from microminer.clustering.hierarchical_clustering import hierarchical_clustering, determine_optimal_max_d
from microminer.helpers.reader import get_number_of_classes

def cluster_services(dissimilarity_matrix, nodes_list, clustering_model, num_clusters=-1, max_d=-1):
    """
    Cluster services based on the specified clustering model.

    Parameters:
    - dissimilarity_matrix: Matrix representing dissimilarities between nodes.
    - nodes_list: List of nodes (services) to be clustered.
    - clustering_model: Name of the clustering model ('cmeans', 'custom_cmeans', 'hierarchical').
    - system_name: Name of the system (used to determine the number of classes).
    - num_clusters: Number of clusters for c-means (default -1 for auto-determination).
    - max_d: Maximum distance for hierarchical clustering (default -1 for auto-determination).

    Returns:
    - memberships: Cluster memberships for each node.
    """
    if clustering_model == 'cmeans':
        if num_clusters == -1:  # Default: determine optimal number of clusters
            max_clusters = int(get_number_of_classes() / 2)
            cluster_range = range(2, max_clusters)
            num_clusters = determine_optimal_clusters(dissimilarity_matrix, cluster_range)

        memberships = fuzzy_cmeans_clustering(dissimilarity_matrix, nodes_list, num_clusters)

    elif clustering_model == 'custom_cmeans':
        memberships = CustomFuzzyCMeans().cluster_services(nodes_list, dissimilarity_matrix)

    elif clustering_model == 'hierarchical':
        if max_d == -1:  # Default: determine optimal maximum distance
            max_d = determine_optimal_max_d(dissimilarity_matrix)

        memberships = hierarchical_clustering(dissimilarity_matrix, nodes_list, max_d=max_d)

    else:
        raise ValueError("Invalid clustering model specified.")

    return memberships