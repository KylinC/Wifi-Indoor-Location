from data import Dataset
from model import MLP, RNN
from train import MLPTrainer, RNNTrainer
import torch

dataset = Dataset()
mlp = MLP(dataset.numAP, dataset.numPos, layers=[512,512,512,256,256,256])
trainer = MLPTrainer(mlp, dataset)
trainer.train(n_iters=30000, plot_every=200, print_every=1000, learning_rate=0.005)
trainer.saveModel()

def getPrediction(Input):
    topi, topv = Input.flatten().topk(1)
    return topv.item()

def predictRoom(Input, dataset):
    topi, topv = Input.flatten().topk(1)

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





dataset = Dataset()
rnn = RNN(input_size = dataset.numAP, hidden_size = 512, output_size = dataset.numPos)
trainer = RNNTrainer(rnn, dataset)
trainer.train(n_iters=30000, plot_every=200, print_every=1000, learning_rate=0.005)
trainer.saveModel()

trainer.rnn = torch.load("result/rnn.pkl")
with torch.no_grad():
    posNum = 0
    for index in range(dataset.numSamples):

        signals, realRoom = dataset.sequenceExamples(seqLen=5)
        realRoom = getPrediction(realRoom)
        realRoom = dataset.posNames[int(realRoom)]

        hidden = trainer.rnn.initHidden()
        for i in range(signals.shape[0]):
            input = signals[i]
            output, hidden = trainer.rnn(input, hidden)

        predictRoom = getPrediction(output)
        predictRoom = dataset.posNames[int(predictRoom)]

        print(index, "realRoom:", realRoom, "    predictRoom:", predictRoom)
        if realRoom==predictRoom:
            posNum += 1
    
    print(posNum/dataset.numSamples)