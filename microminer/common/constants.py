# Description: Constants used in the project

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

SYSTEM_GIT_URL_MAPPING = {'https://github.com/sadatrafsanjani/JavaFX-Point-of-Sales.git': 'pos', 
                          'https://github.com/rafaelsteil/jforum3.git': 'jforum',
                          'https://github.com/spring-projects/spring-petclinic.git': 'petclinic',
                          'https://github.com/javaee/cargotracker.git': 'cargotracker'}