from utils.tfidf import get_word_index
from utils.syntax_tree import load_nlp, get_syntax_tree

import random
random.seed(1)

########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################


def random_swap(words, n, nlp, syntax_tree, tfidf_values):

    if len(words) == 1:
        return words

    if len(words) == 2:
        return [words[1], words[0]]
    current_syntax_tree = syntax_tree
    new_words = words.copy()

    for _ in range(n):
        # get a token that will form the basis of the swapping
        word_index = get_word_index(tfidf_values)
        original_token = syntax_tree[word_index]
        current_token = find_token(original_token, current_syntax_tree)

        # if no children, switch with parent
        if current_token.n_lefts == 0 and current_token.n_rights == 0:
            new_words[current_token.head.i] = current_token.text
            new_words[current_token.i] = current_token.head.text

        # if only left children, put all descendants as right children.
        if current_token.n_lefts != 0 and current_token.n_rights == 0:
            new_words = swap_left(current_token, new_words)

        # if only right children, put all descendants as left children.
        if current_token.n_lefts == 0 and current_token.n_rights != 0:
            new_words = swap_right(current_token, new_words)

        # if left and right children, randomly swap either left or right
        if current_token.n_lefts != 0 and current_token.n_rights != 0:
            options = ["left", "right"]
            choice = random.choice(options)
            if choice == "left":
                new_words = swap_left(current_token, new_words)
            else:
                new_words = swap_right(current_token, new_words)

        # create syntax tree based on new sentence
        current_syntax_tree = get_syntax_tree(' '.join(new_words), nlp)

    return new_words


def find_token(token, syntax_tree):
    for t in syntax_tree:
        if t.text == token.text:
            return t


def swap_left(root_token, words):
    # find all decendants
    to_explore = [child for child in root_token.lefts]
    min_index = root_token.i
    while len(to_explore) != 0:
        current_token = to_explore.pop()
        if current_token.i < min_index:
            min_index = current_token.i
        to_explore += [child for child in current_token.children]

    # swap token with all descendants
    new_words = words.copy()
    new_words[min_index] = words[root_token.i]
    new_words[min_index+1:root_token.i+1] = words[min_index:root_token.i]

    return new_words


def swap_right(root_token, words):
    # find all decendants
    to_explore = [child for child in root_token.rights]
    max_index = root_token.i
    while len(to_explore) != 0:
        current_token = to_explore.pop()
        if current_token.i > max_index:
            max_index = current_token.i
        to_explore += [child for child
                       in current_token.children]

    # swap token with all descendants
    new_words = words.copy()
    new_words[max_index] = words[root_token.i]
    new_words[root_token.i:max_index] = words[root_token.i+1:max_index+1]

    return new_words
