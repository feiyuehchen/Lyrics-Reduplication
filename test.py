import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict


text = "I really really really really like you"
tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)

print(pos_tags)
