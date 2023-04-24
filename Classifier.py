import pandas as pd
import math
import string

class Classifier:
    def __init__(self, document):
        self.document = document
        self.dataSet = pd.read_csv(self.document, sep = "\t", index_col = False,
                                   names = ["type", "text"], header = None)
        self.trainingSet, self.testingSet = self.split()
        self.trainingSpamDic = self.spamDic()
        self.trainingNotSpamDic = self.notSpamDic()

    #split dataset into training and testing
    def split(self):
        total = self.dataSet.count()[0]
        numTraining = math.floor(total*0.7)
        trainingSet = self.dataSet[:numTraining]
        testingSet = self.dataSet[numTraining:]
        return trainingSet, testingSet

    #tokenizer
    def dataSetTokenizing(self):
        dicSet = self.trainingSet.to_dict(orient="records")
        for i in dicSet:
            i["text"] = i["text"].translate(str.maketrans('', '', string.punctuation)).split()
        return dicSet

    #PSpam
    def pSpam(self):
        numSpamNotSpam = dict(self.trainingSet["type"].value_counts())
        pSpam = numSpamNotSpam["spam"] / len(self.trainingSet)
        return pSpam

    #PNotSpam
    def pNotSpam(self):
        numSpamNotSpam = dict(self.trainingSet["type"].value_counts())
        pNotSpam = numSpamNotSpam["ham"] / len(self.trainingSet)
        return pNotSpam

    #dictionary of spam words with their counts
    def spamDic(self):
        #whole processed tokenized training set
        dicSet = self.dataSetTokenizing()

        trainingDicSpam = {}
        for i in dicSet:
            if i["type"] == "spam":
                for j in i["text"]:
                    if j.lower() not in trainingDicSpam:
                        trainingDicSpam[j.lower()] = 1
                    else:
                        trainingDicSpam[j.lower()] += 1
        return trainingDicSpam

    #dictionary of not spam words with their counts
    def notSpamDic(self):
        #whole processed tokenized training set
        dicSet = self.dataSetTokenizing()

        trainingDicNotSpam = {}
        for i in dicSet:
            if i["type"] == "ham":
                for j in i["text"]:
                    if j.lower() not in trainingDicNotSpam:
                        trainingDicNotSpam[j.lower()] = 1
                    else:
                        trainingDicNotSpam[j.lower()] += 1
        return trainingDicNotSpam

    #PTextSpam
    def pTextSpam(self, tokens):
        #count total spam words of training set
        totalSpam = 0
        for i in self.trainingSpamDic.keys():
            totalSpam += self.trainingSpamDic[i]

        pTextSpam = 1
        for i in tokens:
            if i.lower() in self.trainingSpamDic:
                pTextSpam *= self.pTokenSpamNotSpam(self.trainingSpamDic[i.lower()], totalSpam, len(tokens))
            else:
                pTextSpam *= self.pTokenSpamNotSpam(0, totalSpam, len(tokens))
        return pTextSpam

    #PTextNotSpam
    def pTextNotSpam(self, tokens):
        # count total not spam words of training set
        totalNotSpam = 0
        for i in self.trainingNotSpamDic.keys():
            totalNotSpam += self.trainingNotSpamDic[i]

        pTextNotSpam = 1
        for i in tokens:
            if i.lower() in self.trainingNotSpamDic:
                pTextNotSpam *= self.pTokenSpamNotSpam(self.trainingNotSpamDic[i.lower()], totalNotSpam, len(tokens))
            else:
                pTextNotSpam *= self.pTokenSpamNotSpam(0, totalNotSpam, len(tokens))
        return pTextNotSpam

    #PTokenSpamNotSpam
    def pTokenSpamNotSpam(self, number, total, length):
        return (number+1)/(total+length)
