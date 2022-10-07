from textwrap import indent
from this import d
import pandas as pd
import numpy as np
import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from step0_settings.setting import options, win_rate



def make_predict(places, logics):

    # 明日打つ台を格納するテーブル
    tomorrow_table = []

    for place in places:
        # データ取得に必要な項目を取得
        place = options[place]["place"]
        machine = options[place]["machine"]

        for logic in logics:

            # 各path先
            csv_file_path = f"./step5_predict/data/{place}/{machine}/{logic}"
            if os.path.exists(csv_file_path):
                csv_files = sorted(os.listdir(csv_file_path))

                # 一番新しい日付を取得（= 原則、target_date:昨日）
                dte_list = []
                for files in csv_files:
                    str_date = files.split(".")[0]
                    dte = datetime.datetime.strptime(str_date, '%Y-%m-%d') 
                    dte_list.append(dte)

                target_dte = sorted(dte_list)[0]
                target_date = target_dte.strftime('%Y-%m-%d')
        
                # 2つのpathを取得
                # 勝率のテーブルを取得
                path_win_rate = f"./step4_win_rate/data/{place}/{machine}/win_rate_{logic}.csv"

                # 明日、当てはまったlogicを抽出
                logic_path = f"./step5_predict/data/{place}/{machine}/{logic}/{target_date}.csv"
                print(logic_path)

                if os.path.isfile(path_win_rate) and os.path.isfile(logic_path):
                    df = pd.read_csv(path_win_rate, index_col=0)


                    # 勝率の敷居値を設定: setting.pyにて設定

                    df = df[df["recall_value"] != 1.0]
                    print(df)

                    # 勝率以上の台を抽出かつ1ではない（勝率100%は除外する = データが少ない or bug）
                    df_recommend_tables = df[(df["recall_value"] >= win_rate) & (df["recall_value"] != 1.0)]
                    df_recommend_tables = df_recommend_tables.sort_values('recall_value', ascending=False)
                    recommend_tables = list(df_recommend_tables.index)

                    print("----- recommend_tables -----")
                    print(recommend_tables)


                    # 明日、当てはまったlogicを抽出
                    df = pd.read_csv(logic_path, index_col=0)
                    print("---- df ----")
                    print(df)

                    # 最後の行（=昨日）を抽出
                    df_last = df.tail(1)
                    index = df_last.index[0]

                    # intに変換
                    df_last = df_last.astype('int')
                    df_last = df_last.T

                    # logicが適応された台を抽出（=1のcolumn)
                    match_tables = list(df_last[df_last[index] == 1].index)


            
                    recommend_match_tables = []
                    for table in recommend_tables:
                        # strに変換（logicを増やすと管理が大変なため、統一する）
                        table = str(table)
                        
                        if table in match_tables:
                            
                            # historyに格納するテーブル
                            recommend_match_tables.append(table)


                            # 明日打つ台のテーブル
                            rate = df_recommend_tables["recall_value"].loc[int(table)]
                            tomorrow_table.append([place, machine, table, logic, rate]) 

             

                    print(f"{place}, {machine}, {logic}")
                    print(f"勝率が高くおすすめする台: {recommend_tables}")
                    print(f"ロジックが適用された台 {logic}:  {match_tables}")
                    print("------------------------------------------------")
                    print(f"明日おすすめ台：{recommend_match_tables}")
                    print("------------------------------------------------")

                    ## historyに追加
                    if not recommend_match_tables == []:

                        for hist_recommend_table in recommend_match_tables:
                        #hist_recommend_table = recommend_match_tables[0] # まず最もおすすめの台のみ

                            # 日付を取得
                            d_today = datetime.date.today().strftime('%Y-%m-%d')
                            #tomorrow_dte = d_today + datetime.timedelta(days=1)
                            
                            # 追加するデータ
                            add_data = [[d_today, machine, hist_recommend_table, logic]]
                            add_data = pd.Series([d_today, place, machine, hist_recommend_table, logic, np.nan], index =['日付', '店舗', '機種', '台', 'logic', '結果'])

                            # historyの読み込み
                            hist_path = f"./step6_win_rate_history/data/{place}/history_{logic}.csv"
                            
                            if os.path.isfile(hist_path):
                                df_hist = pd.read_csv(hist_path)

                                # 同じ日付がなければ追加
                                date_list = df_hist["日付"].values

                                #if d_today not in date_list:
                                # 全て追加
                                df_hist = df_hist.append([add_data])
                                df_hist = df_hist.drop_duplicates()
                                
                                #print(df_hist)
                                df_hist.to_csv(f"./step6_win_rate_history/data/{place}/history_{logic}.csv", index = False)


    if not tomorrow_table == []:
        df_tomorrow = pd.DataFrame(tomorrow_table)
        df_tomorrow.columns = ["店舗", "機種", "台", "logic", "勝率"]
        df_tomorrow = df_tomorrow.sort_values('勝率', ascending=False)

        # 日付ごとに格納する
        today = datetime.date.today()
        df_tomorrow.to_csv(f"./step5_predict/predict/{today}.csv", index = False)




if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店

    logics = s.logics

   
    # test
    #places = ["osaka_rakuen_namba"]
    #logics = ["logic_1"]
        
    make_predict(places, logics)
    print("ok")