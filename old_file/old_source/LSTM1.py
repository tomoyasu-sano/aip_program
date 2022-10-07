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

## 読み込むモデル（場所 / 機種）を設定
option = options["garo_test"]
file_name = option["file_name"]
#name = option["name"]
table_len = option["table_len"]

# import data
data_arrays = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy')

#  ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"] # 0~7
# 1台のデータの可視化
check_data = 3
check_table = 1

data = data_arrays[check_table][check_data,:]



#win_threshold_value=10000
y = data_arrays[check_table][check_data,:]
#y = data_arrays[check_table][1:3,:]
#print("y:", len(y))
#print(y)
#print(y.shape)

def make_swquence_data(y, num_sequence):
    num_data = len(y)
    seq_data = []
    target_data = []

    for i in range(num_data - num_sequence):
        seq_data.append(y[i:i+num_sequence])
        target_data.append(y[i+num_sequence:i+num_sequence+1])
        #label = y[i+num_sequence:i+num_sequence+1]

        #if label > win_threshold_value:
            #target_data.append([1])
        #else:
            #target_data.append([0])

    seq_arr = np.array(seq_data)
    target_arr = np.array(target_data)
    return seq_arr, target_arr


seq_length = 7 # 何日間のデータのシークエンスにしたいか
y_seq, y_target = make_swquence_data(y, seq_length)
#print(y_seq.shape)
#print(y_seq)


num_test = 3
y_seq_train = y_seq[: -num_test]
y_seq_test = y_seq[-num_test:]
y_target_train = y_target[:-num_test]
y_target_test = y_target[-num_test:]


y_seq_t = torch.FloatTensor(y_seq_train)
y_target_t = torch.FloatTensor(y_target_train)

# LSTM入力 : （シークエンス長, バッチサイズ, input_size）　の順番
y_seq_t = y_seq_t.permute(1,0)
y_target_t = y_target_t.permute(1,0)

y_seq_t = y_seq_t.unsqueeze(dim=-1) # 40*450 → 40*450*1  最後に入力次元数=1が必要
y_target_t = y_target_t.unsqueeze(dim=-1) #

class LSTM(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_size)
        self.linear = nn.Linear(self.hidden_size,1)

    def forward(self, x):
        x, _ = self.lstm(x) #リターン: (シークエンス, 隠れ層やセルの状態のタプル）
        #print("x.shape:", x.shape)
        #print("x.size:", x.size())
        #print("x:",x)
        
        x_last = x[-1] # シークエンスの最後の値を取得
        #print("x_last.shape:", x_last.shape)
        #print("x_last.size:", x_last.size())
        #print("x_last:",x_last)

        x = self.linear(x_last)
        #print("x:", x)
        #print("x.shape:", x.shape)
        #print("x.shape:", x.size())
        return x

model=LSTM(hidden_size=100)
#criterion = nn.MSELoss()
criterion = nn.CrossEntropyLoss()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)



num_epochs = 100
losses =[]

for epoch in range(num_epochs):
    optimizer.zero_grad()
    output = model(y_seq_t)
    print(output.size())
    print(y_target_t.size())
    loss = criterion(output, y_target_t)
    loss.backward()
    losses.append(loss.item())
    optimizer.step()

    print(f"epoch:{epoch}, loss:{loss.item()}")

plt.plot(losses)
plt.show()


