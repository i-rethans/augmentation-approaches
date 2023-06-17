from sklearn.feature_extraction.text import TfidfVectorizer
from utils.eda_stopwords import stop_words
import random
import numpy as np
random.seed(1)


def get_tfidf(lines):
    sentences = [get_sentence(doc) for doc in lines]
    # Calculate TF-IDF weights
    vectorizer = TfidfVectorizer(analyzer="word", stop_words=stop_words)
    X = vectorizer.fit_transform(sentences)
    tfidf_matrix = X.toarray()

    return tfidf_matrix, vectorizer.vocabulary_


def get_sentence(doc):
    sentence = ''
    for token in doc:
        sentence += token.text + ' '
    return sentence


def get_tfidf_per_word(words, tfidf_values, vocabulary):
    word_indices = [vocabulary.get(word) for word in words]
    tfidf_per_word = [tfidf_values[word_index] if word_index !=
                      None else 0 for word_index in word_indices]
    return tfidf_per_word


def get_word_index(tfidf_values):
    tfidf_normalized = tfidf_values / sum(tfidf_values)
    cumulative_probabilites = np.cumsum(tfidf_normalized)

    r = random.uniform(0, 1)
    i = 0
    while r > cumulative_probabilites[i]:
        i += 1

    return i
