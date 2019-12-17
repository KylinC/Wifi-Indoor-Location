from scanner import Scanner
from data import Dataset
import torch
import os

with torch.no_grad():
    # mlp version

    mlp = torch.load("result/mlp.pkl")
    scanner = Scanner()
    dataset = Dataset()

    isFirst = True
    while True:
        os.system("networksetup -setairportpower en0 on")
        result = scanner.scan_all()
        # print(result)
        feature = dataset.result2feature(result)
        predict = mlp(feature)
        pos = dataset.output2pos(predict)
        if not isFirst:
            if (lastPos not in dataset.adj2(pos,dist=0)) and (lastPos not in dataset.adj2(pos,dist=1)) and (lastPos not in dataset.adj2(pos,dist=2)):
                print(pos) 
                print(lastPos)
                pos = lastPos
        else:
            isFirst = False

        lastPos = pos

        print("Current Position is : ", pos)
        os.system("networksetup -setairportpower en0 off")

    # rnn version
    rnn = torch.load("result/rnn.pkl")
    scanner = Scanner()
    dataset = Dataset()
    seqLen = 5

    feature = torch.randn([0])
    while True:
        os.system("networksetup -setairportpower en0 on")
        result = scanner.scan_all()
        # print(result)
        newFeature = dataset.result2feature(result).view(1,1,-1)
        feature = torch.cat([feature, newFeature], dim=0)

        if feature.shape[0]>seqLen:
            feature = feature[1:6]
        if feature.shape[0]<seqLen:
            continue

        hidden = rnn.initHidden()
        for i in range(feature.shape[0]):
            input = feature[i]
            output, hidden = rnn(input, hidden)

        pos = dataset.output2pos(output)
        print("Current Position is : ", pos)
        os.system("networksetup -setairportpower en0 off")