"""
A program to generate a bigram language model of a text, and store it using the Pickle library.
This approach should work on any text, however, I use regex patterns to remove formatting 
specific to Charles Johnston's translation of Evgenii Onegin
(http://lib.ru/LITRA/PUSHKIN/ENGLISH/onegin_j.txt).

Regex for matching Roman numerals from:
http://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression

Sophia Davis, 3/22/2014
"""
import pickle
import sys
import re

def main():
	if len(sys.argv) < 2:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' filename.txt\n')
		sys.exit(1)
	else:
		print "Saving bigram probabilities to model.dat"
		text = ''
		
		f = open(sys.argv[1], 'r')
		for word in f.readlines()[2:]:
			text = text + word + " "
		f.close()
		
		text = text.split(' ')
		word_list = clean(text)
		
		bigram_cts = get_bigram_counts(word_list)
		bigram_probs = get_bigram_probs(bigram_cts)
		# print bigram_probs
		pickle.dump(bigram_probs, open('model.dat', 'w'))
			
		
""" 
Removes text formatting, returns list of individual word/punctuation units.
"""
def clean(text):
	word_list = []

	for token in text:
		# strip formatting
		token = re.sub(r"``", "", token) # quotes
		token = re.sub(r"''", "", token) # quotes
		token = re.sub(r"\n", "", token) # newlines
		token = re.sub(r"\t", "", token) # tabs
		token = re.sub(r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", "", token) # Roman numerals
		token = re.sub(r"{(.*)}", "", token) # page/line markers
		token = re.sub(r"\d{0,2}", "", token) # footnote numbering
		token = re.sub(r",|(\()|(\))|--|:|;", r"", token) # inline punctuation
		
		# preserve sentence-ending punctuation as separate token
		token = re.sub(r"(.*)((\.)|(\?)|(\!))", r"\g<1> \g<2>", token)
		for el in token.split(" "):
			if el == '':
				continue
			else:
				word_list.append(el.lower())
	
	return word_list

def get_bigram_counts(word_list):
	bigram_cts = {}
	for i in xrange(0, len(word_list) - 1):
		if word_list[i] in bigram_cts:
			known_bigrams = bigram_cts[word_list[i]]
			if word_list[i + 1] in known_bigrams:
				known_bigrams[word_list[i + 1]] += 1.0
			else:
				known_bigrams[word_list[i + 1]] = 1.0
		else:
			bigram_cts[word_list[i]] = {word_list[i + 1] : 1.0}
		
	return bigram_cts
	
def get_bigram_probs(bigram_cts):
    bigram_probs = {}
    for first_word in bigram_cts:
        count = 0.0
        bigram_probs[first_word] = {}
        known_bigrams = bigram_cts[first_word]
        for next_word in known_bigrams:
            count += known_bigrams[next_word] # sum up total appearances of first word
        for next_word in known_bigrams:
            bigram_probs[first_word][next_word] = known_bigrams[next_word]/count
    
    return bigram_probs
    
if __name__ == "__main__":
	main()