import re
import nltk
from nltk.corpus import stopwords  # Have to call `nltk.download()` once
from difflib import SequenceMatcher

def stringify_list(l):
    return ' '.join(l)

def sanitize_pipeline(name):
    """
    This work is based on `Lookup interests list using Zefix.ipynb`.
    """

    # Remove parenthesis
    ans = re.sub("\(.*\)?",'', name).strip()

    # Tokenize
    ans = nltk.word_tokenize(ans)

    # Remove stop words
    stop_words = stopwords.words(['german', 'french'])
    ans = [w for w in ans if w.lower() not in stop_words]

    # Remove particular words
    particular_words = ['AG', 'SA']
    ans = [token for token in ans if token.upper() not in particular_words]

    return ans

def likeliness(baseword, testword):
    """
    Quantify how testword appears in baseword
    """
    return SequenceMatcher(None, baseword, testword).ratio()

def includeness(baseword, testword):
    """
    Ratio of words in `baseword` that appear in `testword`. The idea is to bypass
    cases - like Zefix - which will check accronyms inside words.
    """

    base_set = {w.lower() for w in sanitize_pipeline(baseword)}
    base_length = len(base_set)

    if not base_length:
        return 0

    test_set = {w.lower() for w in testword.split()}

    number_word_found = 0
    for w in base_set:
        if w in test_set:
            number_word_found += 1

    return number_word_found / base_length

def similarity(baseword, testword):
    return 0.5 * (likeliness(baseword, testword) + includeness(baseword, testword))


