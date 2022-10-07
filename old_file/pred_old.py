import collections
import datetime
import itertools
import json
import os
import pandas as pd
import numpy as np


from prediction import logic1, logic2, logic3, logic4, logic5, logic6, logic7, logic8, logic9
from step0_settings.setting import options


def predict(use_logic, file_name, table_len, table_list):
    print("logic1 start...")
    if "logic1" in use_logic:
        target = logic1.logic1(file_name, table_len, table_list)

    print("logic2 start...")
    if "logic2" in use_logic:
        target_table2 = logic2.logic2(file_name, table_len, table_list)
    print("logic3 start...")
    if "logic3" in use_logic:
        target_table3 = logic3.logic3(file_name, table_len, table_list)
    if "logic4" in use_logic:
        best_times, dict_time_tables,day_of_week_dict = logic4.logic4(file_name, table_len, table_list)
    if "logic5" in use_logic:
       target_table5 = logic5.logic5(file_name, table_len, table_list)
    if "logic6" in use_logic:
       target_table6 = logic6.logic6(file_name, table_len, table_list)
    if "logic7" in use_logic:
       target_table7 = logic7.logic7(file_name, table_len, table_list)
    if "logic8" in use_logic:
       target_table8 = logic8.logic8(file_name, table_len, table_list)
    if "logic9" in use_logic:
       target_table9 = logic9.logic9(file_name, table_len, table_list)

    print("finish logic...")
    return target, target_table2, target_table3, best_times, dict_time_tables, day_of_week_dict, target_table5, target_table6, target_table7,target_table8, target_table9


