
# 1) 設定
setting.py: 機種や台数等の設定


# 2) データ収集
実行: collect_data_and_make_dataset/pre_scraping_robo.py
保存: save_data/data/　配下に蓄積


# 3) logic
ロジックの実行し、ロジック該当の有無のテーブルを作成
実行: 各logic.py
保存: logics_data/eva_king_kawaracho/logic_1.csv


# 4) 結果のテーブルを取得
勝敗をテーブル化
実行: results/make_result.py
保存: results/eva_king_kawaracho/logic_1.csv


# 5) 台ごとのlogicの性能評価（logicごとの勝率）
収集したcsvデータと、logic該当テーブルを突合し、予測の確率を抽出し保存する
実行: results/win_lose.py
保存：results/eva_king_kawaracho/win_rate_logic_1.csv


# 6) 明日の予想をする
・勝率が高い台とロジックをストック
・３）のテーブルから該当している順に、最も勝率が高い台を表示

# 7)