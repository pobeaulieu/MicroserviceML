
# Functions to generate classification reports
import pandas as pd
import numpy as np
import os
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


def generate_classification_report(y_true, y_pred):
    # Identify unique labels in both true labels and predictions
    unique_labels = np.unique(np.concatenate((y_true, y_pred)))

    # Map unique labels to their corresponding names
    label_names_map = {-1: "None", 0: "Application", 1: "Utility", 2: "Entity"}
    dynamic_label_names = [label_names_map[label] for label in unique_labels]

    # Generate and print the classification report
    print(classification_report(y_true, y_pred, target_names=dynamic_label_names, zero_division=1))


def generate_classification_report_to_csv(y_true, y_pred, model_name, embedding_model):

    csv_file = f'generated_data/classification_reports/classification_reports_{embedding_model}.csv'

    unique_labels = np.unique(np.concatenate((y_true, y_pred)))
    label_names_map = {-1: "None", 0: "Application", 1: "Utility", 2: "Entity"}
    dynamic_label_names = [label_names_map[label] for label in unique_labels]
    
    report = classification_report(y_true, y_pred, target_names=dynamic_label_names, output_dict=True, zero_division=1)
    
    # Create a DataFrame from the report
    new_data = pd.DataFrame(report).transpose().reset_index()
    new_data.columns = ['label', 'precision', 'recall', 'f1-score', 'support']
    new_data['model_name'] = model_name
    
    # If CSV file exists and is non-empty, load it and filter out old model data
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        existing_data = pd.read_csv(csv_file)
        # Filter out the old data for the current model
        existing_data = existing_data[existing_data['model_name'] != model_name]
    else:
        existing_data = pd.DataFrame()

    # Concatenate new data with existing data
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Save the combined data back to CSV
    combined_data.to_csv(csv_file, index=False)


def generate_classification_report_for_types(y_true, y_pred, prediction_model_name):
    # Map unique labels to their corresponding names
    label_names_map = {-1: "None", 0: "Application", 1: "Utility", 2: "Entity"}

    # Generate the classification report
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=1)

    # Extract support values
    supports = [report[str(key)]['support'] for key in sorted(report.keys())[:-3]]
    labels = [label_names_map[int(key)] for key in sorted(report.keys())[:-3]]

    # Colors for each bar
    colors = ['blue', 'green', 'red']

    # Generate the histogram
    plt.bar(labels, supports, color=colors)
    plt.ylabel('Number of classes')
    plt.title(f'Type repartition using {prediction_model_name}')
    plt.show()


def extract_avg_metrics_and_save(embedding_models):
    # Placeholder DataFrame to aggregate results
    aggregated_df = pd.DataFrame()
    
    for embedding_model in embedding_models:
        # Construct the file path based on the provided embedding model name
        file_path = f"generated_data/classification_reports/classification_reports_{embedding_model}.csv"
        
        # Read the CSV data into a DataFrame
        df = pd.read_csv(file_path)
        
        # Filter rows where label is 'macro avg'
        macro_avg_df = df[df['label'] == 'macro avg']

        # Extract desired columns, values, and add embedding model name
        macro_avg_df['embedding_model'] = embedding_model
        result = macro_avg_df[['embedding_model', 'model_name', 'precision', 'recall', 'f1-score']]
        
        # Append the result to the aggregated dataframe
        aggregated_df = pd.concat([aggregated_df, result], ignore_index=True)

    # Save the aggregated dataframe to a new CSV
    aggregated_df.to_csv("generated_data/classification_reports/aggregated_results.csv", index=False)