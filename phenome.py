import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict





pronouncing_dict = cmudict.dict()
word = "hello"
phonemes = pronouncing_dict[word][0]  # Get the first pronunciation
print(phonemes)  # Output: ['HH', 'AH', 'L', 'OW']