from nltk import word_tokenize, pos_tag
import math

from corpus import *

"""
CASES:
AN EXEMPLAR SENTENCE IS PROVIDED FOR EACH CASE
case1
ladder is 10ft long ...

case2
A ladder 10ft long is ...

"""

def tag(sentence):
#returns list of tagges pos
    return pos_tag(word_tokenize(sentence))

def getNouns(tagged):
    result = []
    for tup in tagged:
        if tup[1] == "nn":
            result.append(tup)
    return result

def isNoun(tup):
    if getPos(tup) == "nn" or getPos(tup) == "NN":
        return True
    else:
        return False

def getWord(tup):
    return tup[0]

def getPos(tup):
    return tup[1]

def splitNum(word):
#separates numerical component of a word, returning (num, word)
    result_num = ""
    result_word = ""
    for char in word:
        if char in digits:
            result_num += char
            continue
        else:
            result_word += char
            continue
    return (result_num, result_word)

def hasNum(tup):
#returns whether a result of splitNum has a numerical component
    if tup[0] == "":
        return False
    return True

def isRate(word):
    if "/" in list(word):
        return True
    else:
        return False

def splitRate(word):
#only call this on words where isRate() returns True !
    return 


def getRelationship(mapping):
#be carefule. This expects the value of a dict specifically processed by extractX func
    return mapping[1]

WANT = "" #this is the problem we want to solve, text representing
WRITTEN = False#keep track of whether we found the query

def extractRelationships(tagged):
#when given a list of tagged, returns dictionary of lengths of things with a length
    global WANT
    global WRITTEN 

    result = {}
    prev = tagged[0]
    for i in range(len(tagged)):

        if getWord(tagged[i]) in queries and not WRITTEN:
            for j in range(i, len(tagged)):
                if j == i:
                    WANT += getWord(tagged[j]).title() + " " #captial first letter
                    continue
                WANT += getWord(tagged[j]) + " "
                WRITTEN = True
            result["WANT"] = WANT

        if len(tagged)-i > 1 and getWord(tagged[i]) in post_subj_rate_qualifiers:
            if getWord(tagged[i+1]) in of_POS:
                if isRate(getWord(tagged[i+2])):
                    result["RATE"] = getWord(tagged[i+2])

        if getWord(tagged[i]) in singular_copulatives: #if we found a state-qualifier
            #we want the pre-subject subprocess
            pass

        if getWord(tagged[i]) in post_subj_proximity_qualifiers:
            if hasNum(getWord(tagged[i-1])):
                result["WHEN"] = getWord(tagged[i-1])
        if getWord(tagged[i]) in post_subj_len_qualifiers:
        #sniff for case 2
            if i > 1 and hasNum(splitNum(getWord(tagged[i-1]))): #avoid index errors
                if isNoun(tagged[i-2]):
                    result[getWord(tagged[i-2])] = (getWord(tagged[i-1]),getWord(tagged[i]))
                    continue #don't double count
                elif i > 2 and getWord(tagged[i-2]) in singular_copulatives: #avoid index errors
                #sniff for case 1
                    if isNoun(tagged[i-3]):
                        result[getWord(tagged[i-3])] = (getWord(tagged[i-1]),getWord(tagged[i]))
                    continue
    WRITTEN = False
    return result

def solve(extracted, leaner):
#@extracted is the extracted dict and leaner is the thing that leans on the wall
    steps = []
    lad = extracted[leaner] 
    steps.append("We know the {0} is {1} {2}.".format(leaner, lad[0], lad[1]))
    rat = extracted['RATE']
    steps.append("We are given dy/dx is {0}, we want to find dy/dt".format(rat))
    dist2 = int(   splitNum(lad[0])[0]   )**2 
    steps.append("By the Pythagorean Theorem, we can deduce\n x^2 + y^2 = {0}".format(  int(   splitNum(lad[0])[0]   )**2)   ) #dirty
    
    steps.append("Differentiating each side with respect to t \n using the chain rule, we have: \n 2x * dy/dx + 2 * dy/dt = 0") #neat
    steps.append("Solving this equation for the desired rate, we obtain \n  dy/dt = -x/y * dx/dt")

    whe = extracted['WHEN']
    steps.append("When x={0}, the pythagorean theorem gives y={1}, \n and substituting these values, we have: \n dy/dt = -{0}/{1}".format(whe, math.sqrt(  float(dist2) - float(splitNum(whe)[0])**2 )))
    steps.append('The solution is {0}/{1}'.format(whe, math.sqrt(  float(dist2) - float(splitNum(whe)[0])**2 )))

    return steps

text = tag("My boat is 13ft wide. A ladder 10ft long rests against a vertical wall. My foot is 12ft long. If the bottom of the ladder slides away from the wall at a rate of 1ft/s, how fast is the top of the ladder sliding down the wall when the bottom of the ladder is 6ft from the wall?")

print(solve(extractRelationships(text),  'ladder' ))
