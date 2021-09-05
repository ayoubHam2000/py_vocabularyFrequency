import glob
from functions import *

files = glob.glob("texts/*")
outPut = open("out.txt", "w")


result = getWordsFrequencies(files)
for item in result.keys() :
    o = f'{item} : {result[item]}'
    outPut.write(o + "\n")

print(len(result))