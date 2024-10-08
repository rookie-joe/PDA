'''
1. add 'model' label
2. merge
3. add UUID
4. save merge; filter pda_validity and save merge_annotation.
'''

import json
import uuid
import random

def add_model_key(file_path, model_value):
    # Load the contents of the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Add the "model" key to each sample
    for sample in data:
        sample['model'] = model_value
    
    # Save the modified data back to the JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def merge_json_files(file1, file2, output_file):
    # Load the contents of the first JSON file
    with open(file1, 'r') as f1:
        data1 = json.load(f1)
    
    # Load the contents of the second JSON file
    with open(file2, 'r') as f2:
        data2 = json.load(f2)
    
    # Merge the two lists
    merged_data = data1 + data2
    
    # Set a seed for the random number generator
    random.seed(42)

    # Add replicable UUIDs to each sample
    for i, sample in enumerate(merged_data):
        sample['uuid'] = str(uuid.UUID(int=random.getrandbits(128)))
    
    # Save the merged data to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

def create_annotated_json(input_file, output_file):
    # Load the contents of the merged JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # remove keys, add keys
    for sample in data:
        if 'pda_valid' in sample:
            del sample['pda_valid']
        if 'model' in sample:
            del sample['model']
        sample['human_eval_inform'], sample['human_eval_autoform'] = None, None
    # Save the annotated data to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Define the file paths
file1 = 'baseline.json'
file2 = 'enhanced.json'
merged_file = 'merged.json'
annotated_file = 'merge_annotate.json'

# Add the "model" key to each sample in the two files
add_model_key(file1, 'baseline')
add_model_key(file2, 'enhanced')

# Merge the JSON files and add UUIDs
merge_json_files(file1, file2, merged_file)

# Create the annotated JSON file
create_annotated_json(merged_file, annotated_file)

print(f"Merged data saved to {merged_file}")
print(f"Annotated data saved to {annotated_file}")