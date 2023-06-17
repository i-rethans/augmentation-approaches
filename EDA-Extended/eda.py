# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

from utils.syntax_tree import *
from utils.tfidf import *
from utils.preprocess import get_only_chars
from utils.eda_stopwords import stop_words
from operations.delete import random_deletion
from operations.insert import random_insertion
from operations.replace import synonym_replacement
from operations.swap import random_swap
import random
from random import shuffle
random.seed(1)


########################################################################
# main data augmentation function
########################################################################


def eda(syntax_tree, tfidf_values, vocabulary, nlp, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
    words = [child.text for child in syntax_tree]
    tfidf_values = get_tfidf_per_word(words, tfidf_values, vocabulary)

    if sum(tfidf_values) == 0:
        original_sentence = ' '.join(words)
        return [' '.join(words) for i in range(num_aug + 1)]

    augmented_sentences = []

    if sum(tfidf_values) != 0:
        num_words = len(words)

        num_new_per_technique = int(num_aug/4)+1

        # sr
        if (alpha_sr > 0):
            n_sr = max(1, int(alpha_sr*num_words))
            for _ in range(num_new_per_technique):
                a_words = synonym_replacement(
                    words, n_sr, tfidf_values)
                # print("replaced:", ' '.join(a_words))
                augmented_sentences.append(' '.join(a_words))

        # ri
        if (alpha_ri > 0):
            n_ri = max(1, int(alpha_ri*num_words))
            for _ in range(num_new_per_technique):
                a_words = random_insertion(
                    words, n_ri, syntax_tree, tfidf_values)
                # print("inserted:", ' '.join(a_words))

                augmented_sentences.append(' '.join(a_words))

        # rs
        if (alpha_rs > 0):
            n_rs = max(1, int(alpha_rs*num_words))
            for _ in range(num_new_per_technique):
                a_words = random_swap(
                    words, n_rs, nlp, syntax_tree, tfidf_values)
                # print("swapped-:", ' '.join(a_words))
                augmented_sentences.append(' '.join(a_words))

        # rd
        if (p_rd > 0):
            n_rd = max(1, int(p_rd*num_words))
            for _ in range(num_new_per_technique):
                a_words = random_deletion(
                    words, n_rd, syntax_tree, tfidf_values)
                # print("deleted-:", ' '.join(a_words))
                augmented_sentences.append(' '.join(a_words))

    augmented_sentences = [get_only_chars(
        sentence) for sentence in augmented_sentences]
    shuffle(augmented_sentences)

    # trim so that we have the desired number of augmented sentences
    if num_aug >= 1:
        augmented_sentences = augmented_sentences[: num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [
            s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    # append the original sentence
    original_sentence = ''
    for token in syntax_tree:
        original_sentence += token.text + ' '
    augmented_sentences.append(original_sentence)

    return augmented_sentences
