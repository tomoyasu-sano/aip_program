# drive スプレッドシートからデータを読み込む
# データ先：https://docs.google.com/spreadsheets/d/1LNbPEQIqsb-mjhIBCl2sleI3kl5fwhSKPEdESxB44tQ/edit#gid=0

# 設定：https://tanuhack.com/operate-spreadsheet/

import datetime
import gspread
import json
import pandas as pd

from setting.setting import options



#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('./key/aip-spreadsheet-dd437a9d96af.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1LNbPEQIqsb-mjhIBCl2sleI3kl5fwhSKPEdESxB44tQ'

#共有設定したスプレッドシートのシート1を開く
#ws1= gc.open_by_key(SPREADSHEET_KEY).worksheet('データ')
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
values=worksheet.get_all_values()

df = pd.DataFrame(values)
df.columns=["台番号", "累計スタート", "総大当たり", "初当たり", "確変当", "大当たり確変", "初当たり確変", "最大持ち玉", "前日最終スタート"]

add1= df["大当たり確変"].str[2:].astype(float)
add2 = df["初当たり確変"].str[2:].astype(float)
df = df.drop(["大当たり確変", "初当たり確変"], axis=1)
df["大当たり確変"] = add1
df["初当たり確変"] = add2
df = df.astype('int')
print(df.dtypes)
print(df)

name = option.name
d_today = datetime.date.today()
df.to_csv(f"/Users/tomoyasu/dev/AIP/data/{name}/{d_today}.csv")

