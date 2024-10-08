'''
Load each annotator file.

Rename the keys for each annotator.

Merge the samples based on UUID.

Save the merged samples to a new file.
'''

import json
from collections import defaultdict

# Load the annotator files
with open('annotator_1.json', 'r', encoding='utf-8') as f:
    annotator_1 = json.load(f)

with open('annotator_2.json', 'r', encoding='utf-8') as f:
    annotator_2 = json.load(f)

with open('annotator_3.json', 'r', encoding='utf-8') as f:
    annotator_3 = json.load(f)

with open('annotator_4.json', 'r', encoding='utf-8') as f:
    annotator_4 = json.load(f)

# Function to rename keys for each annotator
def rename_keys(samples, annotator_id):
    renamed_samples = []
    for sample in samples:
        new_sample = sample.copy()
        if 'human_eval_inform' in new_sample:
            new_sample[f'human{annotator_id}_eval_inform'] = new_sample.pop('human_eval_inform')
        if 'human_eval_autoform' in new_sample:
            new_sample[f'human{annotator_id}_eval_autoform'] = new_sample.pop('human_eval_autoform')
        renamed_samples.append(new_sample)
    return renamed_samples

# Rename keys for each annotator
annotator_1 = rename_keys(annotator_1, 1)
annotator_2 = rename_keys(annotator_2, 2)
annotator_3 = rename_keys(annotator_3, 3)
annotator_4 = rename_keys(annotator_4, 4)

# Merge samples based on UUID
merged_samples = defaultdict(dict)

def merge_samples(samples, merged_samples):
    for sample in samples:
        uuid = sample['uuid']
        if uuid not in merged_samples:
            merged_samples[uuid] = {
                "formal": sample.get("formal"),
                "nl_statement": sample.get("nl_statement"),
                "nl_proof": sample.get("nl_proof"),
                "fl_statementproof": sample.get("fl_statementproof"),
                "source": sample.get("source"),
                "uuid": uuid
            }
        for key, value in sample.items():
            if key not in ["formal", "nl_statement", "nl_proof", "fl_statementproof", "source", "uuid"]:
                merged_samples[uuid][key] = value

merge_samples(annotator_1, merged_samples)
merge_samples(annotator_2, merged_samples)
merge_samples(annotator_3, merged_samples)
merge_samples(annotator_4, merged_samples)

# Convert the merged samples back to a list
merged_samples_list = list(merged_samples.values())

# Save the merged samples to a new file
with open('merged_samples.json', 'w', encoding='utf-8') as f:
    json.dump(merged_samples_list, f, ensure_ascii=False, indent=4)

print("Merged samples saved to 'merged_samples.json'")