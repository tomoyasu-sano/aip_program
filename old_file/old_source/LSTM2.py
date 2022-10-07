import datetime
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
#from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import statistics
import torch
torch.manual_seed(0)  #重み初期値の固定
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
#from torchvision import datasets, transforms
#from torch.utils.data import DataLoader

from setting.setting import options
np.set_printoptions(suppress=True)

### LSTM2：台ごとの複数のデータでLSTMを組む

"""
備忘録
内容
・ある台の時系列データ（8変数）を●日間のシークエンスデータに変換（2次元）
・ある台ごとのLSTMでモデルを作る
・それを複数台分適用
・最終的にシークエンスデータが入力値となり、その次の日を予測するモデル

→性能が悪いため、一旦断念。


"""




#####7日寛データならいいが、8日間にしたときにerror　予測データの時かな？あとR2じょうが悪すぎる



# import data
def import_data(file_name):
    data_arrays = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy')
    return data_arrays

# 標準化（平均０, 標準偏差1）
def make_swquence_data(y, num_sequence, data_variable):
    #all_seq_data = []
    #all_target_data = []
    all_seq_data = np.empty([0,num_sequence])
    all_target_data = np.empty([0,num_sequence])

    for l in range(len(y)):
        seq_data = []
        target_data = []
        num_data = len(y[0])

        for i in range(num_data - num_sequence):
            s_data = y[l][i:i+num_sequence]
            t_data = y[l][i+num_sequence:i+num_sequence+1]

            # 標準化（numpy → 2次元 → 標準化 → 1次元 → リスト）
            #s_data = np.array(s_data)
            #s_data = s_data.reshape(7,-1)
            #s_data = ss.fit_transform(s_data)
            #s_data = s_data.reshape(-1)
            #s_data = s_data.tolist()

            seq_data.append(s_data)
            target_data.append(t_data)

        seq_data = np.array(seq_data)
        target_data = np.array(target_data)

        all_seq_data = np.append(all_seq_data, seq_data, axis=0)
        all_target_data = np.append(all_target_data, target_data)

    all_seq_data = all_seq_data.reshape(data_variable, -1, num_sequence)
    all_target_data = all_target_data.reshape(data_variable, -1)
    
    return all_seq_data, all_target_data


class LSTM(nn.Module):
    def __init__(self, dim_i, hidden_size):  #input_size: 入力次元
        super().__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=dim_i, hidden_size=hidden_size)
        self.linear = nn.Linear(self.hidden_size,dim_i)  # アウトプットの次元を指定

    def forward(self, x):
        x, _ = self.lstm(x) #リターン: (シークエンス, 隠れ層やセルの状態のタプル）
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

#########################


