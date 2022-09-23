from typing import List
import requests
import time
import json
import spacy

# load spacy language model
sp = spacy.load('en_core_web_sm')
all_stopwords = sp.Defaults.stop_words

def get_word_meaning_api(word_list: List[str]) -> dict:
    word_meanings = {}
    count = 0
    for word in word_list:
        # separating synonyms
        synonyms = word.split(', ')
        # default meaning -> Nothing found
        word_meanings[synonyms[0]] = 'No noun word meaning found'
        # look for synonymous word if no noun meaning is found
        for one_word in synonyms:
            one_word = one_word.replace('_', ' ')
            resp = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+one_word).json()
            if type(resp) == dict or 'word' not in resp[0]:
                continue
            else:
                for meaning in resp[0]['meanings']:
                    if meaning['partOfSpeech'] == "noun":
                        word_meanings[synonyms[0]] = meaning['definitions'][0]['definition']
                        break
                break
        count += 1
        # avoiding burst requests as the API fails due to lot of requests
        if count % 100 == 0:
            print(f"Completed : {count}, sleeping for 2min")
            time.sleep(120)
            print("waking up and starting again")

    return word_meanings

def gen_imagenet_cat_meanings(filename):
    response = requests.get('https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt') 
    words = response.text
    word_list = words.split("\n")
    word_list.remove('')

    print("STARTING THE REST API METHOD")
    api_start_time = time.time()
    # Processing first 1000 words
    word_meaning_dict = get_word_meaning_api(word_list[0:1001])
    # store the json file
    with open(filename, 'w') as f:
        json.dump(word_meaning_dict, f)
    print(f"Total time taken for the web api approach is: {time.time() - api_start_time} seconds")
    print("="*50)

def get_attributes_from_meaning(word_meaning):
    # let spacy split into tokens and understand the sentence structure
    doc = sp(word_meaning)
    # identify any proper nouns that are part of the tokens
    proper_nouns = [token.text for token in doc if token.pos_ == "PROPN"]
    final_attr_list = []
    for noun in doc.noun_chunks:
        break_word = False
        # if the identified noun chunks contain partial proper noun tokens, then omit the word
        # this should help is removing scientific terminologies or scientific names of animals in the meanings
        for prp in proper_nouns:
            if prp in noun.text:
                break_word = True
                break
        if break_word:
            continue
        # description of nouns are to be retained from the noun chuncks extracted
        # Eg: we don't want to separate a phrase such as `orange beak`
        final_attr = ""
        for token in noun.text.split(" "):
            # stripping off the stopwords that may appear in the noun chunk
            if token.lower() not in all_stopwords:
                final_attr += token + " "
        # append non empty string by stripping off extra white spaces
        if final_attr != "":
            final_attr_list.append(final_attr.rstrip())
    return final_attr_list