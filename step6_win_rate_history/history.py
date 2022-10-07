from ast import Pass
from filecmp import DEFAULT_IGNORES
from locale import D_T_FMT
from operator import index
import pandas as pd
import numpy as np
import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from step0_settings.setting import options


def make_history(places, logics):
    for place in places:
        # データ取得に必要な項目を取得
        place = options[place]["place"]
        machine = options[place]["machine"]
        table_list = options[place]["table_list"]

        for logic in logics:
            # これまでの結果を抽出
            path = f"./step6_win_rate_history/data/{place}/history_{logic}.csv"
            df_all = pd.read_csv(path, index_col=0)     
            #print(df_all)
  
            # 最終行の日付を取得（前日の予測から当日のデータが入力されていない行を抽出）
            # データがなければループを抜ける
            if df_all.empty:
                break
            else:
                last_date = df_all.tail(1).index[0]
                #print("last_date: ", last_date)

           
            # 指定日のdfを取得
            df = df_all.loc[last_date]
            #print(df)

            # 指定以外のdfを取得（後に保存するため）
            _df = df_all.drop(index=last_date)
            #print(_df)
 


            dates = df.index.values
            tables = df["台"].values
            
            # 勝ち負けの結果のデータを抽出
            path_result = f"./step3_results/data/{place}/{machine}/result_win_or_lose.csv"
            df_result = pd.read_csv(path_result, index_col=0)

            #print(f"結果 店舗: {place}, logic: {logic}")
            #print(df_result)

            result_data = []
            for date, table in zip(dates, tables):
                
                # 勝ち負け結果の日付リストにnullの行のdfの日付が入っているか
                """
                2022-09-30,eva_king_kawaracho,42, logic1,null

                2022-09-30 in ['2022-09-08', '2022-09-09', '2022-09-10', '2022-09-11', '2022-09-12',...] 
                """

            
                table = str(table) # 文字列に変換
                table_list = [str(n) for n in table_list] # 文字列に変換


                if (date in list(df_result.index)) and (table in table_list): 

                    # nullのある日と、指定テーブルの結果を取得（勝ち or 負け）  
                    result = df_result.loc[date, table]

                    result_data.append(result)
                    print("result: ", result, "date: ", date, "table: ", table)

        
            if result_data != []:
                # 結果の列を削除し、新しく作成する
                df_new = df.drop("結果", axis=1)
                df_new["結果"] = result_data            
                #print(df_new)

                    
                # 保存するdfを作成
                df_save = pd.concat([_df, df_new], axis=0)
                df_save = df_save.sort_index()
                df_save = df_save.reset_index()
                print(df_save)
                df_save.to_csv(f"./step6_win_rate_history/data/{place}/history_{logic}.csv", index = False)




if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店

    logics = s.logics

    # test
    #places = ["osaka_rakuen_namba"]
    #logics = ["logic_3"]

    make_history(places, logics)
    print("ok")
