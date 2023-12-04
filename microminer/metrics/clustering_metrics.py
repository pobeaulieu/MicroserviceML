def flatten_clusters(services, is_microservice=False):
    """ Flatten services or microservices data into a list of sets. """
    flattened = []
    if is_microservice:
        for microservice in services['microservices']:
            cluster_set = set()
            for service_type, service_groups in microservice['microservice'].items():
                for service_group in service_groups:
                    cluster_set.update([service['className'] for service in service_group['service']])
            flattened.append(cluster_set)
    else:
        for service_groups in services.values():
            for service_group in service_groups:
                cluster_set = set([service['className'] for service in service_group['service']])
                flattened.append(cluster_set)
    return flattened

def calculate_overlap(set1, set2):
    """ Calculate the overlap ratio between two sets, as a number between 0 and 1. """
    intersection = len(set1.intersection(set2))
    bigger_set_size = max(len(set1), len(set2))
    return (intersection / bigger_set_size) if bigger_set_size > 0 else 0

# Suppose set1 = {A, B, C, D} and set2 = {B, C, E, F}.
# The intersection of set1 and set2 is {B, C}, because B and C are the common elements.
# The length of the intersection is 2 (since there are two elements: B and C).
# The size of the bigger set is 4 (both set1 and set2 have 4 elements, so we take the maximum, which is 4).
# The overlap ratio is therefore 2 / 4 = 0.5.
# This means that 50% of the bigger set (in this case, either set since they are of equal size) is found in the other set, indicating a moderate overlap.

# If set2 were {B, C}, then the overlap would be 0.5, as 50% of set1 is found in set2. If set2 had no elements in common with set1, the overlap would be 0, indicating no overlap.

def calculate_clustering_metrics(results, ground_truths, threshold=0.8, is_microservice=False):
    """ Calculate metrics for clustering, with an option for type-specific metrics in Phase 2. """
    metrics = {}
    total_TP = total_FP = total_FN = 0

    if is_microservice:
        # For Phase 3 - Microservices
        result_clusters = flatten_clusters(results, is_microservice)
        ground_truth_clusters = [set(microservice) for microservice in ground_truths]
        
        for result_cluster in result_clusters:
            overlaps = [calculate_overlap(result_cluster, gt_cluster) for gt_cluster in ground_truth_clusters]
            best_overlap = max(overlaps) if overlaps else 0
            if best_overlap >= threshold:
                total_TP += 1
            else:
                total_FP += 1

        for gt_cluster in ground_truth_clusters:
            overlaps = [calculate_overlap(gt_cluster, result_cluster) for result_cluster in result_clusters]
            best_overlap = max(overlaps) if overlaps else 0
            if best_overlap < threshold:
                total_FN += 1

    else:
        # For Phase 2 - Service Types
        for service_type in results.keys():
            result_clusters = flatten_clusters({service_type: results[service_type]})
            ground_truth_clusters = flatten_clusters({service_type: ground_truths[service_type]})

            TP = FP = FN = 0

            for result_cluster in result_clusters:
                overlaps = [calculate_overlap(result_cluster, gt_cluster) for gt_cluster in ground_truth_clusters]
                best_overlap = max(overlaps) if overlaps else 0
                if best_overlap >= threshold:
                    TP += 1
                else:
                    FP += 1

            for gt_cluster in ground_truth_clusters:
                overlaps = [calculate_overlap(gt_cluster, result_cluster) for result_cluster in result_clusters]
                best_overlap = max(overlaps) if overlaps else 0
                if best_overlap < threshold:
                    FN += 1

            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            metrics[service_type] = {
                'true_positives': TP,
                'false_positives': FP,
                'false_negatives': FN,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            }

            total_TP += TP
            total_FP += FP
            total_FN += FN

    # Calculate average precision, recall, and F1-score
    avg_precision = total_TP / (total_TP + total_FP) if (total_TP + total_FP) > 0 else 0
    avg_recall = total_TP / (total_TP + total_FN) if (total_TP + total_FN) > 0 else 0
    avg_f1_score = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0

    metrics['average'] = {
        'total_true_positives': total_TP,
        'total_false_positives': total_FP,
        'total_false_negatives': total_FN,
        'precision': avg_precision,
        'recall': avg_recall,
        'f1_score': avg_f1_score
    }

    return metrics
