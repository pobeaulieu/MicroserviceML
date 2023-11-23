import torch
import numpy as np
import re
from microminer.common.constants import java_stopwords
from microminer.helpers.reader import load_class_code_from_directory
from microminer.config.device_setup import set_device

def generate_embeddings_for_java_code(code, model, tokenizer, is_phase_2_model=False):
    '''Generate embeddings for the provided java file.'''

    if is_phase_2_model:
        # Split the code into words, remove stopwords, and rejoin into a string
        words = re.findall(r'\b\w+\b', code)
        filtered_code = ' '.join(word for word in words if word not in java_stopwords)
    else:
        filtered_code = code
    
    # Tokenize the code
    all_code_tokens = tokenizer.tokenize(filtered_code)

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
        input_tensor = torch.tensor(input_ids).unsqueeze(0).to(set_device())  # add batch dimension and move to device

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


def generate_word_embeddings_for_java_code(code, model, lemmatizer, stopwords=java_stopwords):
    """Process a Java code string to extract, preprocess, and vectorize words."""
    
    # Extract all alphabetic words and filter out stopwords.
    words = [word for word in re.findall("[a-zA-Z]+", code) if word not in stopwords]

    # Get embeddings for lemmatized words that are in the word2vec model.
    embeddings = [model[lemma] for word in words 
                  if (lemma := lemmatizer.lemmatize(word.lower())) in model]

    # Return the mean embedding, if available.
    return np.mean(embeddings, axis=0) if embeddings else None


def create_class_embeddings_for_system(model_type, model, tokenizer, is_phase_2=False, training_system_name=None):
    """
    Creates embeddings for all classes in a system.

    :param system: System string
    :param model_type: Model type string
    :param model: Model object
    :param tokenizer: Tokenizer object
    :return: Dictionary containing embeddings for each class.
    """
    # If embeddings already exist, load them from CSV, skip the rest
    class_code = load_class_code_from_directory(training_system_name)

    if model_type == "word2vec":
        class_embeddings = {class_name: generate_word_embeddings_for_java_code(code, model, tokenizer) for class_name, code in class_code.items()}
    else:
        class_embeddings = {class_name: generate_embeddings_for_java_code(code, model, tokenizer, is_phase_2_model=is_phase_2) for class_name, code in class_code.items()}

    return class_embeddings


def compute_service_embeddings(embeddings, communities):
    """
    Compute service embeddings by averaging the embeddings of classes within each service.

    Parameters:
    - embeddings_dict (dict): Dictionary mapping class names to their embeddings.
    - communities (dict): Dictionary containing nested lists of class names for each service.

    Returns:
    - dict: Dictionary of computed service embeddings.
    """
    service_embeddings = {}
    for service_type, class_groups in communities.items():
        # Flatten the list of class name lists
        flattened_class_names = [class_name for group in class_groups for class_name in group]

        # Compute embeddings
        class_embeddings = [embeddings[class_name] for class_name in flattened_class_names if class_name in embeddings]
        if class_embeddings:
            service_embeddings[service_type] = np.mean(class_embeddings, axis=0)

    return service_embeddings

