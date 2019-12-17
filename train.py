import torch
import torch.nn as nn
from torch import optim
import time
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from data import Dataset
from model import MLP, RNN

# helper functions
def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

class MLPTrainer():
    def __init__(self, mlp, dataset):
        self.mlp = mlp
        self.dataset = dataset

    def train(self, n_iters = 1000, print_every=100, plot_every=20, learning_rate=0.01):
        plot_loss = 0
        print_loss = 0
        all_losses = []
        optimizer = optim.SGD(self.mlp.parameters(), lr=learning_rate)

        start = time.time()
        for iter in range(1, n_iters+1):
            optimizer.zero_grad()
            # get a training example
            signal, room = self.dataset.example()
            
            # get prediction and loss
            loss = 0
            prediction = self.mlp(signal)
            loss += self.__getNLLLoss(prediction, room)

            # update parameter
            loss.backward()
            optimizer.step()

            # show the process
            print_loss += loss
            if iter % print_every == 0:
                print('%d %d%%'%(iter, iter / n_iters * 100), ", Time: ", timeSince(start), ", Loss: ", print_loss/print_every)
                print_loss = 0

            plot_loss += loss
            if iter % plot_every == 0:
                all_losses.append(plot_loss / plot_every)
                plot_loss = 0

        plt.figure()
        plt.plot(all_losses)

    def saveModel(self, filePath = "result/mlp.pkl"):
        torch.save(self.mlp, filePath)

    def __getNLLLoss(self, pred, target):
        criterion = nn.NLLLoss()
        _, targetNum = target.flatten().topk(1)
        return criterion(pred.view(1,-1), targetNum)   



class RNNTrainer():
    def __init__(self, rnn, dataset):
        self.rnn = rnn
        self.dataset = dataset

    def train(self, n_iters = 1000, print_every=100, plot_every=20, learning_rate=0.01, ratio=0.9):
        plot_loss = 0
        print_loss = 0
        all_losses = []
        optimizer = optim.SGD(self.rnn.parameters(), lr=learning_rate)

        start = time.time()
        for iter in range(1, n_iters+1):
            optimizer.zero_grad()
            # get a training example
            signals, room, _ = self.dataset.sequenceExamples(seqLen=5, ratio=ratio)
            
            # get prediction and loss
            loss = 0
            hidden = self.rnn.initHidden()
            for i in range(signals.shape[0]):
                input = signals[0]
                output, hidden = self.rnn(input, hidden)
            loss += self.__getNLLLoss(output, room)

            # update parameter
            loss.backward()
            optimizer.step()

            # show the process
            print_loss += loss
            if iter % print_every == 0:
                print('%d %d%%'%(iter, iter / n_iters * 100), ", Time: ", timeSince(start), ", Loss: ", print_loss/print_every)
                print_loss = 0

            plot_loss += loss
            if iter % plot_every == 0:
                all_losses.append(plot_loss / plot_every)
                plot_loss = 0

        plt.figure()
        plt.plot(all_losses)

    def saveModel(self, filePath = "result/rnn.pkl"):
        torch.save(self.rnn, filePath)

    def __getNLLLoss(self, pred, target):
        criterion = nn.NLLLoss()
        _, targetNum = target.flatten().topk(1)
        return criterion(pred.view(1,-1), targetNum)   


if __name__=="__main__":
    dataset = Dataset()
    mlp = MLP(dataset.numAP, dataset.numPos, layers=[512,512,256,256,128,128])
    trainer = MLPTrainer(mlp, dataset)
    trainer.train(n_iters=40000, plot_every=200, print_every=200, learning_rate=0.001)
    trainer.saveModel(filePath="result/mlp_6.pkl")

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
    rnn = RNN(input_size = dataset.numAP, hidden_size = 512, output_size = dataset.numPos, numLayers=1)
    trainer = RNNTrainer(rnn, dataset)
    trainer.train(n_iters=20000, plot_every=200, print_every=100, learning_rate=0.01, ratio=0.8)
    trainer.saveModel(filePath="result/rnn_random80.pkl")

    dataset = Dataset()
    rnn = RNN(input_size = dataset.numAP, hidden_size = 512, output_size = dataset.numPos, numLayers=1)
    trainer = RNNTrainer(rnn, dataset)
    trainer.train(n_iters=20000, plot_every=200, print_every=100, learning_rate=0.001, ratio=1.0)
    trainer.saveModel(filePath="result/rnn_random100.pkl")

    trainer.rnn = torch.load("result/rnn_random80.pkl")
    with torch.no_grad():
        posNum = 0
        for index in range(dataset.numSamples):

            signals, realRoom, _ = dataset.sequenceExamples(seqLen=5, ratio=0.8)
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

    trainer.rnn = torch.load("result/rnn_random100.pkl")
    with torch.no_grad():
        posNum = 0
        for index in range(dataset.numSamples):

            signals, realRoom, _ = dataset.sequenceExamples(seqLen=5, ratio=1.0)
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