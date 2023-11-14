import numpy as np

def detect_elbow(y_values):
    """
    Detect the 'elbow' point in a list of y-values.

    Parameters:
    - y_values (list): List of y-values.

    Returns:
    - int: Index of the 'elbow' point in the list.
    """
    n_points = len(y_values)
    all_coords = np.vstack((range(n_points), y_values)).T

    # Compute vectors between all points and the first point
    first_point = all_coords[0]
    line_vector = all_coords[-1] - first_point
    line_vector_norm = line_vector / np.sqrt(np.sum(line_vector**2))

    vec_from_first = all_coords - first_point
    scalar_prod = np.sum(vec_from_first * line_vector_norm, axis=1)
    vec_from_first_parallel = np.outer(scalar_prod, line_vector_norm)
    vec_to_line = vec_from_first - vec_from_first_parallel

    # Compute distances to the line for each point
    dist_to_line = np.sqrt(np.sum(vec_to_line ** 2, axis=1))

    # Find the index of the point with the maximum distance to the line
    idx_elbow = np.argmax(dist_to_line)
    return idx_elbow


def calculate_wcss(clusters, dissimilarity_matrix):
    wcss = 0
    for i in np.unique(clusters):
        cluster_points = dissimilarity_matrix[clusters == i]
        centroid = np.mean(cluster_points, axis=0)
        wcss += np.sum((cluster_points - centroid) ** 2)
    return wcss