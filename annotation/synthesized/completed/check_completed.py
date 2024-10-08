'''
1. each annotator does not annotate any repeated samples, 
2. the combination of their annotated samples create exactly two annotations for the original 60 samples.
'''
import json
from collections import Counter

# Load the annotator files
with open('annotator_1.json', 'r', encoding='utf-8') as f:
    annotator_1 = json.load(f)

with open('annotator_2.json', 'r', encoding='utf-8') as f:
    annotator_2 = json.load(f)

with open('annotator_3.json', 'r', encoding='utf-8') as f:
    annotator_3 = json.load(f)

with open('annotator_4.json', 'r', encoding='utf-8') as f:
    annotator_4 = json.load(f)

# Function to extract unique identifiers from samples
def extract_ids(samples):
    return [sample['uuid'] for sample in samples]  # Replace 'id' with the actual key

# Check if each annotator does not annotate any repeated samples
def check_no_repeats(annotator, annotator_number):
    ids = extract_ids(annotator)
    if len(ids) != len(set(ids)):
        print(f"Annotator {annotator_number} has repeated samples.")
    else:
        print(f"Annotator {annotator_number} has no repeated samples.")

def check_completed(annotator, annotator_number):
    count = 0
    for i, sample in enumerate(annotator):
        if sample["human_eval_inform"] == None:
            if sample["formal"] != None:
                print(f"Empty annotation in sample id {i}, annotator {annotator_number}")
                count += 1
        if sample["human_eval_autoform"] == None:
            print(f"Empty annotation in sample id {i}, annotator {annotator_number}")
            count += 1



check_no_repeats(annotator_1, 1)
check_no_repeats(annotator_2, 2)
check_no_repeats(annotator_3, 3)
check_no_repeats(annotator_4, 4)

# Combine all annotations
all_annotations = extract_ids(annotator_1) + extract_ids(annotator_2) + extract_ids(annotator_3) + extract_ids(annotator_4)

# Check if the combination of their annotated samples create exactly two annotations for the original 60 samples
annotation_counts = Counter(all_annotations)
if all(count == 2 for count in annotation_counts.values()) and len(annotation_counts) == 60:
    print("Each original sample is annotated exactly twice.")
else:
    print("The annotations do not create exactly two annotations for each original sample.")


# check completed
check_completed(annotator_1, 1)
check_completed(annotator_2, 2)
check_completed(annotator_3, 3)
check_completed(annotator_4, 4)