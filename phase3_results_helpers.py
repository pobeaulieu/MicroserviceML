import csv

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]


# find_best_match returns the greatest ratio of the matching between the microservice genrated and the ground truths
# For example, a ratio of 0.5 means that half of the services in the result set of a microservice are found in the ground truths that best matches
def find_best_match(microservice_result, microservices_ground_truths):
    max_intersection_ratio = max(
        len(set(microservice_ground_truth).intersection(set(microservice_result))) / len(set(microservice_ground_truth))
        for microservice_ground_truth in microservices_ground_truths
    )
    return max_intersection_ratio


def calculate_microservices_clustering_results(ground_truth_path, results_path, matching_threshold):
    microservices_ground_truths = read_csv(ground_truth_path)
    microservices_results = read_csv(results_path)

    # Initialize True Positives (TP)
    tp = 0

    # Iterate over results to check for True Positives
    for i, microservice_result in enumerate(microservices_results):
        best_match_ratio = find_best_match(microservice_result, microservices_ground_truths)
        print(f"Microservice {i}, best match ratio = {best_match_ratio}")
        if best_match_ratio > matching_threshold:
            tp += 1
    # Calculate False Positives (FP) and False Negatives (FN)
    fp = len(microservices_results) - tp
    fn = len(microservices_ground_truths) - tp

    # Calculate Precision
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    # Calculate Recall
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    # Calculate F-measure
    f_measure = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f_measure, tp, fp, fn

    
def generate_microservices_clustering_results_by_model(models, version, system, best_community_detection_algorithm, matching_threshold):
    ground_truth_path = f"ground_truths/{version}/{system}/microservices/microservices.csv"
    output_file_path = f"generated_data/phase3_microservice_clustering/hierarchical/{version}_{system}_{best_community_detection_algorithm}_metrics.csv"
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = [ 'Model', 'TP', 'FP', 'FN','Precision', 'Recall', 'F-measure']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for m in models:
            print(f"Evaluating model {m}")
            results_path = f"generated_data/phase3_microservice_clustering/{m}/{version}_{system}_{best_community_detection_algorithm}_microservices.csv"
            precision, recall, f_measure, tp, fp, fn = calculate_microservices_clustering_results(ground_truth_path, results_path, matching_threshold)

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