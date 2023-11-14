import skfuzzy as fuzz
import matplotlib.pyplot as plt
from config.constants import FUZZINESS, ERROR_THRESHOLD, MAX_ITERATIONS


def fuzzy_cmeans_clustering(data, node_labels, optimal_clusters):
    """
    Clusters the data using Fuzzy C-Means, returning only significant memberships.
    
    Parameters:
        data: 2D array of shape (features, samples), the input data.
        node_labels: List of labels corresponding to the samples.
        optimal_clusters: The number of clusters to form as well as the number of centroids to generate.
        membership_threshold: Threshold for membership values to determine significant cluster membership.
        
    Returns:
        dict: A dictionary with node labels as keys and lists of (cluster, membership) tuples as values.
    """
    cntr, u, _, _, _, _, _ = fuzz.cmeans(
        data.T,
        c=optimal_clusters,
        m=FUZZINESS,
        error=ERROR_THRESHOLD,
        maxiter=MAX_ITERATIONS
    )
    
    # Create a dictionary to store memberships for each node
    memberships = {label: [] for label in node_labels}
    for i, label in enumerate(node_labels):
        memberships[label] = [(f'cluster{j+1}', u[j, i]) for j in range(optimal_clusters)]

    return memberships


def determine_optimal_clusters(data, cluster_range):
    """Determines the optimal number of clusters using the Elbow method."""
    fpc_values = []
    for c_value in cluster_range:
        _, _, _, _, _, _, fpc = fuzz.cmeans(
            data.T, 
            c=c_value, 
            m=FUZZINESS, 
            error=ERROR_THRESHOLD, 
            maxiter=MAX_ITERATIONS
        )
        fpc_values.append(fpc)

    plt.figure()
    plt.plot(cluster_range, fpc_values)
    plt.title('Fuzzy Partition Coefficient (FPC) for different cluster numbers')
    plt.xlabel('Number of clusters')
    plt.ylabel('FPC')
    plt.grid(True)
    plt.show()