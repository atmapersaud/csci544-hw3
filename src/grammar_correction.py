import sys
import json
import math
import nltk
import datetime
import functools
import itertools

# sbp is the stupid backoff penalty = log(0.4). it's precoded here for efficiency
def lm_prob(ngram_dict, tags, sbp=-0.916290731874155):
    five_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 5, pad_left=True, pad_symbol='<S>')]
    logprob = 0
    for g5 in five_grams: 
        if g5 in ngram_dict['5']:
            logprob += math.log(ngram_dict['5'][g5] / ngram_dict['4'][g5[:g5.rfind(' ')]])
        else: 
            g4 = g5[g5.find(' ')+1:]
            if g4 in ngram_dict['4']:
                logprob += sbp + math.log(ngram_dict['4'][g4] / ngram_dict['3'][g4[:g4.rfind(' ')]])
            else:
                g3 = g4[g4.find(' ')+1:]
                if g3 in ngram_dict['3']:
                    logprob += sbp + sbp + math.log(ngram_dict['3'][g3] / ngram_dict['2'][g3[:g3.rfind(' ')]])
                else:
                    g2 = g3[g3.find(' ')+1:]
                    if g2 in ngram_dict['2']:
                        logprob += sbp + sbp + sbp + math.log(ngram_dict['2'][g2] / ngram_dict['1'][g2[:g2.rfind(' ')]])
                    else:
                        g1 = g2[g2.find(' ')+1:]
                        if g1 in ngram_dict['1']:
                            logprob += sbp + sbp + sbp + sbp + math.log(ngram_dict['1'][g1] / ngram_dict['NUM_TAGS'])
                        else:
                            print(g1 + ' not in ngram_dict')
    return logprob

def lm_prob4(ngram_dict, tags, sbp=-0.916290731874155):
    four_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 4, pad_left=True, pad_symbol='<S>')]
    logprob = 0
    for g4 in four_grams: 
        if g4 in ngram_dict['4']:
            logprob += math.log(ngram_dict['4'][g4] / ngram_dict['3'][g4[:g4.rfind(' ')]])
        else:
            g3 = g4[g4.find(' ')+1:]
            if g3 in ngram_dict['3']:
                logprob += sbp + math.log(ngram_dict['3'][g3] / ngram_dict['2'][g3[:g3.rfind(' ')]])
            else:
                g2 = g3[g3.find(' ')+1:]
                if g2 in ngram_dict['2']:
                    logprob += sbp + sbp + math.log(ngram_dict['2'][g2] / ngram_dict['1'][g2[:g2.rfind(' ')]])
                else:
                    g1 = g2[g2.find(' ')+1:]
                    if g1 in ngram_dict['1']:
                        logprob += sbp + sbp + sbp + math.log(ngram_dict['1'][g1] / ngram_dict['NUM_TAGS'])
                    else:
                        print(g1 + ' not in ngram_dict')
    return logprob

def lm_prob3(ngram_dict, tags, sbp=-0.916290731874155):
    three_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 3, pad_left=True, pad_symbol='<S>')]
    logprob = 0
    for g3 in three_grams: 
        if g3 in ngram_dict['3']:
            logprob += math.log(ngram_dict['3'][g3] / ngram_dict['2'][g3[:g3.rfind(' ')]])
        else:
            g2 = g3[g3.find(' ')+1:]
            if g2 in ngram_dict['2']:
                logprob += sbp + math.log(ngram_dict['2'][g2] / ngram_dict['1'][g2[:g2.rfind(' ')]])
            else:
                g1 = g2[g2.find(' ')+1:]
                if g1 in ngram_dict['1']:
                    logprob += sbp + sbp + math.log(ngram_dict['1'][g1] / ngram_dict['NUM_TAGS'])
                else:
                    print(g1 + ' not in ngram_dict')
    return logprob

def lm_prob2(ngram_dict, tags, sbp=-0.916290731874155):
    bigrams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 2, pad_left=True, pad_symbol='<S>')]
    logprob = 0
    for g2 in bigrams: 
        if g2 in ngram_dict['2']:
            logprob += sbp + math.log(ngram_dict['2'][g2] / ngram_dict['1'][g2[:g2.rfind(' ')]])
        else:
            g1 = g2[g2.find(' ')+1:]
            if g1 in ngram_dict['1']:
                logprob += sbp + sbp + math.log(ngram_dict['1'][g1] / ngram_dict['NUM_TAGS'])
            else:
                print(g1 + ' not in ngram_dict')
    return logprob

