import datetime 
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from step0_settings.setting import options


# logic: お店ごとの、全ての期間における平均の当たる時間帯と、テーブルごとの当たる時間帯を計測


def logic4(file_name, table_len, table_list):
    
    columns = ["大当り回数","時間" ,"スタート回数"]

    dict_time={9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0}
    dict_times_tables = {}

    day_of_week_dict = {
        'Monday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0},
        'Tuesday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0}, 
        'Wednesday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0}, 
        'Thursday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0},
        'Friday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0}, 
        'Saturday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0},
        'Sunday':{9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0}
        }

    for tl in table_list:
        file_path = f'/Users/tomoyasu/dev/AIP/save_data/data/{file_name}/time/table_{tl}'

        dict_times_table = {}
        
        # 複数のcsvに対応
        dict_hit_hours = {10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0}

        # そのお店の機種、曜日別 大当たり数取得
        # day_of_week_dict = {'Monday':0, 'Tuesday':0, 'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0, 'Sunday':0}
        # date = datetime.date(2001, 1, 2)
        # day_of_week = date.strftime('%A') # => 'Tuesday'


        csv_files = sorted(os.listdir(file_path))
        for i in csv_files:
            df  = pd.read_csv(file_path + "/" + str(i), index_col=0, engine='python')
            df = df.replace("--", 0)
            #df = df.drop("table_no", axis=1)
            series_time =pd.to_datetime(df['時間'])
            df = df.drop("時間", axis=1)
            df = df.drop(1, axis=0)
            df["時間"] = series_time

            ## 曜日の獲得
            day = i.split(".")[0]
            date = datetime.datetime.strptime(day, '%Y%m%d')
            day_of_week = date.strftime('%A') # => 'Tuesday'

            dict_hit_hour= df['時間'].dt.hour.value_counts().to_dict()
            
            ## 個々のテーブルに対し、複数のcsvを読み込み、時間帯ごとの大当たり数を加算する
            for k, v in dict_hit_hour.items():
                if k in dict_hit_hours.keys():
                    table_value = dict_hit_hour[k]
                    dict_hit_hours[k] += table_value

                ## お店の機種、曜日別 大当たり数取得
                if day_of_week in day_of_week_dict.keys() and k != 0:
                    day_of_week_dict[day_of_week][k] += table_value
                    
            
            ## 機種別の時間帯後のとの大当たり数を加算する
            for k, v in dict_hit_hour.items():
                if k in dict_time.keys():
                    time_value = dict_hit_hour[k]
                    dict_time[k] += time_value

            #print(day_of_week,  "table:",tl, "時間帯", dict_hit_hour,)


        #print(dict_times_table)
        dict_times_tables[tl] = dict_hit_hours

    #print(dict_times_tables)
    #print(day_of_week_dict)
    
    best_dict_time = sorted(dict_time.items(), key=lambda x:x[1], reverse=True)
    ## 当たる時間帯ベスト3を抽出
    best_time1 =best_dict_time[0][0]
    best_time2 =best_dict_time[1][0]
    best_time3 =best_dict_time[2][0]
    best_times = [best_time1,best_time2, best_time3]

    
    """
    #グラフ化
    x_time = list(dict_time.keys())
    y_value = list(dict_time.values())

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_time, y_value)
    plt.show()
    """

    print("logic4：正常に処理を終えました")
    return best_times, dict_times_tables, day_of_week_dict
    
if __name__ == "__main__":

    predict_shop = "garo_rakuen_nannba"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_list = option["table_list"]
    table_len = len(table_list)
    best_times, dict_time_tables, day_of_week_dict = logic4(file_name, table_len, table_list)

    #print(target_tables)

    #dict_time_tables : {1185: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1186: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1187: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1188: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1189: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1190: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1191: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1192: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1193: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1194: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1195: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1196: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1197: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1198: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1199: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1200: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1201: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1202: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1203: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1204: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1205: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1206: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1207: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}, 1208: {19: 13, 12: 4, 17: 3, 20: 1, 16: 1, 15: 1}}