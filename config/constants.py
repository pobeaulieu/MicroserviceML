from enum import Enum

LABEL_MAPPING = {'Application': 0, 'Utility': 1, 'Entity': 2}
FUZZINESS = 2
ERROR_THRESHOLD = 0.005
MAX_ITERATIONS = 1000

# List of stopwords
java_stopwords = [
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 
    'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 
    'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 
    'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 
    'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 
    'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 
    'try', 'void', 'volatile', 'while', 'true', 'false', 'null', 
    'controller', 'dao', 'model', 'service', 'repository', 'entity', 'component',
    'dto', 'vo', 'util', 'helper', 'factory', 'singleton', 'prototype', 'proxy',
    'delegate', 'strategy', 'adapter', 'facade', 'observer', 'decorator',
    'handle', 'cancel', 'title', 'parent', 'cell', 'bean', 'loader', 'stage',
    'pressed', 'dragged', 'view', 'box', 'initialize', 'total', 'view', 'image',
    'icon', 'offset', 'node', 'scene', 'duration', 'drawer', 'nav', 'load', 
    'data', 'is', 'empty', 'all', 'static', 'cascade', 'transaction', 'override',
    'join', 'one', 'description', 'generation', 'persistence', 'generated', 
    'io', 'projection', 'property', 'commit', 'dao', 'this', 'style', 'menu', 
    'begin', 'column', 'translate', 'on', 'selected', 'name', 'png', 'logo', 
    'string', 'name', 'table', 'exception', 'contains', 'filter', 'controller', 
    'implement', 'button', 'session', 'hibernate', 'array', 'org', 'save', 
    'clear', 'boolean', 'init', 'remove', 'entity', 'observable', 'double', 
    'length', 'alert', 'action', 'field', 'bundle', 'show', 'root', 'list', 
    'index', 'text', 'return', 'wait', 'lower', 'true', 'false', 'java', 'util', 
    'long', 'collection', 'interface', 'layout', 'value', 'valid', 'is', 'value', 
    'type', 'model', 'public', 'private', 'id', 'error', 'void', 'not', 'int', 
    'float', 'for', 'set', 'catch', 'try', 'javafx', 'import', 'class', 'com', 
    'package', 'if', 'else', 'null', 'no', 'delete', 'add', 'edit', 'get', 'new', 
    'open', 'close', 'mouse', 'event', 'window', 'throw'
]

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


