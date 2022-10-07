import pandas as pd
import numpy as np
import statistics

import step0_settings.utility as utility
from setting.setting import options

# logic: 3日前が 2/5、2日前が 4/5 or 5/5、1日前が2日前より良い and  1/5ではない


def logic5(file_name, table_len, start_table, table_number):

    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    columns = ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]
    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    #df_test = pd.DataFrame(data[0], columns=days, index=columns)
    #print(df_test)


    # 設定
    #  ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]
    check_table = table_len  # 全てのテーブルの長さ
    seq_length = 7 # 何日間のデータ範囲とするか
    check_data = 1  # "大当り回数" 
    check_data_t = 1 # "確変当"
    win_threshold_value = 20  # check_data_tが何を勝ちとするか ← 次の日の確変の合計が20以上をとなる確率


    results = []
    for table in range(check_table):
        pred_good = []


        y =data[table][check_data,:]
        t = data[table][check_data_t,:]
        
        seq_arrs, target_arrs = utility.sequence_data_logic1(y, t, seq_length)

        for seq_arr, target_arr in zip(seq_arrs, target_arrs):
            #if np.all(seq_arr < 20000) and target_arr >= win_threshold_value:
            if  seq_arr[0] <20000 and seq_arr[1] <20000 and seq_arr[2] > 20000 and target_arr >= win_threshold_value:
                #pred_good.append(target_arr[1])
                pred_good.append(1)
            elif seq_arr[0] <20000 and seq_arr[1] <20000 and seq_arr[2] > 20000 and target_arr < win_threshold_value:
                pred_good.append(0)

        sum_len = len(pred_good)
        if sum_len == 0:
            continue
        else:
            sum_value  = sum(pred_good)

            result = sum_value/sum_len
            results.append(result)

    probability = round(statistics.mean(results), 2)
    #print("確率：", round(statistics.mean(results), 2), "%")


    #print("-----------------------")
    #print("明日、上記ロジックに当てはまった台は以下")
    ### 上記ロジックに当てはまった、台を選定する

    target_table = []
    for i, table_no in enumerate(table_number):
        l = len(data[0][2])
        days =list(range(l))
        days = np.array(days) + 1
        days = days[::-1]
        df = pd.DataFrame(data[i], columns=days, index=columns)
        df = df.loc[:,seq_length:-1]
        df = df.loc["最大持ち玉"]
        values = df.values

        if  values[0] <20000 and values[1] <20000 and values[2] > 20000:
            target_table.append(table_no)

    #print(target_table)
    return probability, target_table


if __name__ == "__main__":

    predict_shop = "garo_izumi"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_len = option["table_len"]
    start_table = option["start_table"]

    table_number = list(range(start_table,start_table+table_len))
    probability, target_table = simple_logic(file_name, table_len, start_table, table_number)