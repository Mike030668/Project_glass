import numpy as np
import pandas as pd
from scripts.bots import cond_long, cond_short

from tqdm.notebook import tqdm   # отрисовка прохождения цикла

def prepare_data(df_in: pd.DataFrame,
                        depth:int,
                        make_log,
                        scalers,
                        glass,
                        features
                      ):
    # обогащаем данные ранее созданной функцией
    ds = df_in.copy()
    if make_log:
       ds["Volume"] = ds["Volume"].apply(lambda x: np.log(x))
    # Удаление строк с неполными данными
    #ds = clean_dataset(ds)
    # оставляем на глубину depth и только нужные колонки
    x_data = ds[features][-depth:].values
    # нормализуем
    x_out = np.zeros_like(x_data)
    x_out[:,:-glass] = scalers[0].transform(x_data[:,:-glass])  # трансформируем x_train
    x_out[:,-glass:] = scalers[1].transform(x_data[:,-glass:])  # трансформируем x_train

    # выводим с добавлением измерения по axis=0
    return np.expand_dims(x_out, axis=0)

def tresh_trend(trend, trsh_d, trsh_u):
    out = np.zeros(trend.shape[0])
    out[trend > trsh_u] = 1
    out[trend < trsh_d] = -1
    return out.astype(int)


def making_signals(past_df: pd.DataFrame,
                    check_df: pd.DataFrame,
                    pred_lag: int,
                    glass: int,
                    #comis:float,
                    depth: int,
                    make_log_vol: bool,
                    make_log_tgt: bool,
                    fun_action: object,
                    model_price: object,
                    model_trend: object,
                    scalers_price: object,
                    scalers_trend: object,
                    features_price: list,
                    features_trend: list,
                    #use_force_action = False,
                    show_unique_signals = True,
                    ):

    """
    Args:
        past_df (pd.DataFrame) - прошлые OHCL данные до тестируемых
        check_df (pd.DataFrame) - тестируемые OHCL данные
        pred_lag: int - шаг предсказания
        model (class) - ранее обученная модель
        use_force_action (bool): False - выводим чистые действия,
                                 True - выводим действия с учетом уверенности,
        show_unique_signals (bool) - показать ли состав чистых действий

    Return:
         df_signal(pd.DataFrame) - копия OHCL датафрейма из check_df с колонкой Signal
    """
    # сбор действий
    all_actions = [[0, 0]]
    # сбор последнего активного действия и цены
    last_state = {
        "last_price" : 0,
        "pred_prices" : [[]],
        "pred_trend" : [[]]
                    }

    # итеррируемся по длине изучаемого датафрейма
    # берем на страте прошлые данные
    for i in tqdm(range(check_df.shape[0]-pred_lag), unit ="step",
                      desc ="Пробегаемся по всем отсчетам"):
        if not i: # берем на страте прошлые данные
            check_data = past_df.copy()
        # далее отшипываем вначале 1 свечу
        else: #  и присоединяем в коней новую из изучаемого датафрейма
            check_data = check_data[1:].append(check_df[i:i+1])

        price = check_data.Close[-1]
        last_state["last_price"] = price

        # обогащаем данные по аналогии как готовили для убучени
        to_pred_price = prepare_data(df_in = check_data,
                                      depth = depth, #DEPTH ,    # ранее заданная глубина сбора данных в прошлое
                                      make_log = make_log_vol, #MAKE_LOG_VOL,
                                      scalers = scalers_price,
                                      glass = glass,
                                      features = features_price
                                      )

        # предсказание модели price
        pred_price = model_price.predict(to_pred_price, verbose=False)
        pred_price = scalers_price[2].inverse_transform(pred_price)

        if make_log_tgt : pred_price = np.exp(pred_price) #MAKE_LOG_TARGET
        # собираем историю pred_prices и price
        #last_state["pred_prices"] = pred_price[0].astype(float)
        last_state["pred_prices"].append(pred_price[0].astype(float))

        # обогащаем данные по аналогии как готовили для убучени
        to_pred_trend = prepare_data(df_in = check_data,
                                      depth = depth, #DEPTH ,    # ранее заданная глубина сбора данных в прошлое
                                      make_log = make_log_vol, #MAKE_LOG_VOL,
                                      scalers = scalers_trend,
                                      glass = glass, #GLASS,
                                      features = features_trend
                                      )
        # предсказание модели trend
        pred_trend = model_trend.predict(to_pred_trend, verbose=False)[0].astype(float)
        pred_trend = tresh_trend(pred_trend, trsh_d = -0.1, trsh_u = 0.1)
        last_state["pred_trend"].append(pred_trend)

        if i:
          last_state["pred_prices"] = last_state["pred_prices"][-2:]
          last_state["pred_trend"] = last_state["pred_trend"][-2:]
          to_action = fun_action(last_state, cond_long, cond_short)
          all_actions.append(to_action)
          if show_unique_signals:
                # раскомитить чтобы выводило to_action
                if to_action[0] != to_action[0]: print(to_action)



    # переводим классы сигналов в массив сигналов
    all_actions = np.vstack(all_actions)
    # смещаем на pred_lag
    df_signal = check_df[pred_lag:].copy()
    df_signal['to_long']  = all_actions[:, 0]
    df_signal['to_short'] = all_actions[:, 1]
    # берем чистые действия действия
    return  df_signal