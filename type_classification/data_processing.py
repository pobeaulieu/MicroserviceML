import numpy as np
from collections import Counter
from imblearn.over_sampling import SMOTE
from helpers.embedding_helpers import load_embeddings_from_csv


def aggregate_training_data(version, model_type, training_systems, test_system=None):
    training_embeddings, training_labels, training_class_names = [], [], []
    test_embeddings, test_labels, test_class_names = [], [], []

    for system in training_systems:
        filename = f"./generated_data/class_embeddings/{version}_{system}_{model_type}_embeddings.csv"
        class_names, labels, embeddings = load_embeddings_from_csv(filename)

        # Filter out classes with label -1
        filtered_data = [(cn, lbl, emb) for cn, lbl, emb in zip(class_names, labels, embeddings) if lbl != -1]
        filtered_class_names, filtered_labels, filtered_embeddings = zip(*filtered_data)

        # Check if the system is the test_system and split data if needed
        if system == test_system:
            split_index = int(0.8 * len(filtered_embeddings))  # 80% for training
            training_embeddings.extend(filtered_embeddings[:split_index])
            training_labels.extend(filtered_labels[:split_index])
            training_class_names.extend(filtered_class_names[:split_index])

            test_embeddings.extend(filtered_embeddings[split_index:])
            test_labels.extend(filtered_labels[split_index:])
            test_class_names.extend(filtered_class_names[split_index:])
        else:
            training_embeddings.extend(filtered_embeddings)
            training_labels.extend(filtered_labels)
            training_class_names.extend(filtered_class_names)

    Xtrain = np.array(training_embeddings)
    ytrain = np.array(training_labels)
    Xtest = np.array(test_embeddings) if test_system else None
    ytest = np.array(test_labels) if test_system else None

    return Xtrain, ytrain, training_class_names, Xtest, ytest, test_class_names


def prepare_training_data(version, model_type, training_systems, test_system=None):
    Xtrain, ytrain, _, Xtest, ytest, _ = aggregate_training_data(version, model_type, training_systems, test_system)
    Xtrain, ytrain = resample_training_data(Xtrain, ytrain)
    return Xtrain, ytrain, Xtest, ytest



def resample_training_data(Xtrain, ytrain):
    # Calculate class frequencies and mean frequency
    class_freq = Counter(ytrain)
    mean_count = sum(class_freq.values()) // len(class_freq)

    # Identify classes that need resampling (e.g., significantly fewer than mean_count)
    threshold = 0.7  # 70% of the mean_count
    classes_to_resample = {cls: int(mean_count) for cls, count in class_freq.items() if count < mean_count * threshold}

    # make sure there are at least 2 instances of each class to resample
    classes_to_resample = {cls: count for cls, count in classes_to_resample.items() if count > 1}

    # Apply SMOTE
    if classes_to_resample:
        sm = SMOTE(sampling_strategy=classes_to_resample, k_neighbors=1, random_state=42)
        Xtrain, ytrain = sm.fit_resample(Xtrain, ytrain)
    return Xtrain, ytrain


def balance_class_distribution(Xtrain, ytrain, Xtest, ytest):
    """
    Balances the class distribution between training and test sets.

    :param Xtrain: Training data embeddings.
    :param ytrain: Training data labels.
    :param Xtest: Test data embeddings.
    :param ytest: Test data labels.
    :return: Modified training and test data and labels.
    """
    train_class_freq = Counter(ytrain)
    test_class_freq = Counter(ytest)

    # Calculate the ratio between the size of the training and test sets
    ratio = len(ytrain) / len(ytest)

    # Iterate over each class to make sure it has proportional representation in the test set
    for cls, train_count in train_class_freq.items():
        expected_test_count = int(train_count / ratio)
        actual_test_count = test_class_freq.get(cls, 0)

        if actual_test_count < expected_test_count:
            # Find instances in the training set to move to the test set
            for _ in range(expected_test_count - actual_test_count):
                cls_index = ytrain.index(cls)
                Xtest = np.vstack([Xtest, [Xtrain[cls_index]]])
                ytest.append(cls)
                Xtrain = np.delete(Xtrain, cls_index, axis=0)
                ytrain.pop(cls_index)

    return Xtrain, ytrain, Xtest, ytest