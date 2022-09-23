from pathlib import Path
import requests
import json
import time
import utils

meanings_filepath = "./data/image_net_cat_meaning.json"
is_meaning_generated = Path(meanings_filepath)

# if the meanings are not generated, then generate them
if not is_meaning_generated.is_file():
    utils.gen_imagenet_cat_meanings(meanings_filepath)

# At this point we have meanings already stored in a JSON file

# Opening JSON file and reading it into dictionary
with open(meanings_filepath) as json_file:
    cat_meanings = json.load(json_file)

category_attribute_mapping = {}

count = 0
for key in list(cat_meanings.keys()):
    # if meanings is not found, then we skip that category for now
    if cat_meanings[key] == "No noun word meaning found":
        attributes = []
    else:
        # append the found attributes into a dictionary
        attributes = utils.get_attributes_from_meaning(cat_meanings[key])
    category_attribute_mapping[key] = attributes
    count += 1
    if count % 100 == 0:
        print(f"Finished processing - {count} words")

# Store the category attribute mapping into a JSON for manual inspection
with open('./data/category_attribute_mapping.json', 'w') as f:
    json.dump(category_attribute_mapping, f)
print("Attribute list dumped into a file")