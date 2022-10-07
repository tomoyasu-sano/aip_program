import datetime
import numpy as np
import os
import pandas as pd
import pyautogui
import random
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.select import Select
#from selenium.webdriver.common.action_chains import ActionChains


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))



from time import sleep, time
from step0_settings.setting import options, login


####

# 202209
## これまで:  "XPATH_time": ['//*[@id="ata','"]/table/tbody/tr[',']/td[1]/span[2]/a'],   # 2~台数分 tr[] で分割させる
## kyoto:  "XPATH_time": ['//*[@id="ata','"]/table/tbody/tr[',']/td[1]/span[3]/a'],   # 2~台数分 tr[] で分割させる

## これまで：columns_name = ["table_no", "履歴", "|", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
## kyoto: columns_name = ["table_no", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]

## logic4,5あたりの時間帯なし
####


def get_data(places):

    for place in places:
        browser = webdriver.Chrome(ChromeDriverManager().install())

        # データ取得に必要な項目を取得
        place = options[place]["place"]
        machine = options[place]["machine"]
        scrayping_type = options[place]["scraping_type"]
        lists_number_of_days = options[place]["number_of_days"]
        table_len = options[place]["table_len"]
        table_list = options[place]["table_list"]
        XPATH_area1 = options[place]["XPATH_area1"]
        XPATH_area2 = options[place]["XPATH_area2"]
        XPATH_hole = options[place]["XPATH_hole"]
        XPATH_table = options[place]["XPATH_table"]
   
        
        # データ取得
        wait_time = float('{:.3f}'.format((15- 10) * np.random.rand() + 10))
        sleep(wait_time)
        browser.get("https://site777.tv/yahoo/data")

        wait_time = float('{:.3f}'.format((15- 10) * np.random.rand() + 10))
        sleep(wait_time)
        print("指定のURLにアクセス完了")
        print("--------------------------")
        browser.maximize_window() 

        wait_time = float('{:.3f}'.format((20- 15) * np.random.rand() + 15))
        sleep(wait_time)


        ### errorになることがある
        try:
            pyautogui.moveTo(80, 297, duration=2)
            #pyautogui.sleep(2)
            pyautogui.click(80, 297)

        except Exception as ex:
            print("対象が見つかりませんでした。")
            print(ex)

        
        wait_time = float('{:.3f}'.format((15- 12) * np.random.rand() + 12))
        sleep(wait_time)

        print("ログイン画面に移りました。ログインを開始します。")
        # ログイン
        user_name = login["USERNAME"]
        password = login["PASSWORD"]
        elem_username = browser.find_element_by_id("username")
        elem_username.send_keys(user_name)
        

        wait_time = float('{:.3f}'.format((15- 10) * np.random.rand() + 10))
        sleep(wait_time)
        browser.find_element_by_id("btnNext").click()

        wait_time = float('{:.3f}'.format((15- 10) * np.random.rand() + 10))
        sleep(wait_time)

        elem_pass = browser.find_element_by_id("passwd")
        elem_pass.send_keys(password)

        print("ログインしました...")
        wait_time = float('{:.3f}'.format((20- 15) * np.random.rand() + 15))
        sleep(wait_time)

        browser.find_element_by_id("btnSubmit").click()
        wait_time = float('{:.3f}'.format((15- 13) * np.random.rand() + 13))
        sleep(wait_time)

        
        ## １）その日のテーブルデータを取得
        browser.execute_script("window.scrollBy(0, 500);")
        sleep(2)

        browser.find_element_by_xpath(XPATH_area1).click()
        wait_time = float('{:.3f}'.format((15- 12) * np.random.rand() + 12))
        sleep(wait_time)
        print("都道府県を選びました")
    
        browser.find_element_by_xpath(XPATH_area2).click()
        wait_time = float('{:.3f}'.format((15- 13) * np.random.rand() + 13))
        sleep(wait_time)
        print("地域を選びました")
        

        # scrollの幅はホールや機種によって違う
        browser.execute_script("window.scrollBy(0, 300);")
        sleep(2)

        browser.find_element_by_xpath(XPATH_hole).click()
        wait_time = float('{:.3f}'.format((15- 10) * np.random.rand() + 10))
        sleep(wait_time)
        print("ホールを選びました")

        browser.find_element_by_xpath(XPATH_table).click()
        wait_time = float('{:.3f}'.format((16- 12) * np.random.rand() + 12))
        sleep(wait_time)
        print("テーブルを選びました")

        # 週間データの取得
        range_table = 2+table_len
            

        for day in range(lists_number_of_days):
            i = day + 1
            print(f"{i}日前のデータを取得します...")

            browser.find_element_by_xpath(f'//*[@id="ahead{i}"]/a').click()
            wait_time = float('{:.3f}'.format((15- 10) * np.random.rand() + 10))
            sleep(wait_time)
            
            elems = browser.find_elements_by_tag_name("tr")
            values = []
            for inner_i, elem in enumerate(elems):
                if inner_i in range(range_table*i, range_table*(i+1)):
                    value = elem.text
                    value_s= value.split()
                    values.append(value_s)

            df = pd.DataFrame(values)
            df = df[2:range_table]

            #テーブルの長さが変化していないか確認（台の増減確認）
            if i==0 and df.shape[0] != table_len:
                print("台の増減した可能性があります。データを確認していください！")
                # text_date = datetime.datetime.today().strftime("%Y%m%d")
                # pre_table_lits = pd.DataFrame(table_list)
                # path_to_change_table = f"./step1_scrapiing/error/{file_name}_{text_date}_table_list_error.csv"
                # pre_table_lits.to_csv(path_to_change_table)
                pass

            
            # dataframe化のカラム設定

            if scrayping_type == "type1":
                columns_name = ["table_no", "履歴", "|", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
            
            if scrayping_type == "type2":
                columns_name = ["table_no", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
            
            df.columns = columns_name
            
            # 整形
            df = df.drop(['table_no', '詳細', 'チャンス中大当り確率'], axis=1)
            df = df.reset_index(drop=True)
            
            #最終のcolumns = ["累計スタート","大当り回数","初当り回数","最高出玉","大当り確率","初当り確率","只今スタート"]  
            print(f"df  : {df.head()}")
        
            # 保存
            text_date = datetime.datetime.today()
            miuns_day = datetime.timedelta(days=i)
            before_date = text_date - miuns_day
            before_text_date= before_date.strftime("%Y%m%d")
            days_dir = f"./step1_scrapiing/data/{place}/{machine}"
            if not os.path.exists(days_dir):
                os.makedirs(days_dir)
            df.to_csv(f"./step1_scrapiing/data/{place}/{machine}/{before_text_date}.csv")
            wait_time = float('{:.3f}'.format((16- 12) * np.random.rand() + 12))
            sleep(wait_time)
            

        # browserを閉じる
        browser.quit()

        print("--------------------------")
        print("完了....次の機種に移ります...")
        wait_time = random.randint(300,  500)
        sleep(wait_time)


        
    
    print("終了")
    print("--------------------------")


if __name__ == '__main__':
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店

    # 時間測定
    start = time()
    print("-----開始------")
        

    get_data(places=places)


    print("------終了------")
    elapsed_time = time() - start
    print ("スクレイピング総時間:{0}".format(elapsed_time) + "[sec]")
