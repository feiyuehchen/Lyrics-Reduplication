import string


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def is_reduplicate(text):
    text_list = text.replace("\n", " ").split(" ")
    if len(text_list) > 2:
        for i in range(len(text_list)-1):
            if text_list[i] == text_list[i+1]:
                return True
    return False

def find_reduplicate(text):
    sentences = remove_punctuation(text).split("\n")
    
    dup_set = set()
    for s in sentences:
        words = sentences.split(" ")
        if len(words) > 2:
            for i in range(len(words)-1):
                if words[i] == words[i+1]:
                    dup_set.add(words[i])

    return dup_set

def find_reduplicate_pos(text_pairs):
    
    dup_set = set()
    if len(text_pairs) > 2:
        for i in range(len(text_pairs)-1):
            if text_pairs[i][0] == text_pairs[i+1][0]:
                dup_set.add(text_pairs[i])
                dup_set.add(text_pairs[i+1])

    return dup_set