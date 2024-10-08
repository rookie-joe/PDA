# Data construction


This folder contains codes used to construct the **FormL4** dataset.

1. First, preprocess the extracted raw theorems from Mathlib4 by runnning `preprocessing.py`. The raw data should stored in `../../data` including four subsets ('train' 'basic_test', 'random_test', 'real_test') in .json formats. This code filters the unsuitable theorems for informalization, including:
    - filtering all samples with '.mk' in the theorem statement ('train' 'basic_test', 'random_test').
    - filtering all samples with 'python' in the natural language statement ('real_test').

2. Perform informalization using an LLM. We provide codes for using two model families: openai and gemimi. We used few-shot prompt for informalization. The prompt template is located in the `prompt` sub-directory of the repository.

    Example code:

    - GEMINI models:

    ```
    python informalization_gemini_location.py \
        --project_id [YOUR PROJECT ID] \
        --location [YOUR API location] \
        --model_name gemini-1.5-pro-001\
        --input_file_path ../../data/train.json \
        --output_file_path ../../data/FormL4/train.json \
        --num_samples 5 \ # [Set as None if runnning on the full-size set]
        --seed 42
    ```
    - OPENAI models:

    ```
    python informalization_gemini_location.py \
    --api_key [YOUR OPENAI API KEY] \
    --base_url [YOUR OPENAI BASE URL] \
    --model_name gpt-4o\
    --input_file_path ../../data/train.json \
    --output_file_path ../../data/FormL4/train.json \
    --num_samples 5 \ # [Set as None if runnning on the full-size set]
    --seed 42
    ```