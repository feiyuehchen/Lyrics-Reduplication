import nltk
nltk.download('cmudict')
import json
from nltk.corpus import cmudict
pronouncing_dict = cmudict.dict()

def get_phenome(word, pronouncing_dict):
    phonemes = pronouncing_dict[word][0] 
    return phonemes

data_path = 'pos_dup_data.jsonl'
with open(data_path, 'r') as f:
    data = [json.loads(line) for line in f]




for row in data:
    # [["alina", "NN"], ["alina", "IN"], ["alina", "JJ"]]
    print(row["duplicate"])
    reduplication = list(set([text[0] for text in row["duplicate"]]))
    print(reduplication)

    a = [["alina", "NN"], ["alina", "IN"], ["alina", "JJ"]]
    reduplication = list(set([text[0] for text in a]))
    break