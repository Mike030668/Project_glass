from const_predprice import BASE_COLS, TARGET_COLS, DEPTH, PREDICT_LAG
from constants import FUTURE, GLASS_COLS, MAKE_LOG
from utils import csv2df, clean_dataset, future_sequence
import numpy as np # библиотека нампи
import joblib
# Нормировщики
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf           # библиотека машинного обучения



path = "./stock_data/BTCUSDT_1 _min.csv"

def main():
    df_data = csv2df(path)
    df_data = clean_dataset(df_data)


    dataset = df_data[:FUTURE]
    VAL_LEN = int(round(len(dataset)*0.2, -2))   # Используем 300 записей для проверки
    TRAIN_LEN = dataset.shape[0] - VAL_LEN       # Размер тренировочной выборки

    # колонки для тренировочной выборки
    TRAIN_COLUMNS = BASE_COLS + GLASS_COLS
    GLASS = len(GLASS_COLS)

    # Делим данные на тренировочную и тестовую выборки
    x_train, x_val = dataset[TRAIN_COLUMNS][:TRAIN_LEN - PREDICT_LAG + 1].values, \
                    dataset[TRAIN_COLUMNS][TRAIN_LEN + DEPTH + 2:-PREDICT_LAG + 1].values

    # Масштабируем данные (отдельно для X и Y), чтобы их легче было скормить сетке
    X_MAIN_SCALER = MinMaxScaler(feature_range = (0, 1)) #  RobustScaler() # StandardScaler() #
    X_MAIN_SCALER.fit(x_train[:,:-GLASS])                  # обучаем X_SCAILER

    X_GLASS_SCALER = MinMaxScaler(feature_range = (0, 1)) #  RobustScaler() # StandardScaler() #
    X_GLASS_SCALER.fit(x_train[:,-GLASS:])                  # обучаем X_SCAILER

    x_train_sc = np.zeros_like(x_train)
    x_val_sc = np.zeros_like(x_val)

    x_train_sc[:,:-GLASS] = X_MAIN_SCALER.transform(x_train[:,:-GLASS])  # трансформируем x_train
    x_val_sc[:,:-GLASS] = X_MAIN_SCALER.transform(x_val[:,:-GLASS])      # трансформируем x_val

    x_train_sc[:,-GLASS:] = X_GLASS_SCALER.transform(x_train[:,-GLASS:])  # трансформируем x_train
    x_val_sc[:,-GLASS:] = X_GLASS_SCALER.transform(x_val[:,-GLASS:])      # трансформируем x_val

    # Для подготовки yTrain на PREDICT_LAG шагов вперед необходимо создать дополнительный датасет
    # Для таргета берем колонку PRED_PRICE
    y_train = future_sequence(dataset[TARGET_COLS][:TRAIN_LEN], PREDICT_LAG).squeeze()
    y_val =  future_sequence(dataset[TARGET_COLS][TRAIN_LEN + DEPTH + 2:], PREDICT_LAG).squeeze()

    # делаем ли np.log для у
    if MAKE_LOG:
      y_train = np.log(y_train)  # заменяем  y_train на log(y_train)
      y_val = np.log(y_val)      # заменяем  y_val на log(y_val)

    # Масштабируем данные (отдельно для X и Y), чтобы их легче было скормить сетке
    Y_SCAILER = MinMaxScaler(feature_range = (0, 1)) #  RobustScaler() # StandardScaler() #
    Y_SCAILER.fit(y_train)                    # обучаем Y_SCAILER
    y_train_sc = Y_SCAILER.transform(y_train)    # трансформируем y_train
    y_val_sc = Y_SCAILER.transform(y_val)        # трансформируем y_val

    
    joblib.dump(Y_SCAILER, './predprice/y_scailer.save') 
    joblib.dump(X_MAIN_SCALER, './predprice/x_main_scailer.save') 
    joblib.dump(X_GLASS_SCALER, './predprice/x_glass_scailer.save') 
    np.save('./predprice/x_train_sc.npy', x_train_sc) 
    np.save('./predprice/x_val_sc.npy', x_val_sc) 
    np.save('./predprice/y_train_sc.npy', y_train_sc) 
    np.save('./predprice/y_val_sc.npy', y_val_sc) 



if __name__ == "__main__":
    main()