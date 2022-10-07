import pandas as pd
import numpy as np
import re
import sys

import setting.setting as setting

##### scraping_robo.pyに踏襲済

shop_name = "daiku_tennouji_honkan"

# settingより取得
option = setting.options[shop_name]
file_name =option["file_name"]
table_len = option["table_len"]

# csv import 
path = "//Users/tomoyasu/dev/AIP/data/daiku_tennouji_honkan/time/20210829.csv"
df = pd.read_csv(path)

df = df[1:table_len+1]

# これまでと合わせる：["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]

# columns_name = ["no", "table_no", "履歴", "|", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
# df.columns = columns_name
# df = df.drop(['no','table_no' ,'履歴', '|', '詳細', 'チャンス中大当り確率'], axis=1)
# df = df.reset_index(drop=True)


columns_name = ["大当り回数", "時間", "スタート回数", "出玉数（継続数）"]
print(df)

"""
path = "/Users/tomoyasu/dev/AIP/data/daiku_tennouji_honkan/20210828.text"

with open(path, 'r', newline='') as file:
    data = re.sub(r's* ', ',', file.read())
    
#with open(path) as f:
 #   data = f.readlines()


data_str = "".join(map(str, data))
data_str = data_str.replace('履歴', '')
data_str = data_str.replace('詳細', '')
data_str = data_str.replace('|', '')
data_str = data_str.replace('累計スタート', '')
data_str = data_str.replace('大当たり回数', '')
data_str = data_str.replace('初当り回数', '')
data_str = data_str.replace('最高玉数', '')
data_str = data_str.replace('大当り確率', '')
data_str = data_str.replace('初当り確率', '')
data_str = data_str.replace('チャンス中', '')
data_str = data_str.replace('大当り回数 ', '')
data_str = data_str.replace('只今スタート', '')
print(data_str)
#for d in data_str:
 #   print(d)
"""