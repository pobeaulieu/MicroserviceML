import csv

##########################################################################################
#                           Generics for Phase 2 and phase 3 
##########################################################################################

# find_best_match returns the greatest ratio of the matching between the result cluster  (microservice or service)  and the ground truths
# For example, a ratio of 0.5 means that half of the classes in the result set are found in the ground truth that best matches the cluster
def find_best_match(result, ground_truths):
    max_intersection_ratio = max(
        len(set(gt).intersection(set(result))) / len(set(gt))
        for gt in ground_truths
    )
    return max_intersection_ratio

# calculate_clustering_results is generic for phase 2 and phase 3 clustering. 
# It computes precision, recall, f_measure, tp, fp, fn for the result_list (services or microservices) against the ground truth provided
def calculate_clustering_results(results_list, ground_truths_list, matching_threshold):
    # Initialize True Positives (TP)
    tp = 0

    # Iterate over results to check for True Positives
    for i, r in enumerate(results_list):
        best_match_ratio = find_best_match(r, ground_truths_list)
        print(f"Microservice {i}, best match ratio = {best_match_ratio}")
        if best_match_ratio > matching_threshold:
            tp += 1

    # Calculate False Positives (FP) and False Negatives (FN)
    fp = len(results_list) - tp
    fn = len(ground_truths_list) - tp

    # Calculate Precision
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    # Calculate Recall
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    # Calculate F-measure
    f_measure = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f_measure, tp, fp, fn




##########################################################################################
#                          Phase 2 - Service Clustering
##########################################################################################








##########################################################################################
#                          Phase 3 - Microservices Clustering
##########################################################################################
def read_microservice_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

# generate_microservices_clustering_result computes the metrics for phase 3 (microservice clustering) and generates a csv file for results 
def generate_microservices_clustering_results(models, version, system, best_community_detection_algorithm, matching_threshold):
    ground_truth_path = f"ground_truths/{version}/{system}/microservices/microservices.csv"
    output_file_path = f"generated_data/phase3_microservice_clustering/hierarchical/{version}_{system}_{best_community_detection_algorithm}_metrics.csv"
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = [ 'Model', 'TP', 'FP', 'FN','Precision', 'Recall', 'F-measure']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for m in models:
            print(f"Evaluating model {m}")
            results_path = f"generated_data/phase3_microservice_clustering/{m}/{version}_{system}_{best_community_detection_algorithm}_microservices.csv"
            microservices_results = read_microservice_csv(results_path)
            microservices_ground_truths = read_microservice_csv(ground_truth_path)
     
            precision, recall, f_measure, tp, fp, fn = calculate_clustering_results(microservices_results, microservices_ground_truths, matching_threshold)

            writer.writerow({
                'Model': m,
                'TP': tp,
                'FP': fp,
                'FN': fn,
                'Precision': precision,
                'Recall': recall,
                'F-measure': f_measure
            })

    print(f"Results for models {models} generated in file {output_file_path}")