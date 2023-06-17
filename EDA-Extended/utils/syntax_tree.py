import spacy
from spacy import displacy


def load_nlp():
    return spacy.load('en_core_web_sm')


def get_syntax_tree(sentence, nlp):

    return nlp(sentence)

    # print(displacy.render(nlp(sentence),
    #   style='dep', options={'compact': True}))
    # displacy.render(doc, style='dep', jupyter=True, options={'distance': 120})


def get_root(syntax_tree):
    for token in syntax_tree:
        if token.dep_ == "ROOT":
            return token


# token.head -> parent of token
# token.deps -> children
# token.pos -> part of speech tagging, give info about type of word, e.g. NOUN
# token.dep -> syntactic dependency relation
# token.children -> direct children
# token.subtree -> all descendants
