from enum import Enum

# Create enum for version (v_imen, v_team)
class Version(Enum):
    v_imen = 1
    v_team = 2

# Create enum for system (jforum, cargotracker, petclinic, pos)
class System(Enum):
    jforum = 1
    cargotracker = 2
    petclinic = 3
    pos = 4

# Create enum for phase 1 embedding model (ft_codebert, codebert)
class Phase1EmbeddingModel(Enum):
    codebert = 1
    ft_codebert = 2

# Create enum for phase 1 classifier model (svm, knn, decision_tree, logistic_regression, naives_bayes)
class Phase1ClassifierModel(Enum):
    svm = 1
    knn = 2
    decision_tree = 3
    logistic_regression = 4
    naives_bayes = 5

# Create enum for phase 2 embedding model (word2vec, albert, roberta, bert)
class Phase2EmbeddingModel(Enum):
    word2vec = 1
    albert = 2
    roberta = 3
    bert = 4

# Create enum for phase 2 model (Louvain, Infomap, LabelPropagation, FastGreedy, GirvanNewman, Leiden, Walktrap)
class Phase2ClusteringModel(Enum):
    Louvain = 1
    Infomap = 2
    LabelPropagation = 3
    FastGreedy = 4
    GirvanNewman = 5
    Leiden = 6
    Walktrap = 7

# Create enum for phase 3 model (cmeans, custom_cmeans, hierarchical)
class Phase3ClusteringModel(Enum):
    cmeans = 1
    custom_cmeans = 2
    hierarchical = 3