def predict_check_result(predict_shops):
    check_results = []
    pred_lists = []
    
    for predict_shop in predict_shops:
        # 設定
        option = options[predict_shop]
        file_name =option["file_name"]
        table_list = option["table_list"]
        table_len = len(table_list)
        #start_table = option["start_table"]
        #table_number = list(range(start_table,start_table+table_len))

        # 適用するロジック
        logics={
            1: "logic1", 
            2: "logic2", 
            3: "logic3",
            4: "logic4",
            5: "logic5",
            6: "logic6",
            7: "logic7",
            8: "logic8",
            9: "logic9"
        }

        # recommend_tableの合計 
        target_tables = []

        # 適用するロジック
        use_logic = [logics[1], logics[2], logics[3], logics[4], logics[5], logics[6], logics[7], logics[8], logics[9]]

        # 予測値の取得
        target, target_table2, target_table3, best_times, dict_time_tables, day_of_week_dict, target_table5, target_table6, target_table7, target_table8, target_table9= predict(use_logic, file_name, table_len, table_list)


        # 結果の表示
        print(f"予測するお店は；{predict_shop}")
        # １つ目のロジック適用
        print("--------------------------------------------------")
        print("ロジック１:")
        print("")
        print(f"明日打ちに行っても良いか：{target}")

        # ２つ目のロジックを適用
        #target_tables.append(target_table)
        print("--------------------------------------------------")
        target_tables.append(target_table2)
        print("ロジック２: ")
        print("")
        print(f"おすすめ台：{target_table2}")

        # ３つ目のロジックを適用
        #target_tables.append(target_table)
        target_tables.append(target_table3)
        print("--------------------------------------------------")
        print("ロジック３: ")
        print("")
        print(f"おすすめ台：{target_table3}")

        # 5つ目のロジックを適用
        #target_tables.append(target_table)
        target_tables.append(target_table5)
        print("--------------------------------------------------")
        print("ロジック5: ")
        print("")
        print(f"おすすめ台：{target_table5}")
       
        # 6つ目のロジックを適用
        target_tables.append(target_table6)
        print("--------------------------------------------------")
        print("ロジック6: ")
        print("")
        print(f"おすすめ台：{target_table6}")

        # 7つ目のロジックを適用
        target_tables.append(target_table7)
        print("--------------------------------------------------")
        print("ロジック7: ")
        print("")
        print(f"おすすめ台：{target_table7}")

        # 8つ目のロジックを適用
        target_tables.append(target_table8)
        print("--------------------------------------------------")
        print("ロジック8: ")
        print("")
        print(f"おすすめ台：{target_table8}")
        
        # 9つ目のロジックを適用
        target_tables.append(target_table9)
        print("--------------------------------------------------")
        print("ロジック9: ")
        print("")
        print(f"おすすめ台：{target_table9}")
        
        
        # 全てのロジック適用の合計
        target_tables = list(itertools.chain.from_iterable(target_tables))
        count = collections.Counter(target_tables)
        recommend_tables = count.most_common()
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("おすすめ台一覧")
        print(recommend_tables)
        print("--------------------------------------------------")
        rt = recommend_tables[0][0]
        #rt2 = recommend_tables[0][1]
        print("明日のおすすめ台：", rt)
        print("--------------------------------------------------")
        print("--------------------------------------------------")

        ## 予測テーブルに対しておすすめ時間の取得
        if rt in list(dict_time_tables.keys()):
            dict_table_times = dict_time_tables[rt]
            dict_table_times_sorted = sorted(dict_table_times.items(), key=lambda x:x[1], reverse=True)
            table_best_time1 = dict_table_times_sorted[0][0]
            table_best_time2 = dict_table_times_sorted[1][0]
            table_best_time3 = dict_table_times_sorted[2][0]
            table_best_times = [table_best_time1,table_best_time2,table_best_time3]

        ## 明日の曜日のおすすめ時間の取得
        ### ただし、データが１週間以上ないものは参考にしない
        today = datetime.date.today()
        plus_day = datetime.timedelta(days=1)
        tomorrow = today + plus_day
        tomorrow_day_of_week = tomorrow.strftime('%A') # => 'Tuesday'
        tomorrow_time = day_of_week_dict[tomorrow_day_of_week]
        tomorrow_time_sorted = sorted(tomorrow_time.items(), key=lambda x:x[1], reverse=True)
        tomorrow_best_time1 = tomorrow_time_sorted[0][0]
        tomorrow_best_time2 = tomorrow_time_sorted[1][0]
        tomorrow_best_time3 = tomorrow_time_sorted[2][0]
        tomorrow_best_times = [tomorrow_best_time1, tomorrow_best_time2, tomorrow_best_time3]


        # 機種別にまとめる
        pred_list = [today, file_name,target, rt, best_times, table_best_times, tomorrow_best_times]
        pred_lists.append(pred_list)

        
        ## ---- 結果検証 -----
        print("結果検証 -------------------------------------")        

        ## 昨日の予測台に対する結果を取得
        today = datetime.date.today()   
        day = datetime.timedelta(days=1)
        yesterday = today - day
        path_today = f"/Users/tomoyasu/dev/AIP/predict/{yesterday}.csv"
        isfile = os.path.isfile(path_today)
        if isfile:
            print(f"昨日のデータが存在します。結果を記入していきます。")
            df_result = pd.read_csv(path_today)
            
            for index, row in df_result.iterrows():
                if row[1] == file_name:
                    pred_yesterday_table = row[3]    


            ## 本日の結果を取得
            data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
            length_tables= data.shape[0]
            #for i in range(length_tables):
            for i, table in enumerate(table_list):
                # 予測台を指定
                check_table = table
                #print("check_table:", check_table)
                
                if check_table ==pred_yesterday_table:
                    # print("check_table:",check_table, "-------", "rt:", rt)
                    print("チェックテーブルが見つかりました！！")
                    # columns = ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]
                    r = data[i][1]  # 1 = 大当り回数
                    yesterday_r = r[-1]
                    print("昨日の結果：", yesterday_r)

            ## 良い台の3割を当てられたか確認
            check_table = table_len  # 全てのテーブルの長さ
            check_data = 1  # 大当り回数 
            check_data_t = 1 # 大当り回数

            # 3分割にするため、2つのthresholdの値を作る
            arr = np.empty([0,data.shape[2]])
            for table in range(check_table):
                y =data[table][check_data,:]
                arr = np.append(arr, [y],axis=0)

            df = pd.DataFrame(arr)
            mean = round(df.mean(axis='columns'),0)
            df["平均"] = mean
            level, bins = pd.qcut(df["平均"], 3, labels=False, retbins=True)

            threshold_1 = bins[1]  # 低い
            threshold_2 = bins[2]  # 高い
 
            result_yesterday = 0
            if yesterday_r > threshold_2:
                result_yesterday = 1
                print(f"昨日の予測はは、全体{table_len}台中、好調台（全体の1/3）を当てることがきました。")
            else:
                print("昨日の予測は、全体の好調台1/3を当てることはできませんでした")
            print("結果（0 or 1）：", result_yesterday)
            print("実際の値：",yesterday_r )

            ## 結果を昨日に反映させる
            check_results.append([result_yesterday, yesterday_r])

        else:
            print("pathが存在しません")
            print("---------------------------------------------")
            df_result = pd.DataFrame([["no_data","no_data","no_data","no_data","no_data","no_data","no_data"]], columns=["Unnamed: 0","お店","明日打つべきか","おすすめ台","予測機種の時間帯ベスト3","予測テーブルのベスト時間","明日の曜日のおすすめ時間"])
            

    df_check_results = pd.DataFrame(check_results, columns=["結果", "実際の大当たり数"])
    df_result_add_yesterday = pd.concat([df_result, df_check_results],axis=1)
    df_result_add_yesterday = df_result_add_yesterday.drop("Unnamed: 0", axis=1)
    

    df_result_add_yesterday.to_csv(f"/Users/tomoyasu/dev/AIP/results/{yesterday}.csv", index=False)
    print("predict_shops:", predict_shops)
    
    today = datetime.date.today()   
    df_pred = pd.DataFrame(pred_lists, columns=["日付", "お店", "明日打つべきか","おすすめ台", "予測機種の時間帯ベスト3", "予測テーブルのベスト時間", "明日の曜日のおすすめ時間"])
    df_pred.to_csv(f"/Users/tomoyasu/dev/AIP/predict/{today}.csv")
    

if __name__ == '__main__':
    ### 設定が必要
    # 予測する店（settingより取得）
    predict_shops = ["garo_rakuen_nannba", "gandam_yunicorn_rakuen_nannba", "garo_iwata_ogiya"]
    
    import setting.setting as setting
    predict_shops = ["gandam_yunicorn_rakuen_nannba"]
    predict_check_result(predict_shops)
