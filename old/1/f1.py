from nltk import FreqDist
import re

from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist
import enchant
import nltk
from numpy import append
from pattern.text.en import singularize

def getFormatText(file):
    data = open(file).read().lower()
    data = re.sub(r'\n+', '', data)
    data = re.sub(r'\W+-|-\W+', '', data)
    data = re.sub(r'\d+-|-\d+', '', data)
    data = re.sub(r'[^\x00-\x7F]+', '', data)
    data = re.sub(r'\W\d+\W', '', data)
    data = re.sub(r'[?./!;,:*-+{}\[\]\\@#$%^&()_`~‘’]|“|”', '', data)
    return data

def isWordValide(word):
    return (not re.search(r"\d+", word)) and len(word) > 1

def filterWords(data):
    lemmatizer = WordNetLemmatizer()
    dic = enchant.Dict("en_US")
    tokenized = nltk.word_tokenize(data)

    #print(nltk.pos_tag(tokenized))
    result = []
    

    wordType = []
    for (word, pos) in nltk.pos_tag(tokenized):
        t = nltk.word_tokenize(word)
        for (w, p) in nltk.pos_tag(t):
            wordType.append((w, p[:2]))

    for word, pos in wordType:
        item = word
        if not dic.check(item) or not isWordValide(item):
            continue
        if(pos == 'NN'):
            item = singularize(item)
        elif(pos == 'VB'):
            item = lemmatizer.lemmatize(word, 'v')
        else:
            item = word

        if word != item and not dic.check(item):
            result.append(word)
        else:
            result.append(item)
    return result

def getWordsFrequencies(files):
    nltk.download('punkt')
    word_dist = FreqDist()

    for f in files: 
        formatedText = getFormatText(f)
        words = filterWords(formatedText)
        word_dist.update(words)
        print(f'{f} --- > Done')
    result = dict(word_dist)
    result = dict(sorted(result.items(), key=lambda item: item[1]))
    return result