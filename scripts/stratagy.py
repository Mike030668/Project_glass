# Библиотеки backtesting
from backtesting import Strategy

class Long_Strategy(Strategy):

    def init(self):
      #self.column = use_price
      self.to_long = self.I(lambda x: x, self.data.to_long, name ='to_long')

    def next(self):
      # торгуем по крайней цене закрытия
      price = self.data.Close[-1]
      # определяем размер/силу действия из сигнали
      size = abs(self.to_long[-1])

      # закрытие лонга
      if (self.position.is_long and 0> self.to_long[-1] >= -1):
          # Текущий капитал (денежные средства плюс активы).
          print('Текущий капитал ', round(self.equity))
          print('______________________________________________')
          print('Закрытие позиции')
          # Размер позиции в единицах актива. Отрицательно, если позиция короткая.
          print('Размер позиции', self.position.size)
          self.position.close()
          #print('trades ', self.trades)
          # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
          print('Прибыль/убыток (позиции в деньгах', self.position.pl)
          # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
          print('Прибыль/убыток позиции в %', self.position.pl_pct)
          # True, если позиция длинная (размер позиции положительный).
          print('position.is_long', self.position.is_long)
          # True, если позиция короткая (размер позиции отрицательный).
          print('position.is_short', self.position.is_short)
          print('______________________________________________')
          print()


      # Long entry
      elif (self.position.size == 0 and 0 < self.to_long[-1] <= 1):
          # Текущий капитал (денежные средства плюс активы).
          print('Текущий капитал ', round(self.equity))
          print('______________________________________________')
          print('вход в покупку')
          self.buy()
          #self.position.entry_price = price*size
          print('orders ', self.orders)
          print('______________________________________________')
          print()

############################################################################
class Short_Strategy(Strategy):

    def init(self):
      self.to_short = self.I(lambda x: x, self.data.to_short, name='to_short')

    def next(self):
      # торгуем по крайней цене закрытия
      price = self.data.Close[-1]
      # определяем размер/силу действия из сигнали
      size = abs(self.to_short[-1])

      # закрытие шорта
      if (self.position.is_short and 0< self.to_short[-1] <= 1):
        # Текущий капитал (денежные средства плюс активы).
        print('Текущий капитал ', round(self.equity))
        print('______________________________________________')
        print('Закрытие позиции')
        # Размер позиции в единицах актива. Отрицательно, если позиция короткая.
        print('Размер позиции', self.position.size)
        self.position.close()
        # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
        print('Прибыль/убыток (позиции в деньгах', self.position.pl)
        # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
        print('Прибыль/убыток позиции в %', self.position.pl_pct)
        # True, если позиция длинная (размер позиции положительный).
        print('position.is_long', self.position.is_long)
        # True, если позиция короткая (размер позиции отрицательный).
        print('position.is_short', self.position.is_short)
        print('______________________________________________')
        print()

      # Short entry
      if (self.position.size == 0 and  0> self.to_short[-1] >= -1):
          # Текущий капитал (денежные средства плюс активы).
          print('Текущий капитал ', round(self.equity))
          print('______________________________________________')
          print('вход в продажу')
          self.sell()
          # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
          print('Прибыль/убыток (позиции в деньгах', self.position.pl)
          # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
          print('Прибыль/убыток позиции в %', self.position.pl_pct)
          # True, если позиция длинная (размер позиции положительный).
          print('position.is_long', self.position.is_long)
          # True, если позиция короткая (размер позиции отрицательный).
          print('position.is_short', self.position.is_short)
          print('______________________________________________')
          print()

