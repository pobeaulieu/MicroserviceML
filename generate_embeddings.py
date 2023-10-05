import torch
import numpy as np


def generate_embeddings_for_java_file(code, model, tokenizer, device):
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