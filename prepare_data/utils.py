import numpy as np # библиотека нампи
import pandas as pd # библиотека пандас
import matplotlib.pyplot as plt # библиотека матплотлиб для отрисовки


def clean_dataset(df:pd.DataFrame):
    """
    data - типа OHCL
    функция очистки
    """
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    # индексы без nan, inf и -inf
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    return df[indices_to_keep].astype(np.float64)


def csv2df(path: str):
    """
    path - url or file path
    функция очистки
    """
    if path.split(":")[0] in ("https", "http"):
        if path.split("=")[1] in ("sharing"): # for drive.google
            file_id=path.split('/')[-2]
            path='https://drive.google.com/uc?id=' + file_id

    return pd.read_csv(path, index_col=0, parse_dates=True ) 

    

def future_sequence(x_data, predict_lag):
    """
    Функция разделения набора данных на выборки для обучения нейросети
    x_data - набор входных данных
    predict_lag - количество шагов в будущее для предсказания
    
    """
    # Определение максимального индекса
    y_len = x_data.shape[0] - (predict_lag - 1)
    # отстоящих на predict_lag шагов вперед
    y = [x_data[i:i+ predict_lag] for i in range(y_len)]
    # Возврат результатов в виде массивов numpy
    return np.array(y)


def split_sequence(x_data, y_data, seq_len, predict_lags):
    """
    # Функция разделения набора данных на выборки для обучения нейросети
    # x_data - набор входных данных
    # y_data - набор выходных данных
    # seq_len - длина серии (подпоследовательности) входных данных для анализа
    # predict_lags - количество шагов в будущее для предсказания
    """
    # Определение максимального индекса начала подпоследовательности
    x_len = x_data.shape[0] - seq_len - (predict_lags - 1)
    # Формирование подпоследовательностей входных данных
    x = [x_data[i:i + seq_len] for i in range(x_len)]
    # Формирование меток выходных данных,
    # отстоящих на predict_lag шагов после конца подпоследовательности
    y = [[y_data[i+ lag + seq_len -1] for lag in range(predict_lags)] for i in range(x_len)]
    # Возврат результатов в виде массивов numpy
    return np.array(x), np.array(y)