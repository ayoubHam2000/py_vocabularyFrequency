import glob
from functions import *

files = glob.glob("texts/book/*")
outPut = open("out.txt", "w")


wordFreq = getWordsFrequencies(files)
print(len(wordFreq))

res = getOrigins(wordFreq)
for item in res.keys():
    o = f'{item} => {res[item]}'
    #print(o)
    outPut.write(f'{o}\n')

print(len(res))