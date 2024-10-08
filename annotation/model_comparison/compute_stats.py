import json

def contains_t_or_f(annotation):
    """Helper function to determine if the annotation contains 'T' or 'F'."""
    if annotation:
        annotation = annotation.upper()  # Normalize to uppercase for safety
        if 'T' in annotation:
            return 'T'
        elif 'F' in annotation:
            return 'F'
    return None

def calculate_avg_t_rate_across_all_samples(data, annotator_a, annotator_b, field_prefixes):
    """Calculate the average T rate across all samples."""
    t_counts = {field: 0 for field in field_prefixes}
    total_counts = {field: 0 for field in field_prefixes}
    
    for entry in data:
        for field in field_prefixes:
            # Get the annotations for the current field
            val_a = contains_t_or_f(entry.get(f'{field}_{annotator_a}'))
            val_b = contains_t_or_f(entry.get(f'{field}_{annotator_b}'))
            
            if val_a and val_b:
                total_counts[field] += 1
                
                # Count occurrences of 'T'
                if val_a == 'T':
                    t_counts[field] += 1
                if val_b == 'T':
                    t_counts[field] += 1
    
    # Calculate average T rate
    avg_t_rate = {field: (t_counts[field] / (2 * total_counts[field]) * 100) if total_counts[field] else 0 for field in field_prefixes}
    
    return avg_t_rate

# Load the merged JSON file
models = ['gemini', 'gpt4o']
for model in models:
    print("#" * 10, model, "#" * 10)
    with open(f'{model}_sample10_merged_annotation.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fields to calculate stats for
    field_prefixes = ['informalization_success', 'informal_proof_correctness', 'model_preference']
    
    # Calculate average T rate across all samples
    avg_t_rate = calculate_avg_t_rate_across_all_samples(data, 1, 2, field_prefixes)
    
    # Print final combined results
    print("\nAverage T rate across all samples:")
    for field, t_rate in avg_t_rate.items():
        print(f"{field}: {t_rate:.2f}%")

