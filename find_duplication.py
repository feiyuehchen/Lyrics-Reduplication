import jsonlines
import json
from tqdm import tqdm
import string
data_path = "data.jsonl"



def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def is_duplicate(text):
    text_list = text.replace("\n", " ").split(" ")
    if len(text_list) > 2:
        for i in range(len(text_list)-1):
            if text_list[i] == text_list[i+1]:
                return True
    return False


def find_duplicate(text):
    text_list = remove_punctuation(text).replace("\n", " ").split(" ")
    dup_set = set()
    if len(text_list) > 2:
        for i in range(len(text_list)-1):
            if text_list[i] == text_list[i+1]:
                dup_set.add(text_list[i])

    return dup_set



output_path = "dup_data.jsonl"
output_list = []
with jsonlines.open(data_path) as reader:
    for row in tqdm(reader):     
        if is_duplicate(row["lyrics"]):
            row["duplicate"] = list(find_duplicate(row["lyrics"]))
            output_list.append(row)

with open(output_path, 'w') as f:
    for record in output_list:
        f.write(json.dumps(record) + '\n')




