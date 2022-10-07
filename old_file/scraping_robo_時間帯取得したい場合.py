import datetime
import numpy as np
import os
import pandas as pd
import pyautogui
import random
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

browser = webdriver.Chrome(ChromeDriverManager().install())

from time import sleep, time
from step0_settings.setting import options, common_options


####

# 202209
## これまで:  "XPATH_time": ['//*[@id="ata','"]/table/tbody/tr[',']/td[1]/span[2]/a'],   # 2~台数分 tr[] で分割させる
## kyoto:  "XPATH_time": ['//*[@id="ata','"]/table/tbody/tr[',']/td[1]/span[3]/a'],   # 2~台数分 tr[] で分割させる

## これまで：columns_name = ["table_no", "履歴", "|", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
## kyoto: columns_name = ["table_no", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]

## logic4,5あたりの時間帯なし


####


def get_data(next_day=False, places=places):

    for place in places:

        if next_day:
            list_number_of_days = [0]
            lists_number_of_days = [list_number_of_days]

        else: 
            ##### 取得する日にちを設定 一気にやるとロボット対策される
            ## 2~4日ごとに行う（0,1,2,3,4,5,6,7）
            #list_number_of_days = [7,6,5,4,3,2,1]
            list_number_of_days = [2,1,0]
            lists_number_of_days = [list_number_of_days]        
        
        for list_days in lists_number_of_days:
            print(f"{list_days}日前のデータを取得します...")
            # データ取得
            #browser = webdriver.Chrome()
            #browser.implicitly_wait(10) # 秒

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
            user_name = setting.USERNAME
            password = setting.PASSWORD
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

            XPATH_time = common_options["XPATH_time"]
            XPATH_time_days = common_options["XPATH_time_days"]
            option = options[place]  #どこのディレクトリへデータを保存したいか settingより選択
            file_name = option["file_name"]
            table_len = option["table_len"]
            table_list = option["table_list"]
            XPATH_area1 = option["XPATH_area1"]
            XPATH_area2 = option["XPATH_area2"]
            XPATH_hole = option["XPATH_hole"]
            XPATH_table = option["XPATH_table"]

            print(f"データを取得する店舗: {file_name}")
            print("--------------------------")


            

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
            
            print("データ取得開始します...")

            for i in list_days:
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
                    text_date = datetime.datetime.today().strftime("%Y%m%d")
                    pre_table_lits = pd.DataFrame(table_list)
                    path_to_change_table = f"./step1_scrapiing/error/{file_name}_{text_date}_table_list_error.csv"
                    pre_table_lits.to_csv(path_to_change_table)
                    pass

                
            
                # dataframe化
                #columns_name = ["table_no", "履歴", "|", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
                columns_name = ["table_no", "詳細", "累計スタート", "大当り回数", "初当り回数", "最高出玉", "大当り確率", "初当り確率", "チャンス中大当り確率", "只今スタート"]
                df.columns = columns_name
                #df = df.drop(['table_no' ,'履歴', '|', '詳細', 'チャンス中大当り確率'], axis=1)
                df = df.drop(['table_no', '詳細', 'チャンス中大当り確率'], axis=1)
                df = df.reset_index(drop=True)
                #最終のcolumns = ["累計スタート","大当り回数","初当り回数","最高出玉","大当り確率","初当り確率","只今スタート"]  
                print(f"df  : {df.head()}")
            
                # 保存
                text_date = datetime.datetime.today()
                miuns_day = datetime.timedelta(days=i)
                before_date = text_date - miuns_day
                before_text_date= before_date.strftime("%Y%m%d")
                days_dir = f"./step1_scrapiing/data/{file_name}/days"
                if not os.path.exists(days_dir):
                    os.makedirs(days_dir)
                df.to_csv(f"./step1_scrapiing/data/{file_name}/days/{before_text_date}.csv")
                wait_time = float('{:.3f}'.format((16- 12) * np.random.rand() + 12))
                sleep(wait_time)
            
                

                ### 202209 kyotoより画面がやや変更され、時間帯のデータがないため、以降中止
                ## ２）その日の時間帯のテーブルデータを取得

                """
                front_path = XPATH_time[0]
                middle_path =XPATH_time[1]
                back_path = XPATH_time[2]
                print("その日の時間帯のデータパス", front_path, "; ", middle_path, "; ", back_path)
                ## //*[@id="ata ;  "]/table/tbody/tr[ ;  ]/td[1]/span[2]/a

                
                print(f"table_list: {table_list}")
                print(f"range_table: {range_table}")
                for i_time, table_name in zip(range(2,range_table), table_list):
                    if i_time == 0 or i_time == 1:

                        ## //*[@id="ata2"]/table/tbody/tr[2]/td[1]/span[2]/a　　指定path
                        ## //*[@id="ata0"]/table/tbody/tr[2]/td[1]/span[3]/a   クリックしたいpath
                        ## //*[@id="ata0"]/table/tbody/tr[3]/td[1]/span[3]/a
  

                        ## //*[@id="ahead2"]/a
                        ## //*[@id="ata2"]/table/tbody/tr[2]/td[1]/span[3]/a
                        ## all_XPATH_time: //*[@id="ata2"]/table/tbody/tr[2]/td[1]/span[2]/a
                        continue
                    else:
                        browser.find_element_by_xpath(f'//*[@id="ahead{i}"]/a').click()
                        wait_time = float('{:.3f}'.format((10- 8) * np.random.rand() + 8))
                        sleep(wait_time)

                        elems_time = browser.find_elements_by_tag_name("tr")
                        print("elems_time: ", elems_time)
                        print("elems_time type :", type(elems_time))

                        #all_XPATH_time = front_path+str(i)+middle_path+str(i_time)+back_path
                        #print(f"all_XPATH_time: {all_XPATH_time}")
                        #browser.find_element_by_xpath(all_XPATH_time).click()
                        #wait_time = float('{:.3f}'.format((10- 9) * np.random.rand() + 9))
                        #sleep(wait_time)

                        #time_days_value = i + 1
                        #front_path_days = XPATH_time_days[0]
                        #back_path_days = XPATH_time_days[1]
                        #all_XPATH_time_days = front_path_days + str(time_days_value) + back_path_days
                        #browser.find_element_by_xpath(all_XPATH_time_days).click()
                        #wait_time = float('{:.3f}'.format((12- 10) * np.random.rand() +10))
                        #sleep(wait_time)
                        

                        elems_time = browser.find_elements_by_tag_name("tr")
                        values_time = []
                        for elem_time in elems_time:
                            value_time = elem_time.text
                            value_time_s= value_time.split()
                            values_time.append(value_time_s)

                        print("values_time: ", values_time)

                        df_time = pd.DataFrame(values_time)

                        print("df_time: ", df_time)
                        print("df_time columns: ", df_time.columns)
                        #df_time = df_time[1:table_len+1]
                        #df_time.columns = ["大当り回数", "時間", "スタート回数"]
                        
                        table_dir = f"/Users/tomoyasu/dev/AIP/save_data/data/{file_name}/time/table_{table_name}"
                        if not os.path.exists(table_dir):
                            os.makedirs(table_dir)

                        df_time.to_csv(f"/Users/tomoyasu/dev/AIP/save_data/data/{file_name}/time/table_{table_name}/{before_text_date}.csv")

                        
                    
                        XPATH_list = '//*[@id="pankuzu"]/li[2]/a'
                        browser.find_element_by_xpath(XPATH_list).click()
                        wait_time = float('{:.3f}'.format((10- 8) * np.random.rand() + 8))
                        sleep(wait_time)
                
                print(f"{i}日目のデータ取得が終わりました。")
                """
            # browserを閉じる
            browser.quit()

            start_time = time()

            wait_time = random.randint(500,  700)
            print("10minほどの休憩に入ります...")
            sleep(wait_time)

            rest_time = time() - start_time
            print("休憩時間：",rest_time)

    
        print("--------------------------")
        print("完了....次の機種に移ります...")


        
    
    print("終了")
    print("--------------------------")


if __name__ == '__main__':
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    targets = s.options.keys
    print(targets)


    start = time()
    print("-----開始------")

    #get_data(places=places)

    print("------終了------")
    elapsed_time = time() - start
    print ("スクレイピング総時間:{0}".format(elapsed_time) + "[sec]")
