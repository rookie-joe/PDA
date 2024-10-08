import json
import os
from statistics import median

def calculate_lengths(data, field):
    return [len(item[field]) for item in data]

def calculate_combined_lengths(data):
    return [len(item['nl_problem']) + len(item['nl_proof']) for item in data]

def analyze_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    sample_size = len(data)
    
    fields = ['formal', 'nl_problem', 'nl_proof']
    combined_field = 'nl_problem + nl_proof'
    
    results = {
        'sample_size': sample_size,
        'lengths': {}
    }
    
    for field in fields:
        lengths = calculate_lengths(data, field)
        results['lengths'][field] = {
            'avg': sum(lengths) / sample_size,
            'median': median(lengths),
            'min': min(lengths),
            'max': max(lengths)
        }
    
    combined_lengths = calculate_combined_lengths(data)
    results['lengths'][combined_field] = {
        'avg': sum(combined_lengths) / sample_size,
        'median': median(combined_lengths),
        'min': min(combined_lengths),
        'max': max(combined_lengths)
    }
    
    return results

def extract_nl_problem_and_proof(input_str):
    statement_start = input_str.find('# Statement:') + len('# Statement: ')
    proof_start = input_str.find('# Proof:') + len('# Proof: ')
    
    statement_end = input_str.find('\n\n', statement_start)
    proof_end = input_str.find('\n\nTranslate the statement and proof in natural language to Lean:', proof_start)

    nl_problem = input_str[statement_start:statement_end].strip()
    nl_proof = input_str[proof_start:proof_end].strip()
    
    return nl_problem, nl_proof

def analyze_filtered_real_test(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    nl_problem_list = []
    nl_proof_list = []

    for item in data:
        nl_problem, nl_proof = extract_nl_problem_and_proof(item['input'])
        nl_problem_list.append(nl_problem)
        nl_proof_list.append(nl_proof)

    sample_size = len(data)

    results = {
        'sample_size': sample_size,
        'lengths': {
            'nl_problem': {
                'avg': sum(len(s) for s in nl_problem_list) / sample_size,
                'median': median(len(s) for s in nl_problem_list),
                'min': min(len(s) for s in nl_problem_list),
                'max': max(len(s) for s in nl_problem_list),
            },
            'nl_proof': {
                'avg': sum(len(s) for s in nl_proof_list) / sample_size,
                'median': median(len(s) for s in nl_proof_list),
                'min': min(len(s) for s in nl_proof_list),
                'max': max(len(s) for s in nl_proof_list),
            },
            'nl_problem + nl_proof': {
                'avg': sum(len(nl_problem) + len(nl_proof) for nl_problem, nl_proof in zip(nl_problem_list, nl_proof_list)) / sample_size,
                'median': median(len(nl_problem) + len(nl_proof) for nl_problem, nl_proof in zip(nl_problem_list, nl_proof_list)),
                'min': min(len(nl_problem) + len(nl_proof) for nl_problem, nl_proof in zip(nl_problem_list, nl_proof_list)),
                'max': max(len(nl_problem) + len(nl_proof) for nl_problem, nl_proof in zip(nl_problem_list, nl_proof_list)),
            }
        }
    }
    
    return results

def main():
    json_files = ['basic_test.json', 'random_test.json', 'train.json', 'filtered_real_test.json']
    data_dir = './FormL4/'

    json_paths = [os.path.join(data_dir, json_file) for json_file in json_files]

    results = {}
    
    for json_file in json_paths:
        if json_file == os.path.join(data_dir, 'filtered_real_test.json'):
            results[json_file] = analyze_filtered_real_test(json_file)
        else:
            results[json_file] = analyze_json_file(json_file)
    
    for file, result in results.items():
        print(f"Analysis for {file}:")
        print(f"Sample Size: {result['sample_size']}")
        for field, stats in result['lengths'].items():
            print(f"  {field}:")
            print(f"    Avg Length: {stats['avg']:.2f}")
            print(f"    Median Length: {stats['median']}")
            print(f"    Min Length: {stats['min']}")
            print(f"    Max Length: {stats['max']}")
        print()

if __name__ == "__main__":
    main()
