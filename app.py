from scanner import Scanner
from data import Dataset
import torch
import os

mlp = torch.load("result/mlp.pkl")
scanner = Scanner()
dataset = Dataset()

while True:
    os.system("networksetup -setairportpower en0 on")
    result = scanner.scan_all()
    feature = dataset.result2feature(result)
    predict = mlp(feature)
    pos = dataset.output2pos(predict)
    print("Current Position is : ", pos)
    os.system("networksetup -setairportpower en0 off")