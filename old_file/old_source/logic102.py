import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statistics import median 
from statsmodels.tsa.seasonal import STL #STL分解


import step0_settings.utility as utility
from setting.setting import options

# logic: ダウントレンド分析
# - 外れ値定義：総大当たりが95%以上

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
    


def logic3(file_name, table_len, start_table, table_number):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)
    columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  #0~7


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
   
        
        # グラフ描画
        """
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = [12, 9]
        df_test.plot()
        plt.title('Passengers')                            #グラフタイトル
        plt.ylabel('Monthly Number of Airline Passengers') #タテ軸のラベル
        plt.xlabel('Month')                                #ヨコ軸のラベル
        plt.show()
        """
            
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
    logic3(file_name, table_len, start_table, table_number)
    #target_tables = logic2(file_name, table_len, start_table, table_number)

