
from utils.tfidf import get_word_index
from utils.wordnet import get_synonyms

import random
random.seed(1)

########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################


def synonym_replacement(words, n, tfidf_values):
    new_words = words.copy()

    max_attempts = 3*n
    attempts = 0
    replacements = 0

    while replacements < n and attempts < max_attempts:
        word_index = get_word_index(tfidf_values)
        random_word = words[word_index]
        synonyms = get_synonyms(random_word)

        # apply replacement if at least one synonym exists
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words[word_index] = synonym
            replacements += 1
        else:
            attempts += 1

    # this is stupid but we need it, trust me --> was already in code, not sure if I should leave it
    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')

    return new_words
