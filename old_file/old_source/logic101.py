import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statistics import median 
from statsmodels.tsa.seasonal import STL #STL分解


import step0_settings.utility as utility
from setting.setting import options


## シークエンスデータにして、結果検証 + これまでの結果と並べる。２回連続でダメなら、次のロジック適用時はokかも
## 予測データを作る


def sequence_data_logic4(y, t, num_sequence):
    num_data = len(y)
    seq_data = []
    target_data = []

    seq_days = []
    target_days = []

    today = datetime.date.today()  
    a = datetime.timedelta(days=1) 
    today = today - a  # 調整用
    
    for d, i in enumerate(range(num_data - num_sequence)):
        seq_data.append(y[i:i+num_sequence])
        #target_data.append(y[i+num_sequence:i+num_sequence+1])
        label = t[i+num_sequence:i+num_sequence+1]
        target_data.append(label)

        # make seq_day
        
        
        prepare_seq_days =[]
        for s in range(num_sequence):
            s = s + d 
            sd = datetime.timedelta(days=s)
            seq_day = today - sd
            prepare_seq_days.append(seq_day)
        prepare_seq_days = prepare_seq_days[::-1]
        seq_days.append(prepare_seq_days)
        

        miuns_day = datetime.timedelta(days=d)
        target_day = today - miuns_day
        target_day = str(target_day)
        target_days.append(target_day)
        
    target_days = target_days[::-1]
    seq_days = seq_days[::-1]

    seq_arr = np.array(seq_data)
    target_arr = np.array(target_data)
    return seq_arr, target_arr, seq_days, target_days


# トレンド分析関数
def stl(df_fisrt, df_last, table):
    trend = {}
    # STL分解 過去7日間（period値）のトレンド分析
    stl_first =STL(df_fisrt, period=6, robust=True)
    stl_series_first = stl_first.fit()

    stl_last = STL(df_last, period=6, robust=True)
    stl_series_last = stl_last.fit()
    

    # STL分解結果のグラフ化
    #stl_series_first.plot()
    #plt.show()

    # STL分解結果のデータ
    stl_t_first = stl_series_first.trend    #トレンド（trend）
    #stl_r_first = stl_series_first.resid    #残差（resid） 
    
    stl_t_last = stl_series_last.trend    #トレンド（trend）
    #stl_r_last = stl_series_last.resid    #残差（resid） 

    # トレンドを6パターンに分類（上昇緩やか、上昇上昇、上昇下降、下降上昇、下降緩やか、下降下降）    
    first_beginning_value = stl_t_first[0]
    first_end_value = stl_t_first[-1]
    first_residue = stl_t_first[-1] - stl_t_first[0]

    last_beginning_value = stl_t_last[0]
    last_end_value = stl_t_last[-1]
    last_residue = stl_t_last[-1] - stl_t_last[0]

    if first_beginning_value < first_end_value and last_beginning_value < last_end_value:
        if first_residue < last_residue:
            trend["上昇上昇トレンド"] = table
            #print("上昇上昇トレンド",table)
        if first_residue > last_residue:
            trend["上昇緩やかトレンド"] = table
            #print("上昇緩やかトレンド",table)
    if first_beginning_value < first_end_value and last_beginning_value >= last_end_value:
        trend["上昇下降トレンド"] = table
        #print("上昇下降トレンド", table)
    
    if first_beginning_value > first_end_value and last_beginning_value > last_end_value:
        if first_residue < last_residue:
            trend["下降下昇トレンド"] = table
            #print("下降下降トレンド",table)
        if first_residue > last_residue:
            trend["下降緩やかトレンド"] = table
            #print("下降緩やかトレンド",table)
    if first_beginning_value >= first_end_value and last_beginning_value < last_end_value:
        trend["下降上昇トレンド"] = table
        #print("下降上昇トレンド", table)
    
            
    return trend
    


