import subprocess
import pkg_resources
import sys

required = {'leidenalg'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import networkx as nx
from cdlib import algorithms
# from karateclub import EdMot
from visualization import visualize_class_type_subgraph
from optimization import optimize_parameters_for_community_detection
from graphs import remove_self_loops
from constants import LABEL_MAPPING


def remove_duplicate_single_node_communities(communities):
    """Remove duplicated single-node communities."""
    # Get the single-node communities
    single_node_communities = [community for community in communities if len(community) == 1]
    
    # Convert to sets for easy comparison and remove duplicates
    unique_single_node_communities = set(tuple(community) for community in single_node_communities)
    
    # Remove all single-node communities from the original list
    communities = [community for community in communities if len(community) != 1]
    
    # Add back the unique single-node communities
    communities.extend([list(community) for community in unique_single_node_communities])
    
    return communities


class CommunityDetection:
    
    def __init__(self, graph, class_labels_dict, optimize_hyperparameters_flag=False):
        self.graph = graph.copy()  # Create a copy of the graph to avoid modifying the original
        remove_self_loops(self.graph)
        self.class_labels_dict = class_labels_dict
        self.optimize_hyperparameters_flag = optimize_hyperparameters_flag
        self.best_params = {}

    def get_subgraph_reindexed(self, label_type):
        """Get a subgraph based on label type and reindex its nodes."""
        classes = [class_name for class_name, label in self.class_labels_dict.items() if label == LABEL_MAPPING.get(label_type)]
        subgraph = self.graph.subgraph(classes)
        # visualize_class_type_subgraph(subgraph, label_type)
        mapping = {node: i for i, node in enumerate(subgraph.nodes())}
        return nx.relabel_nodes(subgraph, mapping), {i: node for node, i in mapping.items()}
    

    def detect_communities(self, label_type, algorithm):
        """Perform community detection based on a specified algorithm."""
        subgraph_reindexed, inverse_mapping = self.get_subgraph_reindexed(label_type)

        # If hyperparameter optimization flag is set, optimize parameters
        if self.optimize_hyperparameters_flag:
            self.best_params = optimize_parameters_for_community_detection(label_type, subgraph_reindexed, algorithm, self.detect_communities)
            
        ALGORITHMS = {
            'Louvain': lambda: algorithms.louvain(subgraph_reindexed, weight='weight', resolution=self.best_params.get('resolution', 0.5)).communities,
            'Infomap': lambda: algorithms.infomap(subgraph_reindexed).communities,
            'LabelPropagation': lambda: algorithms.label_propagation(subgraph_reindexed).communities,
            'GirvanNewman': lambda: algorithms.girvan_newman(subgraph_reindexed, level=self.best_params.get('level', 1)).communities,
            'FastGreedy': lambda: algorithms.greedy_modularity(subgraph_reindexed).communities,
            # 'EdMot': lambda: self._algorithm_edmot(subgraph_reindexed),
            'Leiden': lambda: algorithms.leiden(subgraph_reindexed).communities,
            'Walktrap': lambda: algorithms.walktrap(subgraph_reindexed).communities
        }
            
        if len(subgraph_reindexed.nodes()) < 4:
            communities_reindexed = list(nx.community.label_propagation_communities(subgraph_reindexed))
        else:
            # If the graph is disconnected and the algorithm is Infomap or FastGreedy, skip the algorithm.
            if (not nx.is_connected(subgraph_reindexed) and (algorithm == 'Infomap' or algorithm == 'FastGreedy')):
                print(f"Graph is disconnected. Skipping {algorithm}.")
                return [[inverse_mapping[node]] for node in subgraph_reindexed.nodes()]  # Treat each node as its own community
            else:
                communities_reindexed = ALGORITHMS.get(algorithm, lambda: print(f"Error: The algorithm '{algorithm}' is not supported. Supported algorithms are: {', '.join(ALGORITHMS.keys())}."))()

        # Handle isolated nodes:
        # Create separate communities for each of them
        isolated_nodes = [node for node in subgraph_reindexed.nodes() if subgraph_reindexed.degree(node) == 0]
        for node in isolated_nodes:
            communities_reindexed.append([node])

        communities = [[inverse_mapping[node] for node in community] for community in communities_reindexed]
        
        # Remove duplicated single-node communities
        communities = remove_duplicate_single_node_communities(communities)

        return communities
    

    # Commented out because causes issues
    # def _algorithm_edmot(self, subgraph_reindexed):
    #     """Compute communities using the EdMot algorithm."""
    #     edmot = EdMot()
    #     edmot.fit(subgraph_reindexed)
    #     memberships = edmot.get_memberships()
    #     unique_communities = set(memberships.values())
    #     return [list({node for node, community_id in memberships.items() if community_id == c}) for c in unique_communities]