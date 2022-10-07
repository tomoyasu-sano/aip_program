
# login情報
login = {
"USERNAME" :'neurorehabili@yahoo.co.jp',
"PASSWORD" : 'neuroREHA0429'
}

# logicごとのレコメンド基準とする勝率
win_rate = 0.5

# スクレイピングする際にデータ取得するお店を設定
places = ["kyoto_kawaracho_king", "osaka_rakuen_namba"]
#places = ["osaka_rakuen_namba"]

# 対象logic
logics = ["logic_1", "logic_2", "logic_3"]

# 予測する店
#predict_shops = ["kyoto_kawaracho_king"]



"""
"XPATH_area1": 都道府県の選択
"XPATH_area2": 市区町村の選択
"XPATH_hole": お店の選択
"XPATH_table": 機種の選択
"""

options = {
    "kyoto_kawaracho_king":{
        "place": "kyoto_kawaracho_king",
        "machine": "eva",  # file_name -> machine
        "scraping_type": "type2",
        "number_of_days": 2,
        "table_len" : 14,
        "start_table": 41,
        "table_list":[41,42,43,44,45,46,47,74,75,76,77,78,79,80],
        "XPATH_area1": '//*[@id="map-search"]/div/div/div[2]/dl[4]/dd/a[3]',
        "XPATH_area2": '//*[@id="area-search"]/div/div/dl[2]/dd/ul/li[2]/a',
        "XPATH_hole": '//*[@id="hall-search-list"]/form/div[2]/div/div/p[1]/a/img',
        "XPATH_table": '//*[@id="hall_contents"]/table/tbody/tr[3]/td/ul/li[1]/input',
        #"XPATH_time": ['//*[@id="ata0"]/table/tbody/tr[',']/td[1]/span[2]/a'],   # 2~台数分 tr[] で分割させる
        #"XPATH_time": ['//*[@id="ata','"]/table/tbody/tr[',']/td[1]/span[2]/a'],   # 2~台数分 tr[] で分割させる
        #"XPATH_time_days": ['//*[@id="daianc"]/span[',']/a']   # 2~台数分 tr[] で分割させる
    },
    "osaka_rakuen_namba":{
        "place": "osaka_rakuen_namba",
        "machine": "eva",
        "scraping_type": "type1",
        "number_of_days": 7,
        "table_len" : 24,
        "start_table": 1337,
        "table_list":[1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360],
        "XPATH_area1": '//*[@id="map-search"]/div/div/div[2]/dl[4]/dd/a[1]',
        "XPATH_area2": '//*[@id="area-search"]/div/div/dl[1]/dd/ul/li[22]/a',
        "XPATH_hole": '//*[@id="hall-search-list"]/form/div[5]/div/div/p[1]/a/img',
        "XPATH_table": '//*[@id="hall_contents"]/table/tbody/tr[4]/td/ul/li[1]/input',
      
    }
}



# データ取得したいお店の設定
# common_options={
#     "XPATH_time": ['//*[@id="ata','"]/table/tbody/tr[',']/td[1]/span[3]/a'],   # 2~台数分 tr[] で分割させる
#     "XPATH_time_days": ['//*[@id="daianc"]/span[',']/a']   # 2~台数分 tr[] で分割させる
# }

