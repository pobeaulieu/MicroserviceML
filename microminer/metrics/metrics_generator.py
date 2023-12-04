from microminer.helpers.reader import load_class_labels, load_results, load_services_from_csv
from microminer.common.constants import SYSTEM_GIT_URL_MAPPING
from microminer.metrics.classification_metrics import calculate_classification_metrics
from microminer.metrics.clustering_metrics import calculate_clustering_metrics
from microminer.helpers.writer import write_metrics_to_excel
import os, glob

def get_most_recent_file(directory):
    list_of_files = glob.glob(f'{directory}/*')  # * means all files
    if not list_of_files:  # Check if list is empty
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

# Add argument parser
import argparse
parser = argparse.ArgumentParser(description='Generate metrics for MicroMiner')

# Add results file path argument with default as the most recent file in results/
default_results_file = get_most_recent_file('results')
parser.add_argument('--results', type=str, help='Path to results file', default=default_results_file)

def generate_metrics(results_file: str):
    # Load results and get system name from GitHub URL
    results_dict = load_results(results_file=results_file)
    system = SYSTEM_GIT_URL_MAPPING[results_dict['config']['github_url']]

    # Load ground truths
    class_labels = load_class_labels(system, version='v_team')
    services_ground_truths = load_services_from_csv(system, version='v_team', data_type='services')
    microservices_ground_truths = load_services_from_csv(system, version='v_team', data_type='microservices')

    # Calculate metrics for phase 1
    precision, recall, f1_score = calculate_classification_metrics(results_dict['phase_1'], class_labels)
    metrics_phase_1 = {
        'cl_avg_precision': precision,
        'cl_avg_recall': recall,
        'cl_avg_f1': f1_score
    }

    # Calculate metrics for phase 2
    metrics_phase_2 = calculate_clustering_metrics(results_dict['phase_2'], services_ground_truths)
    metrics_phase_2 = {
        'nb_services': sum(len(services_ground_truths[key]) for key in services_ground_truths),
        'nb_s_clusters': sum(len(results_dict['phase_2'][key]) for key in results_dict['phase_2']),
        'total_tp': metrics_phase_2['average']['total_true_positives'],
        'total_fp': metrics_phase_2['average']['total_false_positives'],
        'total_fn': metrics_phase_2['average']['total_false_negatives'],
        'avg_precision': metrics_phase_2['average']['precision'],
        'avg_recall': metrics_phase_2['average']['recall'],
        'avg_f1': metrics_phase_2['average']['f1_score']
    }

    # Calculate metrics for phase 3
    metrics_phase_3 = calculate_clustering_metrics(results_dict['phase_3'], microservices_ground_truths, is_microservice=True)
    metrics_phase_3 = {
        'nb_microservices': len(microservices_ground_truths),
        'nb_ms_clusters': len(results_dict['phase_3']['microservices']),
        'tp': metrics_phase_3['average']['total_true_positives'],
        'fp': metrics_phase_3['average']['total_false_positives'],
        'fn': metrics_phase_3['average']['total_false_negatives'],
        'precision': metrics_phase_3['average']['precision'],
        'recall': metrics_phase_3['average']['recall'],
        'f1': metrics_phase_3['average']['f1_score']
    }

    # Consolidate all metrics into a single dict
    metrics = {**results_dict['config'], **metrics_phase_1, **metrics_phase_2, **metrics_phase_3}

    # Write metrics to Excel
    write_metrics_to_excel(metrics, 'microminer/metrics/metrics.xlsx')

if __name__ == '__main__':
    # Parse arguments
    args = parser.parse_args()

    # Check if results file exists
    if not args.results:
        print("No results file found in the 'results/' directory.")
        exit()

    # Generate metrics
    generate_metrics(args.results)

# Example usage:
# python -m microminer.metrics.metrics_generator --results results/results.json

