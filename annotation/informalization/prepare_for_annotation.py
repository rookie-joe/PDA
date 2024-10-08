import json
import os

# Function to add new items to each sample in the JSON data
def add_items_to_samples(json_data):
    for sample in json_data:
        sample['informalization_success'] = None
        sample['informal_proof_correctness'] = None
        sample['model_preference'] = None
    return json_data

# List of input and output file pairs
file_pairs = [
    ('gemini_sample10.json', 'gemini_sample10_annotation.json'),
    ('gpt4o_sample10.json', 'gpt4o_sample10_annotation.json'),
    ('train_gemini_sample10.json', 'train_gemini_sample10_annotate.json'),
]

# Directory where the input files are located
input_dir = './output_to_be_annotated'

# Directory where the output files will be saved
output_dir = './output_to_be_annotated'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

for input_file, output_file in file_pairs:
    # Construct full paths for input and output files
    input_path = os.path.join(input_dir, input_file)
    output_path = os.path.join(output_dir, output_file)

    # Read the original JSON file
    with open(input_path, 'r') as file:
        data = json.load(file)

    # Add the new items to each sample
    updated_data = add_items_to_samples(data)

    # Write the updated data to a new JSON file
    with open(output_path, 'w') as file:
        json.dump(updated_data, file, indent=4)

    print(f"Updated JSON data has been written to {output_path}")