import pandas as pd
import os
from tqdm import tqdm
import json

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

from multiprocessing import Pool, cpu_count

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

import string
DetectorFactory.seed = 0

az_dir = "data/azlyrics-scraper/"
metro_path = "data/lyrics.csv"

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def get_uniqueness(data):
    df = pd.DataFrame(data)
    # Group the songs by artist and calculate pairwise similarities within each group
    artist_groups = df.groupby('artist')
    similarity_results = []

    for artist, group in tqdm(artist_groups):
        lyrics = group['lyrics'].tolist()

        for i in range(len(lyrics)):
            for j in range(len(lyrics)):
                if i != j:  # Skip self-comparisons
                    set_1 = set(remove_punctuation(lyrics[i]).split(" "))  # Split into words and convert to set
                    set_2 = set(remove_punctuation(lyrics[j]).split(" "))  # Split into words and convert to set
                    intersection = len(set_1 & set_2)
                    union = len(set_1 | set_2)
                    sim = intersection / union if union != 0 else 0  # Jaccard similarity
                    
                    if sim < 0.9:  # Filter threshold
                        similarity_results.append({
                            "artist": artist,
                            "song_1": lyrics[i],
                            "song_2": lyrics[j],
                            "similarity": sim
                        })

    similarity_df = pd.DataFrame(similarity_results)
    unique_pairs = similarity_df[
        similarity_df.apply(lambda row: tuple(sorted([row["song_1"], row["song_2"]])), axis=1).duplicated(keep='first') == False
    ]

    # Format as original JSON structure (artist and lyrics only)
    unique_rows = unique_pairs[['artist', 'song_1']].rename(columns={'song_1': 'lyrics'}).drop_duplicates()

    # Convert back to JSONL format
    unique_jsonl = unique_rows.to_dict(orient='records')

    return unique_jsonl

def is_english(text):
    try:
        # Detect the language of the text
        return detect(text) == 'en'
    except LangDetectException:
        # In case of any detection failure, treat it as non-English (or handle as needed)
        return False
    

def merge_df(csv_dir):
    output_df = []
    for csv_name in os.listdir(csv_dir):
        csv_path = os.path.join(csv_dir, csv_name)
        df = pd.read_csv(csv_path, on_bad_lines="skip")
        output_df.append(df)
    
    output_df = pd.concat(output_df, ignore_index=True)
    # If needed, you can save the merged DataFrame to a new CSV file
    output_df.to_csv('az_merged.csv', index=False)
    return output_df

def clean_metro(csv_path):
    df = pd.read_csv(csv_path, on_bad_lines="skip")

    for i, row in tqdm(df.iterrows()):
        # Concatenate all values from columns 6 onward, joining them with '\n'
        additional_data = '\n'.join(row.iloc[6:].dropna().astype(str))

        # Add this concatenated string to column 5
        df.at[i, df.columns[5]] = f"{row.iloc[5]}{('\n' + additional_data if additional_data else '')}"

        # Optionally drop or nullify the additional columns if no longer needed
        # df.iloc[i, 5:] = None


    # If necessary, drop the additional columns entirely
    output_df = df.iloc[:, :6]
    output_df.to_csv('metro.csv', index=False)
    return output_df

def merge_df(a, m):
    # print(len(a)+len(m))

    # a = a.rename(columns={'LYRICS': 'lyrics', 'ARTIST_NAME':'artist'}).to_dict(orient='records')
    # # Convert DataFrames to dictionaries
    # m = m.to_dict(orient='records')

    # # Merge dictionaries on 'lyrics'
    # merged_dict = {}
    # for df in [m,a]:
    #     for item in tqdm(df):
    #         lyrics = str(item['lyrics'])
    #         if is_english(lyrics):
    #             merged_dict[lyrics] = {
    #                 'artist': item['artist'],
    #                 'lyrics': item['lyrics']
    #             }

    # # Removing duplicates and preparing for JSONL
    # en_records = list(merged_dict.values())
    # jsonl_file = 'en_data.jsonl'
    # with open(jsonl_file, 'w') as f:
    #     for record in en_records:
    #         f.write(json.dumps(record) + '\n')

    jsonl_file = 'en_data.jsonl'
    with open(jsonl_file, 'r') as f:
        en_records = [json.loads(line) for line in f]

    unique_en_records = get_uniqueness(en_records)

    # Write to JSON Lines file
    jsonl_file = 'data.jsonl'
    with open(jsonl_file, 'w') as f:
        for record in unique_en_records:
            f.write(json.dumps(record) + '\n')



# merge_df(az_dir)

# clean_metro(metro_path)

a_path = 'az_merged.csv'
m_path = 'metro.csv'

a = pd.read_csv(a_path)
print(len(a))
m = pd.read_csv(m_path)
print(len(m))
merge_df(a,m)