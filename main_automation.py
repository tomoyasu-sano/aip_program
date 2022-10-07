import datetime
import os
import random
import schedule
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import main_scraping
from step0_settings import setting
from step1_scrapiing import scraping_robo
from step2_logics import logic_1
from step3_results import make_result
from step4_win_rate import make_win_rate
from step5_predict import predict
from step6_win_rate_history import history_logic_2

def job():
  print(datetime.datetime.now())
  print("I'm working...")  
  
  # データ取得したいお店を選択する
  places = setting.places 
  
  # 明日の予想したいお店を選択する
  predict_shops = setting.predict_shops
  

  # データ取得
  try:
    print("データ取得を開始します")
    scraping_robo
    print("データ取得が完了しました")
  except:
    print("例外が発生しました")
  else:
    print("問題ありません")

  # 予測データ生成
  try:
    print("ロジックを適用します")
    logic_1
    print("ロジックの適用が完了しました")
  
    print("結果の取得を開始します")
    make_result
    print("結果の取得が完了しました")

    print("勝率を算出します")
    make_win_rate
    print("勝率の算出が完了しました")

    print("明日の予測をします")
    predict
    print("予測が完了しました")
    
    print("履歴を作成します")
    history_logic_2
    print("履歴作成が完了しました")
    

  except:
    print("例外が発生しました")
  else:
    print("問題ありません")

#schedule.every().day.at("22:30").do(job)
#time_list = ["30,35,40,45,50"]
#start_time = random.choice(time_list)
#schedule.every().day.at(f"22:{start_time}").do(job)


schedule.every().day.at(f"07:00").do(job)


while True:
  schedule.run_pending()
  time.sleep(60)