############################################################################
class Long_n_Short_Strategy(Strategy):

    def init(self):
      self.to_long = self.I(lambda x: x, self.data.to_long, name='to_long')
      self.to_short = self.I(lambda x: x, self.data.to_short, name='to_short')

    def next(self):
      # торгуем по крайней цене закрытия
      price = self.data.Close[-1]

      # закрытие лонга
      if (self.position.is_long and 0 > self.to_long[-1] >= -1):
          # Текущий капитал (денежные средства плюс активы).
          print('Текущий капитал ', round(self.equity))
          print('______________________________________________')
          print('Закрытие позиции LONG')
          # Размер позиции в единицах актива. Отрицательно, если позиция короткая.
          print('Размер позиции', self.position.size)
          self.position.close()
          #print('trades ', self.trades)
          # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
          print('Прибыль/убыток (позиции в деньгах', self.position.pl)
          # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
          print('Прибыль/убыток позиции в %', self.position.pl_pct)
          # True, если позиция длинная (размер позиции положительный).
          print('position.is_long', self.position.is_long)
          # True, если позиция короткая (размер позиции отрицательный).
          print('position.is_short', self.position.is_short)
          print('______________________________________________')
          print()


      # закрытие шорта
      elif (self.position.is_short and 0 < self.to_short[-1] <= 1):
        # Текущий капитал (денежные средства плюс активы).
        print('Текущий капитал ', round(self.equity))
        print('______________________________________________')
        print('Закрытие позиции')
        # Размер позиции в единицах актива. Отрицательно, если позиция короткая.
        print('Размер позиции', self.position.size)
        self.position.close()
        # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
        print('Прибыль/убыток (позиции в деньгах', self.position.pl)
        # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
        print('Прибыль/убыток позиции в %', self.position.pl_pct)
        # True, если позиция длинная (размер позиции положительный).
        print('position.is_long', self.position.is_long)
        # True, если позиция короткая (размер позиции отрицательный).
        print('position.is_short', self.position.is_short)
        print('______________________________________________')
        print()


      # Long entry
      if (self.position.size == 0 and 0 < self.to_long[-1] <= 1):
          # Текущий капитал (денежные средства плюс активы).
          print('Текущий капитал ', round(self.equity))
          print('______________________________________________')
          print('вход в покупку')
          self.buy()
          #self.position.entry_price = price*size
          print('orders ', self.orders)
          print('______________________________________________')
          print()

      # Short entry
      elif (self.position.size == 0 and  0> self.to_short[-1] >= -1):
          # Текущий капитал (денежные средства плюс активы).
          print('Текущий капитал ', round(self.equity))
          print('______________________________________________')
          print('вход в продажу')
          self.sell()
          print('orders ', self.orders)
          print('______________________________________________')
          print()

      # Проверка пересечения условий
      if (self.position.size == 0 and 0 < self.to_long[-1] <= 1) and \
         (self.position.size == 0 and  0> self.to_short[-1] >= -1):
         print("Пересечение Long entry и Short entry")

###############################################################################
class Reverse_Strategy(Strategy):

      def init(self):
          self.to_long = self.I(lambda x: x, self.data.to_long, name='to_long')
          self.to_short = self.I(lambda x: x, self.data.to_short, name='to_short')

      def next(self):
          # торгуем по крайней цене закрытия
          price = self.data.Close[-1]
          size = 0.1
          price_delta = 1
          # away from the current closing price.
          upper, lower = price * (1 + np.r_[1, -1]*price_delta)

          # Long entry
          if (self.position.size == 0  and 0 < self.to_long[-1] <= 1):
              # Текущий капитал (денежные средства плюс активы).
              print('Текущий капитал ', round(self.equity))
              print('______________________________________________')
              print('вход в Long')
              self.buy()
              print('orders ', self.orders)
              print('position.is_long', self.position.is_long)
              print('______________________________________________')
              print()

          # Short entry
          if (self.position.size == 0 and  0 > self.to_short[-1] >= -1):
              # Текущий капитал (денежные средства плюс активы).
              print('Текущий капитал ', round(self.equity))
              print('______________________________________________')
              print('вход в Short')
              self.sell()
              print('orders ', self.orders)
              print('position.is_short', self.position.is_short)
              print('______________________________________________')
              print()

          # закрытие лонга
          if (self.position.is_long and 0 > self.to_short[-1] >= -1):
              # True, если позиция длинная (размер позиции положительный).
              print('position.is_long', self.position.is_long)
              # Текущий капитал (денежные средства плюс активы).
              print('Текущий капитал ', round(self.equity))
              print('______________________________________________')
              print('Закрытие позиции LONG')
              # Размер позиции в единицах актива. Отрицательно, если позиция короткая.
              print('Размер позиции', self.position.size)
              self.position.close(portion=size)
              print('______________________________________________')
              # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
              print('Прибыль/убыток (позиции в деньгах', self.position.pl)
              # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
              print('Прибыль/убыток позиции в %', self.position.pl_pct)
              print('______________________________________________')
              print()
              print('вход в продажу')
              self.sell(size=size)
              print('position.is_short', self.position.is_short)
              print('______________________________________________')

          # закрытие шорта
          if self.position.is_short and 0< self.to_long[-1] <= 1: #
            # True, если позиция короткая (размер позиции отрицательный).
            print('position.is_short', self.position.is_short)
            # Текущий капитал (денежные средства плюс активы).
            print('Текущий капитал ', round(self.equity))
            print('______________________________________________')
            print('Закрытие позиции Short')
            # Размер позиции в единицах актива. Отрицательно, если позиция короткая.
            print('Размер позиции', self.position.size)
            self.position.close(portion=size)
            print('______________________________________________')
            # Прибыль (положительная) или убыток (отрицательная) текущей позиции в денежных единицах.
            print('Прибыль/убыток (позиции в деньгах', self.position.pl)
            # Прибыль (положительная) или убыток (отрицательная) текущей позиции в процентах.
            print('Прибыль/убыток позиции в %', self.position.pl_pct)
            print('______________________________________________')
            print()
            print('вход в Long')
            self.buy(size=size)
            print('position.is_long', self.position.is_long)
            print('______________________________________________')