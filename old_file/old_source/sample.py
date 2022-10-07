import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from setting.setting import options

"""
loss = nn.CrossEntropyLoss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.empty(3, dtype=torch.long).random_(5)
output = loss(input, target)


"""

from torch import nn
import torch

loss = nn.CrossEntropyLoss()
input = torch.tensor([0.8, 0.1, 0.1]).unsqueeze(0)
target = torch.tensor(0).unsqueeze(0)
output = loss(input, target)



input_1 = torch.tensor([0.8, 0.1, 0.1]).unsqueeze(0)
input_2 = torch.tensor([0.8, 0.1, 0.1])

#print(input_1)
#print(input_2)


loss = nn.MSELoss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.randn(3, 5)
output = loss(input, target)
print(input)
print(input.shape)


print(target)
print(target.shape)