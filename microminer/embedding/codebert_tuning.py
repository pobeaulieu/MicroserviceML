import optuna
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoModel
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import accelerate # leave here
from helpers.mapper import map_classes_to_type_labels
from helpers.reader import load_class_code_from_directory
from config.device_setup import set_device

# Add argument to tune hyperparameters to the script (False by default)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--optimize_hyperparameters', action='store_true')


def tune_codebert(optimize_hyperparameters=False):
    class_labels = map_classes_to_type_labels('v_imen', 'pos')

    class_code = load_class_code_from_directory('pos')

    examples = []
    for key in class_code.keys():
        if key in class_labels.keys():
            examples.append({"text": class_code[key], "label": class_labels[key]})

    # Split data into train and validation sets
    train_examples, val_examples = train_test_split(examples, test_size=0.1)

    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base", force_download=False)
    model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base", num_labels=3, force_download=False)
    model = model.to(set_device())  

    if optimize_hyperparameters:
        # Create a study to run the hyperparameter optimization
        study = optuna.create_study(direction="minimize")

        # Run the optimization with additional arguments
        study.optimize(lambda trial: objective(trial, train_examples, val_examples, tokenizer), n_trials=10)

        # Print the results
        best_params = study.best_params
        print(f"Best hyperparameters: {best_params}")

        train_model(model, train_examples, tokenizer, set_device(), best_params['lr'], best_params['batch_size'], best_params['num_train_epochs'])
    else:
        # Fine-tune and save the model
        train_model(model, train_examples, tokenizer, set_device())

    model.save_pretrained("./codebert_finetuned")
    tokenizer.save_pretrained("./codebert_finetuned")


# Implement a PyTorch Dataset
class CodingDataset(Dataset):
    def __init__(self, examples, tokenizer):
        self.examples = examples
        self.tokenizer = tokenizer
        
    def __len__(self):
        return len(self.examples)
        
    def __getitem__(self, idx):
        example = self.examples[idx]
        encoding = self.tokenizer(example['text'], padding='max_length', truncation=True, max_length=512, return_tensors='pt')
        encoding = {key: value.squeeze(0) if value.shape[0] == 1 else value for key, value in encoding.items()}
        return {"input_ids": encoding["input_ids"], "attention_mask": encoding["attention_mask"], "labels": example["label"]}
    

def train_model(model, examples, tokenizer, device, lr=0.00014471090778860618, batch_size=16, num_train_epochs=8):
    dataset = CodingDataset(examples, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()

    epochs = num_train_epochs
    for epoch in range(epochs):
        for idx, batch in enumerate(dataloader):
            # First, process tensors in the batch
            batch = {key: value.squeeze(0) if value.shape[0] == batch_size else value for key, value in batch.items()}
            # Next, transfer each tensor to the correct device
            batch = {key: value.to(device) for key, value in batch.items()}
            
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

        print("Training completed.")


# Define objective function for optuna to optimize
def objective(trial, train_examples, val_examples, tokenizer):
    def model_init():
        model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base", num_labels=3)
        model = model.to(set_device())
        return model
    
    # Define hyperparameters for this trial
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-1)  # Learning rate
    batch_size = trial.suggest_categorical('batch_size', [8, 16, 32, 64])  # Batch size

    # Create data loaders
    train_dataset = CodingDataset(train_examples, tokenizer)
    val_dataset = CodingDataset(val_examples, tokenizer)

    # Specify the training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=trial.suggest_int('num_train_epochs', 1, 10), # tune hyperparameter here
        learning_rate=lr,
        per_device_train_batch_size=batch_size,
        logging_dir='./logs',
    )

    # Training
    trainer = Trainer(
        model_init=model_init,
        args=training_args,  
        train_dataset=train_dataset,         
        eval_dataset=val_dataset             
    )

    trainer.train()

    # Evaluate the model on the validation set
    eval_result = trainer.evaluate()
        
    # Optuna seeks for the minimum so return loss as it is
    return eval_result["eval_loss"]

if __name__ == "__main__":
    args = parser.parse_args()
    optimize_hyperparameters = args.optimize_hyperparameters
    tune_codebert(optimize_hyperparameters)
