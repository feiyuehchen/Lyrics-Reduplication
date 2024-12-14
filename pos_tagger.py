import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

import jsonlines
import json
from tqdm import tqdm
from utils import (remove_punctuation, 
                   is_reduplicate, 
                   find_reduplicate_pos)



def get_reduplicate_pos(lyrics):

    text = remove_punctuation(lyrics)
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)


    dup_set = find_reduplicate_pos(pos_tags)

    return dup_set

data_path = 'data.jsonl'
with open(data_path, 'r') as f:
    data = [json.loads(line) for line in f]

output_path = "pos_dup_data.jsonl"
output_list = []
for row in tqdm(data):
    dup_list = list(get_reduplicate_pos(row["lyrics"]))
    if dup_list:
        row["duplicate"] = list(get_reduplicate_pos(row["lyrics"]))
        output_list.append(row)

with open(output_path, 'w') as f:
    for record in output_list:
        f.write(json.dumps(record) + '\n')




