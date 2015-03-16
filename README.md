## Explanation of approach

My approach is n-gram language modeling of the part-of-speech tags.

I convert the data into its part-of-speech tags, then apply n-gram language modeling to obtain the probability of a given sentence.

So, for a sentence containing x homophones, I'll do the following:
1. Create 2^x candidate sentences (if x > 6 we do not generate all 2^x candidate sentences)
2. POS-tag each of the candidate sentences
3. Run n-gram language model on each sentence to get its probability. (NOTE: I am using the "Stupid-Backoff" model in order to deal with unseen n-grams. This applies a fixed penalty of 0.4 to the probability and then searches for the corresponding n-1-gram.)
4. Return the sentence which has highest probability.

## How to run the code

To run ngram_train.py, do `python3 ngram_train.py <modelfile>`. 

This uses a fixed directory of corpus data. The program will POS-tag all of the data and then store the counts of all n-grams up to n=5 in the given `<modelfile>`.

To run grammar_correction.py, do `cat <testfile> | python3 grammar_correction.py <modelfile> <outputfile> <auxfile>`.

The program will apply the aforementioned methodology in order to correct any of the homophone errors that we are looking for. The corrected file is output as `<outputfile>`. (`<auxfile>` is just a logging file with miscellaneous information from the run of the program. It can safely be ignored.)

## Third-party software used

I used the nltk 3.0 library in order to perform sentence tokenization on the training data, as well as word tokenization, part-of-speech tagging, and n-gram generation on both the training and the test data.

## Other relevant information

I used some of the corpus data provided by nltk such as the Reuters dataset as well as a few of the books found in the Gutenberg dataset.