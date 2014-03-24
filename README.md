eo_bigrams
==========


eo_model.py -- removes formatting and calculates bigram probabilities from a given text, 
saving the model as a Pickle file. Tailored to Charles Johnston's translation of Pushkin's 
Evgenii Onegin, from http://lib.ru/LITRA/PUSHKIN/ENGLISH/onegin_j.txt.


eo_generator.py -- uses the Pickle file of bigram probabilities to generate a short Pushkin-y 
sentence, starting with a word chosen by the user.
