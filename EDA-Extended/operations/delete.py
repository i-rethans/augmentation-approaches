
from utils.tfidf import get_word_index

import random
random.seed(1)
########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p
########################################################################


def random_deletion(words, n, syntax_tree, tfidf_values):
    new_words = words.copy()
    inverse_tfidf_values = [1 - value if value !=
                            0 else 0 for value in tfidf_values]

    if len(words) == 1:
        return words

    total_deleted = 0
    while total_deleted < n and sum(1 for word in new_words if word is not None) > 1:
        word_index = get_word_index(inverse_tfidf_values)
        token = syntax_tree[word_index]
        new_words, num_deleted, inverse_tfidf_values = do_delete(
            new_words, token, inverse_tfidf_values)
        total_deleted += num_deleted

    result = [word for word in new_words if word is not None]

    # if you end up deleting all words, return a random word
    if len(result) == 0:
        rand_int = random.randint(0, len(words)-1)
        return [words[rand_int]]

    return result


def do_delete(new_words, token, inverse_tfidf_values):
    num_deleted = 0

    # if word has no children, remove the word
    if token.n_lefts == 0 and token.n_rights == 0:
        new_words[token.i] = None
        inverse_tfidf_values[token.i] = 0
        num_deleted += 1

    # if the word has only children on one side, delete the children
    elif token.n_rights > 0 and token.n_lefts == 0:
        for child in token.rights:
            new_words[child.i] = None
            inverse_tfidf_values[child.i] = 0

        num_deleted += 1 + token.n_rights

    elif token.n_lefts > 0 and token.n_rights == 0:
        for child in token.lefts:
            new_words[child.i] = None
            inverse_tfidf_values[child.i] = 0

        num_deleted += 1 + token.n_lefts

    # else apply delete function to a random child.
    else:
        random_child_index = random.randint(0, token.n_lefts+token.n_rights+1)
        for i, child in enumerate(token.children):
            if i == random_child_index:
                return do_delete(new_words, child, inverse_tfidf_values)

    return new_words, num_deleted, inverse_tfidf_values
