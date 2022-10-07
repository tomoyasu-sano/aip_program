import pandas as pd
import numpy as np
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from setting.setting import options

# logic: 1週間の平均をとり、調子の悪い下位25%は打たない


def logic3(file_name, table_len, table_list):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/save_data/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    #columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  #0~7
    columns = ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]
    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    #df_test = pd.DataFrame(data[0], columns=days, index=columns)
    #print(df_test)
    
    scores = []
    recommend_tables = []
    for table in range(table_len):
    #table_len = 1
    #for table in range(table_len):
        df = pd.DataFrame(data[table], columns=days, index=columns)
        df = df.iloc[:, -7::]  #7日間の平均をとる 
    
        df = df.loc["大当り回数"]
        score = df.mean(axis=0)

        scores.append(round(score,2))
                
    
    print(scores)
    print("-----------------")

    quantile_value = round(pd.DataFrame(scores).quantile([0.25]),2)
    print(quantile_value)
    quantile_value = quantile_value.values
    for table, s in zip(table_list,scores):
        #print(table, ":", s)
        if s > quantile_value:
            recommend_tables.append(table)
        else:
            print(f"こちらのテーブルは1週間で調子の悪い台です：{table}")
    return recommend_tables

if __name__ == "__main__":

    predict_shop = "garo_rakuen_nannba"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_list = option["table_list"]
    table_len = len(table_list)
    #table_number = list(range(start_table,start_table+table_len))

    recommend_tables = logic3(file_name, table_len, table_list)
    



import pandas as pd
import numpy as np
import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from step0_settings.setting import options

# logic: 過去2日以内に外れ値がある場合、打たない
# - 外れ値定義：総大当たりが95%以上


"""
- target: 大当たり確率
- logic
    - 1週間の平均をとり、調子の悪い下位25%は打たない
- description
    - 
    - 
        - 打つべき: 1
        - 打つべきではない: 0
"""


def logic2(places):
    for place in places:
        print("place: ", place)

        # データ取得に必要な項目を取得
        place = options[place]["place"]
        machine = options[place]["machine"]
        table_len = options[place]["table_len"]
        table_list = options[place]["table_list"]
  

    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/save_data/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    columns = ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]

    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    df_test = pd.DataFrame(data[0], columns=days, index=columns)
    #print(df_test)
    

    scores = []
    for table in range(table_len):
        df = pd.DataFrame(data[table], columns=days, index=columns)

        # 外れ値検出
        df = df.loc["大当り回数"]
        score = round(df.quantile(0.95),1)
       
        scores.append(score)
        #print(score)

    ## socresの平均ではなく、scoresのさらに75%以上の外れ値 ← 35程度を外れ値としたい（店によって異なる）
    df_scores = pd.DataFrame(scores)
    value = round(df_scores.quantile(0.6),1).values[0]

    ## 次の日予測
    target_tables = []
    for i, table_no in enumerate(table_list):
        df = pd.DataFrame(data[i], columns=days, index=columns)

        # 前日の指標
        df_yesterday1 = df[1].loc["大当り回数"]       
        # 前前日の指標
        df_yesterday2 = df[2].loc["大当り回数"]    

        # 明日打つべきか確認
        if value < df_yesterday1 or  value < df_yesterday2:
            print(f"2日以内に外れ値が含まれています：{table_no}は明日は打たない方が良いです")
            continue

        else:
            #print("両日とも外れ値はありません。打つ対象にします")
            target_tables.append(table_no)


    #print(target_tables)
    return target_tables

    
if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店


    logic2(places)
