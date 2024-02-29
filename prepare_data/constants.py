# for models predict Close and Trend Close
GLASS_COLS = ['Mkr plus 0,005', 'Mkr plus 0,01', 'Mkr plus 0,015', 'Mkr plus 0,020', 
              'Mkr plus 0,025', 'Mkr plus 0,030', 'Mkr plus 0,035', 'Mkr plus 0,040', 
              'Mkr plus 0,045', 'Mkr plus 0,050', 'Mkr plus 0,075', 'Mkr plus 0,1', 
              'Mkr plus 0,125', 'Mkr plus 0,150', 'Mkr plus 0,175', 'Mkr plus 0,200', 
              'Mkr plus 0,225', 
              'Mkr minus 0,005', 'Mkr minus 0,01', 'Mkr minus 0,015', 'Mkr minus 0,020', 
              'Mkr minus 0,025', 'Mkr minus 0,030', 'Mkr minus 0,035', 'Mkr minus 0,040', 
              'Mkr minus 0,045',  'Mkr minus 0,050', 'Mkr minus 0,075', 'Mkr minus 0,1',
              'Mkr minus 0,125', 'Mkr minus 0,150', 'Mkr minus 0,175', 'Mkr minus 0,200', 
              'Mkr minus 0,225']

# for model predict Trend Close
MAIN_COLS = ['Open', 'High', 'Low', 'Close', 'Volume', 'Rsi', 'Tkr Buy', 'Tkr Sell',
       'Open Interest', 'Number Of Trades', 'Taker Buy Volume',
       'TT LongShortRatio Positions 5m', 'TT LongAccount Ratio Positions 5m',
       'TT ShortAccount Positions 5m', 'TT LongShortRatio Accounts 5m',
       'TT LongAccount Accounts 5m', 'TT ShortAccount Accounts 5m',
       'Buy Sell Ratio 5m', 'Buy Vol 5m', 'Sell Vol 5m', 
       ]

# point for test models on data
FUTURE = 2800
MAKE_LOG = True