import re


def preprocess(lines):
    clean_lines = [clean_and_split(line) for line in lines]
    labels = [line[0] for line in clean_lines]
    lines = [line[1] for line in clean_lines]
    return labels, lines


def clean_and_split(line):
    parts = line[:-1].split('\t')
    label = parts[0]
    sentence = parts[1]
    clean_sentence = get_only_chars(sentence)

    return [label, clean_sentence]

# cleaning up text


def get_only_chars(line):
    clean_line = ""

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ")  # replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")
    line = line.lower()

    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnm ':
            clean_line += char
        else:
            clean_line += ' '

    clean_line = re.sub(' +', ' ', clean_line)  # delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line
