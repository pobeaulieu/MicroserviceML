import torch
import numpy as np
import re
from config.constants import java_stopwords

def generate_embeddings_for_java_code(code, model, tokenizer, device, is_phase2_model=False):
    '''Generate embeddings for the provided java file.'''

    if is_phase2_model:
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


def generate_word_embeddings_for_java_code(code, model, lemmatizer, stopwords=java_stopwords):
    """Process a Java code string to extract, preprocess, and vectorize words."""
    
    # Extract all alphabetic words and filter out stopwords.
    words = [word for word in re.findall("[a-zA-Z]+", code) if word not in stopwords]

    # Get embeddings for lemmatized words that are in the word2vec model.
    embeddings = [model[lemma] for word in words 
                  if (lemma := lemmatizer.lemmatize(word.lower())) in model]

    # Return the mean embedding, if available.
    return np.mean(embeddings, axis=0) if embeddings else None


def compute_service_embeddings(embeddings_dict, communities):
    """
    Compute service embeddings by averaging the embeddings of classes within each service.
    
    Parameters:
    - embeddings_dict (dict): Dictionary mapping class names to their embeddings.
    - communities (DataFrame): DataFrame containing community data for each class.
    
    Returns:
    - dict: Dictionary of computed service embeddings.
    """
    service_embeddings = {}
    for service, class_group in communities.groupby('service')['class_name']:
        class_embeddings = [embeddings_dict[class_name] for class_name in class_group if class_name in embeddings_dict]
        if class_embeddings:
            service_embeddings[service] = np.mean(class_embeddings, axis=0)
    return service_embeddings