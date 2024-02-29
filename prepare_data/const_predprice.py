# for model predict Close
BASE_COLS = ['Open', 'High', 'Low', 'Volume', 'Rsi', 'Tkr Buy', 'Tkr Sell',
       'Open Interest', 'Number Of Trades', 'Taker Buy Volume',
       'TT LongShortRatio Positions 5m', 'TT LongAccount Ratio Positions 5m',
       'TT ShortAccount Positions 5m', 'TT LongShortRatio Accounts 5m',
       'TT LongAccount Accounts 5m', 'TT ShortAccount Accounts 5m']

# for model predict Close
TARGET_COLS = ['Close']

DEPTH = 32          # Анализируем по DIFFBACK прошедшим точкам
PREDICT_LAG = 5     # на сколько шагов вперед
BATCH_SIZE = 64
