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

        # Check if the system is the test_system and split data if needed
        if system == test_system:
            split_index = int(0.8 * len(embeddings))  # 80% for training
            training_embeddings.extend(embeddings[:split_index])
            training_labels.extend(labels[:split_index])
            training_class_names.extend(class_names[:split_index])

            test_embeddings.extend(embeddings[split_index:])
            test_labels.extend(labels[split_index:])
            test_class_names.extend(class_names[split_index:])
        else:
            training_embeddings.extend(embeddings)
            training_labels.extend(labels)
            training_class_names.extend(class_names)

    Xtrain = np.array(training_embeddings)
    ytrain = np.array(training_labels)
    Xtest = np.array(test_embeddings) if test_system else None
    ytest = np.array(test_labels) if test_system else None

    return Xtrain, ytrain, training_class_names, Xtest, ytest, test_class_names


def prepare_training_data(version, model_type, training_systems, test_system=None):
    Xtrain, ytrain, training_class_names, Xtest, ytest, _ = aggregate_training_data(version, model_type, training_systems, test_system)
    Xtrain, ytrain = ensure_minimum_class_instances(Xtrain, ytrain, training_class_names)
    Xtrain, ytrain = resample_training_data(Xtrain, ytrain)
    return Xtrain, ytrain, Xtest, ytest


def ensure_minimum_class_instances(Xtrain: np.ndarray, ytrain: np.ndarray, labels: list) -> (np.ndarray, np.ndarray):
    """
    Ensures that there are at least two instances of each class in the training data.

    :param Xtrain: The training data embeddings.
    :param ytrain: The training data labels.
    :param labels: A list of all unique labels/classes in the dataset.
    :return: Modified training data and labels.
    """
    unique_classes = set(labels)
    for cls in unique_classes:
        cls_indices = [i for i, x in enumerate(labels) if x == cls]

        # If there are no instances in the training set, add two instances if available, otherwise add one
        if cls not in ytrain:
            indices_to_add = cls_indices[:2]  # Take the first two indices or less
            for idx in indices_to_add:
                Xtrain = np.vstack([Xtrain, Xtrain[idx]])
                ytrain = np.append(ytrain, cls)
        # If there is only one instance, add one more if available
        elif np.count_nonzero(ytrain == cls) == 1 and len(cls_indices) > 1:
            second_instance_idx = cls_indices[1]
            Xtrain = np.vstack([Xtrain, Xtrain[second_instance_idx]])
            ytrain = np.append(ytrain, cls)

    return Xtrain, ytrain


def resample_training_data(Xtrain, ytrain):
    # Calculate class frequencies and mean frequency
    class_freq = Counter(ytrain)
    mean_count = sum(class_freq.values()) // len(class_freq)

    # Identify classes that need resampling (e.g., significantly fewer than mean_count)
    threshold = 0.7  # 70% of the mean_count
    classes_to_resample = {cls: int(mean_count) for cls, count in class_freq.items() if count < mean_count * threshold}

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