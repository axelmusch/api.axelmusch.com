import json

from api_functions import shannon_entropy

f = open('./assets/scores.json')
WORDS_SCORES = json.load(f)
f.close()

def result_to_json(dict, filename):
    with open("dump/" + filename + ".json", "w") as outfile: 
        json.dump(dict, outfile)
    outfile.close()

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

def match_word(word_to_check:str,green:list[list],yellow:list,gray:list,yellowspots:list[list]):
    
    for notletter in gray:
        if notletter in word_to_check:
            return False

    for yellowletter in yellow:
        if yellowletter not in word_to_check:
            return False

    for idx,wrongspot in enumerate(yellowspots):
        if word_to_check[idx] in wrongspot:
            return False

    for idx,letter in enumerate(word_to_check):
        if green[idx] != "-" and letter != green[idx]:
            return False
        
    return True

def get_filtered_words(guesses:dict,wordlist:str)->list:
    if wordlist == 'wordle':
        to_filter = WORDLE_WORDS
    elif wordlist == 'all':
        to_filter = ALL_WORDS
    
    letters_green = ["-","-","-","-","-"]
    letters_yellow = []
    letters_gray = []
    letters_yellow_spots= [[],[],[],[],[]]

    for key in guesses:
        guess = key
        guess_result = guesses[key]
        for idx,gr_letter in enumerate(guess_result): 
            if gr_letter == '2':
                letters_green[idx] = guess[idx]
            elif gr_letter == '1':
                letters_yellow.append(guess[idx])
                letters_yellow_spots[idx].append(guess[idx])  
            elif gr_letter == '0':
                letters_gray.append(guess[idx])
    
    matching_words = []
    for word in to_filter:
        matches = match_word(word,letters_green,letters_yellow,letters_gray,letters_yellow_spots)
        
        if matches == True:
            matching_words.append(word)

    print(matching_words)
    print(len(matching_words))

    return matching_words

def get_best_word(possible_words:list[str])->dict[str,float]:
    to_return = dict()
    possible_words_length = len(possible_words)
    for word in ALL_WORDS:
        to_return[word] = float
        results_scores = dict()
        print(f"checking: {word}")
        for word_to_check in possible_words:
            word_result = ""
            for index,letter in enumerate(word):
                if letter == word_to_check[index]:
                    word_result += "2"
                elif letter in word_to_check:
                    word_result += "1"
                else:
                    word_result += "0"

            if word_result in results_scores :
                results_scores[word_result]["total"] += 1
            else:
                results_scores[word_result] = {"total":1}

        sorted_keys = dict(sorted(results_scores.items(), key=lambda item: item[1]["total"],reverse=True))

        probs = []
        for key in sorted_keys:
            t = sorted_keys[key]["total"] / possible_words_length
            probs.append(t)
            sorted_keys[key]["percentage"] = t*100
        entropy = shannon_entropy(probs)

        #to_return[word]["score"] = entropy
        #to_return[word]["patterns"] = sorted_keys
        to_return[word] = entropy

    to_return = dict(sorted(to_return.items(),key=lambda x: (x[1]),reverse=True))
    return to_return

def get_next_best_guess(guesses)->list[dict[str,float]]:
    returnval = {}
    possible_words_all = get_filtered_words(guesses=guesses,wordlist='wordle')
    returnval["count_possible"] = len(possible_words_all)
    returnval["all_possible"] = possible_words_all
    return returnval

if __name__ == "__main__":
    res = get_best_word(["cecal","fecal","feral","fetal","genal","legal","neral","penal","petal","recal","regal","renal","tepal"])
    res = {k: res[k] for k in list(res)[:20]}
    result_to_json(res,"test1")
    print(res)