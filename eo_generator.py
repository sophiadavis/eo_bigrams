"""
A program to generate a sentence using bigram probabilities calculated from a text,
and stored using the Pickle library.

Sophia Davis, 3/22/2014
"""
import pickle
import sys
import random

def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python ' + sys.argv[0] + ' word_to_match bigram_model_file\n')
		sys.exit(1)
	else:
		bigram_probs = pickle.load(open(sys.argv[2], 'r'))
		start_word = sys.argv[1].lower()
		line = generate_line(start_word, bigram_probs)
		
		# format end of sentence
		if len(line) > 0:
			if line[len(line) - 1] not in [".", "?", "!"]:
				line = line + '.'
			else:
				line = line[0:len(line) - 2] + line[len(line) - 1]
			print line.capitalize()
			
def generate_line(start_word, bigram_probs):
	current = start_word
	if current not in bigram_probs:
		print "Please select another word."
		return ''
	sentence = current
	length = 1
	
	# continue adding to sentence until model suggests sentence-ending punctuation
	# or limit to 10 words
	while (length < 10) and (current not in [".", "?", "!"]):
		
		# return current sentence if next word doesn't occur in text (just in case)
		if current not in bigram_probs:
			return sentence
		
		curr_dict = bigram_probs[current]
		
		# select next word
		cut_pt = random.random()
		sum = 0.0
		next_words = curr_dict.keys()
		i = 0
		while sum < cut_pt:
			sum += curr_dict[next_words[i]]
			i += 1
		current = next_words[i - 1]
		sentence = sentence + ' ' + current
		length += 1
	
	return sentence
			
if __name__ == "__main__":
	main()