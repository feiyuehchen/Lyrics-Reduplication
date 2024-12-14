

MAX_TOKENS = 100
MODEL = "gpt-4o"
SYSTEM_PROMPT = "You are a helpful assistant."

OPENAI_BATCH_FORMAT = {"custom_id": None, 
    "method": "POST", 
    "url": "/v1/chat/completions", 
    "body": {"model": MODEL, 
            "messages": 
            [{"role": "system", "content": SYSTEM_PROMPT},  #SYSTEM_PROMPT
            {"role": "user", "content": None}],  # INSTRUCTION+QUESTION
                "max_tokens": MAX_TOKENS}}


import jsonlines
from copy import deepcopy

data_path = "dup_data.jsonl"
save_path = "gpt.jsonl"
output_json = []

with jsonlines.open(data_path, 'r') as f:
    for id, row in enumerate(f):
        template = deepcopy(OPENAI_BATCH_FORMAT)
        reduplication = row["duplicate"]
        lyrics = row["lyrics"]
        text = f"""Here are a list of words and a given context. Please classify each word and return in list format. An example would be given before the list and the context.
There are 9 choices for the word: 
a. noun
b. verb
c. adjective
d. adverb
e. pronoun
f. preposition
g. conjunction
h. interjection
i. determiner

Example:
Word List: please, now, me

Context:
In my place, in my place
Were lines that I couldn't change
I was lost, oh yeah
I was lost, I was lost
Crossed lines I shouldn't have crossed
I was lost, oh yeah
Yeah how long must you wait for it?
Yeah how long must you pay for it?
Yeah how long must you wait for it?
Oh for it
I was scared, I was scared
Tired and under prepared
But I wait for it
If you go, if you go
Leave me down here on my own
Then I'll wait for you (yeah)
Yeah how long must you wait for it?
Yeah how long must you pay for it?
Yeah how long must you wait for it?
Oh for it
Sing it, please, please, please
Come back and sing to me, to me, me
Come on and sing it out, now, now
Come on and sing it out, to me, me
Come back and sing it
In my place, in my place
Were lines that I couldn't change
And I was lost, oh yeah, oh yeah

Answer: 
h, d, e

Here's the list and the context. Please answer the question with the desired format.
Word List:
{reduplication}

Context:
{lyrics}

Answer:
"""
        template["custom_id"] = f"lyrics_{id}"
        template["body"]["messages"][1]["content"] = text
        output_json.append(template)
        


with jsonlines.open(save_path, 'w') as f:
    f.write_all(output_json)

