import json
import random

random.seed(42)

# Load the JSON data
with open('FormL4_autoform.json', 'r') as file:
    data = json.load(file)

# Process each sample
for sample in data:
    # Add "formal": null if it doesn't exist
    if "formal" not in sample:
        sample["formal"] = None
    
    # Reorganize the order of items
    new_order = ["formal"] + [key for key in sample if key != "formal"]
    sample_reordered = {key: sample[key] for key in new_order}
    
    # Add new items
    sample_reordered["human_eval_inform"] = None
    sample_reordered["human_eval_autoform"] = None
    
    # Replace the original sample with the reordered one
    sample.clear()
    sample.update(sample_reordered)

# Shuffle the samples
random.shuffle(data)

# Save the modified JSON data
with open('FormL4_autoform_to_annotate.json', 'w') as file:
    json.dump(data, file, indent=4)