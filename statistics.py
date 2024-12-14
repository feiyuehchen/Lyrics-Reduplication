# type: ignore
import json
from tqdm import tqdm
import matplotlib.pyplot as plt

data_path = 'pos_dup_data.jsonl'
with open(data_path, 'r') as f:
    data = [json.loads(line) for line in f]

pos_dict = {}
different_pos_dict = {}

def check_reduplicate (row, reduplicate_column="duplicate"):
    for word, pos in row[reduplicate_column]:
        same_dict = {}
        if pos in pos_dict:
            pos_dict[pos] += 1
        else:
            pos_dict[pos] = 1
        if word in same_dict:
            same_dict[word].add(pos)
        else:
            same_dict[word] = set(pos)
        
        for _, item in same_dict.items():
            if len(item) in different_pos_dict:
                different_pos_dict[len(item)] += 1
            else:
                different_pos_dict[len(item)] = 1

     

for row in tqdm(data):
    check_reduplicate(row)

total = 0
for key, value in pos_dict.items():
    total += value

print(total)
print(pos_dict)
print(different_pos_dict)

# Plot for POS tags
plt.figure(figsize=(12, 6))
plt.bar(pos_dict.keys(), pos_dict.values(), color='blue', alpha=0.7)
plt.title('Part-of-Speech (POS) Tags Distribution', fontsize=14)
plt.xlabel('POS Tags', fontsize=12)
plt.ylabel('Counts', fontsize=12)
plt.xticks(rotation=90)
plt.savefig('pos_tag.png')

# Plot for n-grams
plt.figure(figsize=(8, 5))
plt.bar(different_pos_dict.keys(), different_pos_dict.values(), color='green', alpha=0.7)
plt.title('Number of words with different POS in the dataset', fontsize=14)
plt.xlabel('POS counts', fontsize=12)
plt.ylabel('Counts', fontsize=12)
plt.xticks([1, 2, 3], ['1', '2', '3'])
plt.savefig('number_tag.png')
