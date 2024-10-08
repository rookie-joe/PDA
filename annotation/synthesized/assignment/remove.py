import json

# Function to remove the "model" key from each sample
def remove_key(samples):
    for sample in samples:
        if "model" in sample:
            del sample["model"]
        if "pda_valid" in sample:
            del sample["pda_valid"]
    return samples

# Load the annotator files
with open('annotator_1.json', 'r', encoding='utf-8') as f:
    annotator_1 = json.load(f)

with open('annotator_2.json', 'r', encoding='utf-8') as f:
    annotator_2 = json.load(f)

with open('annotator_3.json', 'r', encoding='utf-8') as f:
    annotator_3 = json.load(f)

with open('annotator_4.json', 'r', encoding='utf-8') as f:
    annotator_4 = json.load(f)

# Remove the "model" key from each sample
annotator_1 = remove_key(annotator_1)
annotator_2 = remove_key(annotator_2)
annotator_3 = remove_key(annotator_3)
annotator_4 = remove_key(annotator_4)

# Save the modified annotator files
with open('annotator_1.json', 'w', encoding='utf-8') as f:
    json.dump(annotator_1, f, ensure_ascii=False, indent=4)

with open('annotator_2.json', 'w', encoding='utf-8') as f:
    json.dump(annotator_2, f, ensure_ascii=False, indent=4)

with open('annotator_3.json', 'w', encoding='utf-8') as f:
    json.dump(annotator_3, f, ensure_ascii=False, indent=4)

with open('annotator_4.json', 'w', encoding='utf-8') as f:
    json.dump(annotator_4, f, ensure_ascii=False, indent=4)

print("Removed 'model' key from all samples and saved the modified files.")