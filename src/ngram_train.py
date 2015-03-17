import os
import sys
import json
import nltk
import datetime
import itertools

def extract_document(filename):
    with open('../data/reuters/EncartaUnzipped/'+filename, errors='ignore') as curfile:
        return(curfile.read().replace('\n', ' '))

def update_dict(dictionary, key, gram):
    if gram not in dictionary[key]:
        dictionary[key][gram] = 1
    else:
        dictionary[key][gram] += 1

def main():
    print('starting at ' + str(datetime.datetime.now()))
    documents = (extract_document(filename) for filename in os.listdir('../data/reuters/EncartaUnzipped'))
    # NOTE: I am ripping off the first two sentences here because of Reuters dataset as well as Encarta dataset
    sentences = itertools.chain.from_iterable(nltk.sent_tokenize(document)[2:] for document in documents)

    print('starting pos_tagging at ' + str(datetime.datetime.now()))
    tag_sents = [[token[1] for token in nltk.pos_tag(nltk.word_tokenize(sentence))] for sentence in sentences]
    num_sents = len(tag_sents)

    print('starting to generate ngrams at ' + str(datetime.datetime.now()))
    all_1_grams = itertools.chain.from_iterable(tag_sents)
    all_2_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 2, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)
    all_3_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 3, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)
    all_4_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 4, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)
    all_5_grams = itertools.chain.from_iterable(nltk.ngrams(tag_sent, 5, pad_left=True, pad_symbol='<S>') for tag_sent in tag_sents)

    print('starting to update ngram dict at ' + str(datetime.datetime.now()))
    ngram_dict = { '1': {}, '2': {}, '3': {}, '4': {}, '5': {}, 'NUM_TAGS': 0 }

    ngram_dict['1']['<S>'] = num_sents * 4
    ngram_dict['2']['<S> <S>'] = num_sents * 3
    ngram_dict['3']['<S> <S> <S>'] = num_sents * 2
    ngram_dict['4']['<S> <S> <S> <S>'] = num_sents

    for unigram in all_1_grams:
        update_dict(ngram_dict, '1', unigram)
        ngram_dict['NUM_TAGS'] +=1

    for bigram in all_2_grams:
        update_dict(ngram_dict, '2', ' '.join(bigram))

    for trigram in all_3_grams:
        update_dict(ngram_dict, '3', ' '.join(trigram))

    for quadrigram in all_4_grams:
        update_dict(ngram_dict, '4', ' '.join(quadrigram))

    for pentagram in all_5_grams:
        update_dict(ngram_dict, '5', ' '.join(pentagram))

    print('starting to serialize ngram dict at ' + str(datetime.datetime.now()))
    with open(sys.argv[1], 'w') as modelfile:
        json.dump(ngram_dict, modelfile)
    print('complete at ' + str(datetime.datetime.now()))

if __name__ == '__main__':
    main()
