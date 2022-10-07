from textwrap import indent
import pandas as pd
import numpy as np
import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


from step0_settings.setting import options



def make_win_rate(places, logics):
    for place in places:
        # データ取得に必要な項目を取得
        place = options[place]["place"]
        machine = options[place]["machine"]      
  

        # path設定
        for logic in logics:


            path_to_logic= f"./step2_logics/data/{place}/{machine}/{logic}.csv"
            path_result = f"./step3_results/data/{place}/{machine}/result_win_or_lose.csv"

            if os.path.isfile(path_to_logic) and os.path.isfile(path_result): 
            #if os.path.exists(path_to_logic) and os.path.exists(path_result):
                # データの読み込み
                df_result = pd.read_csv(path_result, index_col=0)
                df_logic = pd.read_csv(path_to_logic, index_col=0)



                # nullを削除
                df_result = df_result.dropna(how='any')
                df_logic = df_logic.dropna(how='any')

                # 共通部分のみに変換
                # columnsが同じことが前提
                tables =  df_logic.columns
                index = df_logic.index
                index_start = index[0]
                index_end = index[-1]

                df = df_result[index_start: index_end]

                # df(結果のdf)とdf_logic(ロジックのdf)の作成完了

                # 比較

                judgements_dict = {}

                for i in index:
                    logic_values = df_logic.loc[i]
                    df_values = df.loc[i]

                    judgements = []


                    for logic_val, df_val in zip(logic_values, df_values):
                        logic_val = int(logic_val)
                        df_val = int(df_val)        
                        
                        """
                        # 判定
                        1 : 1 -> logicが該当し、実際結果も勝ち: 1
                        1 : 0 -> logicが該当したが、結果は負け: 2
                        0 : 1 -> logicは該当しないが、結果は勝ち: 3
                        0 : 0 -> logicは該当しないが、結果は負け: 4
                        """

                        # if logic_val == 1 and df_val == 1:
                        #     judgements.append(1)
                        # if logic_val == 1 and df_val == 0:
                        #     judgements.append(2)
                        # if logic_val == 0 and df_val == 1:
                        #     judgements.append(3)
                        # if logic_val == 0 and df_val == 0:
                        #     judgements.append(4)

                        """
                        # 判定
                        1 : 1 -> logicが該当し、実際結果も勝ち: 1
                        1 : 0 -> logicが該当したが、結果は負け: 0
                        0 : 1 -> logicは該当しないが、結果は勝ち: 2
                        0 : 0 -> logicは該当しないが、結果は負け: 2
                        """


                        if logic_val == 1 and df_val == 1:
                            judgements.append(1)
                        if logic_val == 1 and df_val == 0:
                            judgements.append(0)
                        if logic_val == 0 and df_val == 1:
                            judgements.append(2)
                        if logic_val == 0 and df_val == 0:
                            judgements.append(2)
                    
                    judgements_dict[i] = judgements


                df_judgements = pd.DataFrame(judgements_dict, index=tables).T



                        
                ## 性能評価（勝つと予想して、勝ち負けの性能）
                recall_values = []

                df_judgements = df_judgements.T
                #print("df_judgements")
                #print(df_judgements)

                for index, judgement in df_judgements.iterrows():
                    win_count = np.count_nonzero(judgement == 1)
                    lose_count = np.count_nonzero(judgement == 0)

                    if win_count != 0:
                        win_rate = round(win_count/(win_count+lose_count), 2)
                    else:
                        win_rate = 0
                    
                    recall_values.append(win_rate)


                df_judgements["recall_value"] = recall_values



                # 保存
                if not os.path.exists(f'./step4_win_rate/data/{place}/{machine}'):
                    os.mkdir(f'./step4_win_rate/data/{place}')
                    os.mkdir(f'./step4_win_rate/data/{place}/{machine}')
                save_path = f"./step4_win_rate/data/{place}/{machine}/win_rate_{logic}.csv"
                df_judgements.to_csv(save_path)



if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店
    logics = s.logics
    
    
    make_win_rate(places, logics)
    print("ok")