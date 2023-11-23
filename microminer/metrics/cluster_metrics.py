import csv
import pandas as pd 


##########################################################################################
#                           Generics for Phase 2 and phase 3 
##########################################################################################

# find_best_match returns the greatest ratio of the matching between the result cluster  (microservice or service)  and the ground truths
# For example, a ratio of 0.5 means that half of the classes in the result set are found in the ground truth that best matches the cluster
def find_best_match(result, ground_truths):
    max_intersection_ratio = max(
        len(set(ground_truth).intersection(set(result))) / len(set(ground_truth))
        for ground_truth in ground_truths
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
        print(f"Cluster {i}, best match ratio = {best_match_ratio}")
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
import csv
import pandas as pd

def read_services_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def extract_classes_for_services(communities_df, service_names):
    return [
        communities_df.loc[communities_df['service'] == service, 'class_name'].tolist()
        for service in service_names
    ]

def extract_result_clusters(version, system, phase1_model, phase2_model):
        communities_df = pd.read_csv(f"generated_data/service_communities/{phase2_model}/{version}_{system}_{phase1_model}_communities.csv")
        all_services = communities_df['service'].unique().tolist()
        
        application_services_names = [service for service in all_services if service.startswith('Application')]
        entity_services_names = [service for service in all_services if service.startswith('Entity')]
        utility_services_names = [service for service in all_services if service.startswith('Utility')]

        application_services_clusters = extract_classes_for_services(communities_df, application_services_names)
        entity_services_clusters = extract_classes_for_services(communities_df, entity_services_names)
        utility_services_clusters = extract_classes_for_services(communities_df, utility_services_names)

        return application_services_clusters, entity_services_clusters, utility_services_clusters
        

def generate_services_clustering_results(phase2_models, phase1_model, version, system, matching_threshold):
    # Load ground truths
    application_ground_truths = read_services_csv(f"ground_truths/{version}/{system}/services/application.csv")
    entity_ground_truths = read_services_csv(f"ground_truths/{version}/{system}/services/entity.csv")
    utility_ground_truths = read_services_csv(f"ground_truths/{version}/{system}/services/utility.csv")
    all_models_output_file_path = f"generated_data/service_communities/AVERAGE_METRICS_{version}_{system}_{phase1_model}_threshold_{matching_threshold}.csv"

    with open(all_models_output_file_path, 'w', newline='') as all_models_csv_file:
        fieldnames = [ 'Phase 2 Model', 'Average Precision', 'Average Recall', 'Average F-measure']
        all_models_csv_file_writer = csv.DictWriter(all_models_csv_file, fieldnames=fieldnames)
        all_models_csv_file_writer.writeheader()

        for m in phase2_models:

            # Load results
            application_clusters, entity_clusters, utility_clusters = extract_result_clusters(version, system, phase1_model, m)

            # Evaluate metrics 
            print(f"------- Model {m}-------")
            print("Evaluating Application Services")
            precision_as, recall_as, f_measure_as, tp_as, fp_as, fn_as = calculate_clustering_results(application_clusters, application_ground_truths, matching_threshold)

            print("Evaluating Entity Services")
            precision_es, recall_es, f_measure_es, tp_es, fp_es, fn_es = calculate_clustering_results(entity_clusters, entity_ground_truths, matching_threshold)

            print("Evaluating Utility Services")
            precision_us, recall_us, f_measure_us, tp_us, fp_us, fn_us = calculate_clustering_results(utility_clusters, utility_ground_truths, matching_threshold)


            avg_precision = (precision_as + precision_es + precision_us)/3
            avg_recall = (recall_as + recall_es + recall_us)/3
            avg_f_measure = (f_measure_as + f_measure_es + f_measure_us)/3

            output_file_path = f"generated_data/service_communities/{m}/METRICS_{version}_{system}_{phase1_model}_threshold_{matching_threshold}.csv"
            with open(output_file_path, 'w', newline='') as csvfile:
                fieldnames = [ 'Service Type', 'Nb ground truths', 'Nb clusters', 'TP', 'FP', 'FN','Precision', 'Recall', 'F-measure']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                writer.writerow({
                    'Service Type': 'Application Services',
                    'Nb ground truths': len(application_ground_truths),
                    'Nb clusters': len(application_clusters),
                    'TP': tp_as,
                    'FP': fp_as,
                    'FN': fn_as,
                    'Precision': precision_as,
                    'Recall': recall_as,
                    'F-measure': f_measure_as
                })

                writer.writerow({
                    'Service Type': 'Entity Services',
                    'Nb ground truths': len(entity_ground_truths),
                    'Nb clusters': len(entity_clusters),
                    'TP': tp_es,
                    'FP': fp_es,
                    'FN': fn_es,
                    'Precision': precision_es,
                    'Recall': recall_es,
                    'F-measure': f_measure_es
                })

                writer.writerow({
                    'Service Type': 'Utility Services',
                    'Nb ground truths': len(utility_ground_truths),
                    'Nb clusters': len(utility_clusters),
                    'TP': tp_us,
                    'FP': fp_us,
                    'FN': fn_us,
                    'Precision': precision_us,
                    'Recall': recall_us,
                    'F-measure': f_measure_us
                })

                writer.writerow({
                    'Service Type': 'Average',
                    'TP': 'NULL',
                    'FP': 'NULL',
                    'FN': 'NULL',
                    'Precision': avg_precision,
                    'Recall': avg_recall,
                    'F-measure': avg_f_measure
                })

                all_models_csv_file_writer.writerow({
                    'Phase 2 Model': m,
                    'Average Precision': avg_precision,
                    'Average Recall': avg_recall,
                    'Average F-measure': avg_f_measure
                })

                print(f"Results for models {m} generated in file {output_file_path}")
            
            
    print(f"AVERAGE Results for models {phase2_models} generated in file {all_models_output_file_path}")


##########################################################################################
#                          Phase 3 - Microservices Clustering
##########################################################################################
def read_microservice_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

# generate_microservices_clustering_result computes the metrics for phase 3 (microservice clustering) and generates a csv file for results 
def generate_microservices_clustering_results(models, phase2_model, phase1_model, version, system, matching_threshold):
    ground_truth_path = f"ground_truths/{version}/{system}/microservices/microservices.csv"
    microservices_ground_truths = read_microservice_csv(ground_truth_path)
    
    output_file_path = f"generated_data/microservice_clusters/METRICS_{version}_{system}_{phase1_model}_{phase2_model}_threshold_{matching_threshold}.csv"
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = [ 'Model','Microservice Ground Truth Count','Microservice Generated Count', 'TP', 'FP', 'FN','Precision', 'Recall', 'F-measure']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for m in models:
            print(f"Evaluating model {m}")
            results_path = f"generated_data/microservice_clusters/{m}/{version}_{system}_{phase2_model}_microservices.csv"
            microservices_results = read_microservice_csv(results_path)

     
            precision, recall, f_measure, tp, fp, fn = calculate_clustering_results(microservices_results, microservices_ground_truths, matching_threshold)

            writer.writerow({
                'Model': m,
                'Microservice Ground Truth Count': len(microservices_ground_truths),
                'Microservice Generated Count': len(microservices_results),
                'TP': tp,
                'FP': fp,
                'FN': fn,
                'Precision': precision,
                'Recall': recall,
                'F-measure': f_measure
            })

    print(f"Results for models {models} generated in file {output_file_path}")