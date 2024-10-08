'''
To run the script on the entire dataset, use the following command:
python script_name.py --api_key [YOUR API KEY] --base_url [YOUR API BASE URL] --input_file_path ../data/random_test.json --output_file_path ../output/random_test_sample_all.json --prompt_template_path ../prompt/fewshot_informalization.txt --model_name gpt-4o --seed 42
'''

import os
import json
from openai import OpenAI
from tqdm import tqdm  # Import tqdm for progress bars
import random
import re
import argparse

# Function to read the prompt template from a file
def read_prompt_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to read data from a JSON file
def read_samples(file_path, num_samples=None, seed=42):
    # Set the seed for reproducibility
    if seed is not None:
        random.seed(seed)
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # If num_samples is None, return the entire dataset
    if num_samples is None:
        return data
    
    # Randomly sample num_samples from the data
    sampled_data = random.sample(data, min(num_samples, len(data)))
    return sampled_data

# Function to write new samples to the output file
def write_output(file_path, new_data):
    with open(file_path, 'w') as file:
        json.dump(new_data, file, indent=4)

# Function to extract sections from gpt4o_nl
def extract_sections(gpt4o_nl):
    problem_pattern = re.compile(r"# Problem:(.*?)(?=# Explanation:|# Proof:|$)", re.DOTALL)
    explanation_pattern = re.compile(r"# Explanation:(.*?)(?=# Proof:|$)", re.DOTALL)
    proof_pattern = re.compile(r"# Proof:(.*?)(?=# Theorem:|$)", re.DOTALL)
    
    problem = problem_pattern.search(gpt4o_nl)
    explanation = explanation_pattern.search(gpt4o_nl)
    proof = proof_pattern.search(gpt4o_nl)
    
    return {
        "problem": problem.group(1).strip() if problem else "",
        "explanation": explanation.group(1).strip() if explanation else "",
        "proof": proof.group(1).strip() if proof else ""
    }

def main(args):
    # Set up OpenAI API environment
    os.environ["OPENAI_API_KEY"] = args.api_key
    os.environ["OPENAI_BASE_URL"] = args.base_url

    client = OpenAI()

    # Load prompt template
    prompt_template = read_prompt_template(args.prompt_template_path)
    # Load samples from the input JSON file
    samples = read_samples(args.input_file_path, num_samples=args.num_samples, seed=args.seed)

    # Prepare output data list
    new_samples = []

    # Iterate over the samples, generate the new output, and collect results
    # Wrap the loop with tqdm for the progress bar
    for sample in tqdm(samples, desc="Processing samples"):
        # Replace {Theorem} in the template with the actual "output" value
        prompt_input = prompt_template.replace("{Theorem}", sample['output'])
        
        # Generate response from GPT-4o with temperature set to 0.7
        completion = client.chat.completions.create(
            model=args.model_name,
            messages=[
                {"role": "system", "content": "You are a math expert familiar with the Lean 4 theorem prover, a tool used for formal verification of mathematical theorems and proofs."},
                {"role": "user", "content": prompt_input}
            ],
            temperature=0.7
        )

        # Extract the response text
        gpt4o_output = completion.choices[0].message.content
        
        # Extract sections from gpt4o_nl
        sections = extract_sections(gpt4o_output)
        
        # Append to new samples
        new_samples.append({
            "formal": sample["output"],
            "gpt4o_output": gpt4o_output,
            "nl_problem": sections["problem"],
            "nl_explanation": sections["explanation"],
            "nl_proof": sections["proof"]
        })

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output_file_path), exist_ok=True)

    # Write the new output data to the output file
    write_output(args.output_file_path, new_samples)

    print(f"Processing complete! Results saved to {args.output_file_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some JSON data with GPT-4o.")
    parser.add_argument('--input_file_path', type=str, required=True, help='Path to the input JSON file')
    parser.add_argument('--output_file_path', type=str, required=True, help='Path to the output JSON file')
    parser.add_argument('--prompt_template_path', type=str, required=True, help='Path to the prompt template file')
    parser.add_argument('--model_name', type=str, default="gpt-4o", help='Name of the openai model')
    parser.add_argument('--api_key', type=str, default="gpt-4o", help='api_key of the openai model')
    parser.add_argument('--base_url', type=str, default="gpt-4o", help='base_url of the openai model')
    parser.add_argument('--num_samples', type=int, default=10, help='Number of samples to process (None for all)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')

    args = parser.parse_args()
    main(args)