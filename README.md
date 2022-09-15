# word_meaning_curation
Collect noun meanings of words into JSON

This script has two implementations through two different functions for fetching the meanings of the list of words

1) The first method is through a REST Api - https://dictionaryapi.dev/ 
2) Scraping the google search webpage to extract the meaning 

Both the methods fetch the 'noun' meaning of the words. If the meaning is not found for one of the words, we will use the other synonymous words from the word list if present. In case no meanings are found for any of the words, the default string would be - no noun meanings found.

The script at the moment runs for 1000 words from the list. Since we are making burst requests, the API server will fail to respond and Google servers block our address. In order to get around this problem, we give a random sleep of 2 minutes after every 100 calls.

Future work:

1) It is noticed, to no surprise, the web scraping approach is much more time consuming than Rest API based fetching. These processes can be further sped up using techniques like multithreading or multiprocessing, as most of the time will be spent on network calls only, computation can be parallelized and Python's GIL will not be a bottleneck.

2) The noun meanings are taken by the first one that pops up by default. We can gain more context into which noun meanings to choose from by leveraging the synonyms that are given along with the word.

3) At present, if Google search doesn't provide the meaning for any of the word's other synonymns directly, then the meaning for the word is left off as "not found". We can extend this to probably scrape from other search results instead.