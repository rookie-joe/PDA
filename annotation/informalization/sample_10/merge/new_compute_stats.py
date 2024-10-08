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




########### IAA ###########

from sklearn.metrics import cohen_kappa_score

def contains_t_or_f(annotation):
    """Helper function to determine if the annotation contains 'T' or 'F'."""
    if annotation:
        annotation = annotation.upper()  # Normalize to uppercase
        if 'T' in annotation:
            return 'T'
        elif 'F' in annotation:
            return 'F'
    return None

def calculate_kappa(data, annotator_a, annotator_b, field_prefixes):
    """Calculate Cohen's Kappa across all samples."""
    kappa_scores = {}

    for field in field_prefixes:
        annotations_a = []
        annotations_b = []
        
        for entry in data:
            # Get the annotations for the current field
            val_a = contains_t_or_f(entry.get(f'{field}_{annotator_a}'))
            val_b = contains_t_or_f(entry.get(f'{field}_{annotator_b}'))
            
            if val_a and val_b:
                annotations_a.append(val_a)
                annotations_b.append(val_b)

        # Calculate Cohen's Kappa
        kappa_scores[field] = cohen_kappa_score(annotations_a, annotations_b) if annotations_a and annotations_b else None

    return kappa_scores

# Load the merged JSON file
models = ['gemini', 'gpt4o']
for model in models:
    print("#" * 10, model, "#" * 10)
    with open(f'{model}_sample10_merged_annotation.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fields to calculate stats for
    field_prefixes = ['informalization_success', 'informal_proof_correctness', 'model_preference']
    
    # Calculate Cohen's Kappa for the first 5 samples (annotator 1 vs annotator 2)
    print("Calculating for first 5 samples (annotator 1 vs annotator 2)")
    kappa_scores_1 = calculate_kappa(data[:5], 1, 2, field_prefixes)
    
    # Calculate Cohen's Kappa for the last 5 samples (annotator 3 vs annotator 2)
    print("Calculating for last 5 samples (annotator 3 vs annotator 2)")
    kappa_scores_2 = calculate_kappa(data[5:], 3, 2, field_prefixes)
    
    # Combine the results for both sets
    combined_kappa = {}

    for field in field_prefixes:
        combined_kappa[field] = (kappa_scores_1[field] + kappa_scores_2[field]) / 2 if kappa_scores_1[field] and kappa_scores_2[field] else None

    # Print final combined results
    print("\nCombined Cohen's Kappa:")
    for field in field_prefixes:
        print(f"{field}: Cohen's Kappa: {combined_kappa[field]:.2f}" if combined_kappa[field] is not None else f"{field}: Cohen's Kappa: N/A")