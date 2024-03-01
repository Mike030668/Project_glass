from matplotlib import pyplot as plt
from scipy import signal
from scipy.signal import savgol_filter
import pandas as pd # библиотека пандас
import numpy as np # библиотека нампи

class Segment():
    def __init__(self) -> None:
      pass

    def window_back(self, id:int, win:int):
        if (id - win)<0:
          win = id
        return win

    def window(self, id:int, win:int, size:int):
        if (id + win) > size:
          win = size - id
        return win

    def class_data(self, df:pd.DataFrame, id:int, wind:int, ratio:float):
        size = df.shape[0]
        current = df.iloc[id]['Close']
        last = df.iloc[id-1]['Close']

        past_mean = df.iloc[id-1-self.window_back(id-1, wind):id-1]['Close'].mean()
        next_mean = df.iloc[id+1:id+ self.window(id+1, wind, size)]['Close'].mean()

        if current > past_mean*(1-ratio) and current < next_mean*(1+ratio): out = 1
        elif current < past_mean*(1+ratio) and current > next_mean*(1-ratio): out = -1
        else: out = 0
        return out

    def get_segmented(self,
                      df:pd.DataFrame,
                      wind = 32,
                      ratio = 0.001) -> list:

        return [self.class_data(df, id, wind, ratio) for id in range(df.shape[0])]

    def plot_segmented(self, data:pd.Series, figsize=(8, 8))-> None:
        plt.figure(figsize=figsize)
        plt.subplot(2, 1, 1)
        data.plot(kind='line', title = data.name)
        plt.gca().spines[['top', 'right']].set_visible(False);
        plt.subplot(2, 1, 2)
        data.plot(kind='hist', bins=20, title=data.name)
        plt.gca().spines[['top', 'right',]].set_visible(False);

    def plot_trend(self, df:pd.DataFrame, start:int, end:int, figsize=(20,10))-> None:
        # поле графика
        plt.figure(figsize=figsize)
        # дни в датафрейме
        fragment = df[start:end].copy()
        days = np.arange(fragment.shape[0])
        # даты падющего тренда
        down = (fragment["Trend"] == -1)
        flat = (fragment["Trend"] == 0)
        gross = (fragment["Trend"] == 1)  
        # рисуем цену Close фрагмента
        plt.plot(days, fragment["Close"])
        plt.plot(np.where(gross, fragment["Close"], None), color="green", label= 'Рост')
        plt.plot(np.where(flat, fragment["Close"], None), color="blue", label= 'Флэт')
        plt.plot(np.where(down, fragment["Close"], None), color="red", label= 'Падение')
        plt.legend()
        plt.show()



class Gaussignal():
    def __init__(self,
                  classdata,
                  wide_signal = 7,
                  p = .3,
                  sigma = 1.61
                  ) -> None:

      self.wide_signal = wide_signal
      self.p = p
      self.sigma = sigma
      self.make_gausdata(classdata)

    def plot_signal(self, figsize=(5,5)):
        plt.figure(figsize=figsize)
        plt.plot(self.gauss_signal)
        plt.title(f"Generalized Gaussian window (p={self.p}"+r", $\sigma$" + f"={self.sigma})")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")


    def plot_gausdata(self, star, end, signal, title = "Gaussian", figsize=(15,5)):
        plt.figure(figsize=figsize)
        plt.plot(signal[star: end])

        if title == "Gaussian":
          plt.title(f"Смоделированный Gaussian сигнал с параметрами wide={self.wide_signal}"+r", $\sigma$"+f"={self.sigma}, p={self.p} )")
        elif title == "pred":     
          plt.title(f"Предсказаный Gaussian сигнал")
        else:  plt.title(title)
        
        plt.ylabel("Amplitude")
        plt.xlabel("Steps")

    def make_gausdata(self, data):
        self.gauss_signal = signal.windows.general_gaussian(self.wide_signal, p=self.p, sig=self.sigma)
        # создаем отдельный признак падения
        trend_down = np.zeros((data.shape[0]), dtype = float)
        trend_down[data==0] = -1.

        # создаем отдельный сигнал продажи
        trend_up = np.zeros((data.shape[0]), dtype = float)
        trend_up[data==1] = 1.

        # плечо сигнала впаво и влево от пика
        shoulder = self.wide_signal//2

        # проходимся по сигналу покупки
        for i in range(len(trend_up)):
          # если сигнал 1
          if trend_up[i] == 1.:
            # берем влево по сигналу на плечо, но не далее начала сигнала
            left = max(0, i - shoulder)
            # берем вправо по сигналу на плечо, но не далее конца сигнала
            right = min(i + shoulder +1, len(trend_up)-1)

            # отрезаем у сигнала плечо влево от пика
            left_gs = i - left
            # отрезаем у сигнала плечо вправо от пика
            right_gs = right - i
            # накладываем часть сигнала
            trend_up[left:right] = trend_up[i]*self.gauss_signal[shoulder -left_gs: shoulder +right_gs]

        # проходимся по сигналу продажи
        for i in range(len(trend_down)):
          # если сигнал -1
          if trend_down[i] == -1.:
            # берем влево по сигналу на плечо, но не далее начала сигнала
            left = max(0, i - shoulder)
            # берем вправо по сигналу на плечо, но не далее конца сигнала
            right = min(i + shoulder+1, len(trend_down)-1)

            # отрезаем у сигнала плечо влево от пика
            left_gs = i - left
            # отрезаем у сигнала плечо вправо от пика
            right_gs = right - i
            # накладываем часть сигнала
            trend_down[left:right] = trend_down[i]*self.gauss_signal[shoulder -left_gs:shoulder +right_gs]

        # складываем сигналы
        self.regress_signal = trend_up+trend_down
        self.filtered_signal = savgol_filter(self.regress_signal, 4, 1)