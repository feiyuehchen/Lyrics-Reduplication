
def split_jsonl(file_path, output1, output2):
    """
    Splits a JSONL file into two parts: first half and latter half.
    
    Parameters:
        file_path (str): Path to the input JSONL file.
        output1 (str): Path to the first output JSONL file (first half).
        output2 (str): Path to the second output JSONL file (latter half).
    """
    try:
        # Read all lines from the input JSONL file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Calculate the midpoint
        midpoint = len(lines) // 1000
        
        # Write the first half to the first output file
        with open(output1, 'w') as file1:
            file1.writelines(lines[:midpoint])
        
        # Write the latter half to the second output file
        with open(output2, 'w') as file2:
            file2.writelines(lines[midpoint:])
        
        print(f"File split successfully! First half saved to {output1}, latter half saved to {output2}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
# split_jsonl('input.jsonl', 'output_first_half.jsonl

# split_jsonl("gpt.jsonl", "gpt1.jsonl", "gpt2.jsonl")
split_jsonl("en_data.jsonl", "e1.jsonl", "e2.jsonl")