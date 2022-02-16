from nltk import tokenize
from src.preprocessing.preprocess_newlines import preprocess_newlines
from src.preprocessing.preprocess_delimiter import preprocess_delimiter


def chunk_document_by_sentence(document, k):
    preprocessed_document_for_sentences = preprocess_newlines(document)
    preprocessed_document_for_sentences = preprocess_delimiter(preprocessed_document_for_sentences)
    sentences = tokenize.sent_tokenize(preprocessed_document_for_sentences)
    chunked_sentences = [' '.join(sentences[sent_index:sent_index+k]) for sent_index in range(0, len(sentences), k)]
    return chunked_sentences