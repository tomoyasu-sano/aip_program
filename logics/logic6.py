import pandas as pd
import numpy as np
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import step0_settings.utility as utility
from step0_settings.setting import options

# logic: 大当たり確率を5段階に分ける
# logic: 16日~7日前で、2/5が合計7つ以上ある（=悪い台）, かつ6日~1日前までで、5/5がない

def qcut_df(df):
    level, bins = pd.qcut(df, 5, labels=False, retbins=True)
    threshold_0 = bins[0] # 最低
    threshold_1 = bins[1]
    threshold_2 = bins[2]
    threshold_3 = bins[3]
    threshold_4 = bins[4]
    threshold_5 = bins[5]  # 最高

    return threshold_0, threshold_1, threshold_2, threshold_3, threshold_4, threshold_5
    
def logic6(file_name, table_len, table_list):
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
      
    tables = []
    if df.shape[1] >=16:
        df16= df.iloc[:,-16]  #16日前
        df15= df.iloc[:,-15]
        df14= df.iloc[:,-14]  
        df13= df.iloc[:,-13]
        df12= df.iloc[:,-12]  
        df11= df.iloc[:,-11]
        df10= df.iloc[:,-10]  
        df9= df.iloc[:,-9]
        df8= df.iloc[:,-8]  
        df7= df.iloc[:,-7]
        df6= df.iloc[:,-6]
        df5= df.iloc[:,-5]
        df4= df.iloc[:,-4]
        df3= df.iloc[:,-3]
        df2= df.iloc[:,-2]
        df1= df.iloc[:,-1]
        
        threshold16_0, threshold16_1, threshold16_2, threshold16_3, threshold16_4, threshold16_5 = qcut_df(df16)
        threshold15_0, threshold15_1, threshold15_2, threshold15_3, threshold15_4, threshold15_5 = qcut_df(df15)
        threshold14_0, threshold14_1, threshold14_2, threshold14_3, threshold14_4, threshold14_5 = qcut_df(df14)
        threshold13_0, threshold13_1, threshold13_2, threshold13_3, threshold13_4, threshold13_5 = qcut_df(df13)
        threshold12_0, threshold12_1, threshold12_2, threshold12_3, threshold12_4, threshold12_5 = qcut_df(df12)
        threshold11_0, threshold11_1, threshold11_2, threshold11_3, threshold11_4, threshold11_5 = qcut_df(df11)
        threshold10_0, threshold10_1, threshold10_2, threshold10_3, threshold10_4, threshold10_5 = qcut_df(df10)
        threshold9_0, threshold9_1, threshold9_2, threshold9_3, threshold9_4, threshold9_5 = qcut_df(df9)
        threshold8_0, threshold8_1, threshold8_2, threshold8_3, threshold8_4, threshold8_5 = qcut_df(df8)
        threshold7_0, threshold7_1, threshold7_2, threshold7_3, threshold7_4, threshold7_5 = qcut_df(df7)
        threshold6_0, threshold6_1, threshold6_2, threshold6_3, threshold6_4, threshold6_5 = qcut_df(df6)
        threshold5_0, threshold5_1, threshold5_2, threshold5_3, threshold5_4, threshold5_5 = qcut_df(df5)
        threshold4_0, threshold4_1, threshold4_2, threshold4_3, threshold4_4, threshold4_5 = qcut_df(df4)
        threshold3_0, threshold3_1, threshold3_2, threshold3_3, threshold3_4, threshold3_5 = qcut_df(df3)
        threshold2_0, threshold2_1, threshold2_2, threshold2_3, threshold2_4, threshold2_5 = qcut_df(df2)
        threshold1_0, threshold1_1, threshold1_2, threshold1_3, threshold1_4, threshold1_5 = qcut_df(df1)
    
        for table, value16, value15, value14,value13,value12,value11, value10, value9, value8, value7, value6, value5, value4, value3, value2, value1 in zip(table_list,df16, df15, df14, df13, df12, df11, df10, df9, df8, df7, df6, df5, df4, df3, df2, df1):
            ## logic：10日連続 2/5以下
            hits =[]
            #if value10 < threshold10_3 and value9 < threshold9_3 and value8 < threshold8_3 and value7 < threshold7_3 and value6 < threshold6_3 and value5 < threshold5_3 and value4 < threshold4_3 and value3 < threshold3_3 and value2 < threshold2_3 and value1 < threshold1_3 :
            #if value11 < threshold11_3 and value10 < threshold10_3 and value9 < threshold9_3 and value8 < threshold8_4 and value7 < threshold7_4 and value5 < threshold5_3 and value4 < threshold4_3 and value3 < threshold3_3 and value2 < threshold2_3 and value1 < threshold1_3:
            #if value7 < threshold7_3 and value6 < threshold6_3 and value5 < threshold5_3 and value4 < threshold4_3 and value4 < threshold3_4 and value4 < threshold2_4 and value1 < threshold1_4:
            if value16 < threshold16_2:
                hits.append(1)  
            if value15 < threshold15_2:
                hits.append(1)  
            if value14 < threshold14_2:
                hits.append(1)
            if value13 < threshold13_2:
                hits.append(1)
            if value12 < threshold12_2:
                hits.append(1)  
            if value11 < threshold11_2:
                hits.append(1)  
            if value10 < threshold10_2:
                hits.append(1)  
            if value9 < threshold9_2:
                hits.append(1) 
            if value8 < threshold8_2:
                hits.append(1)  
            if value7 < threshold7_2:
                hits.append(1)  

            if sum(hits) >= 7 and value6 < threshold6_4 and value5 < threshold5_4 and value4 < threshold4_4 and value3 < threshold3_4 and value2 < threshold2_4:
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

    tables = logic6(file_name, table_len, table_list)
    print(tables)
    