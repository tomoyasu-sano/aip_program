import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from setting.setting import options

## 相関係数を確認し、0.5以上ある相関係数を抽出

predict_shop = "garo_rakuen_nannba"

option = options[predict_shop]
file_name =option["file_name"]
table_len = option["table_len"]
start_table = option["start_table"]
table_number = list(range(start_table,start_table+table_len))

data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
columns = ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]

data = data.transpose(1, 0, 2)
data = data[1]

df = pd.DataFrame(data, index=table_number).T.astype(np.float64)
df_corr = df.corr()

positive_corr = df_corr[(df_corr > 0.5) & (df_corr < 1)].stack()
negative_corr = df_corr[(df_corr < -0.5) & (df_corr > -1)].stack()

print(positive_corr)
print(negative_corr)


## ヒートマップ
#sns.heatmap(df_corr, vmax=1, vmin=-1, center=0)

## 保存 / 表示
#plt.savefig("/Users/tomoyasu/dev/AIP/analitics/")
#plt.show()

