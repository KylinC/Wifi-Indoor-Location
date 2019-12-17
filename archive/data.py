import torch
import numpy as np
import pandas as pd
import csv
import random
import os

class Dataset:
    def __init__(self, blackList = []):
        self.blackList = blackList

        self.posNames = []
        self.APNames = []
        self.Pos2Index = {}

        self.ModelInputs = []
        self.ModelOutputs = []
        self.ModelOutputsName = []

        self.__readCSV()
        self.numSamples = len(self.ModelInputs)
        self.numAP = len(self.APNames)
        self.numPos = len(self.posNames)

        self.adjDict = {}
        self.__readAdj()

    def __readCSV(self):
        root = "data/"
        fileNames = os.listdir(root)
        for file in fileNames:
            if file.split(sep=".")[1] != "csv":
                fileNames.remove(file)

        # init posNames & APNames
        for file in fileNames:
            self.posNames.append(file.split(sep=".")[0])
            self.Pos2Index[file.split(sep=".")[0]] = []
            data = pd.read_csv(root+file, header=0).values.tolist()
            for item in data:
                if (not pd.isna(item[0])) and (not item[0] in self.APNames) and (self.__isEn(item[0])):
                    self.APNames.append(item[0])

        # prepare training data
        for file in fileNames:
            data = pd.read_csv(root+file, header=0).values.tolist()
            data = self.__splitCsvData(data)
            for eachTest in data:
                self.ModelInputs.append(self.__turn2features(eachTest))
                self.ModelOutputs.append(self.__pos2tensor(file.split(sep=".")[0]))
                self.ModelOutputsName.append(file.split(sep=".")[0])
                self.Pos2Index[file.split(sep=".")[0]].append(len(self.ModelInputs)-1)
                
            
    def __splitCsvData(self, data):
        result = [[]]
        for item in data:
            if pd.isna(item[0]) and pd.isna(item[1]) and pd.isna(item[2]):
                result.append([])
            elif (not pd.isna(item[0])) and (item[0] not in self.blackList) and (self.__isEn(item[0])):
                newItem = item[:2]
                newItem[0] = self.APNames.index(item[0])
                result[-1].append(newItem)
        result.remove([])
        return result

    def __readAdj(self):
        for name in self.posNames:
            self.adjDict[name] = []
        fileName = "data/adjacency.txt"
        adj = open(fileName).read().splitlines()
        for i, seq in enumerate(adj):
            adj[i] = seq.split()
        for seq in adj:
            for i in range(1, len(seq)-1):
                a, b, c  = seq[i-1], seq[i], seq[i+1]
                if b not in self.adjDict[a]: self.adjDict[a].append(b)
                if a not in self.adjDict[b]: self.adjDict[b].append(a)
                if c not in self.adjDict[b]: self.adjDict[b].append(c)
                if b not in self.adjDict[c]: self.adjDict[c].append(b)

    def __turn2features(self, data):
        result = torch.zeros([len(self.APNames)])
        for rssi in data:
            result[rssi[0]] = rssi[1]
        return result

    def __pos2tensor(self, pos):
        result = torch.zeros([len(self.posNames)])
        result[self.posNames.index(pos)] = 1
        return result

    def __isEn(self, name):
        for c in name:
            if c<'!' or c>'~':
                return False
        return True


    def example(self, index=None):
        if index==None:
            index = random.randint(0, self.numSamples-1)
        return self.ModelInputs[index], self.ModelOutputs[index]

    def sequenceExamples(self, seqLen = 5, ratio = 0.6):
        allPoses = [random.choice(self.posNames)]
        for _ in range(seqLen):
            r = random.random()
            if r<ratio:
                allPoses.append(random.choice(self.adj2(allPoses[-1], dist=0)))
            # elif r<0.9:
            #     allPoses.append(random.choice(self.adj2(allPoses[-1], dist=1)))
            else:
                allPoses.append(random.choice(self.adj2(allPoses[-1], dist=1)))
        
        allIndexes = [random.choice(self.Pos2Index[name]) for name in allPoses]
        targetInput = torch.randn([0])

        for index in allIndexes:
            targetInput = torch.cat([targetInput, self.ModelInputs[index].view(1,1,-1)], dim=0)

        return targetInput, self.ModelOutputs[allIndexes[-1]], allPoses        

    def result2feature(self, result):
        feature = torch.zeros([len(self.APNames)])
        for item in result:
            if item["ssid"] in self.APNames:
                feature[self.APNames.index(item["ssid"])] = item["signal"]
        return feature

    def output2pos(self, output):
        topi, topv = output.flatten().topk(1)
        return self.posNames[int(topv.item()) ]

    def adj2(self, posName, dist = 1):
        result = [posName]
        for _ in range(dist):
            newResult = []
            for pos in result:
                for adjPos in self.adjDict[pos]:
                    if adjPos not in newResult: newResult.append(adjPos)
            result = newResult
        if dist>=2:
            result2 = [posName]
            for _ in range(dist-2):
                newResult = []
                for pos in result:
                    for adjPos in self.adjDict[pos]:
                        if adjPos not in newResult: newResult.append(adjPos)
                result2 = newResult
            for pos in result2:
                result.remove(pos)
        return result

if __name__ == "__main__":
    dataset = Dataset()