# Functions to visualize clusters and graphs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
import seaborn as sns


def visualize_heatmap(df, values_column, title):
    """Visualize a heatmap from a dataframe."""
    pivot_table = df.pivot(index='class1', columns='class2', values=values_column)
    
    plt.figure(figsize=(10, 8))
    heatmap = sns.heatmap(pivot_table, cmap='coolwarm', cbar_kws={'label': title})
    
    # Update y-tick labels
    ytick_labels = [label.get_text().split('.')[-1] for label in heatmap.get_yticklabels()]
    heatmap.set_yticklabels(ytick_labels)
    
    # Update x-tick labels
    xtick_labels = [label.get_text().split('.')[-1] for label in heatmap.get_xticklabels()]
    heatmap.set_xticklabels(xtick_labels)
    
    plt.title(title)
    plt.show()


def visualize_clusters(services_graph, fuzzy_clusters):
    """
    Visualize the clusters in a graph by coloring nodes based on their highest membership cluster, labeling them
    with shortened names, and adding a legend for cluster colors.

    Parameters:
        services_graph (networkx.Graph): The graph to visualize.
        fuzzy_clusters (dict): A dictionary with nodes as keys and lists of (cluster, membership) tuples as values.
    """
    # Convert the fuzzy clusters to a simple cluster assignment for each node
    cluster_assignment = {node: max(memberships, key=lambda x: x[1])[0] for node, memberships in fuzzy_clusters.items()}

    # Map each unique cluster to an integer and create a color map
    unique_clusters = list(set(cluster_assignment.values()))
    cluster_to_int = {cluster: i for i, cluster in enumerate(unique_clusters)}
    int_assignment = {node: cluster_to_int[cluster] for node, cluster in cluster_assignment.items()}
    cmap = cm.get_cmap('viridis', len(unique_clusters))

    # Convert the graph to undirected for visualization purposes
    services_graph_undirected = services_graph.to_undirected()

    # Position nodes using a spring layout
    pos = nx.spring_layout(services_graph_undirected, seed=42)

    # Draw nodes with colors from the cluster assignment
    nodes_draw = nx.draw_networkx_nodes(
        services_graph_undirected, pos,
        node_color=[int_assignment.get(node, 0) for node in services_graph_undirected.nodes()],
        cmap=cmap, node_size=50, alpha=0.8
    )

    # Draw the edges
    nx.draw_networkx_edges(services_graph_undirected, pos, alpha=0.5)

    # Create shortened labels for the nodes
    short_labels = {node: node.replace('Application Service ', 'AS')
                            .replace('Entity Service ', 'ES')
                            .replace('Utility Service ', 'US') for node in services_graph_undirected.nodes()}
    
    # Draw the labels for the nodes
    nx.draw_networkx_labels(services_graph_undirected, pos, short_labels, font_size=8)

    # Create a legend for the clusters
    cluster_colors = [cmap(cluster_to_int[cluster]) for cluster in unique_clusters]
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=f'Cluster {i+1}',
                                   markersize=10, markerfacecolor=color) for i, color in enumerate(cluster_colors)]
    plt.legend(handles=legend_elements, title="Clusters", bbox_to_anchor=(1, 1), loc='upper left')

    # Set margins for the axes so that nodes are not cut off
    plt.margins(0.1)

    # Show the plot
    plt.show()


def plot_membership_histograms(memberships):
    """
    Plot histograms of membership strengths for each service.

    Parameters:
    - memberships (dict): Dictionary of services with their membership values.
    """
    for service, membership_values in memberships.items():
        if not membership_values:
            continue

        # Extract membership strengths
        strengths = [membership for _, membership in membership_values]

        # Plot histogram for each service
        plt.figure()
        plt.hist(strengths, bins=len(membership_values), alpha=0.75)
        plt.title(f'Membership Strength Distribution for {service}')
        plt.xlabel('Membership Strength')
        plt.ylabel('Frequency')
        plt.show()
