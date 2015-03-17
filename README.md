## Explanation of approach

My approach is n-gram language modeling of the part-of-speech tags. (I trained my model with the ability to do 5-gram language modeling, but I obtained better results using 3-gram language modeling, so I used that for my final output.)

I convert the data into its part-of-speech tags, then apply n-gram language modeling to obtain the probability of a given sentence.

So, for a sentence containing x homophones, I'll do the following:

1. Create 2^x candidate sentences (the maximum number of candidates we will consider for a given line is 2^6)
2. POS-tag each of the candidate sentences
3. Run n-gram language model on each sentence to get its probability. (NOTE: I am using the "Stupid-Backoff" model in order to deal with unseen n-grams. This applies a fixed penalty of 0.4 to the probability and then searches for the corresponding n-1-gram.)
4. Return the sentence which has highest probability.

### Why?

I chose language models because it seemed to be the most logical and natural fit (to me) for this task. I wanted to be able to compare the probabilities of making a homophone correction vs not making that correction.

I chose to model only the POS tags to solve the data sparsity problem. I noticed that each of the homophones we are working with has a different part of speech tag than its counterpart. "Its", "your", and "their" are all possessive pronouns, while "it's", "you're" and "they're" are all personal pronouns followed by a verb. "Too" is an adverb while "to" is just "to" (using the Penn Treebank P.O.S. tagging system). "Loose" is an adjective (except in situations such as when it is following "let") while "lose" is a verb.

So, I figured I could cut down the total vocabulary to hundreds of thousands or possibly millions of words down to around 40 part of speech tags, without losing much information for this task. This way I could train with less data than you would need to train with if you were language modeling the words themselves.

## How to run the code

To run ngram_train.py, do `python3 ngram_train.py <modelfile>`. 

This uses a fixed directory of corpus data. The program will POS-tag all of the data and then store the counts of all n-grams up to n=5 in the given `<modelfile>`.

To run grammar_correction.py, do `cat <testfile> | python3 grammar_correction.py <modelfile> <outputfile>`.

The program will apply the aforementioned methodology in order to correct any of the homophone errors that we are looking for. The corrected file is output as `<outputfile>`.

## Third-party software used

I used the nltk 3.0 library in order to perform sentence tokenization on the training data, as well as word tokenization, part-of-speech tagging, and n-gram generation on both the training and the test data.

## Other relevant information
I used a Microsoft Encarta 1997 dataset (~87 MB) as well as some of the corpus data provided by nltk such as the Reuters dataset (~10 MB) and a few of the books found in the Gutenberg dataset (~5 MB).

# Development Set Results
##### correct homophones: 22783
##### total homophones: 25218
##### accuracy: 0.9034419858830993

##### correct changes: 6679
##### required changes: 7398
##### recall: 0.9028115706947824

##### correct changes: 6679
##### total changes: 8395
##### precision: 0.7955926146515783

##### f-score: 0.8458177673652884
