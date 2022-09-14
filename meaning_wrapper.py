import bs4
import time
import json
import requests 
from typing import List

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

def get_word_meaning_web_scrape(word_list: List[str]) -> dict:  
    word_meanings = {}
    count = 0
    for word in word_list:
        count += 1
        # separating synonyms
        synonyms = word.split(', ')
        # default meaning -> Nothing found
        word_meanings[synonyms[0]] = 'No noun word meaning found'
        # look for synonymous word if no noun meaning is found
        for one_word in synonyms:
            try:
                one_word = one_word.replace('_', ' ')
                url = f"https://www.google.com/search?q={one_word}+meaning"
                request_result = requests.get(url)
                soup = bs4.BeautifulSoup( request_result.text, "html.parser") 
                print(soup)
                # parsing the noun meaning from the webpage
                meaning = soup.find("span" , class_="r0bn4c rQMQod", string="noun\n").findNext('div', class_="BNeawe s3v9rd AP7Wnd").text 
                word_meanings[synonyms[0]] = meaning
                break
            except Exception as e:
                print(e)
                print(f"No direct meaning found for this word {one_word}")
        # avoiding burst requests as the API fails due to lot of requests
        if count % 100 == 0:
            print(f"Completed : {count}, sleeping for 2min")
            time.sleep(120)
            print("waking up and starting again")

    return word_meanings

response = requests.get('https://storage.googleapis.com/bit_models/imagenet21k_wordnet_lemmas.txt') 
words = response.text
word_list = words.split("\n")
word_list.remove('')

print("STARTING THE REST API METHOD")
api_start_time = time.time()
# Processing first 1000 words
word_meaning_dict = get_word_meaning_api(word_list[0:1000])
# store the json file
with open('meaning_api.json', 'w') as f:
    json.dump(word_meaning_dict, f)
print(f"Total time taken for the web api approach is: {time.time() - api_start_time} seconds")
print("="*50)

print("STARTING THE WEB SCRAPING METHOD")
web_scrape_start_time = time.time()
# Processing first 1000 words
word_meaning_dict = get_word_meaning_web_scrape(word_list[0:1000])
# store the json file
with open('meaning_web_scrape.json', 'w') as f:
    json.dump(word_meaning_dict, f)
print(f"Total time taken for the web api approach is: {time.time() - web_scrape_start_time} seconds")
print("="*50)