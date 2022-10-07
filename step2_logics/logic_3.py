from re import M
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
    - 大当たり確率を5段階に分ける
    - 3日前が 2/5、2日前が 4/5 or 5/5、1日前が2日前より良い and  1/5ではない
- description
    - 打つべき: 1
    - 打つべきではない: 0
"""


# ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]

def qcut_df(df):
    level, bins = pd.qcut(df, 5, labels=False, retbins=True)

    threshold_0 = bins[0] # 最低 大当たり確率: good
    threshold_1 = bins[1]
    threshold_2 = bins[2]
    threshold_3 = bins[3]
    threshold_4 = bins[4]
    threshold_5 = bins[5] # 最高 大当たり確率: bad

    print(threshold_0, threshold_1, threshold_2, threshold_3, threshold_4, threshold_5)
    
    return threshold_0, threshold_1, threshold_2, threshold_3, threshold_4, threshold_5

def run_logic_3(places):
    target = "大当り確率"

    for place in places:
        print("place: ", place)

        df, date_list, machine, table_len, table_list = utility.make_df_from_csvfile(place, target)

        """
        例）
                    41   42   43   44   45   46   47   74   75   76   77   78   79   80（台番号）
        2022-09-07  140  216  290  681   97  348  735  160  130  139  123  192  162  135
        2022-09-08  212  116  401  113  177  149  203  631  135  545  195  156   94  131
        2022-09-09  106  247   99  110  391  445  176  136  247  668  247   97  250  247
        """

        df3= df.iloc[:,-3] # 3日前
        df2= df.iloc[:,-2] # 2日前
        df1= df.iloc[:,-1] # 前日

        #print(df3, df2, df1)

        if df3.shape[0] >= 5:
            threshold3_0, threshold3_1, threshold3_2, threshold3_3, threshold3_4, threshold3_5 = qcut_df(df3)
            threshold2_0, threshold2_1, threshold2_2, threshold2_3, threshold2_4, threshold2_5 = qcut_df(df2)
            threshold1_0, threshold1_1, threshold1_2, threshold1_3, threshold1_4, threshold1_5 = qcut_df(df1)
  
            #結果を格納するdf
            df_results = pd.DataFrame()

            for table in table_list:
                values = df[table].values
               
                # 3日間のデータセットを2次元配列で作成
                num_sequence = 3
                jackpots_3days = utility.make_swquence_data(values, num_sequence)
                #print(jackpots_3days)

                #判定
                results = []
                for jackpots in jackpots_3days:
                    before_3day = int(jackpots[0])
                    before_2day = int(jackpots[1])
                    before_1day = int(jackpots[2])

                    # 大当たり確率は低い方が良い
                    # logic：3日前が2/5, 2日前が 4/5 or 5/5, 1日前が2日前より良い and  1/5ではない
                    #if threshold3_2 <= before_3day < threshold3_4 and before_3day > before_2day and threshold2_1 <= before_2day <= threshold2_3 and before_2day < before_1day:
                    if threshold3_3 <= before_3day < threshold3_5  and threshold2_2 <= before_2day <= threshold2_5 and threshold1_1 <= before_1day <= threshold1_3:
                   #if threshold3_2 <= before_3day < threshold3_4  and threshold2_4 <= before_2day <= threshold2_5 and before_2day > before_1day:
                        results.append(int(1))
                    else:
                        results.append(int(0))

                # 日付順に合うように並び替える
                results = results[::-1]

                # 日付の長さと、データの長さを揃える（2日ごとのロジックのため、全体の日付- 2 のデータしか抽出しないため）
                results.insert(0, np.nan)
                results.insert(0,np.nan)
                results.insert(0,np.nan)
                df_result = pd.DataFrame(results, index=date_list, columns=[table])
                df_results = pd.concat([df_results, df_result], axis=1)

            
            #print(df_results)
            # csvでデータを格納
            if not os.path.exists(f'./step2_logics/data/{place}/{machine}'):
                os.mkdir(f'./step2_logics/data/{place}/{machine}')
            save_path = f"./step2_logics/data/{place}/{machine}/logic_3.csv"
            df_results.to_csv(save_path)




            ## 明日、logic1が該当している台があるかを判定するテーブルを作成する
            df_last = df_results.tail(1)
            
            # 日付を+1日するindexを作成する
            str_date = list(df_last.index)[0]
            
            # datetime型へ変換
            dte = datetime.datetime.strptime(str_date, '%Y-%m-%d')
            tomorrow_dte = dte + datetime.timedelta(days=1)
        
            # str型へ変換
            str_tomorrow_dte = tomorrow_dte.strftime('%Y-%m-%d')
            
            # 明日がlogicに該当したかを確認
            df_match = df.tail(num_sequence)

            #print(df_match)
        
            """
                        1337  1338  1339  1340  1341  1342  1343  1344  1345  1346  1347  1348  1349  1350  1351  1352  1353  1354  1355  1356  1357  1358  1359  1360
            2022-10-02   193   180   133   138   118   138   262   172   203   110   318   271   166   174   104   179   684   140   264   205   203   203   183   144
            2022-10-03   197   249   147   148   162   181   153   194   183   140    91   212   197   189   169   278   315   122   134   258   183   183   165   145
            2022-10-04   140   108   145   203   290   138   272   182   172   196   185   160   250   189   148   184   177   134   139   127   172   172   142   123
            """

            matchs = []
            for table in table_list:
                values = df_match[table].values  
                
                # 判定
                before_3day = int(jackpots[0])
                before_2day = int(jackpots[1])
                before_1day = int(jackpots[2])

                # 大当たり確率は低い方が良い
                # logic：3日前が2/5 ~ 4/5, 2日前が 4/5 ~ 5/5, 1日前が2日前より良い and  1/5ではない
                if threshold3_3 <= before_3day < threshold3_5  and threshold2_2 <= before_2day <= threshold2_5 and threshold1_1 <= before_1day <= threshold1_3:
                #if threshold3_2 >= before_3day:
                    matchs.append(int(1))
                else:
                    matchs.append(int(0))

        
            # 明日の予測のために該当の有無のデータを追加
            df_results.loc[str_tomorrow_dte] = matchs
            df_predict = df_results

            # csvでデータを格納
            if not os.path.exists(f'./step5_predict/data/{place}/{machine}/logic_3'):
                os.mkdir(f'./step5_predict/data/{place}/{machine}/logic_3')

            save_path = f"./step5_predict/data/{place}/{machine}/logic_3/{str_tomorrow_dte}.csv"
            df_predict.to_csv(save_path)

            




    return "ok"

if __name__ == "__main__":
    import step0_settings.setting as s
    import os
    
    # 対象取得データ一覧
    places = s.places
        ## settingで設定した現在データを取得対象のお店

    # test
    #places = ["osaka_rakuen_namba"]
    #logics = ["logic_3"]

    run_logic_3(places)


 