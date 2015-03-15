import os
import sys
import json
import nltk
import itertools

def extract_document(filename):
    with open('../data/lre7/'+filename) as curfile:
        return(curfile.read().replace('\n', ' '))

def update_dict(dictionary, key, gram):
    if gram not in dictionary[key]:
        dictionary[key][gram] = 1
    else:
        dictionary[key][gram] += 1

def main():
    documents = (extract_document(filename) for filename in os.listdir('../data/lre7'))
    sentences = itertools.chain.from_iterable(nltk.sent_tokenize(document) for document in documents)

    # NOTE: I am ripping off the first sentence here because of Reuters dataset
    tag_sents = [[token[1] for token in nltk.pos_tag(nltk.word_tokenize(sentence))[1:]] for sentence in sentences]

    all_1_grams = itertools.chain.from_iterable(tag_sents)
    all_2_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 2, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)
    all_3_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 3, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)
    all_4_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 4, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)
    all_5_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 5, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)

    ngram_dict = { '1': {}, '2': {}, '3': {}, '4': {}, 5: {}, 'NUM_TAGS': 0 }

    for unigram in all_1_grams:
        update_dict(ngram_dict, 1, unigram)
        ngram_dict['NUM_TAGS'] +=1

    for bigram in all_2_grams:
        update_dict(ngram_dict, 2, ' '.join(bigram))

    for trigram in all_3_grams:
        update_dict(ngram_dict, 3, ' '.join(trigram))

    for quadrigram in all_4_grams:
        update_dict(ngram_dict, 4, ' '.join(quadrigram))

    for pentagram in all_5_grams:
        update_dict(ngram_dict, 5, ' '.join(pentagram))

    with open(sys.argv[1], 'w') as modelfile:
        json.dump(ngram_dict, modelfile)

if __name__ == '__main__':
    main()
