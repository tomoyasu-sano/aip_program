
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from step0_settings.setting import options


"""
dataを読み込み、numpy形式で保存（3次元）

・全てintで保存
・「--」は０に置換
"""

def make_dataset(places):
    for place in places:
    ## 読み込むモデル（場所 / 機種）を設定
        option = options[place]
        file_name = option["file_name"]
        table_list = option["table_list"]
        table_len = len(table_list)
        #table_len = option["table_len"]  
        if not os.path.exists(f'./save_data/data_learning/{file_name}'):
            os.mkdir(f'./save_data/data_learning/{file_name}')
        # if not os.path.exists(f'./data_learning/{file_name}/days'):
        #     os.mkdir(f'./data_learning/{file_name}/days')
            

        print("file_name:", file_name)     

        ### 3次元配列の作り方
        ## 方法：3次元の空の配列に、3次元の値をappendしていく
        ## 注意：２次元配列のshapeは同じであること ⇨ 例）14*8 の場合、14=台の数が不変 

        #columns = ["累計スタート", "総大当たり", "初当たり", "確変当", "最大持ち玉", "前日最終スタート", "大当たり確変", "初当たり確変"]  
        columns = ["累計スタート","大当り回数","初当り回数","最高出玉","大当り確率","初当り確率","只今スタート"]  
    
        
        #1) day tableを作成
        # 格納する3次元データを用意
        data_arrays = np.empty((0,table_len,len(columns)), int)
  

        # file名の一覧を配列化
        file_path = f"/Users/tomoyasu/dev/AIP/save_data/data/{file_name}/days"
        csv_file = sorted(os.listdir(file_path))

        for i in csv_file:
            df  = pd.read_csv(file_path + "/" + str(i), index_col=0, engine='python')
            df = df.replace("--", 0)
            #df = df.drop("table_no", axis=1)
            #print(df)
            #df = df.set_index("table_no")
            #print(df.dtypes)
            df['大当り確率'] = df['大当り確率'].astype(int)
            df['初当り確率'] = df['初当り確率'].astype(int)
            print(df.dtypes)

        
            data_array = df.values
            data_array = data_array[np.newaxis, :, :]    
            data_arrays = np.append(data_arrays, data_array, axis=0)

        # 時系列データに並べ変える
        data_arrays = data_arrays.transpose(1,2,0)

        # binary fileで保存
        np.save(f'/Users/tomoyasu/dev/AIP/save_data/data_learning/{file_name}/data_arrays', data_arrays)
        #data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/days/data_arrays.npy',  allow_pickle=True)
       
        
        """
        memo 
        累計スタート     int64
        大当り回数      int64
        初当り回数      int64
        最高出玉       int64
        大当り確率     object
        初当り確率     object
        只今スタート     int64
        """
        """ numpy配列にせず、csvでimportとして分析する
        ## 2)time tableのデータセットを作る
        columns_time = ["大当り回数","時間","スタート回数","出玉数"]  
        print("colums:",len(columns_time))

        #data_arrays_time = np.empty((0,table_len,len(columns_time)), int)
        data_arrays_time = np.empty((0,table_len,len(columns_time)))

        table_list = [39]
        for tl in table_list:
            file_path_time = f"/Users/tomoyasu/dev/AIP/data/{file_name}/time/table_{tl}"
            csv_file_time = sorted(os.listdir(file_path_time))

            for i in csv_file_time:
                df_time  = pd.read_csv(file_path_time + "/" + str(i), index_col=0, engine='python')
                df_time = df_time.replace("--", 0)
                df_time = df_time.drop("出玉数", axis=1)
                df_time.columns = ["大当り回数","時間","スタート回数","出玉数"]  

                data_array_time = df_time.values
                data_array_time = data_array_time[np.newaxis, :, :]    
                data_arrays_time = np.append(data_arrays_time, data_array_time, axis=0)

            # 時系列データに並べ変える
            #data_arrays_time = data_arrays_time.transpose(1,2,0)
            print(data_arrays_time[0])

            #if not os.path.exists(f'./data_learning/{file_name}/time/time_{tl}'):
             #   os.mkdir(f'./data_learning/{file_name}/time/time_{tl}')
                #print(df_time)
            

            np.save(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/time/data_arrays_time', data_arrays_time)
            #data = np.load(f'/Users/tomoyasu/dev/AIP/data_learning/{file_name}/time/data_arrays_time.npy', allow_pickle=True)

            """
    


        print("----------------------------------------------")
        print(f"{file_name}の新しいデータセットを作成しました")
        print("----------------------------------------------")

if __name__ == '__main__':
    import step0_settings.setting as s
    #make_dataset = make_dataset(s.places)

    #"garo_rakuen_nannba", "gandam_yunicorn_rakuen_nannba", "garo_iwata_ogiya"
    places = ["eva_king_kawaracho"]
    make_dataset = make_dataset(places)
    
