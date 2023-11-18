from enum import Enum

LABEL_MAPPING = {'Application': 0, 'Utility': 1, 'Entity': 2}
FUZZINESS = 2
ERROR_THRESHOLD = 0.005
MAX_ITERATIONS = 1000

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

# Create enum for phase 1 model (ft_codebert, word2vec, albert, codebert, roberta, bert)
class Phase1Model(Enum):
    ft_codebert = 1
    word2vec = 2
    albert = 3
    codebert = 4
    roberta = 5
    bert = 6

# Create enum for phase 1 classifier model (svm, knn, decision_tree, logistic_regression, naives_bayes)
class Phase1ClassifierModel(Enum):
    svm = 1
    knn = 2
    decision_tree = 3
    logistic_regression = 4
    naives_bayes = 5

# Create enum for phase 2 model (Louvain, Infomap, LabelPropagation, FastGreedy, GirvanNewman, Leiden, Walktrap)
class Phase2Model(Enum):
    Louvain = 1
    Infomap = 2
    LabelPropagation = 3
    FastGreedy = 4
    GirvanNewman = 5
    Leiden = 6
    Walktrap = 7

class Phase2EmbeddingsModel(Enum):
    word2vec = 1

# Create enum for phase 3 model (cmeans, custom_cmeans, hierarchical)
class Phase3Model(Enum):
    cmeans = 1
    custom_cmeans = 2
    hierarchical = 3


