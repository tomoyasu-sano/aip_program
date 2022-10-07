import pandas as pd
import numpy as np

import step0_settings.utility as utility
from setting.setting import options

# 平均値の確認


def stat3(file_name, table_len, table_list):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    columns = ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]
    
    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    
    scores = []
    recommend_tables = []

    for table, table_no in zip(range(table_len), table_list):
    #table_len = 1
    #for table in range(table_len):
        df = pd.DataFrame(data[table], columns=days, index=columns)
        #df = df.iloc[:, -7::]  #7日間の平均をとる 
    
        # 7, 14, 21, 28

        df = df.loc["大当り回数"]
        score = df.mean(axis=0)

        print(table_no, ":",score )
        print("-----------------")

        scores.append(round(score,2))
                
    
    #print(scores)


    # quantile_value = round(pd.DataFrame(scores).quantile([0.25]),2)
    # print(quantile_value)
    # quantile_value = quantile_value.values
    # for table, s in zip(table_list,scores):
    #     #print(table, ":", s)
    #     if s > quantile_value:
    #         recommend_tables.append(table)
    #     else:
    #         print(f"こちらのテーブルは1週間で調子の悪い台です：{table}")
    # return recommend_tables

if __name__ == "__main__":

    predict_shop = "garo_rakuen_nannba"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_list = option["table_list"]
    table_len = len(table_list)
    #table_number = list(range(start_table,start_table+table_len))

    recommend_tables = stat3(file_name, table_len, table_list)
    
