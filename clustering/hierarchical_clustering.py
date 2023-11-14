import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from helpers.optimization_helpers import detect_elbow, calculate_wcss


def perform_clustering(dissimilarity_matrix, max_d):
    Z = linkage(squareform(dissimilarity_matrix), method='average')
    clusters = fcluster(Z, max_d, criterion='distance')
    return clusters


def hierarchical_clustering(dissimilarity_matrix, nodes, max_d):
    """
    Perform hierarchical clustering and return fuzzy memberships.

    Parameters:
    - dissimilarity_matrix: The matrix of dissimilarity between nodes.
    - nodes: The list of node labels.
    - max_d: The threshold to cut the dendrogram to form clusters.

    Returns:
    - A dictionary with node labels as keys and a list of (cluster, membership) tuples as values.
    """
    # Perform the hierarchical clustering
    clusters = perform_clustering(dissimilarity_matrix, max_d)

    # Calculate the centroids of each cluster
    centroids = {i: np.mean(dissimilarity_matrix[clusters == i], axis=0) for i in np.unique(clusters)}

    # Initialize the fuzzy memberships dictionary
    memberships = {}

    for node_idx, node in enumerate(nodes):
        # Calculate distances to centroids
        distances = {f'cluster{i}': np.linalg.norm(centroids[i] - dissimilarity_matrix[node_idx]) for i in centroids}
        
        # Invert the distances to get membership strengths (higher distance -> lower membership)
        inverted_memberships = {cluster_label: 1 / (distance + 1e-5) for cluster_label, distance in distances.items()}
        
        # Add the inverted memberships to the raw_memberships dictionary for the node
        memberships[node] = list(inverted_memberships.items())
    
    return memberships


def determine_optimal_max_d(dissimilarity_matrix):
    # Detecting the elbow
    wcss_list = []
    max_d_values = np.linspace(0.1, 1.0, 10)  # Adjust the range and step as needed

    for max_d in max_d_values:
        clusters = perform_clustering(dissimilarity_matrix, max_d)
        wcss = calculate_wcss(clusters, dissimilarity_matrix)
        wcss_list.append(wcss)

    elbow_index = detect_elbow(wcss_list)
    optimal_max_d = max_d_values[elbow_index]

    # Output the optimal max_d
    print(f"Optimal max_d is: {optimal_max_d}")

    # Plotting the results with the elbow point highlighted
    plt.plot(max_d_values, wcss_list, 'bo-')
    plt.plot(max_d_values[elbow_index], wcss_list[elbow_index], 'ro')
    plt.title('Elbow Method For Optimal max_d')
    plt.xlabel('max_d')
    plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
    plt.show()

    return optimal_max_d