def make_models_predict_tomorrow_data(make_model, file_name, start_table):
    data_arrays = import_data(file_name)
    check_tables = data_arrays.shape[0]
    d_today = datetime.date.today()

    results = {}

    for check_table in range(check_tables):
    #for check_table in range(1):
        y = data_arrays[check_table]
        ss = preprocessing.StandardScaler()
        y = ss.fit_transform(y)

        data_variable = y.shape[0]  # 8種類の変数を利用する = 8次元 = input_size
        
        ##### 設定
        seq_length = 10 # 何日間のデータのシークエンスにしたいか
        y_seq, y_target = make_swquence_data(y, seq_length, data_variable)


        num_test = int(y_seq.shape[1]*0.8) # 8割学習データ
        #num_test =0

        # 例） y_seq(8,13,7) → y_seq_train(8,10,7)にする感じ
        y_seq_train = y_seq[:, 0:num_test, :]
        y_seq_test = y_seq[:, num_test:y_seq.shape[1], :]
        y_target_train = y_target[:, 0:num_test]
        y_target_test = y_target[:, num_test:y_seq.shape[1]]


        # 訓練、テストデータをpytorch化
        y_seq_t = torch.FloatTensor(y_seq_train)
        y_target_t = torch.FloatTensor(y_target_train)
        
        y_seq_test = torch.FloatTensor(y_seq_test)
        y_target_test = torch.FloatTensor(y_target_test)


        # LSTM入力 : （シークエンス長, バッチサイズ, input_size）　の順番
        y_seq_t = y_seq_t.permute(2,1,0)
        y_target_t = y_target_t.permute(1,0)

        y_seq_test = y_seq_test.permute(2,1,0)
        y_target_test = y_target_test.permute(1,0)

        #y_seq_t = y_seq_t.unsqueeze(dim=-1) # 40*450 → 40*450*1  最後に入力次元数=1が必要
        #y_target_t = y_target_t.unsqueeze(dim=-2) #



        dim_i = data_variable
        model=LSTM(dim_i, hidden_size=100) 
    
        #criterion = nn.MSELoss()
        criterion = nn.CrossEntropyLoss()
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)



        num_epochs =300
        losses =[]

        if make_model == True:
            for epoch in range(num_epochs):
                optimizer.zero_grad()
                output = model(y_seq_t)
                #rint(output.size())
                #print(y_target_t.size())
                loss = criterion(output, y_target_t)
                loss.backward()
                losses.append(loss.item())
                optimizer.step()

                #print(f"epoch:{epoch}, loss:{loss.item()}")
        

            # モデル保存
            torch.save(model.state_dict(), f'/Users/tomoyasu/dev/AIP/models/{file_name}/{d_today}_{check_table+start_table}.pth')

        # テストデータに対して予測する
        output_test = model(y_seq_test)

        output_test = output_test.detach().numpy()
        y_target_test = y_target_test.detach().numpy()

        #output_test = ss.inverse_transform(output_test)
        #y_target_test = ss.inverse_transform(y_target_test)

        metrics = np.sqrt(mean_squared_error(y_target_test, output_test))
        r2score = r2_score(y_target_test, output_test)  
        #print("metrics:", metrics)
        print("r2_score:",r2score)

    #描画
    #plt.plot(losses)
    #plt.show()

    ##################################################################

    ## 新しいデータにおける、性能評価が必要（直近7日間のデータを取得する必要がある）
        test_data = data_arrays[check_table]
        #print("test_data:", test_data.shape)
        #print(test_data.shape) # (8,11)
        range_last = test_data.shape[1]
        #print(range_last)
        #print(range_last-seq_length-1)
        #test_data = test_data[:, range_last-seq_length-1:range_last]   # 7日間のシークエンスだが、過去8日分が必要...理解不足]
        test_data = test_data[:, range_last-seq_length-1:range_last]   # 7日間のシークエンスだが、過去8日分が必要...理解不足]
        #print("test_data:", test_data)
    
        # 標準化とシークエンスデータ化
        #s = preprocessing.StandardScaler()
        test_data = ss.fit_transform(test_data)
        y_seq, y_target = make_swquence_data(test_data, seq_length, data_variable)
        y_seq_t = torch.FloatTensor(y_seq)
        y_seq_t = y_seq_t.permute(2,1,0)


        # モデル読み込み
        model_state_dict = LSTM(dim_i, hidden_size=100) 
        model_state_dict.load_state_dict(torch.load(f"/Users/tomoyasu/dev/AIP/models/{file_name}/{d_today}_{check_table+start_table}.pth"), strict=False)
        y_pred = model_state_dict(y_seq_t)

        # 標準化を元に戻す
        y_pred = y_pred.detach().numpy()
        #print(y_pred.shape)
        ###### 8日間以外の日でerror まだ直っていない
        #y_pred = ss.inverse_transform(y_pred)

        
        #print(y_pred.shape)
        ########8日間以外の日でerror まだ直っていない なので、ラウンドせず。
        #y_pred = np.round(y_pred, 0)
        #print(y_pred)

        y_pred = y_pred[0][6] # ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"] # 0~7
        #result = {"table":check_table, "score":y_pred}  
        table_no = check_table + start_table
        results[table_no] = y_pred

    print(results)
    N = 3
    recommend_tables = {}
    lists = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for i in range(N):
        recommend_tables[lists[i][0]] = lists[i][1]
    print(recommend_tables)
    recommend_tables = list(recommend_tables.keys())

    return recommend_tables



if __name__=='__main__':
    from setting.setting import options

    options_name = "garo_test"

    ## 読み込むモデル（場所 / 機種）を設定
    option = options[options_name]
    file_name = option["file_name"]
    #name = option["name"]
    table_len = option["table_len"]
    start_table = option["start_table"] #　変更に注意

    # 実行 → モデルを作る場合はmake_model=True

    recommend_tables = make_models_predict_tomorrow_data(make_model=True, file_name=file_name, start_table=start_table) 
    print(recommend_tables)


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