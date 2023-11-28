from sklearn.metrics import classification_report

def calculate_classification_metrics(results_phase_1, class_labels):
    label_mapping = {'applicationClasses': 0, 'utilityClasses': 1, 'entityClasses': 2}

    # Prepare data for computation
    y_true = []
    y_pred = []

    # Append ground truth and predictions for each class
    for group, classes in results_phase_1.items():
        mapped_label = label_mapping[group]
        for cls_dict in classes:
            cls_name = cls_dict['className']  # Extract class name from the dictionary
            y_pred.append(mapped_label)
            y_true.append(class_labels.get(cls_name, -1))  # Use class name as the key

    # Calculate and print the classification report
    report = classification_report(y_true, y_pred, labels=[0, 1, 2], zero_division=0, output_dict=True)
    
    # Get weighted average precision, recall, f1-score, and accuracy
    precision = report['weighted avg']['precision']  # Get weighted average precision
    recall = report['weighted avg']['recall']  # Get weighted average recall
    f1_score = report['weighted avg']['f1-score']  # Get weighted average F1-score
    accuracy = report['accuracy']  # Get overall accuracy

    return precision, recall, f1_score, accuracy

    