
from utils.tfidf import get_word_index
from utils.wordnet import get_synonyms

import random
random.seed(1)
########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################


def random_insertion(words, n, syntax_tree, tfidf_values):
    # interjective --> beginning or end
    # noun --> add adjective if possible, else do random insertion
    # main verb --> add adverb if possible, else do random insertion
    # else do random insertion

    insertions = []
    attempts = 0
    max_attempts = 3*n
    while len(insertions) < n and attempts < max_attempts:
        word_index = get_word_index(tfidf_values)
        token = syntax_tree[word_index]
        insertion = None
        if token.pos_ == "NOUN":
            insertion = insert_before_noun(token, syntax_tree)
        elif token.pos_ == "INTJ":
            insertion = insert_interjective(
                token, syntax_tree)
        elif token.pos_ == "VERB" and token.dep_ == "ROOT":
            insertion = insert_verb(token, syntax_tree)

        else:
            insertion = add_word(token, syntax_tree)

        if insertion != None:
            insertions.append(insertion)
        else:
            attempts += 1

    new_words = do_insert(insertions, words)

    return new_words


def insert_before_noun(noun_token, syntax_tree):
    adjectives = [token.text for token in syntax_tree if token.dep_ == "amod"]

    if len(adjectives) != 0:
        random_word = random.choice(adjectives)
        synonyms = get_synonyms(random_word)
        if len(synonyms) == 0:
            return add_word(noun_token, syntax_tree)
        random_synonym = random.choice(synonyms)
        insert_index = noun_token.i - 1
        return insert_index, random_synonym

    return add_word(noun_token, syntax_tree)


def insert_interjective(interjective_token, syntax_tree):
    synonyms = get_synonyms(interjective_token.text)
    if len(synonyms) == 0:
        return None
    random_synonym = random.choice(synonyms)

    # interections almost always occur at the start and end of a sentence
    front_back_indices = [0, len(syntax_tree)-1]
    insert_index = random.choice(front_back_indices)
    return insert_index, random_synonym


def insert_verb(verb_token, syntax_tree):
    adverbs = [token.text for token in syntax_tree if token.pos == "ADV"]
    if len(adverbs) != 0:
        # 2/3 chance to be inserted before the main verb, 1/3 to be inserted after the main verb
        optional_indices = [verb_token.i - 1,
                            verb_token.i - 1, verb_token.i + 1]
        insert_index = random.choice(optional_indices)
        random_word = random.choice(adverbs)
        synonyms = get_synonyms(random_word)

        # if no synonyms, do random insertion
        if len(synonyms) == 0:
            return add_word(verb_token, syntax_tree)

        random_synonym = random.choice(synonyms)

        return insert_index, random_synonym

    return add_word(verb_token, syntax_tree)


def add_word(token, syntax_tree):
    synonyms = get_synonyms(token.text)
    if len(synonyms) == 0:
        return None
    random_synonym = random.choice(synonyms)
    random_index = random.randint(0, len(syntax_tree)-1)
    token_at_index = syntax_tree[random_index]

    # Find a place where the token can be inserted
    # without breaking dependencies in the syntax tree
    if token_at_index.n_lefts == 0:
        return (random_index, random_synonym)

    if token_at_index.n_rights == 0:
        return (random_index + 1, random_synonym)

    children = [child for child in token.children]
    while len(children) != 0:
        child = children.pop(0)
        if child.n_lefts == 0:
            return (child.i, random_synonym)
        if child.n_rights == 0:
            return (child.i + 1, random_synonym)
        children += [c for c in child.children]


def do_insert(insertions, words):
    new_words = words.copy()
    sorted_insertions = sorted(insertions, key=lambda x: x[0], reverse=True)
    for (index, synonym) in sorted_insertions:
        new_words.insert(index, synonym)

    return new_words
