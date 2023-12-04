# Functions for analyzing clusters
import numpy as np
from collections import defaultdict

def assign_clusters_based_on_comparative_ratios(memberships):
    """
    Assign services to clusters based on a comparison of their membership strengths.

    Parameters:
    - memberships (dict): Dictionary of services with their membership values.

    Returns:
    - dict: Cluster assignments based on comparative ratios of membership strengths.
    """
    cluster_assignments = {}

    for service, membership_values in memberships.items():
        if not membership_values:
            continue

        # Sort memberships in descending order of strength
        sorted_memberships = sorted(membership_values, key=lambda x: x[1], reverse=True)
        assigned_clusters = [sorted_memberships[0]]  # Start with the highest membership cluster

        for i in range(1, len(sorted_memberships)):
            current_membership = sorted_memberships[i][1]
            lower_mean = np.mean([m for _, m in sorted_memberships[i+1:]]) if i < len(sorted_memberships) - 1 else 0
            higher_mean = np.mean([m for _, m in sorted_memberships[:i]])

            # Compare ratios to determine cluster assignment
            ratio_with_lower = current_membership / lower_mean if lower_mean > 0 else float('inf')
            ratio_with_higher = current_membership / higher_mean if higher_mean > 0 else float('inf')

            if abs(ratio_with_higher - 1) < abs(ratio_with_lower - 1):
                assigned_clusters.append(sorted_memberships[i])
            else:
                break  # Stop assigning additional clusters

        cluster_assignments[service] = assigned_clusters

    return cluster_assignments

def merge_overlapping_clusters(data, overlap_threshold=0.5):
    """
    Merges clusters that have 50% or more common services and returns the updated data structure with sequential cluster labels.

    :param data: A dictionary with services as keys and list of tuples (cluster, membership) as values.
    :return: Updated data structure with merged clusters and sequential cluster labels.
    """
    # Create a reverse mapping from cluster to services
    cluster_to_services = defaultdict(set)
    for service, clusters in data.items():
        for cluster, _ in clusters:
            cluster_to_services[cluster].add(service)

    # Determine which clusters to merge based on common services
    clusters_to_merge = defaultdict(set)
    for cluster1, services1 in cluster_to_services.items():
        for cluster2, services2 in cluster_to_services.items():
            if cluster1 != cluster2:
                common_services = services1.intersection(services2)
                if len(common_services) >= overlap_threshold * min(len(services1), len(services2)):
                    clusters_to_merge[cluster1].add(cluster2)
                    clusters_to_merge[cluster2].add(cluster1)

    # Merge clusters
    merged_clusters = {}
    next_cluster_id = 1
    visited = set()
    for cluster, related_clusters in clusters_to_merge.items():
        if cluster not in visited:
            merged_cluster_name = f"cluster{next_cluster_id}"
            next_cluster_id += 1
            all_related_clusters = {cluster}.union(related_clusters)
            for c in all_related_clusters:
                merged_clusters[c] = merged_cluster_name
                visited.add(c)

    # Update the original data with the merged clusters
    updated_data = defaultdict(list)
    for service, clusters in data.items():
        for cluster, membership in clusters:
            new_cluster = merged_clusters.get(cluster, cluster)
            # Take the maximum membership for the same cluster
            existing_memberships = [m for c, m in updated_data[service] if c == new_cluster]
            if existing_memberships:
                max_membership = max(max(existing_memberships), membership)
                updated_data[service] = [(c, m) if c != new_cluster else (new_cluster, max_membership) for c, m in updated_data[service]]
            else:
                updated_data[service].append((new_cluster, membership))

    return dict(updated_data)

def identify_standalone_services(cluster_assignments, occurrence_threshold=0.5):
    """
    Identify services that are part of an excessive number of clusters, suggesting they should be standalone microservices.

    Parameters:
    - cluster_assignments (dict): The current cluster assignments of services.

    Returns:
    - dict: Updated cluster assignments with standalone microservices formed.
    """
    # Calculate the total number of unique clusters
    total_clusters = len(set(cluster for memberships in cluster_assignments.values() for cluster, _ in memberships))

    # Set threshold
    max_clusters_per_service = total_clusters * occurrence_threshold

    # Identify services in more clusters than the threshold
    standalone_candidates = {service for service, memberships in cluster_assignments.items() if len(memberships) > max_clusters_per_service}

    # Create standalone microservices for these candidates
    standalone_cluster_id = max(int(cluster[7:]) for memberships in cluster_assignments.values() for cluster, _ in memberships) + 1
    for service in standalone_candidates:
        cluster_assignments[service] = [(f"cluster{standalone_cluster_id}", 1.0)]
        standalone_cluster_id += 1

    # Remove these services from their original clusters
    for service in standalone_candidates:
        for memberships in cluster_assignments.values():
            memberships[:] = [m for m in memberships if m[0] != service]

    return cluster_assignments
