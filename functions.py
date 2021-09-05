from nltk import FreqDist
import re

from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist
import enchant
import nltk
from numpy import append
from pattern.text.en import singularize

def isWordValide(word):
    return (not re.search(r"\d+", word)) and len(word) > 1

def single(word, dic):
    w = singularize(word)
    if word != w and dic.check(w):
        #print(f'{word} => {w}')
        return w
    return word

def origin(word, dic, lemmatizer):
    w = lemmatizer.lemmatize(word, 'v')
    if word != w and dic.check(w):
        #print(f'{word} => {w}')
        return w
    return single(word, dic)

def getFormatText(file):
    data = open(file).read().lower()
    data = re.sub(r'[^\x20-\x7F]+', '', data)
    data = re.sub(r'-\n', '', data)
    data = re.sub(r'\n+', ' ', data)
    data = re.sub(r'-', ' ', data)
    data = re.sub(r'\d+', '', data)
    data = re.sub(r'[?./!;,:*-+{}\[\]\\@#$%^&()_`~‘’]|“|”', '', data)
    data = re.sub(r' +', ' ', data)
    #data = re.sub(r'\W\d+\W', '', data)
    return data

def getWords(file):
    data = getFormatText(file)
    return [item.strip() for item in data.split(' ') if item.strip()]

def getWordsFrequencies(files):
    #nltk.download('punkt')
    word_dist = FreqDist()
    dicts = enchant.Dict("en_US")
    for f in files: 
        words = getWords(f)
        for item in words:
            if dicts.check(item) and isWordValide(item):
                word_dist.update([item])
        print(f'{f} --- > Done')
    result = dict(word_dist)
    #result = dict(sorted(result.items(), key=lambda item: item[1]))
    return result

def getOrigins(wordFreq):
    lemmatizer = WordNetLemmatizer()
    dic = enchant.Dict("en_US")

    res = {}
    for item in wordFreq.keys():
        o = origin(item, dic, lemmatizer)
        if o not in res:
            res[o] = wordFreq[item]
        else:
            res[o] += wordFreq[item]
    res = dict(sorted(res.items(), key=lambda item: item[1]))
    return res