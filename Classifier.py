import pandas as pd
import math
import string

class Classifier:
    def __init__(self, document):
        self.document = document
        self.dataSet = pd.read_csv(self.document, sep = "\t", index_col = False,
                              names = ["type", "text"], header = None)
        self.trainingSet, self.validationSet = self.split()
        self.total = self.totalWords()
        self.trainingSpamDic = self.spamDic()
        self.trainingNotSpamDic = self.notSpamDic()

    def split(self):
        total = self.dataSet.count()[0]
        numTraining = math.floor(total*0.7)
        trainingSet = self.dataSet[:numTraining]
        validationSet = self.dataSet[numTraining:]
        return trainingSet, validationSet

    def dataSetTokenizing(self):
        dicSet = self.trainingSet.to_dict(orient="records")
        for i in dicSet:
            i["text"] = i["text"].translate(str.maketrans('', '', string.punctuation)).split()
        return dicSet

    def totalWords(self):
        dicSet = self.dataSetTokenizing()
        trainingDic = {}
        for i in dicSet:
            for j in i["text"]:
                if j.lower() not in trainingDic:
                    trainingDic[j.lower()] = 1
                else:
                    trainingDic[j.lower()] += 1
        return len(trainingDic)

    def pSpam(self):
        numSpamNotSpam = dict(self.trainingSet["type"].value_counts())
        pSpam = numSpamNotSpam["spam"] / len(self.trainingSet)
        return pSpam

    def pNotSpam(self):
        numSpamNotSpam = dict(self.trainingSet["type"].value_counts())
        pNotSpam = numSpamNotSpam["ham"] / len(self.trainingSet)
        return pNotSpam

    def spamDic(self):
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

    def notSpamDic(self):
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

    def pTextSpam(self, tokens):
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


    def pTextNotSpam(self, tokens):
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

    def pTokenSpamNotSpam(self, number, total, length):
        return (number+1)/(self.total+length)
