import json

f = open('./assets/scores.json')
WORDS_SCORES = json.load(f)
f.close()

def load_words(wordlist_filename:str)->list[str]:
    """load words"""
    print ("Loading word list from file...")
    temp_wordlist = list()
    with open(wordlist_filename,encoding="utf-8") as f:
        for line in f:
            temp_wordlist.append(line.rstrip('\n'))
    print (" ", len(temp_wordlist), "words loaded.")
    return temp_wordlist

WORDLE_WORDS = load_words('./words.txt')
ALL_WORDS = load_words('./allwords.txt')

def get_best_words(amount:int)->list[dict[str,float]]:
    """ Returns an array with the amount of requested words """
    scores = WORDS_SCORES
    words_to_return = {k: scores[k] for k in list(scores)[:amount]}
    return  words_to_return

def get_next_best_guess(guesses)->list[dict[str,float]]:

    ...