from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier
import pickle

# Path to saved_models from root of project is microminer/classification/saved_models
path_to_saved_models = "microminer/classification/saved_models"

def create_classifiers():
    # Initializing classifiers as a dictionary
    classifiers = {
        'svm': SVC(kernel='linear', C=2, probability=True),
        'knn': KNeighborsClassifier(n_neighbors=5),
        'decision_tree': DecisionTreeClassifier(max_depth=2),
        'logistic_regression': LogisticRegression(random_state=0),
        'naive_bayes': GaussianNB()
    }

    # Ensemble classifiers
    ensemble_clf = VotingClassifier(estimators=[
        ('svm', classifiers['svm']), 
        ('knn', classifiers['knn']), 
        ('dt', classifiers['decision_tree']), 
        ('log_reg', classifiers['logistic_regression']), 
        ('gnb', classifiers['naive_bayes'])
    ], voting='soft')

    ada_boost = AdaBoostClassifier(base_estimator=classifiers['svm'], n_estimators=50, algorithm='SAMME.R', random_state=1)

    classifiers['ensemble'] = VotingClassifier(estimators=[
        ('ensemble_clf', ensemble_clf), 
        ('ada_boost', ada_boost)
    ], voting='soft')

    return classifiers

def train_classifiers(classifiers, Xtrain, ytrain):
    for classifier_name, classifier in classifiers.items():
        print(f"Training {classifier_name}...")
        classifier.fit(Xtrain, ytrain)
    return classifiers

def save_classifiers_to_pickle(classifiers, model_type):
    for classifier_name, classifier in classifiers.items():
        # Path to saved models is microminer/classification/saved_models
        filename = f"{path_to_saved_models}/{model_type}_{classifier_name}.pkl"
        pickle.dump(classifier, open(filename, 'wb'))

def load_classifiers_from_pickle(model_type):
    classifiers = {}
    for classifier_name in ['svm', 'knn', 'decision_tree', 'logistic_regression', 'naive_bayes', 'ensemble']:
        filename = f"{path_to_saved_models}/{model_type}_{classifier_name}.pkl"
        classifiers[classifier_name] = pickle.load(open(filename, 'rb'))
    return classifiers

def load_classifier_from_pickle(model_type, classifier_name):
    filename = f"{path_to_saved_models}/{model_type}_{classifier_name}.pkl"
    classifier = pickle.load(open(filename, 'rb'))
    return classifier

def predict_class(classifiers, Xtest):
    predictions = {}
    for classifier_name, classifier in classifiers.items():
        predictions[classifier_name] = classifier.predict(Xtest)
    return predictions

