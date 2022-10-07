import pandas as pd
import numpy as np
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from step0_settings.setting import options

# logic: 大当たり確率を5段階に分ける
# logic: 7~5日前に超大負け（1/5が2つ以上） and 1~4日前が2/5~4/5を推移（グラフ確認 7~5が大負け, 1~4日前が大きく勝っていない

def qcut_df(df):
    level, bins = pd.qcut(df, 5, labels=False, retbins=True)
    threshold_0 = bins[0] # 最低
    threshold_1 = bins[1]
    threshold_2 = bins[2]
    threshold_3 = bins[3]
    threshold_4 = bins[4]
    threshold_5 = bins[5]  # 最高

    return threshold_0, threshold_1, threshold_2, threshold_3, threshold_4, threshold_5
    
def logic9(file_name, table_len, table_list):
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
      
    tables = []
    if df.shape[0] >=7:
        df7= df.iloc[:,-7]
        df6= df.iloc[:,-6]
        df5= df.iloc[:,-5]
        df4= df.iloc[:,-4]
        df3= df.iloc[:,-3]
        df2= df.iloc[:,-2]
        df1= df.iloc[:,-1]
        
        threshold7_0, threshold7_1, threshold7_2, threshold7_3, threshold7_4, threshold7_5 = qcut_df(df7)
        threshold6_0, threshold6_1, threshold6_2, threshold6_3, threshold6_4, threshold6_5 = qcut_df(df6)
        threshold5_0, threshold5_1, threshold5_2, threshold5_3, threshold5_4, threshold5_5 = qcut_df(df5)
        threshold4_0, threshold4_1, threshold4_2, threshold4_3, threshold4_4, threshold4_5 = qcut_df(df4)
        threshold3_0, threshold3_1, threshold3_2, threshold3_3, threshold3_4, threshold3_5 = qcut_df(df3)
        threshold2_0, threshold2_1, threshold2_2, threshold2_3, threshold2_4, threshold2_5 = qcut_df(df2)
        threshold1_0, threshold1_1, threshold1_2, threshold1_3, threshold1_4, threshold1_5 = qcut_df(df1)
    
        for table, value7, value6, value5, value4, value3, value2, value1 in zip(table_list, df7, df6, df5, df4, df3, df2, df1):
            ## logic：10日連続 2/5以下
            hits =[]
            if value7 < threshold7_1:
                hits.append(1)  
            if value6 < threshold6_1:
                hits.append(1)  
            if value5 < threshold5_1:
                hits.append(1)


            if sum(hits) >= 2 and threshold4_1 <= value4 < threshold4_4 and threshold3_1 <= value3 < threshold3_4  and threshold1_2 <= value2 < threshold2_4  and threshold1_1 <= value1 < threshold1_4 :
                tables.append(table)
        return tables
    
    else:
        return tables

    

if __name__ == "__main__":

    predict_shop = "garo_rakuen_nannba"
    # ["garo_rakuen_nannba", "gandam_yunicorn_rakuen_nannba", "garo_iwata_ogiya"]

    # settingより取得
    option = options[predict_shop]
    file_name =option["file_name"]
    table_len = option["table_len"]
    start_table = option["start_table"]
    table_list = option["table_list"]

    tables = logic9(file_name, table_len, table_list)
    print(tables)
    