"""
# 学習データセット設定
seq_length = 3 # 何日ごとの時系列データにするか
win_threshold_value = 10000  # どこから勝ちとするか

def make_swquence_data(data, num_sequence):
    num_data = len(data)
    seq_data = []
    target_data = []

    for i in range(num_data - num_sequence):
        seq_data.append(data[i:i+num_sequence])
        label = data[i+num_sequence:i+num_sequence+1]
        if label > win_threshold_value:
            target_data.append(1)
        else:
            target_data.append(0)

    seq_arr = np.array(seq_data)
    target_arr = np.array(target_data)
    return seq_arr, target_arr


seq_arr, target_arr = make_swquence_data(data, seq_length)

# 訓練とテストデータに分割
num_test = 3

y_seq_train = seq_arr[: -num_test]
y_seq_test = seq_arr[-num_test:]
y_target_train = target_arr[:-num_test]
y_target_test = target_arr[-num_test:]

y_target_train = y_target_train[:, np.newaxis]
y_target_test = y_target_test[:, np.newaxis]


# pytorchのテンソル化
y_seq_t = torch.FloatTensor(y_seq_train)
y_target_t = torch.FloatTensor(y_target_train)


# モデル
class LSTM(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_size)
        self.linear = nn.Linear(self.hidden_size,2)

    def forward(self, x):
        x, _ = self.lstm(x) #シークエンス, タプル（隠れ層やセルの状態）
        x_last = x[-1] # シークエンスの最後の値を取得
        x = self.linear(x_last)
        return x

# 学習
model=LSTM(3)
print(model)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


# LSTMのinput: seqence, batch_size, input_size

y_seq_t = y_seq_t.permute(1,0)
y_target_t = y_target_t.permute(1,0)
y_seq_t = y_seq_t.unsqueeze(dim=-1) #40*450*1 ⇨40*450 その反対
y_target_t = y_target_t.unsqueeze(dim=-1)



#　学習
num_epochs = 30
losses =[]

for epoch in range(num_epochs):
    optimizer.zero_grad()
    output = model(y_seq_t)
    loss = criterion(output, y_target_t)
    loss.backward()
    losses.append(loss.item())
    optimizer.step()
    if epoch*10==0:
        print(f"epoch:{epoch}, loss:{loss.item()}")

"""

##予測


"""
y_seq_test_t = torch.FloatTensor(y_seq_test)
y_seq_test_t = y_seq_test_t.permute(1,0)
y_seq_test_t = y_seq_test_t.unsqueeze(dim=-1)


y_pred = model(y_seq_test_t)

plt.plot(x,y)
plot.plt(np.arange(490,500), y_pred.detach())
plt.xlim([450,500])
"""

"""
# transformの設定
trans1 = transforms.ToTensor()
trans2 = transforms.Compose([transforms.ToTensor()])

class Mydatasets(object):
    def __init__(self, transform1 = None, transform2 = None):
        self.transform1 = transform1
        self.transform2 = transform2

        self.data = data
        self.label = [1, 1, 0, 0, 0, 1, 0]

        self.datanum = len(data)

    def __len__(self):
        return self.datanum

    def __getitem__(self, idx):
        out_data = self.data[idx]
        out_label = self.label[idx]

        if self.transform1:
            out_label = self.transform1(out_label)

        if self.transform2:
            out_data = self.transform2(out_data)

        return out_data, out_label


#dataset = Mydatasets('自分のpath', transform1=trans1, transform2=trans2, train=True)
dataset = Mydatasets(transform1=trans1, transform2=trans2)
print(len(dataset))
print(dataset)

# datasetをdataloaderへ
trainloader = torch.utils.data.DataLoader(dataset, batch_size = 1, shuffle = True)
print(trainloader)

# データの中身確認
"""



"""
# １変数のデータを取得
print(data.shape)
print(data)

inp_dim = 0
train_k, test_k = train_test_split(data, test_size = 0.3, shuffle=True)
train = torch.zeros((len(train_k), inp_dim))
test = torch.zeros((len(test_k), inp_dim))

df_dic = {}
for n, k in enumerate(train_k):
    nd_cast = df_dic[k].values.astype(np.float32)
    train[n] =  torch.from_numpy(nd_cast).clone()
for n, k in enumerate(test_k):
    nd_cast = df_dic[k].values.astype(np.float32)
    test[n] = torch.from_numpy(nd_cast).clone()

"""

"""
seq_len = 3 #何日分の連続データとしたいか？
#データ整形
sequence_length = seq_len + 1   # 配列の正規化の行いやすくするため
result = []

for index in range(len(data) - sequence_length): #4172 - 51 =4121
    d = data[index: index + sequence_length]  #最初 data[0:5]のデータを取得
    #print(d)
    result.append(d)




# データの正規化 
normalised_data = []
for window in result:
    normalised_window = [((float(p) / float(window[0])) - 1) for p in window] 
    normalised_data.append(normalised_window)

result = np.array(normalised_data)
print(result)

"""