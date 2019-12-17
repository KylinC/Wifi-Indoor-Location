import torch
import torch.nn as nn
from torch import optim
import time
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

