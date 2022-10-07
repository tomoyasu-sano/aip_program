import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F

num_layers=3
num_hyperparams=4
batch = 1
hidden_size = 20
rnn = nn.LSTM(input_size=num_hyperparams, hidden_size=hidden_size, num_layers=num_layers)

input = Variable(torch.randn(1, batch, num_hyperparams)) # (seq_len, batch, input_size)
print(input)
h0 = Variable(torch.randn(num_layers, batch, hidden_size)) # (num_layers, batch, hidden_size)
c0 = Variable(torch.randn(num_layers, batch, hidden_size))
output, hn = rnn(input, (h0, c0))
affine1 = nn.Linear(hidden_size, num_hyperparams)

#ipdb.set_trace()
print(output.size())
print(h0.size())