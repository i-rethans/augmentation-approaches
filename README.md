# Augmentation-approaches
This repo contains all code used for the project of the course CS4360 Natural Language processing. For the project we analysed three existing data augmentation approaches and also proposed our own method called Extended EDA

## Extended EDA (Easy Data Augmentation)
Extended EDA builds upon the original EDA method proposed by Jin et al. [1]. Please refer to the paper for more details on the EDA method. The original EDA code can be found at: [EDA Repository](https://github.com/jasonwei20/eda_nlp/blob/master/README.md)

The full details of the method are explained in our paper
# Usage

To run extended EDA, first some prerequisits have to be met:
### Install NLTK (if you don't have it already):

Pip install it.

```bash
pip install -U nltk
```

Download WordNet.
```bash
python
>>> import nltk; nltk.download('wordnet')
```

### Run Extended EDA

For this implementation, the input files have the format `label\tsentence` (note the `\t`). So for instance, your input file should look like this (example from the dataset MNLI found [here](https://cims.nyu.edu/~sbowman/multinli/s)):

```
contradiction   Don't ruin the evening, Jonofi.
neutral   Oh, Lord, I give it up!" said Mr. Beresford.
neutral   His four days' imprisonment had taught him anew to value good food.
entailment   Sometimes it was too small, and sometimes too big, and sometimes not in the right place.
...
```

To run the code, execute the following command

```bash
cd EDA-Extended
python augment.py --input=<input file path>
```
The default output filename will have eda_ appended to the front of the input filename. However, you have the option to specify your own output filename using the --output parameter. Additionally, you can control the number of augmented sentences generated per original sentence by using the --num_aug parameter (default is 4).

Furthermore, you can adjust different alpha parameters that determine the percentage of words in the sentence to be changed according to specific augmentation rules. The alpha parameters for each method are as follows:

- Insertion: alpha_ri
- Deletion: alpha_rd
- Swapping: alpha_rs
- Synonym Replacement: alpha_sr

The default value for the alpha parameters is 0.1 which corresponds to 10%.

## References

[1] Wei, J., & Zou, K. (2019). EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks. [paper](https://arxiv.org/abs/1901.11196).\
[2] Unsupervised Data Augmentation for Consistency Training. Qizhe Xie, Zihang Dai, Eduard Hovy, Minh-Thang Luong, Quoc V. Le. 2020. [paper](https://arxiv.org/abs/1904.12848).\
[3] SSMBA: Self-Supervised Manifold Based Data Augmentation for Improving Out-of-Domain Robustness. Nathan Ng, Kyunghyun Cho, Marzyeh Ghassemi. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), November 2020. [Paper](https://aclanthology.org/2020.emnlp-main.97)



