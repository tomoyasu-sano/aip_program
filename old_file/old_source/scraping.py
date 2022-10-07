import datetime
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from time import sleep

import setting.setting as setting
from setting.setting import options, places


def get_data(places, predict_shop):

    for place in places:
        option = options[place]  #どこのディレクトリへデータを保存したいか settingより選択
        file_name = option["file_name"]
        start_table = option["start_table"] #　変更に注意
        table_length = option["table_len"] #　変更に注意
        url = option["url"]
        table_place = option["table_place"]
        print(f"データを取得する店舗: {file_name}")
        print("--------------------------")


        # データ取得
        browser = webdriver.Chrome()
        sleep(2)
        browser.get(url)
        sleep(2)
        print("指定のURLにアクセス完了")
        print("--------------------------")
        
        #source = browser.page_source

        # 利用規約ボタン：accept_btnの名称がユニークでなくなったり変更すると正常な動きとならない
        browser.find_element_by_class_name("accept_btn").click()
        sleep(2)
        print("利用規約ボタン押下　完了")
        print("--------------------------")
        
    
        # 広告の非表示（変更に注意）
        #browser.find_element_by_id("gn_interstitial_close_icon").click()
        browser.refresh()
        sleep(2)
        print("ブラウザのリフレッシュ完了")
        print("--------------------------")
        

        # その日のdataは全てmodel_nameに格納
        elems = browser.find_elements_by_css_selector('.model_name')
        sleep(2)
        elem = elems[table_place]
        sleep(1)
        elem.click()
        print("指定の台選択完了")
        print("--------------------------")
        sleep(2)

         
        # 指定日の場合 ## 保存csvは今日の日付になるため、変更する
        #browser.find_element_by_xpath("//div[@id='slumpTi']/form/select/option[3]").click() # [3]は2日前

        # その日のデータを取得
        data = browser.find_elements_by_class_name("today")
       
        # 準備
        columns=[ "累計スタート", "総大当たり", "初当たり", "確変当", "大当たり確変", "初当たり確変", "最大持ち玉", "前日最終スタート"]
        tables = []
        for t in range(start_table, start_table+table_length):
            tables.append(t)

        # データをリスト化し2次元配列へ
        values = []
        for value in data:
            v = value.text
            values.append(v)
        np_values = np.array(values)
        np_values = np_values.reshape([-1,8])
        df = pd.DataFrame(np_values)

        # 整形
        df = df.drop(0, axis=0)
        df.columns = columns
        df["台番号"] = tables

        add1= df["大当たり確変"].str[2:].astype(float)
        add2 = df["初当たり確変"].str[2:].astype(float)
        df = df.drop(["大当たり確変", "初当たり確変"], axis=1)
        df["大当たり確変"] = add1
        df["初当たり確変"] = add2
        df = df.astype('int')

        # 保存
        d_today = datetime.date.today()
        df.to_csv(f"/Users/tomoyasu/dev/AIP/data/{file_name}/{d_today}.csv")
        print("その日のデータ取得完了")
        print("--------------------------")

        # browserを閉じる
        browser.quit()
        
    print("終了")
    print("--------------------------")


if __name__ == '__main__':
    import setting.setting as setting
    # どこの台を取得するかチェック
    places = setting.places

    # 明日の予想したいお店を選択する
    predict_shop = "garo_izumi"
    
    print("-----開始------")
    get_data(places, predict_shop)
    print("------終了------")
