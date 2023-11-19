from config.device_setup import set_device
from embedding.embedding_model import select_model_and_tokenizer
from helpers.embedding_helpers import write_embeddings_to_csv
from helpers.embedding_helpers import create_class_embeddings_for_system
from type_classification.data_processing import prepare_training_data
from type_classification.classifiers import create_classifiers, train_classifiers, save_classifiers_to_pickle, predict_class
from config.constants import System
from sklearn.metrics import accuracy_score, confusion_matrix
from type_classification.classification_reports import generate_classification_report, generate_classification_report_to_csv, generate_classification_report_for_types
from helpers.class_helpers import associate_classes_to_types
import os

system_names = [system.name for system in System]

####################################################################################################
# PHASE 1: CLASS TYPING
####################################################################################################

def run_class_typing(version, test_system, training_systems, model_type, selected_classifier):
    tokenizer, model = select_model_and_tokenizer(model_type)
    model = model.to(set_device())

    # Flag to check if test_system is also used for training
    is_test_system_in_training = test_system in training_systems

    # Create embeddings and ground truth labels
    for system in training_systems:
        print(f"Creating embeddings for {system}...")
        class_labels = associate_classes_to_types(version, system)
        # If embeddings already exist, skip the rest
        if os.path.exists(f"./generated_data/class_embeddings/{version}_{system}_{model_type}_embeddings.csv"):
            continue
        class_embeddings = create_class_embeddings_for_system(system, model_type, model, tokenizer)
        write_embeddings_to_csv(version, system, model_type, class_embeddings, class_labels)

    # Prepare training data, with special handling if test_system is also a training system
    Xtrain, ytrain, Xtest, ytest = prepare_training_data(version, model_type, training_systems, test_system if is_test_system_in_training else None)

    # Train classifiers
    classifiers = create_classifiers()
    classifiers = train_classifiers(classifiers, Xtrain, ytrain)
    save_classifiers_to_pickle(classifiers, model_type)

    # Predict and evaluate
    if is_test_system_in_training:
        # Use separated test data for prediction
        predictions = predict_class(classifiers, Xtest)
        y_evaluation = ytest
    else:
        # Normal prediction process
        class_embeddings = create_class_embeddings_for_system(test_system, model_type, model, tokenizer)
        predictions = predict_class(classifiers, list(class_embeddings.values()))
        # Write embeddings with predictions for selected classifier to CSV for next phase
        write_embeddings_to_csv(version, test_system, model_type, class_embeddings, predictions=predictions[selected_classifier])
        y_evaluation = None

    # Generate evaluation metrics and reports
    if y_evaluation.any():
        for classifier_name, prediction in predictions.items():
            prediction = [int(pred) for pred in prediction]
            print(zip(y_evaluation, prediction))
            accuracy = accuracy_score(y_evaluation, prediction)
            print(f"Accuracy for {classifier_name}: {accuracy}")
            print(f"Confusion matrix for {classifier_name}:")
            print(confusion_matrix(y_evaluation, prediction))
            generate_classification_report(y_evaluation, prediction)
            generate_classification_report_to_csv(y_evaluation, prediction, classifier_name, model_type)
            generate_classification_report_for_types(y_evaluation, prediction, classifier_name)


# Example usage:
# run_class_typing(['jforum', 'petclinic', 'cargotracker'], 'v_imen', 'pos', 'word2vec')










