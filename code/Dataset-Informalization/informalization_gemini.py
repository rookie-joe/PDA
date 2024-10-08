import os
import json
from tqdm import tqdm
import random
import re
import argparse
import time
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting, FinishReason
from google.api_core.exceptions import ResourceExhausted 


# Function to read the prompt template from a file
def read_prompt_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to read data from a JSON file
def read_samples(file_path, num_samples=10, seed=42):
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

# Function to extract sections from Gemini Pro output
def extract_sections(gemini_output):
    problem_pattern = re.compile(r"# Problem:(.*?)(?=# Explanation:|# Proof:|$)", re.DOTALL)
    explanation_pattern = re.compile(r"# Explanation:(.*?)(?=# Proof:|$)", re.DOTALL)
    proof_pattern = re.compile(r"# Proof:(.*?)(?=# Theorem:|$)", re.DOTALL)
    
    problem = problem_pattern.search(gemini_output)
    explanation = explanation_pattern.search(gemini_output)
    proof = proof_pattern.search(gemini_output)
    
    return {
        "problem": problem.group(1).strip() if problem else "",
        "explanation": explanation.group(1).strip() if explanation else "",
        "proof": proof.group(1).strip() if proof else ""
    }

def get_response(model, prompt_input, generation_config, safety_settings, retries=8):
    try:
        response = model.generate_content(
            prompt_input,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        return response 
    except ResourceExhausted as e:
        print(f"Quota exceeded: {e}")
        if retries > 0:
            print("Waiting for 10 seconds before retrying...")
            time.sleep(10)
            return get_response(model, prompt_input, generation_config, safety_settings, retries - 1)
        else:
            print("Retries exhausted. Skipping this sample.")
            return None  # Indicate failure


def main(args):

    # Set up Google Cloud Project
    vertexai.init(project=args.project_id, location=args.location)

    # Load the Gemini Pro model
    model = GenerativeModel(model_name=args.model_name)

    # Load prompt template
    prompt_template = read_prompt_template(args.prompt_template_path)

    # Load samples, handling potential for resuming
    samples = read_samples(args.input_file_path, num_samples=args.num_samples, seed=args.seed)
    start_index = 0

    # Check for existing output file to resume from
    output_file = args.output_file_path
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
            start_index = len(existing_data)
            print(f"Resuming from checkpoint: Found {start_index} existing samples in {output_file}")
        except json.JSONDecodeError:
            print("Warning: Output file exists but is not valid JSON. Starting from scratch.")
    samples_to_process = samples[start_index:]


    # Generation parameters for Gemini Pro
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0.7,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
    ]

    # Prepare output data list (potentially loading existing data)
    if start_index == 0:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(args.output_file_path), exist_ok=True)
        new_samples = []
    else:
        new_samples = existing_data

    # Iterate over samples, resuming from the checkpoint
    save_interval = 10 
    try:
        for i, sample in enumerate(tqdm(samples_to_process, desc="Processing samples", initial=start_index)):
            # Replace {Theorem} in the template with the actual "output" value
            prompt_input = prompt_template.replace("{Theorem}", sample['output'])

            # Get the response using the recursive function
            response = get_response(model, prompt_input, generation_config, safety_settings)

            if response is not None: # Check if the API call was successful
                # Extract the response text
                gemini_output = response.text

                # Extract sections from Gemini Pro output
                sections = extract_sections(gemini_output)

                # Append to new samples
                new_samples.append({
                    "formal": sample["output"],
                    "gemini_output": gemini_output,
                    "nl_problem": sections["problem"],
                    "nl_explanation": sections["explanation"],
                    "nl_proof": sections["proof"]
                })

            # Check if it's time to save (outside the retry logic) 
            if (i + 1) % save_interval == 0:
                # Write the new output data to the output file
                write_output(args.output_file_path, new_samples)

    except KeyboardInterrupt: 
        print("\nProcess interrupted! Saving current progress...")

    print(f"Processing complete! Results saved to {args.output_file_path}.")


def int_or_none(value):
    if value.lower() == 'none':
        return None
    else:
        return int(value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some JSON data with Gemini Pro.")
    parser.add_argument('--location', type=str, required=True, help='gemini API model quota location.')
    parser.add_argument('--project_id', type=str, required=True, help='gemini API model project id.')
    parser.add_argument('--input_file_path', type=str, required=True, help='Path to the input JSON file')
    parser.add_argument('--output_file_path', type=str, required=True, help='Path to the output JSON file')
    parser.add_argument('--prompt_template_path', type=str, default='../../prompt/fewshot_informalization.txt', help='Path to the prompt template file')
    parser.add_argument('--model_name', type=str, default="gemini-1.5-pro-001", help='Name of the Gemini Pro model')
    parser.add_argument('--num_samples', type=int_or_none, default=10, help='Number of samples to process (Set None to run on entire)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')

    args = parser.parse_args()
    main(args)