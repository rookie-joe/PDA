'''
This script preprocesses the FORML4 dataset by:
1. filtering all samples with '.mk' in the theorem statement ('train' 'basic_test', 'random_test').
2. filtering all samples with 'python' in the natural language statement ('real_test').
'''

import json

def filter_custom_lemma(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Filter out samples with '.mk' in the 'output'
    filtered_data = [sample for sample in data if '.mk' not in sample['output']]

    # Count the number of filtered samples
    filtered_count = len(data) - len(filtered_data)

    # Write the filtered data to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)

    return filtered_count

def filter_python(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Filter out samples with 'python' in the 'input'
    filtered_data = [sample for sample in data if 'python' not in sample['input']]

    # Count the number of filtered samples
    filtered_count = len(data) - len(filtered_data)

    # Write the filtered data to a new JSON file
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)

    return filtered_count

# Process 'real_test' dataset
real_test_filtered_count = filter_python('../../data/real_test.json', '../../data/filtered_real_test.json')
print(f"Filtered {real_test_filtered_count} samples from real_test.json")

# Process 'train', 'basic_test', and 'random_test' datasets
mathlib4_datasets = ['train', 'basic_test', 'random_test']
for dataset in mathlib4_datasets:
    # Specify the input and output file paths
    input_file = f'../../data/{dataset}.json'
    output_file = f'../../data/filtered_{dataset}.json'

    # Call the function to filter and save the data
    filtered_count = filter_custom_lemma(input_file, output_file)
    print(f"Filtered {filtered_count} samples from {dataset}.json")