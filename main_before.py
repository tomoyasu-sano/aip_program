
import datetime
import numpy as np
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from save_data import make_npdataset
from prediction import pred
from step1_scrapiing import scraping_robo
#import win_rate
import step0_settings.setting as setting
from step0_settings.setting import options, places

#from retry import retry



def main(places, predict_shops): 

    # データ取得
    #scraping_robo.get_data(next_day=True, places=places)
    print("正常にデータ取得を完了しました")

    # データセット更新
    make_npdataset.make_dataset(places)
    print("正常にデータセット更新を完了しました")

    # 予測と昨日の結果検証
    pred.predict_check_result(predict_shops)
    print("正常に予測データの更新を完了しました")

    # 勝率を書き込む
    win_rate.write_win_rate()
    print("正常に勝率データの書き込みを完了しました")


@retry(delay=2)
def retry_func(places, predict_shops):
    try:
        main(places, predict_shops)
        print("main関数は、問題なく処理されました")
    except:
        print('errorとなったため、再度処理を行います')



if __name__ == '__main__':
    import setting.setting as setting
    # どこの台を取得しデータの更新するか
    places = setting.places
    places = ["garo_rakuen_nannba"]
    
    # 明日の予想したいお店を選択する
    predict_shops = setting.predict_shops
    predict_shops = ["garo_rakuen_nannba"]

    print("-----開始------")
    retry_func(places, predict_shops)
    #main(places, predict_shop)
    print("------終了------")

   



    