def laplace5g(ngram_dict, tags):
    five_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 5, pad_left=True, pad_symbol='<S>')]
    counts = [ngram_dict['5'][g5] + 1 if g5 in ngram_dict['5'] else 1 for g5 in five_grams]

    four_grams = [g5[:g5.rfind(' ')] for g5 in five_grams]
    denoms = [ngram_dict['4'][g4] + ngram_dict['VOCAB'] if g4 in ngram_dict['4'] else ngram_dict['VOCAB'] for g4 in four_grams]

    logprobs = [math.log(counts[i]/denoms[i]) for i, item in enumerate(counts)]
    return sum(logprobs)

def laplace4g(ngram_dict, tags):
    four_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 4, pad_left=True, pad_symbol='<S>')]
    counts = [ngram_dict['4'][g4] + 1 if g4 in ngram_dict['4'] else 1 for g4 in four_grams]

    three_grams = [g4[:g4.rfind(' ')] for g4 in four_grams]
    denoms = [ngram_dict['3'][g3] + ngram_dict['VOCAB'] if g3 in ngram_dict['3'] else ngram_dict['VOCAB'] for g3 in three_grams]

    logprobs = [math.log(counts[i]/denoms[i]) for i, item in enumerate(counts)]
    return sum(logprobs)

def laplace3g(ngram_dict, tags):
    three_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 3, pad_left=True, pad_symbol='<S>')]
    counts = [ngram_dict['3'][g3] + 1 if g3 in ngram_dict['3'] else 1 for g3 in three_grams]

    two_grams = [g3[:g3.rfind(' ')] for g3 in three_grams]
    denoms = [ngram_dict['2'][g2] + ngram_dict['VOCAB'] if g2 in ngram_dict['2'] else ngram_dict['VOCAB'] for g2 in two_grams]

    logprobs = [math.log(counts[i]/denoms[i]) for i, item in enumerate(counts)]
    return sum(logprobs)

def main():
    homophones = {'its', "it's", 'your', "you're", 'their', "they're", 'lose', 'loose', 'to', 'too',
                  'Its', "It's", 'Your', "You're", 'Their', "They're", 'Lose', 'Loose', 'To', 'Too'}

    flip = {'its':"it's", "it's":'its', 'your':"you're", "you're":'your', 'their':"they're", 
            'Its':"It's", "It's":'Its', 'Your':"You're", "You're":'Your', 'Their':"They're", 
            "they're":'their', 'lose':'loose', 'loose':'lose', 'to':'too', 'too':'to',
            "They're":'Their', 'Lose':'Loose', 'Loose':'Lose', 'To':'Too', 'Too':'To'}

    with open(sys.argv[1]) as modelfile:
        ngram_dict = json.load(modelfile)

    vocab = len(ngram_dict['1'])
    #print('vocab size is ' + str(vocab))
    ngram_dict['VOCAB'] = vocab

    outfile = open(sys.argv[2], 'w')
    #auxfile = open(sys.argv[3], 'w')

    counter = 0

    for line in sys.stdin:
        counter += 1
        if counter % 1000 == 0:
            print('processed ' + str(counter) + ' lines at ' + str(datetime.datetime.now()))

        words = line.split()

        if not words:
            outfile.write(line)
            #print()
            continue

        enum_words = list(enumerate(words))
        candi = [i for i, word in enum_words if word in homophones]

        if not candi:
            outfile.write(line)
            #print(line)
            continue

        if len(candi) > 6:
            outfile.write(line)
            #auxfile.write(line)
            continue
            
        candidwords = [(words[i], flip[words[i]]) for i in candi]
        candidsets = itertools.product(*candidwords)    
        
        candidates = []
        for candidset in candidsets:
            cset = iter(candidset)
            new_candidate = words
            for i in candi:
                new_candidate[i] = next(cset)                                                
            candidates.append(' '.join(new_candidate)) # TODO: TEST THIS LOOP

        cand_probs= [(sentence, lm_prob3(ngram_dict, [token[1] for token in nltk.pos_tag(nltk.word_tokenize(sentence))])) for sentence in candidates]
        outfile.write(max(cand_probs, key=lambda x: x[1])[0] + '\n')
        #print(max(cand_probs, key=lambda x: x[1])[0])
    
    outfile.close()
    #auxfile.close()
        
if __name__ == '__main__':
    main()
