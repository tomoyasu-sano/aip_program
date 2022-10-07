

from step2_logics import logic_1, logic_2, logic_3
from step3_results import make_result
from step4_win_rate import make_win_rate
from step5_predict import predict
from step6_win_rate_history import history


def do_step_func(places, logics):
    logic_1.run_logic_1(places)
    logic_2.run_logic_2(places)
    logic_3.run_logic_3(places)
    #logic.start_logic(places)

    print("step2 logic: ok")

    make_result.get_result(places)
    print("step3 make_result: ok")

    make_win_rate.make_win_rate(places, logics)
    print("step4 make_win_rate: ok")

    predict.make_predict(places, logics)
    print("step5 predict: ok")

    history.make_history(places, logics)
    print("step6 history: ok")

    return "all ok"



if __name__ == "__main__":
    import step0_settings.setting as s
    
    # 対象取得データ一覧
    places = s.places
    ## settingで設定した現在データを取得対象のお店

    logics = s.logics
    
    do_step_func(places, logics)
    print("ok")