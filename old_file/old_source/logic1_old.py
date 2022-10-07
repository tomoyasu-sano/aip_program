import pandas as pd
import numpy as np

import step0_settings.utility as utility
from setting.setting import options

# logic: これまでの累計スタートに対する総大当たり数の平均をとり、2日前の状況を取得する
# - 両日とも平均より下の場合；次の日は打つことをおすすめする　← 全体的に出す可能性がある
# - 前日、もしくは両日とも、平均以上の場合、打たない方がいい


def logic1(file_name, table_len, start_table, table_number):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/data_arrays.npy')
    columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  #0~7
    columns_name = ["table_no", "履歴", "|", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]

    # dataを確認する時使用する
    l = len(data[0][2])
    days =list(range(l))
    days = np.array(days) + 1
    days = days[::-1]
    df_test = pd.DataFrame(data[0], columns=days, index=columns)
    #print(df_test)

    scores = []
    for table in range(table_len):
        df = pd.DataFrame(data[table], columns=days, index=columns)
        
        all_mean = df.mean(axis=1)
        rotation_count_mean = all_mean[0]
        total_jackpot = all_mean[1]

        score = round((total_jackpot / rotation_count_mean)*100, 4)

        scores.append(score)

    socres_mean = round(sum(scores)/len(scores),4)
    
    ## 次の日予測
    target_tables = []

    yesterday_scores = []
    day_before_yesterday_scores = []
    for i, table_no in enumerate(table_number):
        df = pd.DataFrame(data[i], columns=days, index=columns)

        # 前日の指標
        df_yesterday1 = df[1]
        rotation_count_mean = round(df_yesterday1[0],10)  # 累計スタート
        total_jackpot = round(df_yesterday1[1],10)  # 総大当たり
        
        if total_jackpot == 0 and rotation_count_mean > 100:  # 総大当たりが0回の場合、かつ累計スタートが100以上の場合、採用
            total_jackpot = 0.001

        if rotation_count_mean <= 100: # 全く打たれていない台 = 採用
            rotation_count_mean = 100
        
        yesterday_score = round((total_jackpot / rotation_count_mean)*100, 5)
        yesterday_scores.append(yesterday_score)
    
        # 前前日の指標
        df_yesterday2 = df[2]
        rotation_count_mean = round(df_yesterday2[0],10)
        total_jackpot = round(df_yesterday2[1],10)

        if total_jackpot == 0 and rotation_count_mean > 100:  # 総大当たりが0回の場合、かつ累計スタートが100以上の場合、採用
            total_jackpot = 0.001

        if rotation_count_mean <= 100: # 全く打たれていない台 = 採用
            rotation_count_mean = 100
        
        day_before_yesterday_score = round((total_jackpot / rotation_count_mean)*100, 5)
        day_before_yesterday_scores.append(day_before_yesterday_score)


    yesterday_scores_mean = round(sum(yesterday_scores)/len(yesterday_scores),4)
    day_before_yesterday_scores_mean = round(sum(day_before_yesterday_scores)/len(day_before_yesterday_scores),4)

    # 明日打つべきか確認
    print("全平均：",socres_mean,"前々日値：",day_before_yesterday_scores_mean,"前日値：",yesterday_scores_mean)
    if socres_mean > yesterday_scores_mean and socres_mean > day_before_yesterday_scores_mean:
        #print("両日とも平均より下です：明日はおすすめ日です")
        return True

    elif socres_mean < yesterday_scores_mean and socres_mean < day_before_yesterday_scores_mean:
        return False
        #print("両日とも平均より上です：明日は打たない方が良いです")
    else:
        #print("両日のうち1日は平均以上、1日は平均以下です：明日は打っても良いです")
        return True
 



    
if __name__ == "__main__":

    predict_shop = "garo_izumi"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_len = option["table_len"]
    start_table = option["start_table"]

    table_number = list(range(start_table,start_table+table_len))
    target  = logic1(file_name, table_len, start_table, table_number)

    #print(target)