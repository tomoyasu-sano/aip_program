#from step2_logics import logic_1
#from step2_logics import logic_2
#from step2_logics import logic_3



import logic_1
import logic_2
import logic_3
import step0_settings.setting as s

def start_logic(places):
        logic_1.run_logic_1(places)
        logic_2.run_logic_2(places)
        logic_3.run_logic_3(places)



"""

logic追加
・logic_◯.pyで作成
・logicを作成し、それが適用されたかどうか（1,0）で格納（場所、機種別に日付・テーブルごとに）

logicの設定
・step0_settings/setting.py: logicを追加
・def start_logic(places): 関数の処理にlogicを追加

"""

if __name__ == "__main__":

    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店

    # 対象とするlogic
    # logics = s.logics

    
    start_logic(places)
