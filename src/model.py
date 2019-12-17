import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    '''
    基本的MLP模型
    input -> (1, 1, numAP)
    output -> (numRoom)
    '''
    def __init__(self, numAP, numRoom, layers = [64,32,16]):
        super(MLP, self).__init__()
        self.mlp = nn.Sequential()

        # numAP -> layers[0]
        self.mlp.add_module("Linear_0", nn.Linear(numAP, layers[0]))
        self.mlp.add_module("Relu_0", nn.ReLU(inplace=True))

        # layers[0] -> layers[-1]
        for li in range(1, len(layers)):
            self.mlp.add_module("Linear_%d" % li, nn.Linear(layers[li - 1], layers[li]))
            self.mlp.add_module("Relu_%d" % li, nn.ReLU(inplace=True))

        # layers[-1] -> numRoom
        self.mlp.add_module("Linear_output", nn.Linear(layers[-1], numRoom))
        self.softmax = nn.LogSoftmax(dim = 0)

    def forward(self, Input):
        output = self.mlp(Input.view(1,1,-1))
        output = self.softmax(output.flatten())
        return output

class RNN(nn.Module):
    '''
    基本的RNN模型
    input -> (1, numAP)
    '''
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=0)

    def forward(self, input, hidden):
        output, hidden = self.lstm(input.view(1,1,-1), hidden)
        output = self.fc(output.flatten())
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return (torch.zeros(1, 1, self.hidden_size),torch.zeros(1, 1, self.hidden_size))


if __name__ == "__main__":
    # Test MLP
    mlp = MLP(numAP = 10, numRoom = 3)
    input = torch.randn([1,1,10])
    output = mlp(input)

    rnn = RNN(input_size = 10, hidden_size = 256, output_size = 3)
    input = torch.randn([1,1,10])
    output, next_hidden = rnn(input, rnn.initHidden())