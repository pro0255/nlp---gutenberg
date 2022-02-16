from transformers import TFAutoModel
from src.tokenizers.transformer_tokenizer import TransformerTokenizer
from src.encoder.create_encoder_from_path import create_encoder_from_path
from src.tokenizers.prepare_dataset_from_tokenizer import prepare_dataset_from_tokenizer
from src.models.transformer.bert_pooling_layer import BertPoolingLayer
from transformers import AutoConfig
import numpy as np

class TransformerVectorizer():
    def __init__(
        self, 
        transformer_type,
        transformer_pooling_type,
        path_authors=None,
        encoder=None, 
        max_len=512, 
        preprocess_pipeline=None,
    ):
        self.transformer_type = transformer_type.value
        self.transformer_pooling_type = transformer_pooling_type
        self.encoder = encoder
        self.max_len = max_len
        self.preprocess_pipeline = preprocess_pipeline
        self.path_to_authors = path_authors
        self.setup()

    def setup(self):
        self.config = AutoConfig.from_pretrained(self.transformer_type, output_hidden_states=True)
        self.transformer = TFAutoModel.from_config(self.config)
        encoder = None if self.path_to_authors is None else create_encoder_from_path(self.path_to_authors)
        self.tokenizer = TransformerTokenizer(
            self.transformer_type, 
            encoder
        )

    def fit_transform(self, dataset):
        sentence_embedding = []
        labels = []

        for x in prepare_dataset_from_tokenizer(dataset, self.tokenizer).batch(1):
            transformer_input, label = x
            output = self.transformer(
                transformer_input, 
                output_hidden_states=True
            )
            
            output = BertPoolingLayer()(
                output, 
                self.transformer_pooling_type
            )

            output = output.numpy().reshape(-1)
            label = label.numpy()[0] 

            labels.append(label)
            sentence_embedding.append(output)
        return np.array(sentence_embedding), np.array(labels)

    def create_embedding_matrix(self, X):
        #TODO: add to embedding layer
        pass