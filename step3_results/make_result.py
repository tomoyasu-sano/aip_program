import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from step0_settings.setting import options


################

# 勝ちの定義: 大当たり回数が上位25%になること
# 勝ちか負けかを格納するファイル

######


def get_result(places):

    for place in places:
       
        # データ取得に必要な項目を取得
        place = options[place]["place"]
        machine = options[place]["machine"]
        lists_number_of_days = options[place]["number_of_days"]
        table_len = options[place]["table_len"]
        table_list = options[place]["table_list"]
  


        # csv file名の一覧を配列化
        file_path = f"./step1_scrapiing/data/{place}/{machine}"
        csv_files = sorted(os.listdir(file_path))

        #csv_files = csv_files[0:8]
        # 日付のリスト
        date_list = []


        # 結果を格納
        results = []

        # csv_file: 例) 20220907.csv
        for csv_file in csv_files:

            # 1日ごとのデータを取得
            path = file_path + "/" + str(csv_file)
            df  = pd.read_csv(path,  index_col=0, engine='python')
            
            # 値がないものは0で一旦置き換える
            df = df.replace("--", 0)

            # 大当り確率と初当り確率は文字列のため
            df['大当り確率'] = df['大当り確率'].astype(int)
            df['初当り確率'] = df['初当り確率'].astype(int)


            # 勝ちの定義: 大当たり確率が上位25%以内（上位25%）
            #print(df['大当り確率'])
            win_line_val = df['大当り確率']

            # 0は平均値で埋める（0: 全く当たっていない or 機械の故障で打つことができない台）
            win_line_mean = int(np.mean(win_line_val[win_line_val != 0]))
            win_line_val[win_line_val == 0] = win_line_mean 
            #win_line_val = win_line_val[win_line_val != 0]
            
            win_quantile = win_line_val.quantile(q=[0, 0.33, 0.66, 1])
            win_quantile_value=  win_quantile[0.33]

            """
            0.00     83.0
            0.33    123.2 <- ここ以上を勝ち
            0.66    143.6
            1.00    480.0
            """
    
            #print(win_line_val)
            values = df["大当り確率"].values

            # 勝ちの定義(win_line_val)より、大当たり確率が少ない場合、勝ち(1)
            for val in values:
                if win_quantile_value >= val:
                    results.append(1)
                else:
                    results.append(0)

            #df["結果"] = results
            #print(df)

            # 文字列と日付の交互性を確保するための処理
            str_date = csv_file.split(".")[0]
            str_year = str_date[0:4]
            str_month = str_date[4:6]
            str_day = str_date[6:8]
            str_dte = str_year + "-" + str_month + "-" + str_day # 文字列型 日付
            #dte = datetime.datetime.strptime(str_day, '%Y-%m-%d') # datetime型 日付  error+

            # 日付（文字列）と値を大当たり確率の値を格納
            date_list.append(str_dte)


        results = np.array(results).reshape(-1, table_len )
        df_result = pd.DataFrame(results, columns=table_list, index=date_list)
        print(df_result)


        # 保存
        if not os.path.exists(f'./step3_results/data/{place}/{machine}'):
            os.mkdir(f'./step3_results/data/{place}')
            os.mkdir(f'./step3_results/data/{place}/{machine}')
        save_path = f"./step3_results/data/{place}/{machine}/result_win_or_lose.csv"

        df_result.to_csv(save_path)



if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店

    
    get_result(places)
    print("ok")


 