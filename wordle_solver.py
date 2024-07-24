import json

f = open('./assets/scores.json')
WORDS_SCORES = json.load(f)
f.close()


def get_best_words(amount:int)->list[dict[str,float]]:
     
    words_to_return = {k: WORDS_SCORES[k] for k in list(WORDS_SCORES)[:amount]}
    return  words_to_return