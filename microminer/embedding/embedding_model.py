from transformers import AutoTokenizer, AutoModel, AlbertTokenizer, AlbertModel, RobertaModel, RobertaTokenizer, BertTokenizer, BertModel
import nltk
from nltk.stem import WordNetLemmatizer
import gensim.downloader as api
from config.device_setup import set_device

def select_model_and_tokenizer(model_type):
  # Select the model and tokenizer
    if (model_type == "codebert"):
        tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base",force_download=False)
        model = AutoModel.from_pretrained("microsoft/codebert-base",force_download=False)
        model = model.to(set_device())
    elif (model_type == "ft_codebert"):
        tokenizer = AutoTokenizer.from_pretrained("./codebert_finetuned",force_download=False)
        model = AutoModel.from_pretrained("./codebert_finetuned",force_download=False)
        model = model.to(set_device())
    elif (model_type == "bert"):
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased") 
        model = BertModel.from_pretrained("bert-base-uncased") 
        model = model.to(set_device())
    elif (model_type == "roberta"):
        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        model = RobertaModel.from_pretrained("roberta-base")
        model = model.to(set_device())
    elif (model_type == "albert"): 
        # pip3 install sentencepiece
        tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")
        model = AlbertModel.from_pretrained("albert-base-v2")
        model = model.to(set_device())
    elif model_type == "word2vec":
        # Download required NLTK datasets and initialize the lemmatizer
        nltk.download('wordnet')
        tokenizer = WordNetLemmatizer()

        # Load Word2Vec model
        model = api.load('word2vec-google-news-300')
    else:
        raise NameError("model type not supported")
    
    return tokenizer, model