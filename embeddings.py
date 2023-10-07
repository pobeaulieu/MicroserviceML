import torch
import numpy as np


def generate_embeddings_for_java_code(code, model, tokenizer, device):
    '''Generate embeddings for the provided java file.'''
    
    # Tokenize the code
    all_code_tokens = tokenizer.tokenize(code)

    # Initialize an empty list to store the embeddings
    embeddings_for_file = []

    # Process the tokens in chunks of maximum length 510 (to account for [CLS] and [SEP])
    chunk_size = 510

    for n in range(0, len(all_code_tokens), chunk_size):
        chunk_code_tokens = all_code_tokens[n:n+chunk_size]

        # Add CLS (start) and SEP (end) tokens to the chunk tokens
        tokens = [tokenizer.cls_token] + chunk_code_tokens + [tokenizer.sep_token]

        # Convert the tokens to input IDs and create a PyTorch tensor
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_tensor = torch.tensor(input_ids).unsqueeze(0).to(device)  # add batch dimension and move to device

        # Generate embeddings using the model
        with torch.no_grad():
            outputs = model(input_tensor)
        
        # Retrieve the [CLS] token's embeddings (the first token) from the outputs
        cls_embedding = outputs.last_hidden_state[0][0].cpu().numpy()

        # Append this embedding to our embeddings list
        embeddings_for_file.append(cls_embedding)

    # Compute the mean of all embeddings for this file
    mean_of_embeddings = np.mean(embeddings_for_file, axis=0)

    return mean_of_embeddings


# List of stopwords
java_stopwords = [
    'handle', 'cancel', 'title', 'parent', 'cell', 'bean', 'loader', 'stage',
    'pressed', 'dragged', 'view', 'box', 'initialize', 'total', 'view', 'image',
    'icon', 'offset', 'node', 'scene', 'duration', 'drawer', 'nav', 'load', 
    'data', 'is', 'empty', 'all', 'static', 'cascade', 'transaction', 'override',
    'join', 'one', 'description', 'strategy', 'generation', 'override',
    'persistence', 'generated', 'io', 'projection', 'property', 'commit', 'dao',
    'this', 'style', 'menu', 'begin', 'column', 'translate', 'on', 'selected',
    'name', 'png', 'logo', 'string', 'name', 'table', 'exception', 'contains',
    'filter', 'controller', 'implement', 'button', 'session', 'hibernate', 'array',
    'org', 'save', 'clear', 'boolean', 'init', 'remove', 'entity', 'observable',
    'double', 'length', 'alert', 'action', 'field', 'bundle', 'show', 'root', 
    'list', 'index', 'text', 'return', 'wait', 'lower', 'true', 'false', 'java',
    'util', 'long', 'collection', 'interface', 'layout', 'value', 'valid', 'is',
    'value', 'type', 'model', 'public', 'private', 'id', 'error', 'void', 'not',
    'int', 'float', 'for', 'set', 'catch', 'try', 'javafx', 'import', 'class',
    'com', 'package', 'if', 'else', 'null', 'no', 'delete', 'add', 'edit', 'get',
    'new', 'open', 'close', 'mouse', 'event', 'window', 'throw'
]

def generate_word_embeddings_for_java_code(code, model, lemmatizer, stopwords=java_stopwords):
    """Process a Java code string to extract, preprocess, and vectorize words."""
    
    # Extract all alphabetic words and filter out stopwords.
    words = [word for word in re.findall("[a-zA-Z]+", code) if word not in stopwords]

    # Get embeddings for lemmatized words that are in the word2vec model.
    embeddings = [model[lemma] for word in words 
                  if (lemma := lemmatizer.lemmatize(word.lower())) in model]

    # Return the mean embedding, if available.
    return np.mean(embeddings, axis=0) if embeddings else None