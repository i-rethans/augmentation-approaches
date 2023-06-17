import argparse
from eda import *
from utils.preprocess import preprocess
from utils.tfidf import *
from utils.syntax_tree import load_nlp, get_syntax_tree


# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou


# arguments to be parsed from command line
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str,
                help="input file of unaugmented data")
ap.add_argument("--output", required=False, type=str,
                help="output file of unaugmented data")
ap.add_argument("--output_label", required=False, type=str,
                help="output file of unaugmented data")
ap.add_argument("--num_aug", required=False, type=int,
                help="number of augmented sentences per original sentence")
ap.add_argument("--alpha_sr", required=False, type=float,
                help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_ri", required=False, type=float,
                help="percent of words in each sentence to be inserted")
ap.add_argument("--alpha_rs", required=False, type=float,
                help="percent of words in each sentence to be swapped")
ap.add_argument("--alpha_rd", required=False, type=float,
                help="percent of words in each sentence to be deleted")
args = ap.parse_args()

# the output file
output = None
if args.output:
    output = args.output
else:
    from os.path import dirname, basename, join
    output = join(dirname(args.input), 'eda_extended_' + basename(args.input))

# the output_label file
output_label = None
if args.output_label:
    output_label = args.output_label
else:
    from os.path import dirname, basename, join
    output_label = join(dirname(args.input),
                        'eda_label_extended_' + basename(args.input))

# number of augmented sentences to generate per original sentence
num_aug = 4  # default
if args.num_aug:
    num_aug = args.num_aug

# how much to replace each word by synonyms
alpha_sr = 0.1  # default
if args.alpha_sr is not None:
    alpha_sr = args.alpha_sr

# how much to insert new words that are synonyms
alpha_ri = 0.1  # default
if args.alpha_ri is not None:
    alpha_ri = args.alpha_ri

# how much to swap words
alpha_rs = 0.1  # default
if args.alpha_rs is not None:
    alpha_rs = args.alpha_rs

# how much to delete words
alpha_rd = 0.1  # default
if args.alpha_rd is not None:
    alpha_rd = args.alpha_rd

if alpha_sr == alpha_ri == alpha_rs == alpha_rd == 0:
    ap.error('At least one alpha should be greater than zero')

# generate more data with standard augmentation


def gen_eda(train_orig, output_file, output_label, alpha_sr, alpha_ri, alpha_rs, alpha_rd, num_aug=9):
    writer = open(output_file, 'w')
    writer_label = open(output_label, 'w')
    lines = open(train_orig, 'r').readlines()

    labels, clean_lines = preprocess(lines)

    nlp = load_nlp()
    analyzed_lines = [get_syntax_tree(line, nlp) for line in clean_lines]

    tdidf_matrix, vocabulary = get_tfidf(analyzed_lines)

    for i, (label, doc) in enumerate(zip(labels, analyzed_lines)):
        tfidf_values = tdidf_matrix[i]
        aug_sentences = eda(doc, tfidf_values, vocabulary, nlp, alpha_sr=alpha_sr, alpha_ri=alpha_ri,
                            alpha_rs=alpha_rs, p_rd=alpha_rd, num_aug=num_aug)
        if len(aug_sentences) != 5:
            print("wrong lengths")
            print(aug_sentences)
            print(tfidf_values)
        # for aug_sentence in aug_sentences:
        #     writer.write(aug_sentence + '\n')
        #     writer_label.write(label + '\n')

    writer.close()
    writer_label.close()
    print("generated augmented sentences with eda for " + train_orig +
          " to " + output_file + " with num_aug=" + str(num_aug))


# main function
if __name__ == "__main__":

    # generate augmented sentences and output into a new file
    gen_eda(args.input, output, output_label, alpha_sr=alpha_sr,
            alpha_ri=alpha_ri, alpha_rs=alpha_rs, alpha_rd=alpha_rd, num_aug=num_aug)
