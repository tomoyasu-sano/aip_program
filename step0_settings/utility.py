import pandas as pd
import numpy as np
import sys
import os
import datetime

from step0_settings.setting import options

## make df from csv_files
### target: "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"
def make_df_from_csvfile(place, target):

    # データ取得に必要な項目を取得
    place = options[place]["place"]
    machine = options[place]["machine"]
    table_len = options[place]["table_len"]
    table_list = options[place]["table_list"]

    # csv file名の一覧を配列化
    file_path = f"./step1_scrapiing/data/{place}/{machine}"
    csv_files = sorted(os.listdir(file_path))

    # 日付のリスト
    date_list = []

    # 大当たり確率を格納するnp_array
    value_array = np.empty((0, table_len), int)

    # csv_file: 例) 20220907.csv
    for csv_file in csv_files:
        path = file_path + "/" + str(csv_file)
        df  = pd.read_csv(path,  index_col=0, engine='python')
        
        # 値がないものは0で一旦置き換える
        df = df.replace("--", 0)

        # 大当り確率と初当り確率は文字列のため
        df['大当り確率'] = df['大当り確率'].astype(int)
        df['初当り確率'] = df['初当り確率'].astype(int)

        # 大当たり確率のみ抽出
        jackpot_probability = df[target].values

        # 0は平均値で埋める
        jackpot_mean = int(np.mean(jackpot_probability[jackpot_probability != 0]))
        jackpot_probability[jackpot_probability == 0] =jackpot_mean 
    
        # 文字列と日付の交互性を確保するための処理
        str_date = csv_file.split(".")[0]
        str_year = str_date[0:4]
        str_month = str_date[4:6]
        str_day = str_date[6:8]
        str_dte = str_year + "-" + str_month + "-" + str_day # 文字列型 日付
        #dte = datetime.datetime.strptime(str_day, '%Y-%m-%d') # datetime型 日付  error+

        # 日付（文字列）と値を大当たり確率の値を格納
        date_list.append(str_dte)
        value_array = np.append(value_array, [jackpot_probability], axis=0)
        

    # 日付、テーブル台別の大当たり確率のdfを作成
    df = pd.DataFrame(value_array, columns=table_list, index=date_list)


    return df, date_list, machine, table_len, table_list

## logic1
def make_swquence_data(y, num_sequence):
        num_data = len(y)
        seq_data = []
        target_data = []

        for i in range(num_data - num_sequence):
            seq_data.append(y[i:i+num_sequence])
            #target_data.append(y[i+num_sequence:i+num_sequence+1])
            #label = y[i+num_sequence:i+num_sequence+1]

            #if label > win_threshold_value:
                #target_data.append([1])
            #else:
                #target_data.append([0])

        seq_arr = np.array(seq_data)
        #target_arr = np.array(target_data)
        return seq_arr

def sequence_data_logic1(y, t, num_sequence):
    num_data = len(y)
    seq_data = []
    target_data = []

    for i in range(num_data - num_sequence):
        seq_data.append(y[i:i+num_sequence])
        #target_data.append(y[i+num_sequence:i+num_sequence+1])
        label = t[i+num_sequence:i+num_sequence+1]
        target_data.append(label)

    seq_arr = np.array(seq_data)
    target_arr = np.array(target_data)
    return seq_arr, target_arr



## logic2
def sequence_data_logic2(y, num_sequence, threshold_1, threshold_2, threshold_3):
    num_data = len(y)
    seq_data = []
    target_data = []

    for no, i in enumerate(range(num_data - num_sequence)):
        seq_data.append(y[i:i+num_sequence])

        # thresholdの値によって４つに分ける
        label = y[i+num_sequence:i+num_sequence+1]
        #label = []

        #print(seq_data[0][0:3])
        day6_data = y[i:i+num_sequence]
        day4to6 = day6_data[0:3]
        day1to3 = day6_data[3:6]
        #print(day4to6)
        # 4-6日は平均より悪く、1-3日はthreshold_1より悪い　→　徐々によくなっている傾向
        if np.count_nonzero(day4to6 > threshold_2) >= 2 and np.all(day1to3>threshold_1) and label[0] < 100 :
            target_data.append(1)
        elif np.count_nonzero(day4to6 > threshold_2) >= 2 and np.all(day1to3>threshold_1) and label[0] > 100 :
            target_data.append(0)
        else:
            target_data.append(9)
        
    seq_arr = np.array(seq_data)
    target_arr = np.array(target_data)
    return seq_arr, target_arr



## logic3
def sequence_data_logic3(y, t, num_sequence, win_threshold_value):
    num_data = len(y)
    seq_data = []
    target_data = []

    for no, i in enumerate(range(num_data - num_sequence)):
        seq_data.append(y[i:i+num_sequence])
        label = t[i+num_sequence:i+num_sequence+1]

        value = y[i:i+num_sequence][0]
        

        # thresholdの値によって４つに分ける
        if 10 < value < 400 and label < win_threshold_value:
            target_data.append(1)
        elif 10 < value < 400 and label > win_threshold_value:
            target_data.append(0)
        else:
            target_data.append(9)

    
    seq_arr = np.array(seq_data)
    target_arr = np.array(target_data)
    return seq_arr, target_arr
    






