'''
Assignement ruules:
double the 60 samples to 120 samples by make a new identical sample for each sample.
split the 120 samples into 4 annotator files with unequal sample size of 35, 35, 35, 15. Make sure that:
1. each annotator does not annotate any repeated samples, 
2. and that the combination of their annotated samples create exactly two annotations for the original 60 samples.

'''

import json
import random

# Load your JSON data
with open('../FormL4_autoform_annotation.json', 'r', encoding='utf-8') as f:
    samples = json.load(f)

# Step 1: Double the samples
doubled_samples = samples * 2  # Create two identical copies of each sample

# Step 2: Shuffle to ensure randomness
random.seed(42)
random.shuffle(doubled_samples)

# Step 3: Split into 4 annotator files
annotator_1 = []
annotator_2 = []
annotator_3 = []
annotator_4 = []

# Track which samples have been assigned to each annotator
assigned_samples = {i: [] for i in range(len(samples))}

for sample in doubled_samples:
    original_index = samples.index(sample)
    
    # Assign to an annotator ensuring no repeats within an annotator
    if len(annotator_1) < 35 and original_index not in assigned_samples[0]:
        annotator_1.append(sample)
        assigned_samples[0].append(original_index)
    elif len(annotator_2) < 35 and original_index not in assigned_samples[1]:
        annotator_2.append(sample)
        assigned_samples[1].append(original_index)
    elif len(annotator_3) < 35 and original_index not in assigned_samples[2]:
        annotator_3.append(sample)
        assigned_samples[2].append(original_index)
    elif len(annotator_4) < 15 and original_index not in assigned_samples[3]:
        annotator_4.append(sample)
        assigned_samples[3].append(original_index)

# Save the annotator files
with open('annotator_1.json', 'w', encoding='utf-8') as f:
    json.dump(annotator_1, f, ensure_ascii=False, indent=4)

with open('annotator_2.json', 'w') as f:
    json.dump(annotator_2, f, ensure_ascii=False, indent=4)

with open('annotator_3.json', 'w') as f:
    json.dump(annotator_3, f, ensure_ascii=False, indent=4)

with open('annotator_4.json', 'w') as f:
    json.dump(annotator_4, f, ensure_ascii=False, indent=4)