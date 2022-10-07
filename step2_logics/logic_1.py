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
    - 2日連続大当たり確率が平均よりも低い場合は打たない（逆にそうでなければ打つ）
- description
    - 台ごとの大当たり確率の平均を取得
    - 2日前と1日前の両日の大当たり確率と、平均を比較して、両日ともに平均より高ければ、打つべきではないと判断
        - 打つべき: 1
        - 打つべきではない: 0
"""


# ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]

def run_logic_1(places):
    
    for place in places:
        print("place: ", place)

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
            jackpot_probability = df["大当り確率"].values

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
        """
        例）
                    41   42   43   44   45   46   47   74   75   76   77   78   79   80（台番号）
        2022-09-07  140  216  290  681   97  348  735  160  130  139  123  192  162  135
        2022-09-08  212  116  401  113  177  149  203  631  135  545  195  156   94  131
        2022-09-09  106  247   99  110  391  445  176  136  247  668  247   97  250  247
        """

        # 結果を格納するdf
        df_results = pd.DataFrame()

    
        for table in table_list:
            values = df[table].values

            jackpot_mean = int(np.mean(values))
            #print(jackpot_mean)

            # 3日間のデータセットを2次元配列で作成
            num_sequence = 2
            jackpots_3days = utility.make_swquence_data(values, num_sequence)

    
            #判定
            results = []
            for jackpots in jackpots_3days:
                before_2day = int(jackpots[0])
                before_1day = int(jackpots[1])

                # 大当たり確率は低い方が良い: 
                #print(jackpot_mean, before_2day, jackpot_mean, before_1day)
                if jackpot_mean > before_1day and jackpot_mean > before_2day:
                    results.append(int(0))
                else:
                    results.append(int(1))

            # 日付の長さと、データの長さを揃える（2日ごとのロジックのため、全体の日付- 2 のデータしか抽出しないため）
            
            # 逆にすることで、日付通りの並びになる
            results = results[::-1]

            """
                        1337
            2022-09-29   1.0
            2022-09-30   0.0
            2022-10-01   0.0

            → 入れ替える

                        1337
            2022-09-29   0.0
            2022-09-30   0.0
            2022-10-01   1.0
            """

            results.insert(0, np.nan)
            results.insert(0,np.nan)
            df_result = pd.DataFrame(results, index=date_list, columns=[table])
            df_results = pd.concat([df_results, df_result], axis=1)



        # csvでデータを格納
        if not os.path.exists(f'./step2_logics/data/{place}/{machine}'):
            os.mkdir(f'./step2_logics/data/{place}/{machine}')
        save_path = f"./step2_logics/data/{place}/{machine}/logic_1.csv"
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
    
        """
                    41   42   43   44   45   46   47   74   75   76   77   78   79   80
        2022-09-29  140  216  290  681   97  348  735  160  130  139  123  192  162  135
        2022-09-30  212  116  401  113  177  149  203  631  135  545  195  156   94  131
        """

        matchs = []
        for table in table_list:
            
            # 大当たり確率の平均を取得
            values = df[table].values
            jackpot_mean = int(np.mean(values))


            values = df_match[table].values

            before_2day = values[0]
            before_1day = values[1]

            #print(table, ":", jackpot_mean, before_2day, jackpot_mean, before_1day)

            # 大当たり確率は低い方が良い: 
            if jackpot_mean > before_1day and jackpot_mean > before_2day:
                matchs.append(int(0))
            else:
                matchs.append(int(1))


        #print(matchs)
        #### matchs = matchs[::-1]  <- 不要
        # 明日の予測のために該当の有無のデータを追加
        df_results.loc[str_tomorrow_dte] = matchs
        df_predict = df_results

        #print(df_predict)

        # csvでデータを格納
        if not os.path.exists(f'./step5_predict/data/{place}/{machine}/logic_1'):
            os.mkdir(f'./step5_predict/data/{place}/{machine}/logic_1')

        save_path = f"./step5_predict/data/{place}/{machine}/logic_1/{str_tomorrow_dte}.csv"
        df_predict.to_csv(save_path)

    
    return "ok"

if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店


    # test
    #places = ["osaka_rakuen_namba"]
    #logics = ["logic_1"]


    run_logic_1(places)


 