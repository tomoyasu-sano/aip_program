import datetime
import pandas as pd
import os 

"""
例）       結果  　　累積勝率(%)
20210908  1  　　　　１00
20210908  0          50
20210930  0          33
20211001  1          50

"""
 
def daily_win_rate():

    # 前回までの結果を取得
    win_rate_base_path = "/Users/tomoyasu/dev/AIP/win_rate/"
    target = "garo_rakuten_nannba/"
    win_rate_path = f"{win_rate_base_path}{target}win_rate.csv"
    df_win_rate = pd.read_csv(win_rate_path, index_col=0)
    print(df_win_rate)

    win_rate_length = len(df_win_rate["結果"].values)
    results = 0
    past_days = df_win_rate.index.values
    for index, row in df_win_rate.iterrows():
        result = row[0]
        if result == 1:
            results += 1


    # 今回の結果を
    file_path = f"/Users/tomoyasu/dev/AIP/results"
    csv_file = sorted(os.listdir(file_path))


    

    for i in csv_file:
        basename_without_ext = os.path.splitext(os.path.basename(i))[0]
        if basename_without_ext not in past_days:
            df  = pd.read_csv(file_path + "/" + str(i), index_col=0, engine='python')

            result_list = []
            result_day = ""
            

            for index, row in df.iterrows():
                print(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7])
                if row[0] == "garo_rakuen_nannba" and row[1] == True:
                    #result_list.append(basename_without_ext)
                    result_day = basename_without_ext
                    result_list.append(row[6])
                    
                    
                    win_rate_length +=1
                    if row[6] == 1:
                        results+=1
            

                    add_win_rate = round((results / win_rate_length) *100, 1)
                    result_list.append(add_win_rate)
  
    
    df_result_list = pd.DataFrame([result_list], index=[result_day], columns=["結果", "累積勝率"])    
    print(df_result_list)

    print(df_win_rate)
    df_win_rate = pd.concat([df_win_rate, df_result_list],) 
    
    
    #df_win_rate = df_win_rate.drop("Unnamed: 0", axis=1)
    print(df_win_rate)

    save_file_base_name = win_rate_base_path + target
    save_file_name = save_file_base_name + "/win_rate.csv"
    df_win_rate.to_csv(save_file_name)


    ##### 20220327 とりあえず、１つの機種の1日ずつなら、win_rate更新可
    ##### 更新忘れた日やその他errorチェック　一通り動くか再度チェック
        


def write_win_rate():
    file_path = f"/Users/tomoyasu/dev/AIP/results"
    csv_file = sorted(os.listdir(file_path))

    garo_rakuen_nannba = 1
    gandam_yunicorn_rakuen_nannba = 1
    garo_iwata_ogiya = 1


    len_garo_rakuen_nannba = 1
    len_gandam_yunicorn_rakuen_nannba = 1
    len_garo_iwata_ogiya = 1

    for i in csv_file:
        df  = pd.read_csv(file_path + "/" + str(i), index_col=0, engine='python')

        for index, row in df.iterrows():
            if row[1] == "garo_rakuen_nannba":
                len_garo_rakuen_nannba +=1
                garo_rakuen_nannba += row[4]

            if row[1] == "gandam_yunicorn_rakuen_nannba":
                len_gandam_yunicorn_rakuen_nannba+=1
                gandam_yunicorn_rakuen_nannba += row[4]

            if row[1] == "garo_iwata_ogiya":
                len_garo_iwata_ogiya+=1
                garo_iwata_ogiya += row[4]




    result_garo_rakuen_nannba = round((garo_rakuen_nannba / len_garo_rakuen_nannba),1)
    result_gandam_yunicorn_rakuen_nannba = round((gandam_yunicorn_rakuen_nannba / len_gandam_yunicorn_rakuen_nannba),1)
    result_garo_iwata_ogiya= round((garo_iwata_ogiya / len_garo_iwata_ogiya),1)


    win_rate_list = [result_garo_rakuen_nannba,result_gandam_yunicorn_rakuen_nannba, result_garo_iwata_ogiya]

    print(win_rate_list)
    columns = ["garo_rakuen_nannba","gandam_yunicorn_rakuen_nannba","garo_iwata_ogiya" ]

    today_date = datetime.date.today()   

    win_rate = pd.DataFrame([win_rate_list], index=["勝率"], columns=columns).T

    win_rate.to_csv(f"/Users/tomoyasu/dev/AIP/win_rate/{today_date}.csv")

        


if __name__ == '__main__':
    daily_win_rate()
