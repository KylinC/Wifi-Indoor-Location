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

        self.ModelInputs = []
        self.ModelOutputs = []

        self.__readCSV()
        self.numSamples = len(self.ModelInputs)
        self.numAP = len(self.APNames)
        self.numPos = len(self.posNames)

    def __readCSV(self):
        root = "data/"
        fileNames = os.listdir(root)

        # init posNames & APNames
        for file in fileNames:
            self.posNames.append(file.split(sep=".")[0])
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
            
    def __splitCsvData(self, data):
        result = [[]]
        for item in data:
            if pd.isna(item[0]) and pd.isna(item[1]) and pd.isna(item[2]) and pd.isna(item[2]):
                result.append([])
            elif (not pd.isna(item[0])) and (item[0] not in self.blackList) and (self.__isEn(item[0])):
                newItem = item[:2]
                newItem[0] = self.APNames.index(item[0])
                result[-1].append(newItem)
        result.remove([])
        return result

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

    def sequenceExamples(self, seqLen = 5):
        index = random.randint(0, self.numSamples-1)
        targetInput = self.ModelInputs[index].view(1,1,-1)
        for i in range(max(index-10, 0), min(index+10, len(self.ModelInputs))):
            if self.ModelOutputs[i].equal(self.ModelOutputs[index]):
                targetInput = torch.cat([targetInput, self.ModelInputs[i].view(1,1,-1)], dim=0)
            if targetInput.shape[0]>=seqLen:
                return targetInput, self.ModelOutputs[index]
        

    def result2feature(self, result):
        feature = torch.zeros([len(self.APNames)])
        for item in result:
            if item["ssid"] in self.APNames:
                feature[self.APNames.index(item["ssid"])] = item["signal"]
        return feature

    def output2pos(self, output):
        topi, topv = output.flatten().topk(1)
        return self.posNames[int(topv.item()) ]

if __name__ == "__main__":
    dataset = Dataset()
    print(dataset.posNames)