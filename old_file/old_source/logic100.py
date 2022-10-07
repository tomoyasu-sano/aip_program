import pandas as pd
import numpy as np

import step0_settings.utility as utility
from setting.setting import options

# logic: 前日最終スタートが10以下または450以上は次の日の初当たり確率が大きいと仮定

def yesterday_start_logic(file_name, table_len, start_table, table_number):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  #0~7

    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    df_test = pd.DataFrame(data[0], columns=days, index=columns)
    #print(df_test)


    # 設定
    #  ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"] # 0~7
    check_table = table_len  # 全てのテーブルの長さ
    seq_length = 1 # 何日間のデータ範囲とするか
    check_data = 5  
    check_data_t = 7 
    win_threshold_value = 330  # check_data_tが何を勝ちとするか 
    #data = pd.DataFrame(data[0], columns=columns)


    wins = []
    loses = []

    for table in range(check_table):

        y =data[table][check_data,:]
        t = data[table][check_data_t,:]


        seq_arrs, target_arrs = utility.sequence_data_logic3(y, t, seq_length, win_threshold_value)

        win = np.sum(target_arrs==1)
        lose =np.sum(target_arrs==0)

        wins.append(win)
        loses.append(lose)


    sum_win = sum(wins)
    sum_lose = sum(loses)
    probability = round(sum_win / (sum_win+sum_lose), 2)
    #print("確率：", probability)



    #print("-----------------------")
    #print("明日、上記ロジックに当てはまった台は以下")
    ### 上記ロジックに当てはまった、台を選定する
    table_number = list(range(start_table,start_table+table_len))
    target_table = []

    for i, table_no in enumerate(table_number):
        l = len(data[0][2])
        days =list(range(l))
        days = np.array(days) + 1
        days = days[::-1]
        df = pd.DataFrame(data[i], columns=days, index=columns)

        df = df.loc[:,seq_length:-1]
        df = df.loc["初当たり確変"]
        value = df.values

        if 10 < value[0] < 400:
            target_table.append(table_no)

    #print(target_table)
    return probability, target_table
