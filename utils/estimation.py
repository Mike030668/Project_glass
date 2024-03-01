import matplotlib.pyplot as plt # библиотека матплотлиб для отрисовки
import numpy as np # библиотека нампи
from prepare_data.constants import MAKE_LOG

# Функция рассчитываем результаты прогнозирования сети
def get_scalepred(model: object, x: list, y: list, у_scaler: object):
  '''
  Функция рассчитываем результаты прогнозирования сети
  В аргументы принимает сеть (model) и проверочную выборку
  Выдаёт результаты предсказания y_pred
  И правильные ответы в исходной размерности y_true (какими они были до нормирования)
  model - нейронная сеть
  x - x данные для предикта
  y - y проверочные данные
  у_scaler - ранее обученный скэйлер для y

  '''
  # Предсказываем ответ сети по проверочной выборке
  # И возвращаем исходны масштаб данных, до нормализации
  y_pred = у_scaler.inverse_transform(model.predict(x))
  y_true = у_scaler.inverse_transform(y)
  if MAKE_LOG:
    y_pred = np.exp(y_pred)
    y_true = np.exp(y_true)
  return (y_pred, y_true)


# Функция визуализирует графики, что предсказала сеть и какие были правильные ответы
def show_predict(start: int, finish: int, pred_lags: int,
                 y_pred: list, y_true: list, name: str, figsize=(25,10)):
  '''
  Функция визуализирует графики, что предсказала сеть и какие были правильные ответы
  start - точка с которой начинаем отрисовку графика
  finish - длина графика, которую отрисовываем
  pred_lags - какие шаги предсказания отрисовываем
  y_pred - предсказания модели
  y_true - верные ответы
  name - имя предсказания
  '''
  plt.figure(figsize=(figsize))
  for lag in pred_lags:
      plt.plot(y_pred[start:start+finish, lag],
              label=f'Прогноз на {lag+1}й шаг')
      plt.plot(y_true[start:start+finish, lag],
              label=f'Базовый ряд на {lag+1}м шаге')
  plt.xlabel('Отсчеты')
  plt.ylabel(f'Значение {name}')
  plt.legend()
  plt.show()


# Функция расёта корреляции дух одномерных векторов
def correlate(a, b):
  '''
  # Функция расчёта корреляции дух одномерных векторов
  a, b - вектора
  '''
  # Рассчитываем основные показатели
  ma = a.mean() # Среднее значение первого вектора
  mb = b.mean() # Среднее значение второго вектора
  mab = (a*b).mean() # Среднее значение произведения векторов
  sa = a.std() # Среднеквадратичное отклонение первого вектора
  sb = b.std() # Среднеквадратичное отклонение второго вектора

  #Рассчитываем корреляцию
  val = 0
  if ((sa>0) & (sb>0)):
    val = (mab-ma*mb)/(sa*sb)
  return val


# Функция рисуем корреляцию прогнозированного сигнала с правильным
def auto_corr(pred_lags: list, corr_steps: list, y_pred: list, y_true: list,
             show_graf = True, return_data = False, figsize=(18,7)):
  '''
  Функция рисуем корреляцию прогнозированного сигнала с правильным
  Смещая на различное количество шагов назад
  Для проверки появления эффекта автокорреляции
  pred_lags -  какие шаги предсказания для проверки корреляцию
  corr_steps - на какое количество шагов смещать сигнал назад для рассчёта корреляции
  show_graf - показываем график или нет
  return_data - возвращаем массивы автокорреляции или нет
  '''
  # Запоминаем размер проверочной выборки
  y_len = y_true.shape[0]
  # Если нужно показать график
  if show_graf:
    plt.figure(figsize=(figsize))
  # Проходим по всем каналам
  for lag in pred_lags:
    # Создаём пустой лист, в нём будут корреляции при смещении на i шагов обратно
    corr = []
    # Создаём пустой лист, в нём будут самокорреляции графика с собой
    # при смещении на i шагов обратно
    own_corr = []
    # Смещаем сигнал по предсказаниям для проверки автокорреляции
    for i in range(corr_steps):
      #print('i', i)
      # Получаем сигнал, смещённый на i шагов назад
      # y_pred[i:, lag]
      # Сравниваем его с верными ответами, без смещения назад
      # y_true[:y_len-i, lag]
      # Рассчитываем их корреляцию и добавляем в лист
      corr.append(correlate(y_true[:y_len-i, lag], y_pred[i:, lag]))
      # Рассчитываем корреляцию графика самого с сообой и добавляем в лист
      own_corr.append(correlate(y_true[:y_len-i, lag], y_true[i:, lag]))

    # Отображаем график коррелций для данного шага
    if show_graf: # Если нужно показать график
      plt.plot(corr, label= f'Предсказание на {str(lag+1)}й шаг')
      plt.plot(own_corr, label=f'Эталон на {str(lag+1)}м шаге')
  # Если нужно показать график
  if show_graf:
    plt.xlabel('Отсчеты')
    plt.ylabel('Значение корреляции')
    plt.legend()
    plt.show()
  # Если нужно вернуть массивы автокорреляции
  if return_data:
    return corr, own_corr



def confusion_matrix(y_true, y_pred, labels=None, normalize=None,
                     cmap="Blues", encoded_labels=True,
                     plot=True, verbose = False,
                     figsize = (10,10)
                     ):
    """
    Args:
        y_true (ndarray)
        y_pred (ndarray)
        labels (list)
        normalise (str) : {'all', None}
        cmap (maplotlib.pyplot.cmap)
        encoded_labels (bool): Need to be False if labels are not one hot encoded
        plot (bool): If False, plot will not appear for confusion matrix

    Return:
        conf_mat (tuple): TN, FP, FN, TP
    """

    import seaborn as sns
    from sklearn.metrics import confusion_matrix

    if normalize not in ('all', None):
        raise ValueError("normalize must be one of {'all', None}")

    conf_labels = None if encoded_labels else labels
    fmt = 'g' if normalize == None else '.2%'

    conf_mat = confusion_matrix(y_true, y_pred, normalize=normalize, labels=conf_labels)

    if plot:
        plt.figure(figsize = figsize)
        ax = sns.heatmap(conf_mat, cmap=cmap,
                         square=True, cbar=False,
                         annot=True, fmt=fmt,
                         annot_kws={'fontsize': int(figsize[0]*1.7),
                                    'fontweight': 'bold',
                                    'fontfamily': 'serif',
                                    }
                         )
        ax.set_title("Confusion Matrix", fontsize=int(figsize[0]*1.7))
        ax.set_xlabel("Predicted", fontsize=int(figsize[0]*1.5), color = "orange")
        ax.set_ylabel("Actual", fontsize=int(figsize[0]*1.5), color = "orange")
        if labels != None:
            ax.set_yticklabels(labels,  fontsize=int(figsize[0])*1.7)
            ax.set_xticklabels(labels,  fontsize=int(figsize[0])*1.7)
    if verbose: return conf_mat