import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict


# text = "I really really really really like you"
text = "brian brian brian"
tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)

print(pos_tags)