def logic4(file_name, table_len, start_table, table_number):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  #0~7

    maintain_trend = 0
    up_trend = 0
    small_up_trend = 0
    down_trend = 0
    small_down_trend = 0

    maintain_trend_lose = 0
    up_trend_lose = 0
    small_up_trend_lose= 0
    down_trend_lose = 0
    small_down_trend_lose = 0

    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    df_test = pd.DataFrame(data[0], columns=days, index=columns)
    #print(df_test)

    seq_length = 15 # 何日間のデータ範囲とするか
    check_data = 3
    check_data_t = 3 
    #data = pd.DataFrame(data[0], columns=columns)

    #結果格納
    recommend_tables = []
    results = []
    for table, table_no in enumerate(table_number):
    #table_no = 1
    #tables = 1
    #for table in range(tables):

        #設定値
        
        win_threshold_value = 20
        residue_threshold_value = 5
       
        y =data[table][check_data,:]
        t = data[table][check_data_t,:]

        # 5段階分類
        df_bins = pd.Series(y)
        level, bins = pd.qcut(df_bins, 5, labels=False, retbins=True)

        threshold_0 = round(bins[0],2)
        threshold_1 = round(bins[1],2)
        threshold_2 = round(bins[2],2)
        threshold_3 = round(bins[3],2)
        threshold_4 = round(bins[4],2)
        threshold_5 = round(bins[5],2)


        seq_arrs, target_arrs, seq_days, target_days = sequence_data_logic4(y, t, seq_length)


        # df用
        col = []
        values = []
        
        ## 結果確認用
        results = []


        # シークエンスデータ作成
        for seq, sd, target, td in zip(seq_arrs, seq_days, target_arrs, target_days):

            trend_results = {}
            df = pd.DataFrame(seq, index=sd)

            df_stl = df[:-3]
            df_near = df[-3:]
   
            ## 3日前以前のトレンド分析
            stl =STL(df_stl, period=6, robust=True)
            stl = stl.fit()
            stl_trend = stl.trend    #トレンド（trend）

            beginning_value = round(stl_trend[0], 4)
            end_value = round(stl_trend[-1], 4)
            residue = end_value - beginning_value
            target = target[0]
            
            # 負けは０, 勝ちは１
            if beginning_value == end_value:
                trend_name = "維持トレンド"
                if target < win_threshold_value:
                    r = 0
                    trend_results[td] = [table_no, trend_name, target, r]
        
                if target > win_threshold_value:
                    r = 1
                    trend_results[td] = [table_no, trend_name, target, r]
            
            if beginning_value > end_value and residue > residue_threshold_value: #高下降トレンド
                trend_name = "高下降トレンド"
                if target < win_threshold_value:
                    r = 0
                    trend_results[td] = [table_no, trend_name, target, r]
                
                if target > win_threshold_value:
                    r = 1
                    trend_results[td] = [table_no, trend_name, target, r]
        

            if  beginning_value > end_value and residue < residue_threshold_value: #小下降トレンド
                trend_name = "小下降トレンド"
                if target < win_threshold_value:
                    r = 0
                    trend_results[td] = [table_no, trend_name, target, r]
                  
                if target > win_threshold_value:
                    r = 1
                    trend_results[td] = [table_no, trend_name, target, r]

            if beginning_value < end_value and residue > residue_threshold_value: #高上昇トレンド
                trend_name = "高上昇トレンド"
                if target < win_threshold_value:
                    r = 0
                    trend_results[td] = [table_no, trend_name, target, r]
                   
                if target > win_threshold_value:
                    r = 1
                    trend_results[td] = [table_no, trend_name, target, r]

            
            if beginning_value < end_value and residue < residue_threshold_value: #高上昇トレンド
                trend_name = "小上昇トレンド"
                if target < win_threshold_value:
                    r = 0
                    trend_results[td] = [table_no, trend_name, target, r]
              
                if target > win_threshold_value:
                    r = 1
                    trend_results[td] = [table_no, trend_name, target, r]

            ## 直近3日間を分析
            # 5段階に分類し、3日前：40-60に入っており、2,1日前は20-80の間に入っている、2,1日は3日前より確変当たりが低いこと
            # df_near 直近3日間 / threshold_0 ~ 5

            #print(df_near)
            before_day_3 = df_near[-3:-2].values[0][0]
            before_day_2 = df_near[-2:-1].values[0][0]
            before_day_1 = df_near[-1::].values[0][0]

            print(threshold_0, threshold_1, threshold_2, threshold_3,threshold_4,threshold_5) 
            print(before_day_3, before_day_2, before_day_1, trend_name)

            if threshold_3 <= before_day_3 <= threshold_5 and threshold_2 <= before_day_2 <= threshold_4 and threshold_3 <= before_day_1 <= threshold_4 and before_day_3 >= before_day_2 and before_day_3 >= before_day_1 and trend_name=="小下降トレンド" or trend_name=="高下降トレンド":
                print("ロジック4を適用されました")
                if target >= win_threshold_value: 
                    results.append(1)
                else:
                    results.append(0)

        df_trend = pd.DataFrame(values, index=col, columns=["トレンド名","勝敗"])
        #print(df_trend)
        # pvit table 

        # トレンド名を取得
        df_trend_name = list(set(df_trend["トレンド名"].values))

        # トレンド名の勝敗平均を取得
        #df_trend_pivod = pd.pivot_table(df_trend, index="トレンド名", values="勝敗")
        #print(df_trend_pivod)
        

        #####################################

        """
        #予測をする
        pred_data =data[table][check_data,:][-7::]
        #print(pred_data)
        # pred_dataのトレンド把握
    
        pred_today = datetime.date.today()  
        #a = datetime.timedelta(days=1) 
        #pred_today = pred_today + a  # 調整用
        pred_days = []
        for day in range(7):
            md = datetime.timedelta(days=day+1) 
            pred_days.append(pred_today - md)

        pred_days = pred_days[::-1]
        

        pred_df = pd.DataFrame(pred_data, index=pred_days)
        
        pred_stl =STL(pred_df, period=6, robust=True)
        pred_stl = pred_stl.fit()
        spred_tl_trend = pred_stl.trend    #トレンド（trend）

        beginning_value = round(spred_tl_trend[0], 4)
        end_value = round(spred_tl_trend[-1], 4)
        residue = end_value - beginning_value

        # get trend_name 
        if beginning_value == end_value:
            pred_trend_name = "維持トレンド"
            
        if beginning_value > end_value and residue > residue_threshold_value: #高下降トレンド
            pred_trend_name = "高下降トレンド"
               
        if  beginning_value > end_value and residue < residue_threshold_value: #小下降トレンド
            pred_trend_name = "小下降トレンド"

        if beginning_value < end_value and residue > residue_threshold_value: #高上昇トレンド
            pred_trend_name = "高上昇トレンド"
        
        if beginning_value < end_value and residue < residue_threshold_value: #高上昇トレンド
            pred_trend_name = "小上昇トレンド"
        
        print("---------------------------")
        print(pred_trend_name)
        pred_df_trend = df_trend[df_trend["トレンド名"] == pred_trend_name]
        #pred_df_trend = df_trend[df_trend["トレンド名"] == "小下降トレンド"]
        pred_df_trend_last = pred_df_trend[-6::]
        print(pred_df_trend_last)
        
        check_values = pred_df_trend_last["勝敗"].values
        print(check_values)
        print(table_no)
        if len(check_values) == 6:
            if 1 not in check_values:
                recommend_tables.append(table_no)
                print("追加追加")
        #if len(check_values) == 2:
         #   if 1 not in check_values:
          #      recommend_tables.append(table_no)
        """
    #print(recommend_tables)

    ## 結果検証：全ての台+シークエンスデータから、logic4の当てはまった際、結果の表示
    print("ロジック４の結果は：",results)


    """
    print(maintain_trend)
    print(up_trend)
    print(small_up_trend)
    print(down_trend)
    print(small_down_trend)
    print("-------------------------")
    print(maintain_trend_lose)
    print(up_trend_lose)
    print(small_up_trend_lose)
    print(down_trend_lose)
    print(small_down_trend_lose)
    print("-------------------------")
    print(maintain_trend/maintain_trend_lose)
    print(up_trend/up_trend_lose)
    print(small_up_trend/small_up_trend_lose)
    #print(down_trend/down_trend_lose+1)
    print(small_down_trend/small_down_trend_lose)
    """


    #a = df_trend[df_trend["トレンド名"] == "小上昇トレンド"]
    #print(a)
    #print(results)
    #df_trend = pd.DataFrame.from_dict(results, orient='index')
    #df = pd.DataFrame.from_dict(d, orient='index').T
    #print(df_trend)





    """

    upuplarge_trends = []
    upuplittle_trends = []
    updown_trends = []
    downdownlarge_trends = []
    downdownlittle_trends =[]
    downup_trends =[]

    for  i, table in enumerate(table_number):
        # dataを確認する時使用する
        l = len(data[0][2])
        days =list(range(l))
        days = np.array(days) + 1
        days = days[::-1]
        df_test = pd.DataFrame(data[i], columns=days, index=columns)
        
        df_test = df_test.loc["確変当"]  
        #print(df_test.shape)

        # 時系列のindexを作成
        index_col = []
        for i  in range(df_test.shape[0]):
            today = datetime.date.today()
            minus_day = datetime.timedelta(days=-i)
            day = today + minus_day
            day = str(day)
            index_col.append(day)
            
        index_col = index_col[::-1]
        df_test.index = index_col
        df_test.columns = "確変当"
 
            
        day = 7
        last_day = len(index_col)  # 12
        # 12日間のうち後ろの7日間と前の7日間に分ける




        ###################################
        # 直近データと少し前のデータに絞る
        edit_day = day-1
        df_first = df_test.iloc[last_day-edit_day*2:last_day-edit_day+1]
        df_last = df_test.iloc[last_day-day::]

        # データが多い時、こちらが正確
        edit_day=day
        df_first = df_test.iloc[last_day-edit_day*2:last_day-edit_day]
        df_last = df_test.iloc[last_day-day::]

        # このような取り方もある（直近2日間はカウントせず、その前の14日間のトレンド
        edit_day=day
        df_first = df_test.iloc[last_day-edit_day*2-3:last_day-edit_day-3]
        df_last = df_test.iloc[last_day-day-3:-3]

        #print(df_first)
        #print(df_last)
        ########################上記、どのパターンがいいか確認する
     


        # トレンド分析
        trend = stl(df_first, df_last, table)

        # トレンド整理
        if "上昇上昇トレンド" in trend.keys():
            upuplarge_trends.append(list(trend.values())[0])
        if "上昇緩やかトレンド" in trend.keys():
            upuplittle_trends.append(list(trend.values())[0])
        if "上昇下降トレンド" in trend.keys():
            updown_trends.append(list(trend.values())[0])

        if "下降下降トレンド" in trend.keys():
            downdownlarge_trends.append(list(trend.values())[0])
        if "下降緩やかトレンド" in trend.keys():
            downdownlittle_trends.append(list(trend.values())[0])
        if "下降上昇トレンド" in trend.keys():
            downup_trends.append(list(trend.values())[0])



    #print("上昇上昇トレンド:",upuplarge_trends)
    #print("上昇緩やかトレンド:",upuplittle_trends)
    #print("上昇下降トレンド:",updown_trends)
    #print("下降下降トレンド:",downdownlarge_trends)
    #print("下降緩やかトレンド:",downdownlittle_trends)
    #print("下降上昇トレンド",downup_trends)
    
    recommend_tables = []
    not_recommend_tables = []
    normal_recommend_tables = []
    for  i, table in enumerate(table_number):
        if table in downdownlittle_trends or table in downdownlarge_trends:
            recommend_tables.append(table)
        
        if table in upuplittle_trends :
            #print("下降上昇トレンド")
            not_recommend_tables.append(table)

        if table in upuplarge_trends or table in downup_trends or table in updown_trends :
            #print("下降上昇トレンド")
            normal_recommend_tables.append(table)

        
     
    print(recommend_tables)
    print(not_recommend_tables)
    print(normal_recommend_tables)
        

    
    """



    """
    scores = []
    for table in range(table_len):
        df = pd.DataFrame(data[table], columns=days, index=columns)

        # 外れ値検出
        df = df.loc["総大当たり"]
        score = round(df.quantile(0.95),1)
       
        scores.append(score)
        #print(score)

    ## socresの平均ではなく、scoresのさらに75%以上の外れ値 ← 40程度を外れ値としたい（店によって異なる）
    df_scores = pd.DataFrame(scores)
    value = round(df_scores.quantile(0.6),1).values[0]
    

    ## 次の日予測
    target_tables = []
    for i, table_no in enumerate(table_number):
        df = pd.DataFrame(data[i], columns=days, index=columns)

        # 前日の指標
        #df_yesterday1 = df.loc["総大当たり"]
        df_yesterday1 = df[1].loc["総大当たり"]       
        # 前前日の指標
        df_yesterday2 = df[2].loc["総大当たり"]       
   

        # 明日打つべきか確認
        if value < df_yesterday1 or  value < df_yesterday2:
            print("2日以内に外れ値が含まれています：明日は打たない方が良いです")
            #print(table_no, df_yesterday1,df_yesterday2 )

        else:
            #print("両日とも外れ値はありません：logic対象にします")
            target_tables.append(table_no)


    #print(target_tables)
    return target_tables
    """

    
if __name__ == "__main__":

    predict_shop = "garo_izumi"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_len = option["table_len"]
    start_table = option["start_table"]

    table_number = list(range(start_table,start_table+table_len))
    logic4(file_name, table_len, start_table, table_number)
    #target_tables = logic2(file_name, table_len, start_table, table_number)

