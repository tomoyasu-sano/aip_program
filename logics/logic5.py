import pandas as pd
import numpy as np
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from step0_settings.setting import options

# logic: 大当たり確率を5段階に分ける
# logic: 3日前が 2/5、2日前が 4/5 or 5/5、1日前が2日前より良い and  1/5ではない

def qcut_df(df):
    level, bins = pd.qcut(df, 5, labels=False, retbins=True)

    threshold_0 = bins[0] # 最低
    threshold_1 = bins[1]
    threshold_2 = bins[2]
    threshold_3 = bins[3]
    threshold_4 = bins[4]
    threshold_5 = bins[5]  # 最高

    return threshold_0, threshold_1, threshold_2, threshold_3, threshold_4, threshold_5
    
def logic5(file_name, table_len, table_list):
    # データを読み込み / 可視化
    data = np.load(f'/Users/tomoyasu/dev/AIP/save_data/data_learning/{file_name}/data_arrays.npy', allow_pickle=True)

    #  ["累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "只今スタート"]
    check_table = table_len  # 全てのテーブルの長さ
    check_data = 1  # "大当り回数"



    # check_data のdfを作成
    arr = np.empty([0,data.shape[2]])
    for table in range(check_table):
        y =data[table][check_data,:]
        arr = np.append(arr, [y],axis=0)
    df = pd.DataFrame(arr)


    # 3日前~1日前のデータを取得
    tables = []
    df3= df.iloc[:,-3]  # 3日前
    df2= df.iloc[:,-2]
    df1= df.iloc[:,-1]  # 前日

    threshold3_0, threshold3_1, threshold3_2, threshold3_3, threshold3_4, threshold3_5 = qcut_df(df3)
    threshold2_0, threshold2_1, threshold2_2, threshold2_3, threshold2_4, threshold2_5 = qcut_df(df2)
    threshold1_0, threshold1_1, threshold1_2, threshold1_3, threshold1_4, threshold1_5 = qcut_df(df1)
  
    for table, value3, value2, value1 in zip(table_list,df3, df2, df1):
        ## logic：3日前が2/5, 2日前が 4/5 or 5/5, 1日前が2日前より良い and  1/5ではない
        if threshold3_2 <= value3 < threshold3_4 and value3 > value2 and threshold2_1 <= value2 <= threshold2_3 and value2 < value1:
            tables.append(table)

    return tables


if __name__ == "__main__":

    predict_shop = "garo_rakuen_nannba"
    #"garo_rakuen_nannba", "gandam_yunicorn_rakuen_nannba", "garo_iwata_ogiya"

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_len = option["table_len"]
    start_table = option["start_table"]
    table_list = option["table_list"]

    tables = logic5(file_name, table_len, table_list)
    print(tables)
    