import sys
import json
import math
import nltk
import itertools

# sbp is the stupid backoff penalty = log(0.4). it's precoded here for efficiency
def lm_prob(ngram_dict, tags, sbp=-0.916290731874155):
    five_grams = [' '.join(ngram) for ngram in nltk.ngrams(tags, 5, pad_left=True, pad_symbol='<S>')]
    logprob = 0
    for g5 in five_grams: # need to lookup in the proper dictionary
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
                        logprob += sbp + sbp + sbp + math.log(ngram_dict['2'][g2] / ngram_dict['2'][g2[:g2.rfind(' ')]])
                    else:
                        g1 = g2[g2.find(' ')+1:]
                        if g1 in ngram_dict['1']:
                            logprob += sbp + sbp + sbp + sbp + math.log(ngram_dict[g1] / ngram_dict['NUM_TAGS'])
                        else:
                            print(g1 + ' not in ngram_dict')
    return logprob

def main():
    homophones = {'its', "it's", 'your', "you're", 'their', "they're", 'lose', 'loose', 'to', 'too',
                  'Its', "It's", 'Your', "You're", 'Their', "They're", 'Lose', 'Loose', 'To', 'Too'}

    flip = {'its':"it's", "it's":'its', 'your':"you're", "you're":'your', 'their':"they're", 
            'Its':"It's", "It's":'Its', 'Your':"You're", "You're":'Your', 'Their':"They're", 
            "they're":'their', 'lose':'loose', 'loose':'lose', 'to':'too', 'too':'to',
            "They're":'Their', 'Lose':'Loose', 'Loose':'Lose', 'To':'Too', 'Too':'To'}

    with open(sys.argv[1]) as modelfile:
        ngram_dict = json.load(modelfile)

    for line in sys.stdin:
        words = line.split()
        enum_words = list(enumerate(words))
        candi = [i for i, word in enum_words if word in homophones]

        if not candi:
            print(line)
            continue

        candidwords = [words[i], flip[words[i]] for i in candi]
        candidsets = itertools.product(*candidwords)    
        
        candidates = []
        for candidset in candidsets:
            cset = iter(candidset)
            new_candidate = words
            for i in candi:
                new_candidate[i] = next(cset)                                                
            candidates.append(' '.join(new_candidate)) # TODO: TEST THIS LOOP

        cand_probs= [(sentence, lm_prob(ngram_dict, [token[1] for token in nltk.pos_tag(nltk.word_tokenize(sentence))])) for sentence in candidates]
        print(max(cand_probs, key=lambda x: x[1])[0])
        
if __name__ == '__main__':
    main()
