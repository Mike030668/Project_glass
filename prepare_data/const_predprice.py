# for model predict Close
BASE_COLS = ['Open', 'High', 'Low', 'Volume', 'Rsi', 'Tkr Buy', 'Tkr Sell',
       'Open Interest', 'Number Of Trades', 'Taker Buy Volume',
       'TT LongShortRatio Positions 5m', 'TT LongAccount Ratio Positions 5m',
       'TT ShortAccount Positions 5m', 'TT LongShortRatio Accounts 5m',
       'TT LongAccount Accounts 5m', 'TT ShortAccount Accounts 5m',
       'Buy Sell Ratio 5m', 'Buy Vol 5m', 'Sell Vol 5m', ]

# for model predict Close
TARGET_COLS = ['Close']

MAKE_LOG_TARGET = True


