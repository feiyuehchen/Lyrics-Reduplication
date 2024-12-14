from openai import OpenAI
import yaml
import pandas as pd
import os

data_path = "gpt1.jsonl"

cred_path = "creds.yaml"
with open(cred_path, 'r') as f:
    creds = yaml.safe_load(f)


os.environ["OPENAI_API_KEY"] = creds["OPENAI_API_KEY"]


client = OpenAI()

batch_input_file = client.files.create(
  file=open(data_path, "rb"),
  purpose="batch"
)

# batch_output_file = client.files.create(
#   file=open("batch_output.jsonl"),
#   purpose="batch"
# )

batch_input_file_id = batch_input_file.id
print(batch_input_file_id)
Batch = client.batches.create(
    input_file_id=batch_input_file_id,
    # output_file_id=batch_output_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)


