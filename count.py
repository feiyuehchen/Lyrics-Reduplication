import jsonlines
from tqdm import tqdm

data_path1 = "gpt_response_1.jsonl"
data_path2 = "gpt_response_2.jsonl"

choices = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

c = {
    "a": 0,
    "b": 0,
    "c": 0, 
    "d": 0,
    "e": 0,
    "f": 0,
    "g": 0,
    "h": 0,
    "i": 0,
    "total": 0
}

stat = {
    "success": 0,
    "error": 0,
    "total": 0
}

def count_choices(text_list):
    for t in text_list:
        c["total"] += 1
        c[t] += 1



def clean_text(text):
    stat["total"] += 1
    text_list = text.replace("[", "").replace("]", "").replace(" ", "").replace("Answer: ", "").split(",")
    # print(text_list)
    if len(text_list) == 0:
        stat["total"] += 1
        return ""

    for t in text_list:
        if t not in choices:
            stat["error"] += 1
            return ""
    
    stat["success"] += 1
    count_choices(text_list)
    return text_list


    

data = []

def process_data(data_path):

    with jsonlines.open(data_path, 'r') as f:
        for row in tqdm(f):
            response = row["response"]["body"]["choices"][0]["message"]["content"]
            # print(response)
            response = clean_text(response)
            
            data.append({
                "custom_id": row["custom_id"], 
                "response": row["response"]["body"]["choices"][0]["message"]["content"]
            })
            # break

process_data(data_path1)
process_data(data_path2)
# print(data)
print(c)
print(stat)