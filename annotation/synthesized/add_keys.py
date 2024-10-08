'''
finding matched uuids in the two JSON files, 
replacing specific keys in annotated_samples with values from the matched samples, 
and then adding two new items ("pda_valid" and "model") to annotated_samples
'''
import json

# Load your JSON data
with open('FormL4_autoform.json', 'r', encoding='utf-8') as f:
    samples = json.load(f)

with open('FormL4_autoform_annotation.json', 'r', encoding='utf-8') as f:
    annotated_samples = json.load(f)

# Create a mapping of uuid to relevant data from samples
uuid_map = {sample['uuid']: sample for sample in samples}

# Iterate through annotated_samples to find matches
for annotated_sample in annotated_samples:
    uuid = annotated_sample.get('uuid')
    if uuid in uuid_map:
        matched_sample = uuid_map[uuid]
        
        # Replace specified values
        annotated_sample['formal'] = matched_sample.get('formal', annotated_sample['formal'])
        annotated_sample['nl_statement'] = matched_sample.get('nl_statement', annotated_sample['nl_statement'])
        annotated_sample['nl_proof'] = matched_sample.get('nl_proof', None)  # Assuming it might be None
        annotated_sample['fl_statementproof'] = matched_sample.get('fl_statementproof', annotated_sample['fl_statementproof'])
        annotated_sample['source'] = matched_sample.get('source', annotated_sample['source'])
        
        # Add new items
        annotated_sample['pda_valid'] = matched_sample.get('pda_valid')
        annotated_sample['model'] = matched_sample.get('model')

# Save the updated annotated_samples back to a JSON file
with open('Final_FormL4_Annotation.json', 'w', encoding='utf-8') as f:
    json.dump(annotated_samples, f, ensure_ascii=False, indent=4)

print("Updated annotated samples saved to Final_FormL4_Annotation.json")

