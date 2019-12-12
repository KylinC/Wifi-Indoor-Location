from data import Dataset
from model import MLP
from train import MLPTrainer
import torch

dataset = Dataset()
mlp = MLP(dataset.numAP, dataset.numPos, layers=[256,256,256,128,128,64,32])
trainer = MLPTrainer(mlp, dataset)
trainer.train(n_iters=25000, plot_every=200, print_every=1000)
trainer.saveModel()

def getPrediction(Input):
    topi, topv = Input.flatten().topk(1)
    return topv.item()

with torch.no_grad():
    posNum = 0
    for index in range(dataset.numSamples):

        signal = dataset.ModelInputs[index]
        realRoom = getPrediction(dataset.ModelOutputs[index])
        realRoom = dataset.posNames[int(realRoom)]

        predictRoom = getPrediction(trainer.mlp(signal))
        predictRoom = dataset.posNames[int(predictRoom)]

        print(index, "realRoom:", realRoom, "    predictRoom:", predictRoom)
        if realRoom==predictRoom:
            posNum += 1
    
    print(posNum/dataset.numSamples)
