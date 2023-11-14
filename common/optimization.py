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
