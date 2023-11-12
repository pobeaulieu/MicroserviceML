import numpy as np
import networkx as nx


def optimize_parameters_for_community_detection(label_type, subgraph_reindexed, algorithm, detect_communities_fn):
        best_params = {}
        best_modularity = -1  # initialize with a low value

        PARAM_RANGES = {
            'Louvain': (np.arange(0.1, 2.0, 0.2), 'resolution'),
            'GirvanNewman': (range(1, 10), 'level')
        }

        if algorithm in PARAM_RANGES:
            param_values, param_name = PARAM_RANGES[algorithm]

            for value in param_values:
                # Make sure the subgraph is connected before computing modularity
                if not nx.is_connected(subgraph_reindexed):
                    continue
                
                communities = detect_communities_fn(label_type, algorithm, **{param_name: value})
                modularity_value = nx.community.modularity(subgraph_reindexed, communities)

                if modularity_value > best_modularity:
                    best_modularity = modularity_value
                    best_params[param_name] = value
        else:
            print(f"Parameter optimization not supported for {algorithm}")
        return best_params


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
