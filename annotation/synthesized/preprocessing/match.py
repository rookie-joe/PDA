import json

# Load the autoform JSON file
with open('../autoformalization/merged.json', 'r', encoding='utf-8') as file:
    autoform_data = json.load(file)

# Load the forml4 JSON files
forml4_data = {}
subsets = ['basic_test', 'random_test']
for subset in subsets:
    with open(f'../../data/FormL4/{subset}.json', 'r', encoding='utf-8') as file:
        forml4_data[subset] = json.load(file)

# Create a dictionary for quick lookup in the forml4 JSON
forml4_dict = {}
for subset in subsets:
    for item in forml4_data[subset]:
        item['nl_problem'] = item['nl_problem'].replace('\\', '\\\\')
        if subset not in forml4_dict:
            forml4_dict[subset] = {}
        forml4_dict[subset][item['nl_problem'].strip()] = item['formal']

# Mapping source to subset
source_to_subset = {
    'lean_basic': 'basic_test',
    'lean_random': 'random_test',
    'math': 'filtered_real_test'
}

# Iterate through the autoform JSON and append the 'formal' field
miss = 0
for item in autoform_data:
    nl_problem = item['nl_statement'].strip()
    source = item['source']
    
    # Determine the appropriate subset based on the source
    subset = source_to_subset.get(source)
    
    if source == 'math':
        continue
    elif subset and nl_problem in forml4_dict[subset]:
        item['formal'] = forml4_dict[subset][nl_problem]
    else:
        item['formal'] = None  # or some default value if no match is found
        print(f"Found no matching formal statement for the sample: {subset}! {nl_problem}")
        miss += 1

# Save the updated autoform JSON
with open('FormL4_autoform.json', 'w', encoding='utf-8') as file:
    json.dump(autoform_data, file, ensure_ascii=False, indent=4)

print("Updated JSON has been saved to 'FormL4_autoform.json'")
print(f"Found no matching formal statement for {miss} samples!")
