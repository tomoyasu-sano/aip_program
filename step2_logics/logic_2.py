import pandas as pd
import numpy as np
import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from step0_settings.setting import options


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


def run_logic_2(places):
    target = "大当り確率"

    scores = []
    for place in places:
        df, date_list, machine, table_len, table_list = utility.make_df_from_csvfile(place, target)
        df = df.T

        # 7日間の平均をとる
        df = df.iloc[:, -7::] 
        scores = df.mean(axis=1)

        #ソートする
        scores_sort = scores.sort_values()

        #上位75%（=下位25%) 取り出し(列にサンプル数があって、25 %計算時に小数点以下切り捨て)
        scores_sort = scores_sort.head(int(len(scores)*0.75)) 

        # 1wで調子の悪い台を除外
        recommend_table = list(scores_sort.index)

        # 
        values = []
        for table in table_list:
            if table in recommend_table:
                values.append(1)
            else:
                values.append(0)
        df_result = pd.DataFrame([values], index=date_list, columns=table_list)
        print(recommend_table)
        print(df_result)

        # csvでデータを格納
        if not os.path.exists(f'./step2_logics/data/{place}'):
            os.mkdir(f'./step2_logics/data/{place}')
            os.mkdir(f'./step2_logics/data/{place}/{machine}')
        save_path = f"./step2_logics/data/{place}/{machine}/logic_2.csv"
        df_result.to_csv(save_path)


        
        ## 明日、logic1が該当している台があるかを判定するテーブルを作成する
        df_last = df_result.tail(1)
        df_last_values = df_last.values[0]

        # 日付を+1日するindexを作成する
        str_date = list(df_last.index)[0]
    
        # datetime型へ変換
        dte = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        tomorrow_dte = dte + datetime.timedelta(days=1)
    
        # str型へ変換
        str_tomorrow_dte = tomorrow_dte.strftime('%Y-%m-%d')
        
        # 明日がlogicに該当したかを確認
        df_predict = df_result
        df_predict.loc[str_tomorrow_dte] = df_last_values

        # csvでデータを格納
        if not os.path.exists(f'./step5_predict/data/{place}/{machine}/logic_2'):
            os.mkdir(f'./step5_predict/data/{place}/{machine}/logic_2')

        save_path = f"./step5_predict/data/{place}/{machine}/logic_2/{str_tomorrow_dte}.csv"
        df_predict.to_csv(save_path)

      

    
if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店


    run_logic_2(places)
