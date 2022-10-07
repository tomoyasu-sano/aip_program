

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from setting.setting import options


## 読み込むモデル（場所 / 機種）を設定
option = options["garo_test"]
file_name = option["file_name"]
table_len = option["table_len"]
start_table = option["start_table"]


# データを読み込み / 可視化
data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy')
columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  

# dataを確認する時使用する
l = len(data[0][2])
days =list(range(l))
days = np.array(days) + 1
days = days[::-1]
df_test = pd.DataFrame(data[0], columns=days, index=columns)
#print(df_test)


# 3次元を2次元データに
data = data.transpose(1,0,2)
data_2d = np.resize(data, (len(data[0]),len(data[1])*len(data[2][0])))

# 平均を追加
df = pd.DataFrame(data_2d)
mean = round(df.mean(axis='columns'),0)
df["平均"] = mean


np.set_printoptions(np.inf)
np.set_printoptions(threshold=np.inf)
#df.index =columns
print(df)
